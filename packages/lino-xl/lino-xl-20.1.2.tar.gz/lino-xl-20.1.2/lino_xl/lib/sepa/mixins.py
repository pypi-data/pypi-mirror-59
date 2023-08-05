# -*- coding: UTF-8 -*-
# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.db import models
from django.core.exceptions import ValidationError

from lino.api import dd, rt, _
from lino.utils import SumCollector
from lino.modlib.checkdata.choicelists import Checker
from lino_xl.lib.ledger.utils import DEBIT
from lino_xl.lib.ledger.choicelists import TradeTypes
# from lino_xl.lib.ledger.utils import myround

from lino_xl.lib.ledger.mixins import PartnerRelated


class BankAccount(dd.Model):
    class Meta:
        abstract = True

    bank_account = dd.ForeignKey('sepa.Account', blank=True, null=True)

    def full_clean(self):
        if not self.bank_account:
            self.partner_changed(None)

        super(BankAccount, self).full_clean()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(BankAccount, cls).get_registrable_fields(site):
            yield f
        yield 'bank_account'

    def partner_changed(self, ar):
        # dd.logger.info("20160329 BankAccount.partner_changed")
        Account = rt.models.sepa.Account
        qs = Account.objects.filter(partner=self.get_partner(), primary=True)
        if qs.count() == 1:
            self.bank_account = qs[0]
        else:
            qs = Account.objects.filter(partner=self.get_partner())
            if qs.count() == 1:
                self.bank_account = qs[0]
            else:
                self.bank_account = None
        super(BankAccount, self).partner_changed(ar)

    @dd.chooser()
    def bank_account_choices(cls, partner, project):
        # dd.logger.info(
        #     "20160329 bank_account_choices %s, %s", partner, project)
        partner = partner or project
        return rt.models.sepa.Account.objects.filter(
            partner=partner).order_by('iban')

    def get_bank_account(self):
        """Implements
        :meth:`Voucher.get_bank_account<lino_xl.lib.ledger.models.Voucher.get_bank_account>`.

        """
        return self.bank_account


class Payable(PartnerRelated):
    class Meta:
        abstract = True

    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
    # title = models.CharField(_("Description"), max_length=200, blank=True)

    def full_clean(self):
        if self.payment_term is None and self.partner_id is not None:
            self.payment_term = self.partner.payment_term
        if not self.due_date:
            if self.payment_term:
                self.due_date = self.payment_term.get_due_date(
                    self.voucher_date or self.entry_date)
        super(Payable, self).full_clean()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Payable, cls).get_registrable_fields(site):
            yield f
        yield 'your_ref'

    def get_due_date(self):
        return self.due_date or self.voucher_date

    def get_payable_sums_dict(self):
        raise NotImplemented()

    def get_movement_description(self, mvt, ar=None):
        for chunk in super(Payable, self).get_movement_description(mvt, ar):
            yield chunk
        if self.your_ref:
            yield self.your_ref

    def get_wanted_movements(self):
        item_sums = self.get_payable_sums_dict()
        # logger.info("20120901 get_wanted_movements %s", sums_dict)
        counter_sums = SumCollector()
        partner = self.get_partner()
        has_vat = dd.is_installed('vat')
        kw = dict()
        for k, amount in item_sums.items():
            # amount = myround(amount)
            # first item of each tuple k is itself a tuple (account, ana_account)
            acc_tuple, prj, vat_class, vat_regime = k
            account, ana_account = acc_tuple
            # if not isinstance(acc_tuple, tuple):
            #     raise Exception("Not a tuple: {}".format(acc_tuple))
            if not isinstance(account, rt.models.ledger.Account):
                raise Exception("Not an account: {}".format(account))
            if has_vat:
                kw.update(
                    vat_class=vat_class, vat_regime=vat_regime)

            if account.needs_partner:
                kw.update(partner=partner)
            yield self.create_movement(
                None, acc_tuple, prj, self.journal.dc, amount, **kw)
            counter_sums.collect(prj, amount)

        tt = self.get_trade_type()
        if tt is None:
            if len(counter_sums.items()):
                raise Warning("No trade type for {}".format(self))
            return
        acc = self.get_trade_type().get_main_account()
        if acc is None:
            if len(counter_sums.items()):
                raise Warning("No main account for {}".format(tt))
            return

        total_amount = 0
        for prj, amount in counter_sums.items():
            total_amount += amount
            yield self.create_movement(
                None, (acc, None), prj, not self.journal.dc, amount,
                partner=partner if acc.needs_partner else None,
                match=self.get_match())

        if dd.plugins.ledger.worker_model \
                and TradeTypes.clearings.main_account \
                and self.payment_term_id and self.payment_term.worker:
            worker = self.payment_term.worker
            dc = self.journal.dc
            # one movement to nullify the credit that was booked to the partner account,
            # another movment to book it to the worker's account:
            yield self.create_movement(
                None, (acc, None), None, dc, total_amount,
                partner=partner, match=self.get_match())
            yield self.create_movement(
                None, (TradeTypes.clearings.get_main_account(), None), None, not dc, total_amount,
                partner=worker, match=self.get_match())


class BankAccountChecker(Checker):
    """Checks for the following data problems:

    - :message:`Bank account owner ({0}) differs from partner ({1})` --

    """
    verbose_name = _("Check for partner mismatches in bank accounts")
    model = BankAccount
    messages = dict(
        partners_differ=_(
            "Bank account owner ({0}) differs from partner ({1})"),
    )

    def get_checkdata_problems(self, obj, fix=False):

        if obj.bank_account:
            if obj.bank_account.partner != obj.get_partner():

                yield (False, self.messages['partners_differ'].format(
                    obj.bank_account.partner, obj.get_partner()))

BankAccountChecker.activate()
