import uuid
from cipher.entities.cipher_message import CipherMessage
from cipher.database.cipher_message_database import CipherMessageDatabase


class CipherMessageProcessor:
    def __init__(self):
        self.db = CipherMessageDatabase()

    def create_cipher(
            self,
            title,
            ciphertext,
            user_id=None,
            plaintext=None,
            status="unsolved",
            cipher_type=None,
            suspected_language=None,
            source=None,
    ):
        if not title.strip():
            raise ValueError("Title required")

        if not ciphertext.strip():
            raise ValueError("Ciphertext required")

        cipher = CipherMessage(
            cipher_id=str(uuid.uuid4()),
            title=title.strip(),
            ciphertext=ciphertext.strip(),
            plaintext=plaintext.strip() if plaintext else None,
            status=status.strip() if status else "unsolved",
            cipher_type=cipher_type.strip() if cipher_type else None,
            suspected_language=suspected_language.strip() if suspected_language else None,
            source=source.strip() if source else None,
            created_by=user_id,
        )

        return self.db.create(cipher)

    def list_ciphers(self):
        return self.db.retrieve_all()

    def get_cipher(self, cipher_id):
        return self.db.retrieve_by_id(cipher_id)

    def delete_cipher(self, cipher_id, user_id=None, is_admin=False):
        cipher = self.get_cipher(cipher_id)

        if not cipher:
            raise ValueError("Cipher not found.")

        if not is_admin and str(cipher.created_by) != str(user_id):
            raise PermissionError("You are not allowed to delete this cipher.")

        return self.db.delete_by_id(cipher_id)