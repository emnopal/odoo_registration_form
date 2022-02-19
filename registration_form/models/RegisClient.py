# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


# this won't be shown in menu if it's not listed in the security rules
class RegisClient(models.Model):
    _name = "regis.client"
    _description = "Client Registration Form"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _rec_name = 'fullname_seq'

    first_name = fields.Char(string='First Name', required=True, size=64, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, size=64, tracking=True)
    age = fields.Integer(string='Age', size=5, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='male', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    bio = fields.Text(string='Bio', tracking=True)

    user_id = fields.Many2one(comodel_name='regis.user', string='User', tracking=True)

    # TODO: add one2many field here, to create user client

    reference = fields.Char(string='Reference', required=True, readonly=True, tracking=True, copy=False,
                            default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if not vals.get('bio'):
            vals['bio'] = "This is default bio"

        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('regis.client') or _('New')

        return super(RegisClient, self).create(vals)

    fullname_seq = fields.Char(string='Sequencing Fullname', compute='_compute_fields_combination_seq')

    @api.depends('first_name', 'last_name', 'reference')
    def _compute_fields_combination_seq(self):
        for com in self:
            if com.first_name:
                com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()}"
                if com.last_name:
                    com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname_seq = f"{str(com.reference)} - "

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

    # TODO: User count per client here

    @api.onchange('first_name')
    def onchange_first_name(self):
        for com in self:
            if com.first_name:
                val = str(com.first_name)
                com.first_name = val.title()
            else:
                com.first_name = ""

    @api.onchange('last_name')
    def onchange_last_name(self):
        for com in self:
            if com.last_name:
                val = str(com.last_name)
                com.last_name = val.title()
            else:
                com.last_name = ""

    @api.model
    def default_get(self, fields):
        res = super(RegisClient, self).default_get(fields)
        res['address'] = 'Jakarta, Indonesia'
        res['bio'] = 'This is default bio, delete this line if you want to create other bio'
        return res
