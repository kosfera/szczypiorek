
# Lily-Env - environment management for humans

**lily-env** allows one:
1. to define ones settings / credentials as a part of incredibly readable and flexible **yaml** format
2. using as an extra **template variables** and **imports**
3. and then define with minimal amount of code **environment parsers** which can be used to parse such yaml files
4. and allow one to use them directly in their python code
5. all of that on top of the mechanism allowing the secured storage and usage of most likely containing sensitive information yaml files.

## Getting Started

In order to start one needs those thing:

### Creating yaml env file

It should contain some sort of settings, let's create one under `deploy/development.yml` folder:

```yaml
aws:
  secret: this is my secret
  is_sensitive: true
  age_days: 121
```

### Creating parser

Somewhere in your code create a parser (e.g. `env.py`):

```python
import lily_env as ev


class MyEnvParser(ev.EnvParser):

    aws_secret = ev.CharField()

    aws_is_sensitive = ev.BooleanField()

    aws_age_days = ev.IntegerField()


env = MyEnvParser().parse()

```

Finally one must make sure that the yaml file will be protected therefore run in the terminal:
```bash
lily-env encrypt ./deploy
```

Make sure to add to `.gitignore`
```
.lily_env_encryption_key
deploy/development.yml
```

## FAQ

### How lily-env behaves when deployed?

When deployed for the parser to work correctly one needs two things:
1. A single `env.gpg` file available in the root of the project
2. A `.lily_env_encryption_key` storing the secret generated during the `encrypt` phase. WARNING! Make sure that this file is not kept in the repository itself but rather created dynamically during the deployment phase. Till that time it could be stored in for example `github secrets` or similar system such as `AWS secrets`, `Azure Key Vault` etc.

### How lily-env behaves locally?

For the `lily-env` to work locally one needs 3 things:
1. One `gpg` file for example `development.gpg`
2. A environment variable `LILY_ENV_PATH=development.gpg` pointing to that file's location
3. A `.lily_env_encryption_key` file where a secret for decryption is stored.

### One contributor changed gpg files would after PUSH & PULL sequence see the changes?

TODO: add it

### One contributor is changing the yaml files but the other cannot see those reflected in the gpg file?

TODO: add it

## The CLI - Available commands

TODO: add it

## The Environment Parser - Available fields

TODO: add it

USE BELOW LEGACY AS INSPIRATION:

Use the below example as a inspiration regarding type of fields one can define.

```python

import lily_env as env


class MyEnvParser(env.EnvParser):

    secret_key = env.CharField()

    is_important = env.BooleanField()

    aws_url = env.URLField()

    number_of_workers = env.IntegerField()

    unit_price = env.FloatField()

```

Each field supports the following arguments:

- `required` (boolean) - if environment variable is required to be present
- `default` (target type) - default to be used in case environment variable was not found
- `allow_null` (boolean) - if environment variable can be nullable
- `description` (str) - where one can describe the purpose of a given field when the name itself is not enough to capture it.

Besides those some fields are supporting extra fields:

- `CharField`:

    - `min_length` - validates if minimum amount of characters was provided
    - `max_length` - validates if maximum amount of characters was provided


## The Environment YAML files - Reference

TODO: add it
    - decribe the usage of template variables

## TODOS

There's still a lot of work to do, even though the basic functionality of **lily-env** is production ready:

- [ ] **[HIGH PRIO]** handle `as_env` and  `as_file` attributes of the fields

- [ ] **[HIGH PRIO]** use https://github.com/squidfunk/mkdocs-material for docs

- [ ] **[HIGH PRIO]** host the docs on github pages https://www.mkdocs.org/user-guide/deploying-your-docs/

- [ ] **[HIGH PRIO]** think about different name for the project since `lily-env` suggests as if the project has something to do with `lily` which is not true. `lily-env` is a generic tool that can be used in any python project.

- [ ] **[HIGH PRIO]** add an option to sync the secret of the admin

- [ ] **[HIGH PRIO]** for `encrypt` add a file which stores information about which `key` encoded which file so that one could in theory use strong key to encode one set of files and then use another one which can be shared to encode for example `development.yml`. The current idea is to introduce the 3rd field in the `.lily_env_encryption_key` file which then can be stored in the history.

- [ ] **[LOW PRIO]** Enable imports in the yml files. It should take the following form:
```yaml
imports:
  - shared.yml
  - development.yml
```
And then when running `encrypt` one stores at the level of gpg files all its dependencies therefore making it self contained. Before creating the gpg file it could create structure like:
```yaml
- filename: shared.yml
  content: ...

- filename: development.yml
  content: ...

# MAIN FILE
- filename: integration.yml
  content: ...
```
When running `decrypt` it "unpacks" all files with warnings that existing ones would be overwritten. There will be an option to force it without messages. When `decrypting` in the parser the imports are taken into account and therefore applied right away so the resulting `env` is just a result of applying all dependencies.

- [ ] **[LOW PRIO]** support **DB_POSTGRES_CONNECT validator**:
* it expects certain fields to be present
* it allows fields mapping

- [ ] **[LOW PRIO]** support **SENTRY_PING validator**:
* it uses https://develop.sentry.dev/sdk/store/
* it just pings the API

- [ ] **[LOW PRIO]** support **OAUTH2_PING validator**:
* it just creates a OAUTH2 session and tries not to fail while doing this

- [ ] **[LOW PRIO]** support **API_PING validator**:
* it just pings the API
* it allows fields mapping

- [ ] **[LOW PRIO]** support **AWS_S3_CLOUDFRONT_PING validator**:
* it just pings the endpoint

- [ ] **[LOW PRIO]** support **AWS_S3_BUCKET_LIST validator**:
* it just lists the bucket

- [ ] **[LOW PRIO]** support **AWS_POLLY_RENDER_SAMPLE validator**:
* it renders simple text

- [ ] **[LOW PRIO]** handle ROTATION of the **lily_env** secret itself. One can with one command run:
* `decrypt`
* render new key
* `encrypt`

- [ ] **[LOW PRIO]** support PRODUCTION gpg file where all validators etc are removed only the essential parts are left
