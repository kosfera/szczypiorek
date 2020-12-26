
class BaseException(Exception):
    pass


#
# VALIDATORS
#
class ValidatorError(Exception):
    pass


#
# CRYPTO
#
class DecryptionError(BaseException):
    pass


class EncryptionKeyFileMissingError(BaseException):
    pass


class EncryptionKeyTooShortError(BaseException):
    pass


class EncryptionKeyBrokenBase64Error(BaseException):
    pass


class EncryptionKeyBrokenJsonError(BaseException):
    pass


#
# GIT
#
class FileNotIgnoredError(BaseException):
    pass
