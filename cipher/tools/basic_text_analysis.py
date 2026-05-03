import string
from collections import Counter


class BasicTextAnalysis:
    @staticmethod
    def analyze(text):
        total_characters = len(text)

        letters_only = [
            c.upper() for c in text if c.upper() in string.ascii_uppercase
        ]

        total_letters = len(letters_only)
        unique_letters = len(set(letters_only))

        symbols = [c for c in text if not c.upper() in string.ascii_uppercase]
        unique_symbols = len(set(symbols))

        counter = Counter(letters_only)

        most_common = None
        if counter:
            most_common = counter.most_common(1)[0][0]

        return {
            "total_characters": total_characters,
            "total_letters": total_letters,
            "unique_letters": unique_letters,
            "unique_symbols": unique_symbols,
            "most_common_letter": most_common,
        }