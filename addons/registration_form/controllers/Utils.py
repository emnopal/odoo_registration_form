from odoo.http import Response
import json
from odoo import http, _, exceptions


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


def JsonValidResponse(data, valid_code=200):
    """
    Return a JsonResponse with the given data and status code if code is valid or no exceptions.
    """
    Response.status = str(valid_code)
    return {
        'status_code': valid_code,
        'message': _('success'),
        'data': data
    }

def JsonErrorResponse(error, error_code=400):
    """
    Return a JsonResponse with the given data and status code if code is not valid or with exceptions.
    """
    Response.status = str(error_code)
    return {
        'code': error_code,
        'message': _('failed'),
        'error': error
    }

