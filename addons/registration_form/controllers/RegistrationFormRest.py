from odoo import http, _
from odoo.http import request
from .Utils import JsonValidResponse

ENDPOINT = '/api/model'


class RegistrationFormRest(http.Controller):

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
        [f'{ENDPOINT}/<string:model>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetDatasInModel(self, model):

        """
        Get All Data in Model

        Allowed Method:
            - GET

        required parameter:
            - Model: str

        optional parameter:
            - Fields: str
            - Ids: str|int

        usage:
            - only required parameter: http://<host>:<port>/api/model/model.name
            - with optional parameter: http://<host>:<port>/api/model/model.name?fields=field1,field2&ids=1,2,3

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        record = request.env[model].sudo().search([])

        if args.get('ids'):
            ids = list(map(int, args.get('ids').split(',') if args.get('ids') else []))
            record = request.env[model].sudo().browse(ids)

        records = record.read()

        if args.get('field') and args.get('field').strip() != '':
            fields = args.get('field').split(',')
            records = record.read(fields)

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<string:field>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetDatasFromAFieldInModel(self, model, field):

        """
        Get All Data in Model based on a field

        Allowed Method:
            - GET

        required parameter:
            - Model: str
            - Fields: str

        optional parameter:
            - Ids: str|int

        usage:
            - only required parameter: http://<host>:<port>/api/model/model.name/field
            - with optional parameter: http://<host>:<port>/api/model/model.name/field?ids=1,2,3

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        record = request.env[model].sudo().search([])

        if args.get('ids'):
            ids = list(map(int, args.get('ids').split(',') if args.get('ids') else []))
            record = request.env[model].sudo().browse(ids)

        records = record.read([field])

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<int:ids>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetADataInModel(self, model, ids):

        """
        Get A Data in Model

        Allowed Method:
            - GET

        required parameter:
            - Model: str
            - Ids: int

        optional parameter:
            - Fields: str

        usage:
            - only required parameter: http://<host>:<port>/api/model/model.name/1
            - with optional parameter: http://<host>:<port>/api/model/model.name/1?fields=field1,field2

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        record = request.env[model].sudo().browse([ids])
        records = record.read()

        if args.get('field') and args.get('field').strip() != '':
            fields = args.get('field').split(',')
            records = record.read(fields)

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<int:ids>/<string:field>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetADataFromAFieldInModel(self, model, ids, field):

        """
        Get A Data in Model based on a field

        Allowed Method:
            - GET

        required parameter:
            - Model: str
            - Ids: int
            - Fields: str

        optional parameter:
            None

        usage:
            - only required parameter: http://<host>:<port>/api/model/model.name/1/field

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        record = request.env[model].sudo().browse([ids])
        records = record.read([field])

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

