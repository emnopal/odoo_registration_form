# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _


# Name of file must follow name of class
class RegisUser(models.Model):
    _name = "regis.user"
    _description = "User Registration Form"
    # if you want to inherit
    # _inherit = "{Model you want to inherit}", if inherit multiple model = _inherit = ["{Model 1}", "{Model 2}"]
    # Added Chatter View to the form
    _inherit = [
        'mail.thread',  # for basic chatter
        'mail.activity.mixin'  # for activity in chatter
    ]
    _rec_name = 'fullname'

    # specify the fields you want to add on inherit model
    # if you want to track the changes on the model (activate field tracking)
    # set tracking = True
    first_name = fields.Char(string='First Name', required=True, size=64, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, size=64, tracking=True)
    age = fields.Integer(string='Age', size=5, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='male', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    bio = fields.Text(string='Bio', tracking=True)
    fullname = fields.Char(string='Fullname', compute='_compute_fields_combination')

    # To add status bar, you have to create state field in database
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft', tracking=True)

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

    # To add action into statusbar you have to create method on the class
    # since on the xml view, we specify type equal to object
    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
