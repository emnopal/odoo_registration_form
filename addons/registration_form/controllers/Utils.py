import json


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


def JsonValidResponse(data, status=200):
    """
        Return a JsonResponse with the given data and status code.
    """
    return {
        'status_code': status,
        'message': 'success',
        'response': {
            'data': data
        }
    }