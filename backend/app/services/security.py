import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESService:
    def __init__(self, key_b64: str):
        self.key = base64.b64decode(key_b64)
        if len(self.key) != 32:
            raise ValueError('AES key must be 32 bytes for AES-256')
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plaintext: str) -> str:
        nonce = os.urandom(12)
        data = self.aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + data).decode()

    def decrypt(self, ciphertext_b64: str) -> str:
        raw = base64.b64decode(ciphertext_b64)
        nonce, data = raw[:12], raw[12:]
        return self.aesgcm.decrypt(nonce, data, None).decode()
