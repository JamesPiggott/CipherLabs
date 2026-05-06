from collections import Counter
from math import sqrt
import string

from cipher.reference.language_digrams import LANGUAGE_DIGRAMS


class DigramSimilarity:
    @staticmethod
    def normalize_text(text):
        return "".join(
            char.upper()
            for char in text
            if char.upper() in string.ascii_uppercase
        )

    @staticmethod
    def get_observed_digrams(text):
        normalized_text = DigramSimilarity.normalize_text(text)

        if len(normalized_text) < 2:
            return {}

        digrams = [
            normalized_text[i:i + 2]
            for i in range(len(normalized_text) - 1)
        ]

        counter = Counter(digrams)
        total = sum(counter.values())

        if total == 0:
            return {}

        return {
            digram: count / total
            for digram, count in counter.items()
        }

    @staticmethod
    def cosine_similarity(vector_a, vector_b):
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        magnitude_a = sqrt(sum(a ** 2 for a in vector_a))
        magnitude_b = sqrt(sum(b ** 2 for b in vector_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    @staticmethod
    def compare_to_language(observed, expected):
        all_digrams = set(observed.keys()) | set(expected.keys())

        observed_vector = [
            observed.get(digram, 0)
            for digram in all_digrams
        ]

        expected_vector = [
            expected.get(digram, 0)
            for digram in all_digrams
        ]

        return DigramSimilarity.cosine_similarity(
            observed_vector,
            expected_vector,
        )

    @staticmethod
    def analyze(text):
        observed = DigramSimilarity.get_observed_digrams(text)

        if not observed:
            return []

        results = []

        for language, expected_digrams in LANGUAGE_DIGRAMS.items():
            score = DigramSimilarity.compare_to_language(
                observed,
                expected_digrams,
            )

            results.append({
                "language": language,
                "score": round(score, 4),
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        return results