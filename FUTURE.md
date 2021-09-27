
Szczypiorek must evolve in order to deal with some of the issue seen in the current version

# The issues

- it's hard to avoid difficult to fix conflicts in a collaborative environment for example when multiple people are changing same .szczyp file
- yaml that is recreated from .szczyp file lacks the structure, ordering and comments of the orignal one.

# The goal

We want a tool which can transform a given yml in a way that is:
- not obstructing its original form (leaves comments, original ordering, empty lines etc.)
- easily deals with multiple people changing same .szczyp file
- is very easy to start with and use directly in the python code.

## The solution

1. Allow users to create arbitrary .yml (multi document one like in k8s or single document like in API settings)
2. The original .yml is literally cloned and all of its values (leaves) replaced by szczyp keys.

For example if original file is `development.yaml` and has the following content:

```yaml
# hello world this is my comment
auth-service:
    db:
        password: secret123
        user: jack
---
media-service:
    jacky: chang
```

Then after performing `szczypiorek encrypt development.yaml` one will produce two files

`development-szczyp.yaml` with the following content:

```yaml
# hello world this is my comment
auth-service:
    db:
        password: 'szczyp://auth-service/db/password'
        user: 'szczyp://auth-service/db/user'
---
media-service:
    jacky: 'szczyp://media-service/jacky'
```

and `development.szczyp` with the following content:

```txt
auth-service/db/password: ds9d0s9d0sd9s0d9s0d9s0DSDSDAGA
auth-service/db/user: ds0cxxzCZSD54590ZS54590XCS545
media-service/jacky: ds90s9d0sd9s09xs0
```

Now having two versioned controlled files: `development-szczyp.yaml` and `development.szczyp` one can easily reproduce exactly the content of `development.yml`. Additionally `development.szczyp` stores one secret per line therefore it's very git-friendly and easy to work with in the case of git conflicts.

As an extra the warning should be created every time one uses `szczypiorek` to inform about the fact that `development.yml` is not `gitignored`.

## Supporting python

Python should be supported automatically. It should be possible to do:

```python
from szczypiorek import env

print(env.auth_service.db.password)
```

Without user needing to add any extra line of code.
