import string


class SubstitutionCipher:
    LETTERS = string.ascii_uppercase

    @staticmethod
    def clean_key(key):
        return "".join(
            char.upper()
            for char in key
            if char.upper() in SubstitutionCipher.LETTERS
        )

    @staticmethod
    def validate_key(key):
        cleaned_key = SubstitutionCipher.clean_key(key)

        if len(cleaned_key) != 26:
            return False

        return sorted(cleaned_key) == sorted(SubstitutionCipher.LETTERS)

    @staticmethod
    def translate_message(key, message, mode):
        cleaned_key = SubstitutionCipher.clean_key(key)

        if not SubstitutionCipher.validate_key(cleaned_key):
            raise ValueError("Substitution key must contain each A-Z letter exactly once.")

        chars_a = SubstitutionCipher.LETTERS
        chars_b = cleaned_key

        if mode == "decrypt":
            chars_a, chars_b = chars_b, chars_a

        translated = ""

        for symbol in message:
            upper_symbol = symbol.upper()

            if upper_symbol in chars_a:
                symbol_index = chars_a.find(upper_symbol)
                translated_symbol = chars_b[symbol_index]

                translated += (
                    translated_symbol
                    if symbol.isupper()
                    else translated_symbol.lower()
                )
            else:
                translated += symbol

        return translated

    @staticmethod
    def encrypt(key, message):
        return SubstitutionCipher.translate_message(key, message, "encrypt")

    @staticmethod
    def decrypt(key, message):
        return SubstitutionCipher.translate_message(key, message, "decrypt")