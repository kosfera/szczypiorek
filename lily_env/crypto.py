
import string
import random
import os
from datetime import datetime
import json
import base64

import gnupg

from .git import assert_is_git_repository, assert_is_git_ignored
from .exceptions import (
    DecryptionError,
    EncryptionKeyFileMissingError,
    EncryptionKeyBrokenBase64Error,
    EncryptionKeyBrokenJsonError,
    EncryptionKeyTooShortError,
)
from .constants import (
    ENCRYPTION_KEY_FILE,
    ENCRYPTION_KEY_MIN_LENGTH,
    ENCRYPTION_KEY_LENGTH,
)


def encrypt(content):
    gpg = gnupg.GPG()

    create_encryption_key_if_not_exist()
    return str(
        gpg.encrypt(
            content,
            symmetric='AES256',
            passphrase=get_encryption_key(),
            recipients=None))


def decrypt(content):
    gpg = gnupg.GPG()

    decrypted = gpg.decrypt(
        content,
        passphrase=get_encryption_key())

    if decrypted.ok:
        return str(decrypted)

    else:
        raise DecryptionError()


def get_encryption_key():

    try:
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            content = f.read()
            content = base64.b64decode(content).decode('utf8')
            encryption_key = json.loads(content)['key']

    except FileNotFoundError:
        raise EncryptionKeyFileMissingError()

    except base64.binascii.Error:
        raise EncryptionKeyBrokenBase64Error()

    except (KeyError, json.decoder.JSONDecodeError):
        raise EncryptionKeyBrokenJsonError()

    if assert_is_git_repository():
        assert_is_git_ignored(ENCRYPTION_KEY_FILE)

    if len(encryption_key) < ENCRYPTION_KEY_MIN_LENGTH:
        raise EncryptionKeyTooShortError()

    return encryption_key


def create_encryption_key_if_not_exist():

    if os.path.exists(ENCRYPTION_KEY_FILE):
        return False

    with open(ENCRYPTION_KEY_FILE, 'wb') as f:
        content = {
            'key': ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=ENCRYPTION_KEY_LENGTH)),
            'created_datetime': datetime.utcnow().isoformat(),
        }
        content = json.dumps(content)
        content = content.encode('utf8')
        content = base64.b64encode(content)

        f.write(content)

    return True
