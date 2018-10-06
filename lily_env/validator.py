
# -- import all external validators, some of them will be overloaded
# -- with the custom implementations
import validators as vals  # noqa


NULL = 'NULL'


class ValidatorError(Exception):
    pass


def not_null(value):

    message = 'Null value are not allowed'

    if value is None:
        raise ValidatorError(message)


def url(url_text):

    message = f'Text "{url_text}" is not valid URL'

    if vals.url(url_text) is not True:
        raise ValidatorError(message)
