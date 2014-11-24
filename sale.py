# This file is part of the sale_rule_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['SaleRuleCondition']
__metaclass__ = PoolMeta


class SaleRuleCondition:
    __name__ = 'sale.rule.condition'
    manufacturer = fields.Many2One('party.party', 'Manufacturer',
        states={
            'required': Eval('criteria') == 'manufacturer',
            'invisible': Eval('criteria') != 'manufacturer',
            },
        domain=[
            ('manufacturer', '=', True),
            ],
        depends=['criteria'])

    @classmethod
    def __setup__(cls):
        super(SaleRuleCondition, cls).__setup__()
        criteria = ('manufacturer', 'Total Product Manufacturer Quantity')
        if criteria not in cls.criteria.selection:
            cls.criteria.selection.append(criteria)

    def evaluate_manufacturer(self, sale):
        return self.evaluate_sum(sale)
