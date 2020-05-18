from xxhash import xxh64
from cryptography.fernet import Fernet

from models import Secret


class Crypto:

    _f: Fernet = None

    def __init__(self):
        if not self._f:
            self._f = Fernet(Fernet.generate_key())

    def encrypt_secret(self, secret: Secret):
        """Encrypts 'secret_text' and 'phrase' fields of the passed object"""
        secret.secret_text = self._f.encrypt(secret.secret_text.encode()).decode('utf-8')
        secret.phrase = self._f.encrypt(secret.phrase.encode()).decode('utf-8')

    def decrypt_secret(self, secret: Secret):
        """Decrypts 'secret_text' and 'phrase' fields of the passed object"""
        secret.secret_text = self._f.decrypt(secret.secret_text.encode()).decode('utf-8')
        secret.phrase = self._f.decrypt(secret.phrase.encode()).decode('utf-8')

    def generate_secret_key(self, secret: Secret):
        """Changes the secret_key field by filling it in with generated code based on other object fields"""
        secret.secret_key = xxh64(secret.secret_text + secret.phrase).hexdigest()[:10]
