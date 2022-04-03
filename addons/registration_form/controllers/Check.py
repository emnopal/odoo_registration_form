from odoo import http, _
from .Utils import JsonErrorResponse, JsonValidResponse


class Check(http.Controller):

    @http.route(
        '/api/ping',
        auth="public", type="json", csrf=False
    )
    def CheckServer(self):
        try:
            return JsonValidResponse(_('Okay'))
        except Exception as e:
            return JsonErrorResponse(_(e))
