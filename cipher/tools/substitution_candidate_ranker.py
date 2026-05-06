import math
import re
from collections import Counter

from cipher.reference.language_digrams import LANGUAGE_DIGRAMS


class SubstitutionCandidateRanker:
    """
    Ranks plaintext word candidates for a cipher word.

    This is intentionally heuristic, not a full substitution solver.
    It gives the UI useful "try these first" suggestions while keeping
    the existing word-pattern assistant intact.
    """

    COMMON_WORD_SCORE = {
        "THE": 50,
        "AND": 45,
        "THAT": 40,
        "HAVE": 35,
        "FOR": 34,
        "NOT": 32,
        "WITH": 30,
        "YOU": 30,
        "THIS": 28,
        "BUT": 26,
        "ARE": 24,
        "FROM": 22,
        "WAS": 22,
        "WERE": 20,
        "HET": 50,
        "EEN": 45,
        "DAT": 42,
        "VAN": 40,
        "DE": 38,
        "EN": 36,
        "IN": 34,
        "TE": 32,
        "IS": 30,
        "OP": 28,
        "VOOR": 26,
        "NIET": 25,
        "MET": 24,
        "ALS": 22,
    }

    @staticmethod
    def normalize_word(word):
        return re.sub(r"[^A-Z]", "", word.upper())

    @staticmethod
    def get_word_counts(cipher_words):
        return Counter(
            SubstitutionCandidateRanker.normalize_word(word)
            for word in cipher_words
            if SubstitutionCandidateRanker.normalize_word(word)
        )

    @staticmethod
    def mapping_conflict_count(cipher_word, candidate_word, current_mapping=None):
        """
        Counts how many positions conflict with the user's existing mapping.
        current_mapping is expected as:
            { "A": "E", "B": "T", ... }
        """
        if not current_mapping:
            return 0

        conflicts = 0

        for cipher_letter, plain_letter in zip(cipher_word, candidate_word):
            mapped_plain = current_mapping.get(cipher_letter)

            if mapped_plain and mapped_plain != plain_letter:
                conflicts += 1

        return conflicts

    @staticmethod
    def duplicate_plaintext_conflict_count(cipher_word, candidate_word, current_mapping=None):
        """
        Prevents suggestions that reuse a plaintext letter already assigned
        to another cipher letter.
        """
        if not current_mapping:
            return 0

        reverse_mapping = {
            plain: cipher
            for cipher, plain in current_mapping.items()
            if plain
        }

        conflicts = 0

        for cipher_letter, plain_letter in zip(cipher_word, candidate_word):
            assigned_cipher = reverse_mapping.get(plain_letter)

            if assigned_cipher and assigned_cipher != cipher_letter:
                conflicts += 1

        return conflicts

    @staticmethod
    def digram_score(candidate_word, language=None):
        """
        Scores candidates by expected plaintext digrams.

        This works best when LANGUAGE_DIGRAMS contains the selected language.
        Unknown digrams are neutral-small rather than zero, so short words
        are not punished too aggressively.
        """
        if not language or language not in LANGUAGE_DIGRAMS:
            return 0.0

        expected = LANGUAGE_DIGRAMS[language]

        if len(candidate_word) < 2:
            return 0.0

        score = 0.0

        for index in range(len(candidate_word) - 1):
            digram = candidate_word[index:index + 2]
            score += expected.get(digram, 0.0005)

        return score

    @staticmethod
    def common_word_score(candidate_word):
        return SubstitutionCandidateRanker.COMMON_WORD_SCORE.get(candidate_word, 0)

    @staticmethod
    def length_score(candidate_word):
        """
        Longer words are more informative in substitution solving,
        but avoid making length dominate the ranking.
        """
        return min(len(candidate_word), 12) * 1.5

    @staticmethod
    def repeated_cipher_word_score(cipher_word, word_counts):
        """
        If a cipher word appears multiple times, ranking its candidates well
        is more valuable.
        """
        count = word_counts.get(cipher_word, 1)
        return min(count - 1, 5) * 4

    @staticmethod
    def calculate_score(
        cipher_word,
        candidate_word,
        word_counts=None,
        language=None,
        current_mapping=None,
    ):
        cipher_word = SubstitutionCandidateRanker.normalize_word(cipher_word)
        candidate_word = SubstitutionCandidateRanker.normalize_word(candidate_word)
        word_counts = word_counts or {}

        mapping_conflicts = SubstitutionCandidateRanker.mapping_conflict_count(
            cipher_word,
            candidate_word,
            current_mapping,
        )

        duplicate_conflicts = SubstitutionCandidateRanker.duplicate_plaintext_conflict_count(
            cipher_word,
            candidate_word,
            current_mapping,
        )

        score = 0.0
        score += SubstitutionCandidateRanker.common_word_score(candidate_word)
        score += SubstitutionCandidateRanker.length_score(candidate_word)
        score += SubstitutionCandidateRanker.repeated_cipher_word_score(cipher_word, word_counts)
        score += SubstitutionCandidateRanker.digram_score(candidate_word, language) * 500

        score -= mapping_conflicts * 100
        score -= duplicate_conflicts * 80

        return round(score, 4)

    @staticmethod
    def candidate_to_mapping(cipher_word, candidate_word):
        mapping = {}

        for cipher_letter, plain_letter in zip(cipher_word, candidate_word):
            mapping[cipher_letter] = plain_letter

        return mapping

    @staticmethod
    def rank_candidates(
        cipher_word,
        candidates,
        cipher_words=None,
        language=None,
        current_mapping=None,
        limit=10,
    ):
        cipher_word = SubstitutionCandidateRanker.normalize_word(cipher_word)

        word_counts = SubstitutionCandidateRanker.get_word_counts(cipher_words or [])

        ranked = []

        for candidate in candidates:
            candidate_word = SubstitutionCandidateRanker.normalize_word(candidate)

            if len(candidate_word) != len(cipher_word):
                continue

            mapping_conflicts = SubstitutionCandidateRanker.mapping_conflict_count(
                cipher_word,
                candidate_word,
                current_mapping,
            )

            duplicate_conflicts = SubstitutionCandidateRanker.duplicate_plaintext_conflict_count(
                cipher_word,
                candidate_word,
                current_mapping,
            )

            score = SubstitutionCandidateRanker.calculate_score(
                cipher_word=cipher_word,
                candidate_word=candidate_word,
                word_counts=word_counts,
                language=language,
                current_mapping=current_mapping,
            )

            ranked.append({
                "word": candidate_word,
                "score": score,
                "mapping": SubstitutionCandidateRanker.candidate_to_mapping(
                    cipher_word,
                    candidate_word,
                ),
                "mapping_conflicts": mapping_conflicts,
                "duplicate_conflicts": duplicate_conflicts,
            })

        ranked.sort(key=lambda item: item["score"], reverse=True)

        return ranked[:limit]