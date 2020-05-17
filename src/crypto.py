from xxhash import xxh64
from cryptography.fernet import Fernet

from models import Secret


class Crypto:

    _f: Fernet = None

    def __init__(self):
        if not self._f:
            self._f = Fernet(Fernet.generate_key())

    def encrypt_secret(self, secret: Secret):
        secret.secret_text = self._f.encrypt(secret.secret_text.encode()).decode('utf-8')
        secret.phrase = self._f.encrypt(secret.phrase.encode()).decode('utf-8')

    def decrypt_secret(self, secret: Secret):
        secret.secret_text = self._f.decrypt(secret.secret_text.encode()).decode('utf-8')
        secret.phrase = self._f.decrypt(secret.phrase.encode()).decode('utf-8')

    def generate_secret_key(self, secret: Secret):
        secret.secret_key = xxh64(secret.secret_text + secret.phrase).hexdigest()[:10]
