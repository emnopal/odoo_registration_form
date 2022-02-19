# -*- coding: utf-8 -*-
# need to add view of the wizard inside wizard folder not in views folder
# wizard is in WindowAction
from odoo import api, fields, models, _


# Naming convention: {name_of_model}Wizard
# Transient model need to add to security rule
class CreateScheduleWizard(models.TransientModel):  # Wizard don't need to store data to DB to avoid performance issues
    _name = "create.schedule.wizard"  # odoo standard is {name_of_model_in_db}.wizard
    _description = "Wizard for creating a schedule"

    name = fields.Char(string="Name")
    schedule_date = fields.Datetime(string="Schedule Date")
    user_id = fields.Many2one(comodel_name="regis.user", string="User", required=True)
    note = fields.Text(string="Note")

    # this is action of the wizard
    # if button on wizard is clicked, this method will be called
    def action_create_schedule(self):
        for com in self:
            # create a schedule, and write the data from wizard to schedule models
            # add the schedule field into dict
            # name of key must be same as field in the model you want to add the data
            vals = {
                "schedule_name": com.name,
                "date_schedule": com.schedule_date,
                "user_id": com.user_id.id,
                "note": com.note,
            }
            # after it, add to the model you want to add
            # for example schedule (schedule.user) model
            # this will return schedule.user(number_of_last_record_in_schedule_user,)
            # if you want to get the value from schedule.user just passing it to var
            # rec = self.env["schedule.user"].create(vals)
            # rec.note => to get note from schedule.user
            rec = self.env["schedule.user"].create(vals)

            # this is return view from backend side, so if button on wizard is clicked, it will return to the view
            # if this not initialized, if the button that corresponding to this method is clicked
            # it will return nothing and closed the wizard

            return {
                "name": _("Schedule"),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "schedule.user",
                "res_id": rec.id,
                "target": "current",  # if target is new, it still in popup wizard
                # if you don't specify target or target = current, it will return to the new view
            }

    def action_view_schedule(self):
        # this will return the view to corresponding user schedule

        # Method 1:
        # action = self.env['ir.actions.act_window'].for_xml_id('registration_form.schedule_user_action')
        # action["domain"] = [("user_id", "=", self.user_id.id)]  # this will filter the schedule based on user
        # return action

        # Method 2:
        # action = self.env.ref("registration_form.schedule_user_action").read()[0]
        # action["domain"] = [("user_id", "=", self.user_id.id)] # this will filter the schedule based on user
        # return action

        # Method 3:
        return {
            "name": _("Schedule"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "schedule.user",
            "domain": [("user_id", "=", self.user_id.id)],
            "context": {"default_user_id": self.user_id.id},
        }
