import json
from odoo import http, _, exceptions
from odoo.http import request, Response  # need authentication to odoo

ENDPOINT = '/api'
ENDPOINT_AUTH = '/api/auth'


class Auth(http.Controller):

    # Do not use json.dumps if type=='json'
    @http.route(
        f'{ENDPOINT_AUTH}/login',
        auth="none", type="json", methods=['POST'], csrf=False
    )
    def login(self):
        params = request.jsonrequest
        try:
            request.session.authenticate(
                params['db'], params['login'], params['password'])
            Response.status = "200"
            return {
                'status_code': Response.status,
                'message': 'success',
                'response': {
                    'data': request.env['ir.http'].session_info()
                }
            }
        except Exception as e:
            Response.status = "400"
            raise exceptions.AccessDenied(message=e)

    @http.route(
        f'{ENDPOINT_AUTH}/logout',
        auth="user", type="json", methods=['POST', 'GET'], csrf=False
    )
    def logout(self):
        try:
            Response.status = "200"
            request.session.logout(keep_db=True)
            return {
                'status_code': Response.status,
                'message': 'success',
                'response': {
                    'message': _('Logout successful')
                }
            }
        except Exception as e:
            Response.status = "400"
            raise exceptions.AccessDenied(message=e)
