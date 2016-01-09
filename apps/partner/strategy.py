# from oscar.apps.partner import strategy


# class Selector(object):
#     """
#     Custom selector class to returns a US strategy
#     """

#     def strategy(self, request=None, user=None, **kwargs):
#         return DigitalStrategy()


# class DigitalStrategy(strategy.UseFirstStockRecord, strategy.NoTax, strategy.Structured):
#     """
#     - No tax
#     - Use first stockrecord
#     - Don't enforce stock
#     """
#     pass
