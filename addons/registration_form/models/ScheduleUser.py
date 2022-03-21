# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError # this is for validation error exception


# Name of file must follow name of class
class ScheduleUser(models.Model):
    _name = "schedule.user"
    _description = "User Schedule Form"
    _inherit = [
        'mail.thread',  # for basic chatter
        'mail.activity.mixin'  # for activity in chatter
    ]
    _rec_name = 'name_seq'
    # default order attribute, this will order by default of the field that specify here
    # you can use 1 or more field, eg: _order = "name, age desc" desc for desc, asc for asc or _order = "name desc, age asc"
    _order = "create_date desc, schedule_name asc"

    schedule_name = fields.Char(string='Schedule Name', required=True, tracking=True)
    user_id = fields.Many2one('regis.user', string='User', required=True, tracking=True)
    note = fields.Text(string='Note', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft', tracking=True, copy=False) # set copy to false, if you want to disable copy for this field
    address = fields.Text(string='Address', tracking=True)

    # Create sequence field
    schedule_reference = fields.Char(string='Schedule Reference', required=True, readonly=True, tracking=True,
                                     copy=False, default=lambda self: _('New'))

    name_seq = fields.Char(string='Sequencing Name', compute='_compute_fields_combination_seq')

    # this is field for date
    # date_schedule = fields.Date(string='Date Schedule', tracking=True, default=fields.Date.today())

    # this is field for datetime
    date_schedule = fields.Datetime(string='Date Schedule', tracking=True, default=fields.Datetime.now(), required=True)

    # this will add the data from related field
    # Add related field based on many2one field
    partner = fields.Many2one('res.partner', string='Partner', related='user_id.partner_id')

    # or related field based on another field
    age = fields.Integer(string='Age', related='user_id.age')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "None"
        if vals.get('schedule_reference', _('New')) == _('New'):
            vals['schedule_reference'] = self.env['ir.sequence'].next_by_code('schedule.user') or _('New')
        return super(ScheduleUser, self).create(vals)

    # This is compute field
    @api.depends('schedule_name', 'schedule_reference')
    def _compute_fields_combination_seq(self):
        for com in self:
            if com.schedule_name:
                com.name_seq = f"{str(com.schedule_reference)} - {str(com.schedule_name).title()}"
            else:
                com.name_seq = f"{str(com.schedule_reference)} - "

    # onchange method
    @api.onchange('schedule_name')
    def onchange_schedule_name(self):
        if self.schedule_name:
            val = str(self.schedule_name)
            self.schedule_name = val.title()
        else:
            self.schedule_name = ""

    # This will add the data from related field that correspond from m2o field
    @api.onchange('user_id')
    def onchange_address(self):
        if self.user_id:
            if self.user_id.address:
                self.address = self.user_id.address
        else:
            self.address = ""

    # To add action into statusbar you have to create method on the class
    # since on the xml view, we specify type equal to object
    def action_confirm(self):
        for status in self:
            if status.state == 'confirm':
                raise ValidationError(_('You cannot confirm twice'))
            status.state = 'confirm'

    def action_done(self):
        for status in self:
            if status.state == 'done':
                raise ValidationError(_('Schedule is already done'))
            status.state = 'done'

    def action_draft(self):
        for status in self:
            if status.state == 'draft':
                raise ValidationError(_('Schedule is already draft'))
            status.state = 'draft'

    def action_cancel(self):
        for status in self:
            if status.state == 'cancel':
                raise ValidationError(_('Schedule is already cancel'))
            status.state = 'cancel'

    # override copy method
    # this will override copy method if duplicate action is executed
    def copy(self, default=None):
        if default is None:
            default = {}
        default['schedule_name'] = self.schedule_name + _(' (copy)')
        default['note'] = self.note + _('. This is copy of note')
        return super(ScheduleUser, self).copy(default)

    # for consistency reason, you shouldn't delete a record in done state
    # for avoid this, you can override the delete method to prevent delete in done state
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_(f"Can't delete a record {self.name_seq}, because status is done"))
        return super(ScheduleUser, self).unlink()

    # create archive/unarchive button
    active = fields.Boolean(string='Active', default=True) # default is True, if default is False, so all of data will be archived
