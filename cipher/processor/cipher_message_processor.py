import uuid
from cipher.entities.cipher_message import CipherMessage
from cipher.database.cipher_message_database import CipherMessageDatabase


class CipherMessageProcessor:
    def __init__(self):
        self.db = CipherMessageDatabase()

    def create_cipher(self, title, ciphertext, user_id=None):
        if not title.strip():
            raise ValueError("Title required")

        if not ciphertext.strip():
            raise ValueError("Ciphertext required")

        cipher = CipherMessage(
            cipher_id=str(uuid.uuid4()),
            title=title.strip(),
            ciphertext=ciphertext.strip(),
            created_by=user_id,
        )

        return self.db.create(cipher)

    def list_ciphers(self):
        return self.db.retrieve_all()

    def get_cipher(self, cipher_id):
        return self.db.retrieve_by_id(cipher_id)