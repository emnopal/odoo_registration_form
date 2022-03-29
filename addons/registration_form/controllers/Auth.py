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
        """
        Authenticate User

        Allowed Method:
            - POST

        required parameter:
            - db: str
            - login: str
            - password: str

        optional parameter:
            None

        usage:
            - only required parameter: /api/auth/login

        return:
            - JsonValidResponse: dict
        """

        params = request.jsonrequest
        try:
            request.session.authenticate(
                params['db'], params['username'], params['password'])
            return JsonValidResponse(request.env['ir.http'].session_info())
        except Exception as e:
            if str(e) == 'Access Denied':
                return JsonErrorResponse('Unauthorized, Access Denied. Check your db, username or password', 401)
            return JsonErrorResponse(f'Missing required fields: {e}', 400)

    @http.route(
        f'{ENDPOINT_AUTH}/logout',
        auth="user", type="json", methods=['POST', 'GET'], csrf=False
    )
    def Logout(self):
        """
        Remove Session

        Allowed Method:
            - GET
            - POST

        required parameter:
            None

        optional parameter:
            None

        usage:
            - only required parameter: /api/auth/logout

        return:
            - JsonValidResponse: dict
        """

        try:
            request.session.logout(keep_db=True)
            return JsonValidResponse({'message': _('Logout successful')})
        except Exception as e:
            return JsonErrorResponse(e)
