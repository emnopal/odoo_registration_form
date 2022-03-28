import json
from odoo import http, _, exceptions
from odoo.http import request, Response
from .Utils import JsonValidResponse

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
            - only required parameter: http://<host>:<port>/api/auth/login

        return:
            - JsonValidResponse: dict
        """

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
            - only required parameter: http://<host>:<port>/api/auth/logout

        return:
            - JsonValidResponse: dict
        """

        try:
            Response.status = "200"
            request.session.logout(keep_db=True)
            data = {'message': _('Logout successful')}
            return JsonValidResponse(data)
        except Exception as e:
            Response.status = "400"
            raise exceptions.AccessDenied(message=e)
