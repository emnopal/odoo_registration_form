# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
from odoo import api, fields, models, _


# Name of file must follow name of class
class ScheduleUser(models.Model):
    _name = "schedule.user"
    _description = "User Schedule Form"
    _inherit = [
        'mail.thread',  # for basic chatter
        'mail.activity.mixin'  # for activity in chatter
    ]
    _rec_name = 'name_seq'

    schedule_name = fields.Char(string='Schedule Name', required=True, size=64, tracking=True)
    user_id = fields.Many2one('regis.user', string='User', required=True, tracking=True)
    note = fields.Text(string='Note', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft', tracking=True)
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
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
