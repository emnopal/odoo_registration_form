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

    @http.route([
            f'{ENDPOINT}/<string:model>',
            f'{ENDPOINT}/<string:model>/<string:field>',
            f'{ENDPOINT}/<string:model>/<int:id>',
            f'{ENDPOINT}/<string:model>/<int:id>/<string:field>',
        ], auth="user", type="json", methods=['GET'], csrf=False)
    def GetData(self, model, id=None, field=None):

        args = request.httprequest.args

        try:
            if id:
                record = request.env[model].sudo().browse(id)
            else:
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

                    if args.get('offset'):
                        offset = int(args.get('offset'))
                    else:
                        offset = 0
                    record = request.env[model].sudo().search(
                        filter, order=order, limit=limit, offset=offset)
        except Exception as e:
            return JsonErrorResponse(_(f"Invalid: {e}"))

        try:
            if field:
                records = record.read([field])
            else:
                if args.get('fields') and args.get('fields').strip() != '':
                    fields = args.get('fields').split(',')
                    records = record.read(fields)
                else:
                    records = record.read()
        except Exception as e:
            return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'length_record': len(records),
            'record': records,
        })

    @http.route([
            f'{ENDPOINT}/<string:model>',
        ], auth="user", type="json", methods=['POST'], csrf=False)
    def PostData(self, model):
        params = request.jsonrequest

        try:
            record = request.env[model].sudo().create(params)
        except Exception as e:
            return JsonErrorResponse(_(e))

        return JsonValidResponse({
            'result': record.id,
        })

