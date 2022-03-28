import imp
import json
from odoo import http, _
from .Utils import JsonValidResponse


class Check(http.Controller):

    @http.route(
        '/api/ping',
        auth="public", type="json", csrf=False
    )
    def CheckServer(self):

        """
        Check if server still alive

        Allowed Method:
            - GET
            - POST
            - PUT
            - DELETE
            - PATCH

        required parameter:
            None

        optional parameter:
            None

        usage:
            - only required parameter: http://<host>:<port>/api/ping

        return:
            - JsonValidResponse: dict
        """

        return JsonValidResponse({
            'message': _('okay, everything is working fine')
        })
