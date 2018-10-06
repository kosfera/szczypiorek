
import json
import os

from .fields import BaseField


class Env:
    """
    Class which captures all already validated and discovered environment
    variables.

    """

    # FIXME: test it!!!
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        with open('./env_dump.json', 'w') as f:
            f.write(json.dumps(kwargs))

    # FIXME: test it!!!
    @classmethod
    def from_dump(cls):
        with open('./env_dump.json', 'r') as f:
            return json.loads(f.read())


class NotUniqueError(Exception):
    pass


class EnvParser:

    instance = None

    def __init__(self):
        # FIXME: test it!!!
        if self.instance:
            raise NotUniqueError(
                'One can have only one instance of `EnvParser`')

        else:
            self.instance = self

        env_variables = {}
        for field_name, field in self.fields.items():
            if field.required:
                raw_value = os.environ[field_name.upper()]

            else:
                raw_value = os.environ.get(
                    field_name.upper(), field.default)

            env_variables[field_name] = field.serialize(raw_value)

        self.env_variables = env_variables

    @property
    def fields(self):
        fields = {}
        for name in dir(self):
            if name != 'fields':
                attr = getattr(self, name)
                if isinstance(attr, BaseField):
                    fields[name] = attr

        return fields

    def parse(self):
        return Env(**self.env_variables)
