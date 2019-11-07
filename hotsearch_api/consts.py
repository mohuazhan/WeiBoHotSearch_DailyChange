# encoding: utf-8

from collections import namedtuple


response = [
    'OK',
    'BAD_REQUEST',
    'UNAUTHORIZED',
    'NOT_FOUND',
    'METHOD_NOT_ALLOWED',
    'INTERNAL_SERVER_ERROR',
]

# response code
_response_code = namedtuple('RESPONSE_CODE', response)
RESPONSE_CODE = _response_code(200, 400, 401, 404, 405, 500)

# response message
_response_msg = namedtuple('RESPONSE_MSG', response)
RESPONSE_MSG = _response_msg(
    'OK',
    'Bad Request',
    'Unauthorized',
    'Not Found',
    'Method Not Allowed',
    'Internal Server Error',
)


# manage all url
