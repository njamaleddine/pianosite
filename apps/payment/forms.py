from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.apps.payment import bankcards
from oscar.apps.payment.forms import BankcardForm as OscarBankcardForm
from oscar.apps.payment.forms import BankcardNumberField
from oscar.apps.payment.forms import BankcardCCVField
from oscar.apps.payment.forms import BankcardStartingMonthField
from oscar.apps.payment.forms import BankcardExpiryMonthField

from apps.payment.models import Bankcard


class BankcardForm(OscarBankcardForm):
    """
    Override BankcardForm from django-oscar to add stripe_token which
    is necessary for anonymous transactions
    """
    # By default, this number field will accept any number. The only validation
    # is whether it passes the luhn check. If you wish to only accept certain
    # types of card, you can pass a types kwarg to BankcardNumberField, e.g.
    #
    # BankcardNumberField(types=[bankcards.VISA, bankcards.VISA_ELECTRON,])

    number = BankcardNumberField()
    ccv = BankcardCCVField()
    start_month = BankcardStartingMonthField(widget=forms.HiddenInput)
    expiry_month = BankcardExpiryMonthField()
    stripe_token = forms.CharField(max_length=100, widget=forms.HiddenInput)

    class Meta:
        model = Bankcard
        fields = ('number', 'start_month', 'expiry_month', 'ccv', 'stripe_token')

    def clean(self):
        data = self.cleaned_data
        number, ccv = data.get('number'), data.get('ccv')
        if number and ccv:
            if bankcards.is_amex(number) and len(ccv) != 4:
                raise forms.ValidationError(_(
                    "American Express cards use a 4 digit security code"))
        return data

    def save(self, *args, **kwargs):
        # It doesn't really make sense to save directly from the form as saving
        # will obfuscate some of the card details which you normally need to
        # pass to a payment gateway.  Better to use the bankcard property below
        # to get the cleaned up data, then once you've used the sensitive
        # details, you can save.
        raise RuntimeError("Don't save bankcards directly from form")

    @property
    def bankcard(self):
        """
        Return an instance of the Bankcard model (unsaved)
        """
        return Bankcard(
            number=self.cleaned_data['number'],
            expiry_date=self.cleaned_data['expiry_month'],
            start_date=self.cleaned_data['start_month'],
            ccv=self.cleaned_data['ccv'],
            stripe_token=self.cleaned_data['stripe_token']
        )
