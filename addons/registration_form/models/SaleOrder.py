from odoo import fields, models, api


# Inherit from Sale Model from: C:\odoo\server\odoo\addons\sale\models\sale.py
# Sale model name: sale.order
# we need to follow convention of naming models,
# so we need to use same as model name that we inherit from
# Name of file must follow name of class
class SaleOrder(models.Model):
    _inherit = 'sale.order'  # inherit with name of model

    sale_description = fields.Char(string='Sale Description')
