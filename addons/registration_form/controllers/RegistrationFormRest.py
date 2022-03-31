import json
import logging
from odoo import http, _, exceptions
from odoo.http import request
from .Utils import JsonErrorResponse, JsonValidResponse

ENDPOINT = '/api/model'
_logging = logging.getLogger(__name__)


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
        [f'{ENDPOINT}/<string:model>', ],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetDatasInModel(self, model):
        """
        Get All Data in Model

        Allowed Method: GET

        required parameter:
            - model: str
                model name that available in odoo database

        optional parameter:
            - fields: str
                return only some fields

            - ids: int
                return only some ids

            - order: str
                order record by some fields (only available if ids is not set (if user query to all records))

            - limit: int
                limit the record (only available if ids is not set (if user query to all records))

            - filter: list
                filter the record (only available if ids is not set (if user query to all records))
                for filter syntax, we are using odoo standard, please refer to these link for usage:
                    - https://www.odoo.com/documentation/14.0/reference/sql.html
                    - https://www.odoo.com/forum/help-1/how-to-customize-search-in-order-to-simultaneusly-look-for-multiple-fields-140159
                    - https://learnopenerp.blogspot.com/2021/08/list-of-search-domain-operators-odoo.html

        usage:
            - only required parameter: /api/model/model.name
            - with optional parameter (with ids): /api/model/model.name?fields=field1,field2&ids=1,2,3
            - with optional parameter (without ids): /api/model/model.name?fields=field1,field2&order=id%20asc&limit=10&filter&filter=[('field1','=','value1'),('field2','=','value2')]

        return:
            success:
                - JsonValidResponse: dict
            failed:
                - JsonErrorResponse: dict
        """

        args = request.httprequest.args

        try:
            if args.get('ids'):
                ids = list(map(int, args.get('ids').split(',')))
                record = request.env[model].sudo().browse(ids)
            else:
                if args.get('order'):
                    order = args.get('order')
                else:
                    order = None
                if args.get('limit'):
                    limit = int(args.get('limit'))
                else:
                    limit = None
                if args.get('filter'):
                    filter = eval(args.get('filter'))
                else:
                    filter = []
                record = request.env[model].sudo().search(filter, order=order, limit=limit)
            records = record.read()
        except Exception as e:
            return JsonErrorResponse(_(f"Invalid: {e}"))

        if args.get('field') and args.get('field').strip() != '':
            fields = args.get('field').split(',')
            try:
                records = record.read(fields)
            except Exception as e:
                return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<string:field>', ],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetDatasFromAFieldInModel(self, model, field):
        """
        Get All Data in Model based on a field

        allowed method: GET

        required parameter:
            - model: str
                model name that available in odoo database
            - fields: str
                get a field from database model

        optional parameter:
            - fields: str
                return only some fields

            - ids: int
                return only some ids

            - order: str
                order record by some fields (only available if ids is not set (if user query to all records))

            - limit: int
                limit the record (only available if ids is not set (if user query to all records))

            - filter: list
                filter the record (only available if ids is not set (if user query to all records))
                for filter syntax, we are using odoo standard, please refer to these link for usage:
                    - https://www.odoo.com/documentation/14.0/reference/sql.html
                    - https://www.odoo.com/forum/help-1/how-to-customize-search-in-order-to-simultaneusly-look-for-multiple-fields-140159
                    - https://learnopenerp.blogspot.com/2021/08/list-of-search-domain-operators-odoo.html

        usage:
            - only required parameter: /api/model/model.name
            - with optional parameter (with ids): /api/model/model.name?fields=field1,field2&ids=1,2,3
            - with optional parameter (without ids): /api/model/model.name?fields=field1,field2&order=id%20asc&limit=10&filter&filter=[('field1','=','value1'),('field2','=','value2')]

        return:
            success:
                - JsonValidResponse: dict
            failed:
                - JsonErrorResponse: dict
        """

        args = request.httprequest.args

        try:
            if args.get('ids'):
                ids = list(map(int, args.get('ids').split(',')))
                record = request.env[model].sudo().browse(ids)
            else:
                if args.get('order'):
                    order = args.get('order')
                else:
                    order = None
                if args.get('limit'):
                    limit = int(args.get('limit'))
                else:
                    limit = None
                if args.get('filter'):
                    filter = eval(args.get('filter'))
                else:
                    filter = []
                record = request.env[model].sudo().search(filter, order=order, limit=limit)
            records = record.read()
        except Exception as e:
            return JsonErrorResponse(_(f"Invalid: {e}"))

        try:
            records = record.read([field])
        except Exception as e:
            return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<int:id>', ],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetADataInModel(self, model, id):
        """
        Get A Data in Model

        allowed method: GET

        required parameter:
            - model: str
                model name that available in odoo database
            - id: int
                return only some ids

        optional parameter:
            - fields: str

        usage:
            - only required parameter: /api/model/model.name/1
            - with optional parameter: /api/model/model.name/1?fields=field1,field2

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        try:
            record = request.env[model].sudo().browse(id)
        except Exception as e:
            return JsonErrorResponse(_(f"Invalid: {e}"))

        records = record.read()

        if args.get('field') and args.get('field').strip() != '':
            fields = args.get('field').split(',')
            try:
                records = record.read(fields)
            except Exception as e:
                return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route(
        [f'{ENDPOINT}/<string:model>/<int:id>/<string:field>', ],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetADataFromAFieldInModel(self, model, id, field):
        """
        Get A Data in Model based on a field

        allowed method: GET

        required parameter:
            - model: str
            - id: int
            - fields: str

        optional parameter:
            None

        usage:
            - only required parameter: /api/model/model.name/1/field

        return:
            - JsonValidResponse: dict
        """

        args = request.httprequest.args

        try:
            record = request.env[model].sudo().browse([id])
        except Exception as e:
            return JsonErrorResponse(_(f"Invalid: {e}"))

        try:
            records = record.read([field])
        except Exception as e:
            return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })
