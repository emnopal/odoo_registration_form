# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError # this is for validation error exception

_logger = logging.getLogger(__name__) # Show logs based on the module name
# if you want to log validation error, use Warning instead of any

# this won't be shown in menu if it's not listed in the security rules
class RegisClient(models.Model):
    _name = "regis.client"
    _description = "Client Registration Form"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _rec_name = 'fullname_seq'
    # default order attribute, this will order by default of the field that specify here
    # you can use 1 or more field, eg: _order = "name, age desc" desc for desc, asc for asc or _order = "name desc, age asc"
    _order = "create_date desc, first_name asc"

    first_name = fields.Char(string='First Name', required=True, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='male', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    bio = fields.Text(string='Bio', tracking=True)

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
        res['bio'] = _('This is default bio, delete this line if you want to create other bio')
        return res

    # override copy method
    # this will override copy method if duplicate action is executed
    def copy(self, default=None):
        if default is None:
            default = {}
        default['first_name'] = self.first_name + _(' (copy)')
        default['last_name'] = self.last_name + _(' (copy)')
        default['bio'] = self.bio + _('. This is copy of bio')
        _logger.warning(f"{default['id']} is coppied")
        return super(RegisClient, self).copy(default)

    # not valid constraint
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age < 1 or rec.age > 150:
                _logger.warning('Age is not valid')
                raise ValidationError(_(f"{rec.age} is not a valid age"))

    # another example
    @api.constrains('first_name', 'last_name')
    def check_first_last_name(self):
        for rec in self:
            if rec.first_name == rec.last_name:
                _logger.warning('Not a valid name')
                raise ValidationError(_(f"Not a valid name"))

    # create archive/unarchive button
    active = fields.Boolean(string='Active', default=True) # default is True, if default is False, so all of data will be archived