# This file is part of the sale_rule_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Equal, In, Not

__all__ = ['SaleRuleCondition']


class SaleRuleCondition:
    __metaclass__ = PoolMeta
    __name__ = 'sale.rule.condition'
    manufacturer = fields.Many2One('party.party', 'Manufacturer',
        states={
            'required': In(Eval('criteria'),
                ['manufacturer', 'product_manufacturer',
                    'category_manufacturer']),
            'invisible': Not(In(Eval('criteria'),
                    ['manufacturer', 'product_manufacturer',
                        'category_manufacturer'])),
            },
        domain=[
            ('manufacturer', '=', True),
            ],
        depends=['criteria'])

    @classmethod
    def __setup__(cls):
        super(SaleRuleCondition, cls).__setup__()
        criteria = ('manufacturer', 'Total Amount of Products of a '
            'Manufacturer')
        if criteria not in cls.criteria.selection:
            cls.criteria.selection.append(criteria)
        criteria = ('product_manufacturer', 'Total Amount of a Product of a '
            'Manufacturer')
        if criteria not in cls.criteria.selection:
            cls.criteria.selection.append(criteria)
        required = Equal(Eval('criteria'), 'product_manufacturer')
        previous_required = cls.product.states['required']
        if previous_required:
            required |= previous_required
        invisible = Not(Equal(Eval('criteria'), 'product_manufacturer'))
        previous_invisible = cls.product.states['invisible']
        if previous_invisible:
            invisible &= previous_invisible
        cls.product.states.update({
                'required': required,
                'invisible': invisible,
                })

        criteria = ('category_manufacturer', 'Total Amount of a Category '
            'of Product of a Manufacturer')
        if criteria not in cls.criteria.selection:
            cls.criteria.selection.append(criteria)
        required = Equal(Eval('criteria'), 'category_manufacturer')
        previous_required = cls.category.states['required']
        if previous_required:
            required |= previous_required
        invisible = Not(Equal(Eval('criteria'), 'category_manufacturer'))
        previous_invisible = cls.category.states['invisible']
        if previous_invisible:
            invisible &= previous_invisible
        cls.category.states.update({
                'required': required,
                'invisible': invisible,
                })

    def evaluate_manufacturer(self, sale):
        return self.evaluate_sum(sale)

    def evaluate_product_manufacturer(self, sale):
        quantity = sum([l.quantity for l in sale.lines
                if (getattr(l, 'product') == getattr(self, 'product') and
                    getattr(l, 'manufacturer') == getattr(self, 'manufacturer')
                    )
                ])
        return self.apply_comparison(quantity)

    def evaluate_category_manufacturer(self, sale):
        pool = Pool()
        Template = pool.get('product.template')
        templates = Template.search([
                ('category', '=', self.category.id),
                ])
        quantity = sum([l.quantity for l in sale.lines
                if (l.product and l.product.template) in templates and
                    getattr(l, 'manufacturer') == getattr(self, 'manufacturer')
                ])
        return self.apply_comparison(quantity)
