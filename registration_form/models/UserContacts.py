# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _


# Name of file must follow name of class
class UserContact(models.Model):
    _name = "user.contact"
    _description = "User Contact"

    contact = fields.Char(string="Contact", required=True)
    account = fields.Text(string="Account", required=True)
    description = fields.Text(string="Description")

    # this is needed to define o2m field in odoo
    # this is corresponding to the field you want to create o2m form
    user_id = fields.Many2one(comodel_name="regis.user", string="User")