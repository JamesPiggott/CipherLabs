import re
from collections import Counter


class CipherClassifier:
    LETTER_RE = re.compile(r"[A-Z]")

    @staticmethod
    def normalize_text(text):
        return (text or "").upper()

    @staticmethod
    def extract_letters(text):
        return CipherClassifier.LETTER_RE.findall(CipherClassifier.normalize_text(text))

    @staticmethod
    def calculate_ioc(letters):
        total = len(letters)

        if total < 2:
            return 0.0

        counts = Counter(letters)

        numerator = sum(count * (count - 1) for count in counts.values())
        denominator = total * (total - 1)

        return numerator / denominator

    @staticmethod
    def has_word_boundaries(text):
        return bool(re.search(r"\s+", text.strip()))

    @staticmethod
    def has_punctuation(text):
        return bool(re.search(r"[^A-Za-z0-9\s]", text))

    @staticmethod
    def mostly_alphabetic(text):
        compact = re.sub(r"\s+", "", text or "")

        if not compact:
            return False

        letters = CipherClassifier.extract_letters(compact)
        return len(letters) / len(compact) >= 0.8

    @staticmethod
    def repeated_sequence_count(text, min_length=3):
        cleaned = "".join(CipherClassifier.extract_letters(text))

        if len(cleaned) < min_length * 2:
            return 0

        seen = Counter(
            cleaned[index:index + min_length]
            for index in range(len(cleaned) - min_length + 1)
        )

        return sum(1 for count in seen.values() if count > 1)

    @staticmethod
    def classify(text, declared_cipher_type=None):
        normalized_text = CipherClassifier.normalize_text(text)
        letters = CipherClassifier.extract_letters(normalized_text)

        ioc = CipherClassifier.calculate_ioc(letters)
        has_spaces = CipherClassifier.has_word_boundaries(normalized_text)
        has_punctuation = CipherClassifier.has_punctuation(normalized_text)
        mostly_alpha = CipherClassifier.mostly_alphabetic(normalized_text)
        repeated_sequences = CipherClassifier.repeated_sequence_count(normalized_text)

        signals = []

        if mostly_alpha:
            signals.append("Text is mostly alphabetic.")

        if has_spaces:
            signals.append("Word boundaries are preserved.")
        else:
            signals.append("No clear word boundaries detected.")

        if has_punctuation:
            signals.append("Punctuation is preserved.")
        else:
            signals.append("No punctuation detected.")

        if ioc >= 0.06:
            signals.append("Index of Coincidence is close to natural-language substitution text.")
        elif ioc < 0.045:
            signals.append(
                "Index of Coincidence is low, which can indicate polyalphabetic encryption or flattened text.")

        if repeated_sequences:
            signals.append("Repeated letter sequences are present.")

        declared = (declared_cipher_type or "").strip().lower()

        if "caesar" in declared:
            primary_type = "Caesar cipher"

            return {
                "primary_type": primary_type,
                "confidence": 0.9,
                "ioc": round(ioc, 4),
                "signals": signals + ["Cipher type was declared as Caesar."],
                "recommended_next_step": "Use Caesar brute force first, then validate the most readable result.",
                "next_actions": CipherClassifier.get_next_actions(primary_type),
            }

        if has_spaces and has_punctuation and mostly_alpha and ioc >= 0.055:
            primary_type = "Aristocrat"

            return {
                "primary_type": primary_type,
                "confidence": 0.78,
                "ioc": round(ioc, 4),
                "signals": signals,
                "recommended_next_step": "Use frequency analysis, word patterns, and the substitution assistant.",
                "next_actions": CipherClassifier.get_next_actions(primary_type),
            }

        if not has_spaces and mostly_alpha and ioc >= 0.055:
            primary_type = "Patristocrat"

            return {
                "primary_type": primary_type,
                "confidence": 0.72,
                "ioc": round(ioc, 4),
                "signals": signals,
                "recommended_next_step": "Use frequency analysis first. Word-pattern solving is harder because word boundaries are missing.",
                "next_actions": CipherClassifier.get_next_actions(primary_type),
            }

        if (len(letters) >= 20 and ioc < 0.045) or repeated_sequences >= 2:
            primary_type = "Possible polyalphabetic cipher"

            return {
                "primary_type": primary_type,
                "confidence": 0.65,
                "ioc": round(ioc, 4),
                "signals": signals,
                "recommended_next_step": "Inspect repeated sequences and consider a future Vigenère or Kasiski workflow.",
                "next_actions": CipherClassifier.get_next_actions(primary_type),
            }

        primary_type = "Unknown"

        return {
            "primary_type": primary_type,
            "confidence": 0.4,
            "ioc": round(ioc, 4),
            "signals": signals,
            "recommended_next_step": "Start with basic statistics, language hints, and frequency analysis.",
            "next_actions": CipherClassifier.get_next_actions(primary_type),
        }

    @staticmethod
    def get_next_actions(primary_type):
        normalized_type = (primary_type or "").lower()

        if "caesar" in normalized_type:
            return [
                {
                    "title": "Run Caesar brute force",
                    "reason": "A Caesar cipher has only 25 meaningful shifts to test.",
                    "target_widget": "caesar",
                },
                {
                    "title": "Validate readable output",
                    "reason": "The best shift should produce recognizable language.",
                    "target_widget": "language-hints",
                },
            ]

        if "aristocrat" in normalized_type:
            return [
                {
                    "title": "Check frequency analysis",
                    "reason": "Letter frequencies usually survive simple substitution.",
                    "target_widget": "frequency-analysis",
                },
                {
                    "title": "Inspect word patterns",
                    "reason": "Spaces are preserved, so word shapes can reveal likely plaintext words.",
                    "target_widget": "word-patterns",
                },
                {
                    "title": "Use substitution assistant",
                    "reason": "Candidate words can produce useful mapping suggestions.",
                    "target_widget": "substitution-assistant",
                },
            ]

        if "patristocrat" in normalized_type:
            return [
                {
                    "title": "Start with frequency analysis",
                    "reason": "Word boundaries are missing, so single-letter patterns are the safest first signal.",
                    "target_widget": "frequency-analysis",
                },
                {
                    "title": "Build mappings manually",
                    "reason": "Without spaces, word-pattern suggestions are less reliable.",
                    "target_widget": "substitution-solver",
                },
            ]

        if "polyalphabetic" in normalized_type:
            return [
                {
                    "title": "Inspect repeated sequences",
                    "reason": "Repeated sequences may reveal key-length clues.",
                    "target_widget": "repeated-sequences",
                },
                {
                    "title": "Compare IoC",
                    "reason": "A low IoC can point toward polyalphabetic encryption.",
                    "target_widget": "basic-analysis",
                },
            ]

        return [
            {
                "title": "Review basic analysis",
                "reason": "Start by checking text length, alphabet use, and statistical indicators.",
                "target_widget": "basic-analysis",
            },
            {
                "title": "Compare language hints",
                "reason": "Language assumptions influence which solving tools are useful.",
                "target_widget": "language-hints",
            },
        ]