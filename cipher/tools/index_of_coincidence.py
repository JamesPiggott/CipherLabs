import string
from collections import Counter


class IndexOfCoincidence:
    @staticmethod
    def normalize_text(text):
        return "".join(
            char.upper()
            for char in text
            if char.upper() in string.ascii_uppercase
        )

    @staticmethod
    def calculate(text):
        normalized_text = IndexOfCoincidence.normalize_text(text)
        n = len(normalized_text)

        if n < 2:
            return {
                "value": 0,
                "interpretation": "Not enough text to calculate reliably.",
            }

        counts = Counter(normalized_text)

        numerator = sum(count * (count - 1) for count in counts.values())
        denominator = n * (n - 1)

        ioc = numerator / denominator

        if ioc >= 0.06:
            interpretation = "Close to natural language. This may suggest plaintext, a transposition cipher, or a monoalphabetic substitution."
        elif ioc >= 0.045:
            interpretation = "Some language structure may be present, but the result is not decisive."
        else:
            interpretation = "Closer to random text. This may suggest a polyalphabetic cipher or strong mixing."

        return {
            "value": round(ioc, 4),
            "interpretation": interpretation,
        }