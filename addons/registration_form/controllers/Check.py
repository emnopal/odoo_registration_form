import json
from odoo import http, _


class Check(http.Controller):

    @http.route(
        '/api/ping',
        auth="public", type="http", csrf=False
    )
    def CheckServer(self):
        return json.dumps({
            'status_code': 200,
            'message': 'success',
            'response': {
                'message': _('okay, everything is working fine')
            }
        })
