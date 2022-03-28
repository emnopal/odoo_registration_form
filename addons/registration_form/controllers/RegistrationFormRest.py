from odoo import http, _
from odoo.http import request
from .Utils import JsonValidResponse

ENDPOINT = '/api'


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
        data = {
            'param1': args.get('param1'),
            'param2': args.get('param2'),
        }
        return JsonValidResponse(data)

    """

    @http.route(
        [f'{ENDPOINT}/model/<string:model>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetDataInModel(self, model):
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
        [f'{ENDPOINT}/model/<string:model>/<int:ids>',],
        auth="user", type="json", methods=['GET'], csrf=False
    )
    def GetADataInModel(self, model, ids):
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
