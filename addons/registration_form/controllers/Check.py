from odoo import http, _
from .Utils import JsonErrorResponse, JsonValidResponse


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
            - only required parameter: /api/ping

        return:
            - JsonValidResponse: dict
        """

        try:
            return JsonValidResponse('Okay')
        except Exception as e:
            return JsonErrorResponse(e)
