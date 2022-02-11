# -*- coding: utf-8 -*-
{
    'name': 'Registration Form',

    # Version of module, if you set to 1.0 then it will be {odoo_version}.1.0. ex: 14.0.1.0
    # If you set to 14.0.1.0.5 then it still 14.0.1.0.5
    'version': '1.0',

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
        'data/sequence.xml',  # this is sequence file, for sequencing the registration form
        # third must be wizard file
        # fourth must be view file
        'views/regis.xml',
        'views/sale.xml',  # new view for sale from inherited view
        # fifth must be report file

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
