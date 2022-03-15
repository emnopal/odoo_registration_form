# -*- coding: utf-8 -*-
{
    'name': 'Registration Form',

    # Version of module, if you set to 1.0 then it will be {odoo_version}.1.0. ex: 14.0.1.0
    # If you set to 14.0.1.0.5 then it still 14.0.1.0.5
    'version': '1.1',

    'summary': 'Simple Registration Form',

    # sequence, where to put the module in the menu
    'sequence': -100,

    'description': """Simple Registration Form""",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',

    'website': '',

    'license': '',

    # any module necessary for this one to work correctly
    'depends': [
        'sale',  # added sale here to make it work
        'mail',  # because mail is required since we use the mail.thread for Chatter view
        'report_xlsx',  # added report_xlsx here to make it work
        # https://apps.odoo.com/apps/modules/14.0/report_xlsx/
    ],
    # By default, all modules will inherit from base module of odoo

    # always loaded
    'data': [

        # this need following code convention,
        # first must be security file
        # if group_id:id is empty, then access will be grant globally
        # 1: True, 0: False
        'security/ir.model.access.csv',  # this is required for the registration form to work

        # second must be data file
        # user
        'data/user_regis_sequence.xml',  # this is sequence file, for sequencing the registration form
        # client
        'data/client_regis_sequence.xml',  # this is sequence file, for sequencing the registration form
        # schedule
        'data/schedule_sequence.xml',  # this is sequence file, for sequencing the schedule form

        # third must be wizard file
        # to create wizard, you must create new python module named wizard
        'wizards/create_schedule_form_wizard.xml',  # this is wizard file, for creating schedule form

        # fourth must be view file
        # User
        'views/user/regis/action/regis_view_action.xml',
        'views/user/regis/action/regis_partner_view_action.xml',
        'views/user/regis/action/regis_kids_view_action.xml',
        'views/user/regis/action/regis_male_view_action.xml',
        'views/user/regis/action/regis_female_view_action.xml',
        'views/user/regis/action/regis_draft_view_action.xml',
        'views/user/regis/action/regis_done_view_action.xml',
        'views/user/regis/action/regis_cancel_view_action.xml',
        'views/user/regis/action/regis_confirm_view_action.xml',
        'views/user/regis/view/regis_view_form.xml',
        'views/user/regis/view/regis_view_kanban.xml',
        'views/user/regis/view/regis_view_search.xml',
        'views/user/regis/view/regis_view_tree.xml',

        # Client
        'views/client/regis/action/regis_view_action.xml',
        'views/client/regis/view/regis_view_form.xml',
        'views/client/regis/view/regis_view_kanban.xml',
        'views/client/regis/view/regis_view_search.xml',
        'views/client/regis/view/regis_view_tree.xml',

        # if you have inherited new view from other module, then you have to upgrade the inherited module, not from parent module
        # Sale inherited view
        'views/sale/inherit_sale.xml',  # new view for sale from inherited view

        # Inherited res.partner view
        'views/partner/partner_view_inherited.xml',  # new view for partner from inherited view

        # Schedule View
        'views/schedule/action/schedule_view_action.xml',
        'views/schedule/action/schedule_cancel_view_action.xml',
        'views/schedule/action/schedule_done_view_action.xml',
        'views/schedule/action/schedule_confirm_view_action.xml',
        'views/schedule/action/schedule_draft_view_action.xml',
        'views/schedule/view/schedule_view_form.xml',
        'views/schedule/view/schedule_view_kanban.xml',
        'views/schedule/view/schedule_view_search.xml',
        'views/schedule/view/schedule_view_tree.xml',

        # Action Server
        'views/actions_server.xml',

        # fifth must be report file
        # report
        # PDF
        'reports/report_user_card_pdf.xml',  # template
        'reports/report_user_detail_pdf.xml',  # template
        # XLSX
        'reports/report_user_detail_xlsx.xml',  # template
        # TEXT
        'reports/report_user_detail_text.xml',  # template
        # HTML
        'reports/report_user_detail_html.xml',  # template
    ],

    # only loaded in demonstration mode
    'demo': [],

    'qweb': [],

    # If it's True, the modules will available in the addons menu to install
    'installable': True,

    'application': True,

    # If it's True, the modules will be auto-installed when all dependencies are installed
    'auto_install': False,
}
