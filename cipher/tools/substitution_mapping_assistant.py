import re
import copy
import string
from collections import Counter

from cipher.reference.word_patterns import get_word_pattern
from cipher.tools.substitution_candidate_ranker import SubstitutionCandidateRanker

try:
    from cipher.reference.word_patterns_dictionary import ALL_PATTERNS
except ImportError:
    ALL_PATTERNS = {}


class SubstitutionMappingAssistant:
    LETTERS = string.ascii_uppercase
    NON_LETTERS_OR_SPACE = re.compile(r"[^A-Z\s]")

    @staticmethod
    def get_blank_mapping():
        return {letter: [] for letter in SubstitutionMappingAssistant.LETTERS}

    @staticmethod
    def extract_words(message):
        cleaned = SubstitutionMappingAssistant.NON_LETTERS_OR_SPACE.sub(
            "",
            message.upper(),
        )
        return cleaned.split()

    @staticmethod
    def normalize_current_mapping(current_mapping):
        """
        Converts saved workspace mapping into strict A-Z mapping.

        Expected input:
            { "A": "E", "B": "T" }

        Invalid or empty entries are ignored.
        """
        normalized = {}

        if not current_mapping:
            return normalized

        for cipher_letter, plain_letter in current_mapping.items():
            cipher_letter = str(cipher_letter).upper().strip()
            plain_letter = str(plain_letter).upper().strip()

            if (
                len(cipher_letter) == 1
                and len(plain_letter) == 1
                and cipher_letter in SubstitutionMappingAssistant.LETTERS
                and plain_letter in SubstitutionMappingAssistant.LETTERS
            ):
                normalized[cipher_letter] = plain_letter

        return normalized

    @staticmethod
    def add_letters_to_mapping(letter_mapping, cipher_word, candidate_word):
        updated_mapping = copy.deepcopy(letter_mapping)

        for index in range(len(cipher_word)):
            cipher_letter = cipher_word[index]
            candidate_letter = candidate_word[index].upper()

            if candidate_letter not in updated_mapping[cipher_letter]:
                updated_mapping[cipher_letter].append(candidate_letter)

        return updated_mapping

    @staticmethod
    def intersect_mappings(mapping_a, mapping_b):
        intersected = SubstitutionMappingAssistant.get_blank_mapping()

        for letter in SubstitutionMappingAssistant.LETTERS:
            if mapping_a[letter] == []:
                intersected[letter] = copy.deepcopy(mapping_b[letter])
            elif mapping_b[letter] == []:
                intersected[letter] = copy.deepcopy(mapping_a[letter])
            else:
                intersected[letter] = [
                    mapped_letter
                    for mapped_letter in mapping_a[letter]
                    if mapped_letter in mapping_b[letter]
                ]

        return intersected

    @staticmethod
    def remove_solved_letters_from_mapping(letter_mapping):
        reduced_mapping = copy.deepcopy(letter_mapping)

        loop_again = True

        while loop_again:
            loop_again = False

            solved_letters = []

            for cipher_letter in SubstitutionMappingAssistant.LETTERS:
                if len(reduced_mapping[cipher_letter]) == 1:
                    solved_letters.append(reduced_mapping[cipher_letter][0])

            for cipher_letter in SubstitutionMappingAssistant.LETTERS:
                if len(reduced_mapping[cipher_letter]) == 1:
                    continue

                for solved_letter in solved_letters:
                    if solved_letter in reduced_mapping[cipher_letter]:
                        reduced_mapping[cipher_letter].remove(solved_letter)

                        if len(reduced_mapping[cipher_letter]) == 1:
                            loop_again = True

        return reduced_mapping

    @staticmethod
    def collect_mapping_votes(matched_words):
        votes = {
            cipher_letter: Counter()
            for cipher_letter in SubstitutionMappingAssistant.LETTERS
        }

        for item in matched_words:
            ranked_candidates = item.get("ranked_candidates", [])

            for rank_index, candidate in enumerate(ranked_candidates):
                rank_weight = max(1, 10 - rank_index)

                for cipher_letter, plain_letter in candidate["mapping"].items():
                    votes[cipher_letter][plain_letter] += rank_weight

        return votes

    @staticmethod
    def build_suggested_mappings(matched_words, minimum_confidence=0.45):
        votes = SubstitutionMappingAssistant.collect_mapping_votes(matched_words)

        suggestions = []

        for cipher_letter, letter_votes in votes.items():
            total_votes = sum(letter_votes.values())

            if total_votes == 0:
                continue

            plain_letter, vote_count = letter_votes.most_common(1)[0]
            confidence = vote_count / total_votes

            if confidence < minimum_confidence:
                continue

            suggestions.append({
                "cipher_letter": cipher_letter,
                "plain_letter": plain_letter,
                "confidence": round(confidence, 2),
                "votes": vote_count,
                "total_votes": total_votes,
            })

        suggestions.sort(
            key=lambda item: (item["confidence"], item["votes"]),
            reverse=True,
        )

        return suggestions

    @staticmethod
    def analyze(
        message,
        language=None,
        current_mapping=None,
        candidate_limit=10,
    ):
        if not ALL_PATTERNS:
            return {
                "available": False,
                "message": (
                    "Word pattern dictionary is not available yet. "
                    "Create cipher/reference/word_patterns_dictionary.py first."
                ),
                "mapping": {},
                "solved_count": 0,
                "matched_words": [],
                "suggested_mappings": [],
            }

        normalized_current_mapping = SubstitutionMappingAssistant.normalize_current_mapping(
            current_mapping,
        )

        intersected_mapping = SubstitutionMappingAssistant.get_blank_mapping()
        cipher_words = SubstitutionMappingAssistant.extract_words(message)

        matched_words = []

        for cipher_word in cipher_words:
            pattern = get_word_pattern(cipher_word)

            if pattern not in ALL_PATTERNS:
                continue

            candidates = ALL_PATTERNS[pattern]

            new_mapping = SubstitutionMappingAssistant.get_blank_mapping()

            for candidate in candidates:
                new_mapping = SubstitutionMappingAssistant.add_letters_to_mapping(
                    new_mapping,
                    cipher_word,
                    candidate,
                )

            intersected_mapping = SubstitutionMappingAssistant.intersect_mappings(
                intersected_mapping,
                new_mapping,
            )

            ranked_candidates = SubstitutionCandidateRanker.rank_candidates(
                cipher_word=cipher_word,
                candidates=candidates,
                cipher_words=cipher_words,
                language=language,
                current_mapping=normalized_current_mapping,
                limit=candidate_limit,
            )

            matched_words.append({
                "cipher_word": cipher_word,
                "pattern": pattern,
                "candidate_count": len(candidates),
                "sample_candidates": candidates[:10],
                "ranked_candidates": ranked_candidates,
                "best_candidate": ranked_candidates[0] if ranked_candidates else None,
            })

        reduced_mapping = SubstitutionMappingAssistant.remove_solved_letters_from_mapping(
            intersected_mapping,
        )

        solved_count = sum(
            1
            for possible_letters in reduced_mapping.values()
            if len(possible_letters) == 1
        )

        suggested_mappings = SubstitutionMappingAssistant.build_suggested_mappings(
            matched_words,
        )

        return {
            "available": True,
            "message": None,
            "mapping": reduced_mapping,
            "solved_count": solved_count,
            "matched_words": matched_words[:30],
            "suggested_mappings": suggested_mappings,
        }