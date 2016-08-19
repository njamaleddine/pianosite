# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from oscar.apps.checkout import views
from oscar.apps.payment import forms
from oscar.apps.payment.models import SourceType
from djstripe.models import Customer as DJStripeCustomer

User = get_user_model()


class PaymentDetailsView(views.PaymentDetailsView):

    def get_context_data(self, **kwargs):
        # Override method so the bankcard form can be added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get('bankcard_form', forms.BankcardForm())

        # Get or create a new customer if the user is authenticated
        ctx['customer'] = None
        if self.request.user.is_authenticated():
            user = self.request.user
        else:
            user, created = User.objects.get_or_create(username=ctx.get('guest_email'), email=ctx.get('guest_email'))
            ctx['is_anonymous_user'] = True
        customer, created = DJStripeCustomer.get_or_create(subscriber=user)
        ctx['customer'] = customer
        return ctx

    def get(self, request, *args, **kwargs):
        # Skip if the user is authenticated and has a valid stripe credit card
        ctx = self.get_context_data()
        customer = ctx['customer']
        if customer and customer.can_charge():
            # Don't show the bank card form if the customer is authenticated
            return self.render_preview(request, bankcard_form=None)
        return super(PaymentDetailsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = forms.BankcardForm(request.POST)
        if not bankcard_form.is_valid():
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(bankcard_form=bankcard_form)
            return self.render_to_response(ctx)

        # Render preview with bankcard details hidden
        return self.render_preview(request, bankcard_form=bankcard_form)

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        print("IN HERE!")
        ctx = self.get_context_data()
        customer = ctx['customer']

        if customer and customer.can_charge():
            print("CAN CHARGE")
            submission = self.build_submission()
            return self.submit(**submission)

        bankcard_form = forms.BankcardForm(request.POST)
        if not bankcard_form.is_valid():
            print("INVALID")
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        print(submission)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>> ", submission['payment_kwargs']['bankcard'].__dict__)
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to Stripe
        """
        ctx = self.get_context_data()
        customer = ctx['customer']

        # Record payment source and event
        # stripe_ref = Facade().charge(order_number, total, card=self.request.POST[STRIPE_TOKEN],
        #                              description=self.payment_description(order_number, total, **kwargs),
        #                              metadata=self.payment_metadata(order_number, total, **kwargs))
        source_type, is_created = SourceType.objects.get_or_create(name='Stripe')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=total.incl_tax, currency=total.currency,
            amount_debited=total.incl_tax)  # , reference=stripe_ref)
        self.add_payment_source(source)

        # Create the charge on stripe
        try:
            customer.charge(total.incl_tax)

            if ctx['is_anonymous_user']:
                try:
                    # Delete the user
                    user = User.objects.get(email=ctx['guest_email'])
                    user.delete()
                except User.DoesNotExist:
                    user = None
        except Exception as e:
            # Some invalid card error here
            raise ValidationError(str(e))
        self.add_payment_event('charge-created', total.incl_tax)
