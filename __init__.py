# This file is part of the sale_rule_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .sale import *


def register():
    Pool.register(
        SaleRuleCondition,
        module='sale_rule_manufacturer', type_='model')
