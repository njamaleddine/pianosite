# -*- coding: utf-8 -*-
from oscar.apps.partner import strategy
from oscar.core.loading import get_class

Unavailable = get_class('partner.availability', 'Unavailable')
Available = get_class('partner.availability', 'Available')
StockRequiredAvailability = get_class('partner.availability', 'StockRequired')


class Selector(object):
    """
    Custom selector to return a Digital-specific strategy that disables
    purchases if product is not available for purchase
    """

    def strategy(self, request=None, user=None, **kwargs):
        return DigitalStrategy()


class DigitalStockRequired(object):
    """
    Availability policy mixin for use with the ``Structured`` base strategy.
    This mixin ensures that a product can only be bought if it has stock
    available (if stock is being tracked).
    """

    def availability_policy(self, product, stockrecord):
        if not product.is_available_for_digital_purchase():
            # Check that the digital product can be purchased
            return Unavailable()
        if not stockrecord or stockrecord.price_excl_tax is None:
            return Unavailable()
        if not product.get_product_class().track_stock:
            return Available()
        else:
            return StockRequiredAvailability(
                stockrecord.net_stock_level)

    def parent_availability_policy(self, product, children_stock):
        # A parent product is available if one of its children is
        for child, stockrecord in children_stock:
            policy = self.availability_policy(product, stockrecord)
            if policy.is_available_to_buy:
                return Available()
        return Unavailable()


class DigitalStrategy(strategy.UseFirstStockRecord, DigitalStockRequired,
                      strategy.NoTax, strategy.Structured):
    """
    Default Strategy but for digital products
    """
