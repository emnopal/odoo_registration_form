# -*- coding: utf-8 -*-
# need to add view of the wizard inside wizard folder not in views folder
# wizard is in WindowAction
from odoo import api, fields, models, _


# Naming convention: {name_of_model}Wizard
# Transient model need to add to security rule
class CreateScheduleWizard(models.TransientModel):  # Wizard don't need to store data to DB to avoid performance issues
    _name = "create.schedule.wizard"  # odoo standard is {name_of_model_in_db}.wizard
    _description = "Wizard for create schedule"

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one(comodel_name="regis.user", string="User", required=True)

    # this is action of the wizard
    # if button on wizard is clicked, this method will be called
    def action_create_schedule(self):
        for com in self:
            print("Create schedule: ", com, com.name, com.user_id)
