
from . import validators as val


class BaseField:

    def __init__(
            self,
            required=True,
            default=None,
            allow_null=False,
            description=None):

        self.required = required
        self.default = default
        self.allow_null = allow_null
        self.description = description

    def serialize(self, value):

        if not self.allow_null:
            val.not_null(value)

        elif value is None and self.allow_null:
            return val.NULL


class CharField(BaseField):

    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super(CharField, self).__init__(**kwargs)

    def serialize(self, value):

        # -- base validation
        serialized = super(CharField, self).serialize(value)
        if serialized == val.NULL:
            return None

        return value


class BooleanField(BaseField):

    def serialize(self, value):

        # -- base validation
        serialized = super(BooleanField, self).serialize(value)
        if serialized == val.NULL:
            return None

        if isinstance(value, bool):
            return value

        return value.upper() == 'TRUE'


class URLField(BaseField):

    def serialize(self, value):

        # -- base validation
        serialized = super(URLField, self).serialize(value)
        if serialized == val.NULL:
            return None

        URLValidator()(value)

        return value


class IntegerField(BaseField):

    def serialize(self, value):

        # -- base validation
        serialized = super(IntegerField, self).serialize(value)
        if serialized == val.NULL:
            return None

        return int(value)
