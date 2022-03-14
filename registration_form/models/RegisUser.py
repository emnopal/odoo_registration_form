# -*- coding: utf-8 -*-

# To upgrade models you need to restart the server
import re
from odoo import api, fields, models, _
# this is for validation error exception
from odoo.exceptions import ValidationError


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
    # default order attribute, this will order by default of the field that specify here
    # you can use 1 or more field, eg: _order = "name, age desc" desc for desc, asc for asc or _order = "name desc, age asc"
    _order = "create_date desc, first_name asc"

    # specify the fields you want to add on inherit model
    # if you want to track the changes on the model (activate field tracking)
    # set tracking = True
    first_name = fields.Char(
        string='First Name', required=True, size=64, tracking=True)
    last_name = fields.Char(
        string='Last Name', required=True, size=64, tracking=True)
    age = fields.Integer(string='Age', size=5, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='male', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    bio = fields.Text(string='Bio', tracking=True)

    # To add status bar, you have to create state field in database
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft', tracking=True,
        copy=False)  # set copy to false, if you want to disable copy for this field)

    client_id = fields.Many2one(
        'regis.client', string='Client', tracking=True)  # foreign key

    # Example of adding many2one field
    # We are going to use comodel_name res.partner as example
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', tracking=True)  # foreign key

    # this is example for notebook and page section
    client_note = fields.Text(string='Client Note', tracking=True)
    partner_note = fields.Text(string='Partner Note', tracking=True)

    # one2many fields or many2many fields
    # naming field_name + _ids
    # inverse_name: name of the field that refers to this model in other model, is required to define o2m field
    user_todo_ids = fields.One2many(
        comodel_name='user.todo', inverse_name='user_id', string='User Todo')  # foreign key
    user_contact_ids = fields.One2many(
        comodel_name='user.contact', inverse_name='user_id', string='User Contact')  # foreign key

    # Simple overriding method
    # This is example how to override create method
    # vals is list of field that return the data field as dictionary
    # and create method is returning name of model db and their data that passed to db
    # more info: https://www.youtube.com/watch?v=_-fs_NBeOLI&list=PLqRRLx0cl0homY1elJbSoWfeQbRKJ-oPO&index=17
    # same as default_get method, but this only executed when form is saved
    # @api.model
    # def create(self, vals):
    #     return super(RegisUser, self).create(vals)

    # Create sequence field
    reference = fields.Char(string='Reference', required=True, readonly=True, tracking=True, copy=False,
                            default=lambda self: _('New'))

    # This is example how to override field with create method
    # to create default value of bio
    # for create method, don't need to iterate the data
    # same as default_get method, but this only executed when form is saved
    @api.model
    def create(self, vals):
        if not vals.get('bio'):
            vals['bio'] = "This is default bio"

        # this is how to add sequence to the form
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'regis.user') or _('New')

        return super(RegisUser, self).create(vals)

    # without create method
    # @api.onchange('bio')
    # def set_bio_default(self):
    #     if not self.bio:
    #         self.bio = "This is default bio"

    # This is example how to create new field (fullname) and sequence it
    # based from existing field (first, last)
    # This is computed field
    fullname_seq = fields.Char(
        string='Sequencing Fullname', compute='_compute_fields_combination_seq')

    # unless if compute method has depended on other field (with api.depends decorator)
    # naming will be: _compute_fields_ + {other name that explain how the method is working (optional)}
    @api.depends('first_name', 'last_name', 'reference')
    def _compute_fields_combination_seq(self):
        for com in self:
            if com.first_name:
                com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()}"
                if com.last_name:
                    com.fullname_seq = f"{str(com.reference)} - {str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname_seq = f"{str(com.reference)} - "

    # or you can use name_get method to combine sequence and name
    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = f"{rec.reference} - {rec.first_name} {rec.last_name}"
    #         result.append((rec.id, name))

    # This is example how to create new field (fullname)
    # based from existing field (first, last)
    # This is computed field
    fullname = fields.Char(
        string='Fullname', compute='_compute_fields_combination')

    # unless if compute method has depended on other field (with api.depends decorator)
    # naming will be: _compute_fields_ + {other name that explain how the method is working (optional)}
    @api.depends('first_name', 'last_name')
    def _compute_fields_combination(self):
        for com in self:
            if com.first_name:
                com.fullname = f"{str(com.first_name).title()}"
                if com.last_name:
                    com.fullname = f"{str(com.first_name).title()} {str(com.last_name).title()}"
            else:
                com.fullname = ""

    # This is example how to create new field (Schedule Count)
    # based from existing module that corresponding to this field (ScheduleUser)
    # This is computed field

    # Compute how many schedule per user
    schedule_count = fields.Integer(
        string='Schedule Count', compute='_compute_schedule_count')

    # naming: _compute_ + {field name} + _ + {other name that explain how the method is working (optional)}
    # (_ before compute means it is private method)
    def _compute_schedule_count(self):
        # if you add this on tree view, it will get singleton error
        # Because regis.user doesn't return a single record per data,
        # instead of it, it will return multiple record per data.
        # So it will get an error.
        # Odoo get confusing when translating the data,
        # so instead of giving any data, it will only give an error.
        # self.schedule_count = self.env['schedule.user'].search_count([('user_id', '=', self.id)])
        # this is a solution
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            com.schedule_count = self.env['schedule.user'].search_count(
                [('user_id', '=', com.id)])
        # equivalent with: select count(*) from `schedule_user` where `user_id` = `self.id`
        # if search_count without argument, it will return number of records in schedule_user

    # This is example how to override field (without create method)
    # by changing first_name to title case automatically
    # this is also name onchange method, that means this function will execute
    # when field is changed
    # naming convention: onchange_{field_name}
    @api.onchange('first_name')
    def onchange_first_name(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.first_name:
                val = str(com.first_name)
                com.first_name = val.title()
            else:
                com.first_name = ""

    # This is example how to override field (without create method)
    # by changing last_name to title case automatically
    # this is also name onchange method, that means this function will execute
    # when field is changed
    # naming convention: onchange_{field_name}
    @api.onchange('last_name')
    def onchange_last_name(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.last_name:
                val = str(com.last_name)
                com.last_name = val.title()
            else:
                com.last_name = ""

    # To add action into statusbar you have to create method on the class
    # since on the xml view, we specify type equal to object
    def action_confirm(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.state == 'confirm':
                raise ValidationError(_("User already confirmed"))
            com.state = 'confirm'

    def action_done(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.state == 'done':
                raise ValidationError(_("User already done"))
            com.state = 'done'

    def action_draft(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.state == 'draft':
                raise ValidationError(_("User already draft"))
            com.state = 'draft'

    def action_cancel(self):
        # so best practice is always iterate odoo module to avoid any singleton error
        for com in self:
            if com.state == 'cancel':
                raise ValidationError(_("User already cancel"))
            com.state = 'cancel'

    # overriding default value with default_get method
    # this method will be executed when form is opened
    # field will return field of the model (RegisUser)
    # super(RegisUser, self).default_get(fields) -> will return default value in model
    # same as create method, but this method will be executed when form is opened
    # so if form is opened, the value of field that specified in default_get will be returned
    # for example, if you set res['note'] = 'test', the form if opened, the note field will be 'test'
    # this is same as default value in view
    # <field name="context">{'default_age':24}</field> this will fill the form age with 24
    # why use this? because you can't set default value in view, only in model (server side) so it's more secure
    # and this is more flexible and fast than default value in view, because view can't be inherited
    @api.model
    def default_get(self, fields):
        # example
        res = super(RegisUser, self).default_get(fields)
        # if not res.get('gender'):
        #     res['gender'] = 'female' # default is male
        # return res
        res['address'] = 'Jakarta, Indonesia'
        res['bio'] = _(
            'This is default bio, delete this line if you want to create other bio')
        return res

    # add image field
    # by default image field is binary field
    avatar = fields.Binary(string='Avatar')

    # override copy method
    # this will override copy method if duplicate action is executed
    # note: _("str") is translation
    def copy(self, default=None):
        if default is None:
            default = {}
        default['first_name'] = self.first_name + _(' (copy)')
        default['last_name'] = self.last_name + _(' (copy)')
        default['bio'] = self.bio + _('. This is copy of bio')
        return super(RegisUser, self).copy(default)

    # for consistency reason, you shouldn't delete a record in done state
    # for avoid this, you can override the delete method to prevent delete in done state
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(
                _(f"Can't delete a record {self.fullname_seq}, because status is done"))
        return super(RegisUser, self).unlink()

    # constrains
    # unique constraints
    # i create an example of unique constraint field
    email = fields.Char(string='Email')

    @api.constrains('email')
    def check_email(self):
        for rec in self:
            if self.env['regis.user'].search([('email', '=', rec.email), ('id', '!=', rec.id)]):
                raise ValidationError(_(f"Email {rec.email} is already used"))
            else:
                if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', rec.email):
                    raise ValidationError('Not a valid email address')

    # not valid constraint
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age < 1 or rec.age > 150:
                raise ValidationError(_(f"{rec.age} is not a valid age"))

    # another example
    @api.constrains('first_name', 'last_name')
    def check_first_last_name(self):
        for rec in self:
            if rec.first_name == rec.last_name:
                raise ValidationError(_(f"Not a valid name"))

    # relating to schedule
    schedule_ids = fields.One2many(
        'schedule.user', 'user_id', string='Schedule Details')

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.google.com/',
            'target': 'new',  # new, open in new tab. self, open in current tab
        }

    # this is action for smart button in odoo
    def action_schedule_user(self):
        return {
            "name": _("Schedule"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "schedule.user",
            "domain": [("user_id", "=", self.id)],
            "context": {"default_user_id": self.id},
        }

    # create archive/unarchive button
    # default is True, if default is False, so all of data will be archived
    active = fields.Boolean(string='Active', default=True)
