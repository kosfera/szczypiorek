
import re

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

    # -- in order to force the underlying library to work correctly
    # -- with websockets protocol as well as some other future protocols
    # -- the following trick must be included
    modified_url_text = re.sub(r'^wss?', 'http', url_text)
    if vals.url(modified_url_text) is not True:
        raise ValidatorError(message)

    return True


def length(text, min_length=None, max_length=None):

    if min_length:
        message = (
            f'Text "{text}" is too short. min length: {min_length}')

        if vals.length(text, min=min_length) is not True:
            raise ValidatorError(message)

    if max_length:
        message = (
            f'Text "{text}" is too long. max length: {max_length}')

        if vals.length(text, max=max_length) is not True:
            raise ValidatorError(message)

    return True
