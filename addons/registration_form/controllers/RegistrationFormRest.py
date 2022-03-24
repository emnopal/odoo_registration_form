import json
from odoo import http, _, exceptions
from odoo.http import request, Response  # need authentication to odoo

ENDPOINT = '/api'


class DatetimeEncoder(json.JSONEncoder):

    """
        Avoid `TypeError: Object of type datetime is not JSON serializable` Exception
        https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


class RegistrationFormRest(http.Controller):

    """
    just for example
    @http.route(
        f'{ENDPOINT}/test', # use http if you want to use query parameter
        auth="user", type="http", methods=['GET'], csrf=False
    )
    def test_route(self, **kwargs):
        return json.dumps({
            'param1': kwargs.get('param1'),
            'param2': kwargs.get('param2'),
        })
    """

    @http.route(
        f'{ENDPOINT}/get/<string:model_name>',
        auth="user", type="http", methods=['GET'], csrf=False
    )
    def get_db_data(self, model_name, **kwargs):
        model = request.env[model_name].sudo().search([])
        if kwargs.get('length'):
            if kwargs.get('length') in [1,"1", 'True', 'true']:
                rec = {}
                for record in model:
                    rec[record.id] = {
                        'id': record.id,
                        'name': record.name,
                    }
                return json.dumps({
                    'status_code': 200,
                    'message': 'success',
                    'response': {
                        'data': {
                            'list': rec,
                            'length': len(model),
                        }
                    }
                })
        Response.status = "200"
        return json.dumps({
            'status_code': Response.status,
            'message': 'success',
            'response': {
                'data': model.read()
            }
        }, cls=DatetimeEncoder)
