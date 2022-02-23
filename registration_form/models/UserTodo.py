# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _


# Name of file must follow name of class
class UserTodo(models.Model):
    _name = "user.todo"
    _description = "User Todo"

    name = fields.Char(string="Todo Title", required=True)
    description = fields.Text(string="Description")
    due_date = fields.Datetime(string="Due Date")

    # this is needed to define o2m field in odoo
    # this is corresponding to the field you want to create o2m form
    user_id = fields.Many2one(comodel_name="regis.user", string="User")