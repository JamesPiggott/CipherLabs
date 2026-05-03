from core.database.database import db
from cipher.entities.cipher_message import CipherMessage


class CipherMessageDatabase:
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS cipher_messages (
            id UUID PRIMARY KEY,
            title TEXT NOT NULL,
            ciphertext TEXT NOT NULL,
            plaintext TEXT,
            status TEXT NOT NULL DEFAULT 'unsolved',
            cipher_type TEXT,
            suspected_language TEXT,
            source TEXT,
            created_by UUID,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(query)

    def create(self, cipher):
        query = """
        INSERT INTO cipher_messages (
            id, title, ciphertext, plaintext, status,
            cipher_type, suspected_language, source, created_by
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING *;
        """
        row = db.execute_returning(
            query,
            (
                cipher.id,
                cipher.title,
                cipher.ciphertext,
                cipher.plaintext,
                cipher.status,
                cipher.cipher_type,
                cipher.suspected_language,
                cipher.source,
                cipher.created_by,
            ),
        )
        return CipherMessage.from_row(row)

    def retrieve_all(self):
        query = "SELECT * FROM cipher_messages ORDER BY created_at DESC;"
        rows = db.fetch_all(query)
        return [CipherMessage.from_row(r) for r in rows]

    def retrieve_by_id(self, cipher_id):
        query = "SELECT * FROM cipher_messages WHERE id = %s;"
        row = db.fetch_one(query, (cipher_id,))
        return CipherMessage.from_row(row)