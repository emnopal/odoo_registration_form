# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _


class FormRegist(models.Model):
    _name = "form.regist"
    _description = "Form Regist"
    # if you want to inherit
    # _inherit = "{Model you want to inherit}"
    _rec_name = 'fullname'

    # specify the fields you want to add on inherit model
    first_name = fields.Char(string='First Name', required=True, size=64)
    last_name = fields.Char(string='Last Name', required=True, size=64)
    age = fields.Integer(string='Age', size=5)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='male')
    address = fields.Text(string='Address')
    bio = fields.Text(string='Bio')
    fullname = fields.Char(string='Fullname', compute='_compute_fields_combination')

    @api.depends('first_name', 'last_name')
    def _compute_fields_combination(self):
        for com in self:
            if com.first_name:
                com.fullname = f"{str(com.first_name).title()}"
                if com.last_name:
                    com.fullname = f"{str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname = ""

    @api.onchange('first_name')
    def set_first_name_caps(self):
        if self.first_name:
            val = str(self.first_name)
            self.first_name = val.title()
        else:
            self.first_name = ""

    @api.onchange('last_name')
    def set_last_name_caps(self):
        if self.last_name:
            val = str(self.last_name)
            self.last_name = val.title()
        else:
            self.last_name = ""
