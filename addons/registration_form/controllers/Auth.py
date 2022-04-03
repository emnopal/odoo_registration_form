from odoo import http, _, exceptions
from odoo.http import request, Response
from .Utils import JsonErrorResponse, JsonValidResponse

ENDPOINT_AUTH = '/api/auth'


class Auth(http.Controller):

    """
    just for example
    Do not use json.dumps if type=='json'

    @http.route(
        f'{ENDPOINT}/test/<type:param>',
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def SampleRoute(self, param):
        args = request.httprequest.args # get parameter from url
        jsonargs = request.jsonrequest # get parameter from json
        data = {
            'param1': args.get('param1'),
            'param2': args.get('param2'),
        }
        return JsonValidResponse(data)
    """

    @http.route(
        f'{ENDPOINT_AUTH}/login',
        auth="none", type="json", methods=['POST'], csrf=False
    )
    def Login(self):

        params = request.jsonrequest
        try:
            request.session.authenticate(
                params['db'], params['username'], params['password'])
            return JsonValidResponse(request.env['ir.http'].session_info())
        except Exception as e:
            if str(e) == _('Access Denied'):
                return JsonErrorResponse(_('Unauthorized, Access Denied. Check your db, username or password'), 401)
            return JsonErrorResponse(_(f'Missing required fields: {e}'), 400)

    @http.route(
        f'{ENDPOINT_AUTH}/logout',
        auth="user", type="json", methods=['GET', 'POST'], csrf=False
    )
    def Logout(self):

        try:
            request.session.logout(keep_db=True)
            return JsonValidResponse(_('Logout successful'))
        except Exception as e:
            return JsonErrorResponse(_(e))
