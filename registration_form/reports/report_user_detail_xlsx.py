from odoo import models, fields, api, _


class ReportUserDetailXLSX(models.AbstractModel):
    _name = 'report.registration_form.report_user_detail_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format = workbook.add_format({'font_size': 12, 'align': 'vcenter'})
        row = 0
        col = 0

        for line in lines:

            sheet0 = workbook.add_worksheet(f"{line.reference} Details")

            sheet0.write(row, col, 'UID', format)
            sheet0.write(row+1, col, line.reference, format)

            col += 1
            sheet0.write(row, col, 'Name', format)
            sheet0.write(row+1, col, line.fullname, format)

            col += 1
            sheet0.write(row, col, 'Email', format)
            sheet0.write(row+1, col, line.email, format)

            col += 1
            sheet0.write(row, col, 'Age', format)
            sheet0.write(row+1, col, line.age, format)

            col += 1
            sheet0.write(row, col, 'Gender', format)
            sheet0.write(row+1, col, line.gender, format)

            col += 1
            sheet0.write(1, 6, 'Address', format)
            sheet0.write(row+1, col, line.address, format)

            col += 1
            sheet0.write(row, col, 'Bio', format)
            sheet0.write(row+1, col, line.bio, format)

            col += 1
            sheet0.write(row, col, 'State', format)
            sheet0.write(row+1, col, line.state, format)

            col += 1
            sheet0.write(row, col, 'Partner Name', format)
            sheet0.write(row+1, col, line.partner_id.name, format)

            col += 1
            sheet0.write(row, col, 'Partner Note', format)
            sheet0.write(row+1, col, line.partner_note, format)

            col += 1
            sheet0.write(row, col, 'Client Name', format)
            sheet0.write(row+1, col, line.client_id.fullname, format)

            col += 1
            sheet0.write(row, col, 'Client Note', format)
            sheet0.write(row+1, col, line.client_note, format)

            col += 1
            sheet0.write(row, col, 'Create Date', format)
            sheet0.write(row+1, col, line.create_date, format)
