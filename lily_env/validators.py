
# -- import all external validators, some of them will be overloaded
# -- with the custom implementations
from validators import *  # noqa


NULL = 'NULL'


class ValidationError(Exception):
    pass


def not_null_validator(value):

    message = 'Null value are not allowed'

    if value is None:
        raise utils.ValidationFailure(message)


def url(url_text):

    if url.url(url_text)
