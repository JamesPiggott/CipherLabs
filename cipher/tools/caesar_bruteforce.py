import string


class CaesarBruteForce:
    ALPHABET = string.ascii_uppercase

    COMMON_WORDS = [
        "THE", "AND", "IS", "TO", "OF", "IN", "THAT", "IT", "AS", "FOR",
        "HELLO", "WORLD", "THIS", "MESSAGE", "SECRET", "WITH", "YOU"
    ]

    COMMON_LETTERS = {
        "E": 12,
        "T": 9,
        "A": 8,
        "O": 8,
        "I": 7,
        "N": 7,
        "S": 6,
        "H": 6,
        "R": 6,
    }

    @staticmethod
    def shift_letter(letter, shift):
        if letter.upper() not in CaesarBruteForce.ALPHABET:
            return letter

        alphabet = CaesarBruteForce.ALPHABET
        original_index = alphabet.index(letter.upper())
        shifted_index = (original_index - shift) % 26
        shifted_letter = alphabet[shifted_index]

        return shifted_letter if letter.isupper() else shifted_letter.lower()

    @staticmethod
    def decrypt_with_shift(text, shift):
        return "".join(
            CaesarBruteForce.shift_letter(char, shift)
            for char in text
        )

    @staticmethod
    def score_text(text):
        upper_text = text.upper()
        score = 0

        for word in CaesarBruteForce.COMMON_WORDS:
            if f" {word} " in f" {upper_text} ":
                score += 20

        for char in upper_text:
            score += CaesarBruteForce.COMMON_LETTERS.get(char, 0)

        return score

    @staticmethod
    def brute_force(text):
        results = []

        for shift in range(26):
            plaintext = CaesarBruteForce.decrypt_with_shift(text, shift)
            score = CaesarBruteForce.score_text(plaintext)

            results.append({
                "shift": shift,
                "plaintext": plaintext,
                "score": score,
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        return results

    @staticmethod
    def best_guess(text):
        results = CaesarBruteForce.brute_force(text)

        if not results:
            return None

        return results[0]