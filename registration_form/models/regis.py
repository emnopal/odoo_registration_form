# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FormRegist(models.Model):
    _name = "form.regist"
    _description = "Form Regist"

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='male')
    address = fields.Text(string='Address')

