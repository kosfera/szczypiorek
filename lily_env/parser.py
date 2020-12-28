
import os

from .fields import BaseField
from .crypto import decrypt
from .utils import load_yaml, flatten, substitute


class Env:

    def __init__(self, **env):
        for k, v in env.items():
            setattr(self, k, v)

        self.env = env


class EnvParser:

    def __init__(self):
        env_path = os.environ.get('LILY_ENV_PATH', 'env.gpg')

        with open(env_path, 'r') as f:
            env = decrypt(f.read())
            env = load_yaml(env)
            env = flatten(env)
            env = substitute(env)

        env_variables = {}
        for field_name, field in self.fields.items():
            if field.required:
                raw_value = env[field_name]

            else:
                raw_value = env.get(field_name, field.default)

            env_variables[field_name] = field.to_python(field_name, raw_value)

        self._env_variables = env_variables

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
        return Env(**self._env_variables)
