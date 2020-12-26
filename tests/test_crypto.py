
import json
import base64

import pytest

from lily_env.crypto import (
    encrypt,
    decrypt,
    get_encryption_key,
    create_encryption_key_if_not_exist,
)
from lily_env.exceptions import (
    DecryptionError,
    EncryptionKeyBrokenBase64Error,
    EncryptionKeyBrokenJsonError,
    EncryptionKeyFileMissingError,
    EncryptionKeyTooShortError,
    FileNotIgnoredError,
)
from tests import BaseTestCase


class CryptTestCase(BaseTestCase):

    #
    # ENCRYPT
    #
    def test_encrypt__empty_content__success(self):

        self.mocker.patch(
            'lily_env.crypto.get_encryption_key').return_value = 'secret'

        encrypted = encrypt('').strip()

        assert encrypted.startswith('-----BEGIN PGP MESSAGE-----')
        assert encrypted.endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == ''

    def test_encrypt__no_encryption_key__success(self):

        assert self.root_dir.join('.lily_env_encryption_key').exists() is False

        encrypted = encrypt('hello world').strip()

        assert encrypted.startswith('-----BEGIN PGP MESSAGE-----')
        assert encrypted.endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == 'hello world'
        assert self.root_dir.join('.lily_env_encryption_key').exists() is True

    def test_encrypt__encryption_key_exists__success(self):

        create_encryption_key_if_not_exist()

        encrypted = encrypt('hello world').strip()

        assert encrypted.startswith('-----BEGIN PGP MESSAGE-----')
        assert encrypted.endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == 'hello world'
        assert len(self.root_dir.join('.lily_env_encryption_key').read()) > 128

    #
    # DECRYPT
    #
    def test_decrypt__empty_gpg_content__success(self):

        assert decrypt(encrypt('')) == ''

    def test_decrypt__wrong_content__error(self):

        self.mocker.patch(
            'lily_env.crypto.get_encryption_key'
        ).return_value = 'secret'

        with pytest.raises(DecryptionError):
            decrypt('what is it')

    def test_decrypt__wrong_passphrase__error(self):

        self.mocker.patch(
            'lily_env.crypto.get_encryption_key'
        ).side_effect = ['secret.0', 'secret.1']

        encrypted = encrypt('what is it')

        with pytest.raises(DecryptionError):
            decrypt(encrypted)

    #
    # GET_ENCRYPTION_KEY
    #
    def test_get_encryption_key__all_good__success(self):

        key = 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        self.root_dir.join('.lily_env_encryption_key').write(
            base64.b64encode(json.dumps({'key': key}).encode('utf8')),
            mode='wb')

        assert get_encryption_key() == key

    def test_get_encryption_key__not_base64__error(self):

        self.root_dir.join('.lily_env_encryption_key').write(
            json.dumps({'key': 'key'}).encode('utf8'),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenBase64Error):
            get_encryption_key()

    def test_get_encryption_key__not_json__error(self):

        self.root_dir.join('.lily_env_encryption_key').write(
            base64.b64encode(b'"key": "whatever"'),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenJsonError):
            get_encryption_key()

    def test_get_encryption_key__missing_json_fields__error(self):

        self.root_dir.join('.lily_env_encryption_key').write(
            base64.b64encode(json.dumps({'not.key': 'what'}).encode('utf8')),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenJsonError):
            get_encryption_key()

    def test_get_encryption_key__file_does_not_exist__error(self):

        with pytest.raises(EncryptionKeyFileMissingError):
            get_encryption_key()

    def test_get_encryption_key__file_not_gitignored__error(self):

        key = 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        self.root_dir.join('.lily_env_encryption_key').write(
            base64.b64encode(json.dumps({'key': key}).encode('utf8')),
            mode='wb')

        self.mocker.patch(
            'lily_env.crypto.assert_is_git_repository'
        ).return_value = True
        self.mocker.patch(
            'lily_env.crypto.assert_is_git_ignored'
        ).side_effect = FileNotIgnoredError

        with pytest.raises(FileNotIgnoredError):
            get_encryption_key()

    def test_get_encryption_key__to_short__error(self):

        key = 'abc123'
        self.root_dir.join('.lily_env_encryption_key').write(
            base64.b64encode(json.dumps({'key': key}).encode('utf8')),
            mode='wb')

        with pytest.raises(EncryptionKeyTooShortError):
            get_encryption_key()

    #
    # CREATE_ENCRYPTION_KEY_IF_NOT_EXIST
    #
    def test_create_encryption_key_if_not_exist__exists__success(self):

        key = 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        content = base64.b64encode(json.dumps({'key': key}).encode('utf8'))
        self.root_dir.join('.lily_env_encryption_key').write(
            content, mode='wb')

        assert create_encryption_key_if_not_exist() is False
        assert self.root_dir.join(
            '.lily_env_encryption_key').read('rb') == content

    def test_create_encryption_key_if_not_exist__does_not_exist__success(self):

        assert create_encryption_key_if_not_exist() is True
        content = self.root_dir.join('.lily_env_encryption_key').read('rb')
        content = json.loads(base64.b64decode(content).decode('utf8'))

        assert len(content['key']) == 128
        assert len(set(content['key'])) > 20
