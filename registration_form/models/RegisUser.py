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
    _rec_name = 'fullname_seq'

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

    # Example of adding many2one field
    # We are going to use comodel_name res.partner as example
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', tracking=True)

    # Create sequence field
    reference = fields.Char(string='Reference', required=True, readonly=True, tracking=True, copy=False,
                            default=lambda self: _('New'))

    fullname_seq = fields.Char(string='Sequencing Fullname', compute='_compute_fields_combination_seq')

    # Simple overriding method

    # This is example how to override create method
    # vals is list of field that return the data field as dictionary
    # and create method is returning name of model db and their data that passed to db
    # more info: https://www.youtube.com/watch?v=_-fs_NBeOLI&list=PLqRRLx0cl0homY1elJbSoWfeQbRKJ-oPO&index=17
    # @api.model
    # def create(self, vals):
    #     return super(RegisUser, self).create(vals)

    # This is example how to override field with create method
    # to create default value of bio
    @api.model
    def create(self, vals):
        if not vals.get('bio'):
            vals['bio'] = "This is default bio"

        # this is how to add sequence to the form
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('regis.user') or _('New')

        return super(RegisUser, self).create(vals)

    # without create method
    # @api.onchange('bio')
    # def set_bio_default(self):
    #     if not self.bio:
    #         self.bio = "This is default bio"

    # This is example how to create new field (fullname) and sequence it
    # based from existing field (first, last)
    # This is computed field
    @api.depends('first_name', 'last_name', 'reference')
    def _compute_fields_combination_seq(self):
        for com in self:
            if com.first_name:
                com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()}"
                if com.last_name:
                    com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname_seq = f"{str(com.reference)} - "

    # This is example how to create new field (fullname)
    # based from existing field (first, last)
    # This is computed field
    @api.depends('first_name', 'last_name')
    def _compute_fields_combination(self):
        for com in self:
            if com.first_name:
                com.fullname = f"{str(com.first_name).title()}"
                if com.last_name:
                    com.fullname = f"{str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname = ""

    # This is example how to override field (without create method)
    # by changing first_name to title case automatically
    # this is also name onchange method, that means this function will execute
    # when field is changed
    # naming convention: onchange_{field_name}
    @api.onchange('first_name')
    def onchange_first_name(self):
        if self.first_name:
            val = str(self.first_name)
            self.first_name = val.title()
        else:
            self.first_name = ""

    # This is example how to override field (without create method)
    # by changing last_name to title case automatically
    # this is also name onchange method, that means this function will execute
    # when field is changed
    # naming convention: onchange_{field_name}
    @api.onchange('last_name')
    def onchange_last_name(self):
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
