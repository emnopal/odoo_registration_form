import json
from odoo import http, _, exceptions
from odoo.http import request, Response
from .Utils import JsonValidResponse

ENDPOINT = '/api'
ENDPOINT_AUTH = '/api/auth'


class Auth(http.Controller):

    # Do not use json.dumps if type=='json'
    @http.route(
        f'{ENDPOINT_AUTH}/login',
        auth="none", type="json", methods=['POST'], csrf=False
    )
    def Login(self):
        params = request.jsonrequest
        try:
            request.session.authenticate(
                params['db'], params['login'], params['password'])
            Response.status = "200"
            return JsonValidResponse(request.env['ir.http'].session_info())
        except Exception as e:
            Response.status = "400"
            raise exceptions.AccessDenied(message=e)

    @http.route(
        f'{ENDPOINT_AUTH}/logout',
        auth="user", type="json", methods=['POST', 'GET'], csrf=False
    )
    def Logout(self):
        try:
            Response.status = "200"
            request.session.logout(keep_db=True)
            data = {'message': _('Logout successful')}
            return JsonValidResponse(data)
        except Exception as e:
            Response.status = "400"
            raise exceptions.AccessDenied(message=e)
