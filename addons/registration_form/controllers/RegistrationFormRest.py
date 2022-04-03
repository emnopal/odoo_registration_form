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
        f'{ENDPOINT}/<string:model>/<int:rec_id>',
        f'{ENDPOINT}/<string:model>/<int:rec_id>/<string:field>',
    ], auth="user", type="json", methods=['GET'], csrf=False)
    def GetData(self, model, rec_id=None, field=None):

        args = request.httprequest.args

        try:
            if rec_id:
                record = request.env[model].sudo().browse(rec_id)
            else:
                if args.get('rec_ids'):
                    rec_ids = list(map(int, args.get('rec_ids').split(',')))
                    record = request.env[model].sudo().browse(rec_ids)
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

    @http.route([
        f'{ENDPOINT}/<string:model>',
        f'{ENDPOINT}/<string:model>/<int:rec_id>',
    ], auth="user", type="json", methods=['PUT'], csrf=False)
    def PutData(self, model, rec_id=None):

        params = request.jsonrequest
        args = request.httprequest.args

        try:
            records = request.env[model].sudo()
            if rec_id:  # return singleton record
                record = records.browse(rec_id).ensure_one()
                data = rec_id
            else:
                if args.get('rec_ids'):  # return multiple records
                    rec_ids = list(map(int, args.get('rec_ids').split(',')))
                    record = records.browse(rec_ids)
                    data = rec_ids
                else:
                    # return multiple records (or maybe single record) by filter
                    if args.get('filter'):
                        filter = eval(args.get('filter'))
                        record = records.search(filter)
                        data = args.get('filter')
                    else:  # if no filter, raise error
                        data = None
                        raise exceptions.ValidationError(_('Invalid filter'))
        except Exception as e:
            return JsonErrorResponse({
                'result': False,
                'message': _(f"Invalid update {data}: {e}"),
            })

        try:
            result = record.write(params)
        except Exception as e:
            return JsonErrorResponse({
                'result': False,
                'message': _(f"Invalid update {data}: {e}"),
            })

        return JsonValidResponse({
            'result': True,
            'message': _(f"Successfully update {data}"),
        })

    @http.route([
        f'{ENDPOINT}/<string:model>',
        f'{ENDPOINT}/<string:model>/<int:rec_id>',
    ], auth="user", type="json", methods=['DELETE'], csrf=False)
    def DeleteData(self, model, rec_id=None):

        params = request.jsonrequest
        args = request.httprequest.args

        try:
            records = request.env[model].sudo()
            if rec_id:  # return singleton record
                record = records.browse(rec_id).ensure_one()
                data = rec_id
            else:
                if args.get('rec_ids'):  # return multiple records
                    rec_ids = list(map(int, args.get('rec_ids').split(',')))
                    record = records.browse(rec_ids)
                    data = rec_ids
                else:
                    # return multiple records (or maybe single record) by filter
                    if args.get('filter'):
                        filter = eval(args.get('filter'))
                        record = records.search(filter)
                        data = args.get('filter')
                    else:  # if no filter, raise error
                        data = None
                        raise exceptions.ValidationError(_('Invalid filter'))
        except Exception as e:
            return JsonErrorResponse({
                'result': False,
                'message': _(f"Invalid delete {data}: {e}"),
            })

        try:
            result = record.unlink()
        except Exception as e:
            return JsonErrorResponse({
                'result': False,
                'message': _(f"Invalid delete {data}: {e}"),
            })

        return JsonValidResponse({
            'result': True,
            'message': _(f"Successfully delete {data}"),
        })
