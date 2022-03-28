import imp
import json
from odoo import http, _
from .Utils import JsonValidResponse


class Check(http.Controller):

    """
        Check if server still alive
    """

    @http.route(
        '/api/ping',
        auth="public", type="json", csrf=False
    )
    def CheckServer(self):
        return JsonValidResponse({
            'message': _('okay, everything is working fine')
        })
