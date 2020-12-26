
import os

import yaml

from .fields import BaseField
from .crypto import decrypt
from .utils import yaml_is_valid, fix, flatten, substitute


class Env:

    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)


class EnvParser:

    def __init__(self):
        env_path = os.environ.get('LILY_ENV_PATH', 'env.gpg')

        # FIXME: !!!! add one complex test!!!
        with open(env_path, 'r') as f:
            env = decrypt(f.read())
            yaml_is_valid(env)
            env = fix(env)
            env = yaml.load(env, Loader=yaml.FullLoader)
            env = flatten(env)
            env = substitute(env)

        env_variables = {}
        for field_name, field in self.fields.items():
            if field.required:
                raw_value = env[field_name]

            else:
                raw_value = env.get(field_name, field.default)

            env_variables[field_name] = field.to_python(field_name, raw_value)

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
