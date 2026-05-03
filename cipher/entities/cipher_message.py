class CipherMessage:
    def __init__(
        self,
        cipher_id,
        title,
        ciphertext,
        plaintext=None,
        status="unsolved",
        cipher_type=None,
        suspected_language=None,
        source=None,
        created_by=None,
        created_at=None,
    ):
        self.id = cipher_id
        self.title = title
        self.ciphertext = ciphertext
        self.plaintext = plaintext
        self.status = status
        self.cipher_type = cipher_type
        self.suspected_language = suspected_language
        self.source = source
        self.created_by = created_by
        self.created_at = created_at

    @staticmethod
    def from_row(row):
        if not row:
            return None

        return CipherMessage(
            cipher_id=row["id"],
            title=row["title"],
            ciphertext=row["ciphertext"],
            plaintext=row.get("plaintext"),
            status=row.get("status"),
            cipher_type=row.get("cipher_type"),
            suspected_language=row.get("suspected_language"),
            source=row.get("source"),
            created_by=row.get("created_by"),
            created_at=row.get("created_at"),
        )