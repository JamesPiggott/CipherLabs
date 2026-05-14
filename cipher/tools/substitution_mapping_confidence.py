# cipher/tools/substitution_mapping_confidence.py

import string
from collections import Counter


class SubstitutionMappingConfidence:
    LETTERS = string.ascii_uppercase

    @staticmethod
    def build_from_assistant(substitution_mapping_assistant):
        if not substitution_mapping_assistant:
            return {
                "available": False,
                "items": [],
                "strong_count": 0,
                "medium_count": 0,
                "weak_count": 0,
            }

        matched_words = substitution_mapping_assistant.get("matched_words", [])
        suggested_mappings = substitution_mapping_assistant.get("suggested_mappings", [])

        votes = {
            letter: Counter()
            for letter in SubstitutionMappingConfidence.LETTERS
        }

        for item in matched_words:
            ranked_candidates = item.get("ranked_candidates", [])

            for index, candidate in enumerate(ranked_candidates):
                weight = max(1, 10 - index)
                mapping = candidate.get("mapping", {})

                for cipher_letter, plain_letter in mapping.items():
                    cipher_letter = str(cipher_letter).upper()
                    plain_letter = str(plain_letter).upper()

                    if (
                        cipher_letter in SubstitutionMappingConfidence.LETTERS
                        and plain_letter in SubstitutionMappingConfidence.LETTERS
                    ):
                        votes[cipher_letter][plain_letter] += weight

        suggestion_lookup = {
            item["cipher_letter"]: item
            for item in suggested_mappings
        }

        items = []

        for cipher_letter in SubstitutionMappingConfidence.LETTERS:
            letter_votes = votes[cipher_letter]
            total_votes = sum(letter_votes.values())

            if total_votes == 0:
                continue

            plain_letter, top_votes = letter_votes.most_common(1)[0]
            confidence = top_votes / total_votes

            suggestion = suggestion_lookup.get(cipher_letter)

            if suggestion:
                confidence = max(confidence, suggestion.get("confidence", 0))

            alternatives = [
                {
                    "plain_letter": letter,
                    "votes": count,
                    "confidence": round(count / total_votes, 2),
                }
                for letter, count in letter_votes.most_common(5)
            ]

            if confidence >= 0.75:
                tier = "strong"
            elif confidence >= 0.45:
                tier = "medium"
            else:
                tier = "weak"

            items.append({
                "cipher_letter": cipher_letter,
                "plain_letter": plain_letter,
                "confidence": round(confidence, 2),
                "confidence_percent": int(round(confidence * 100)),
                "tier": tier,
                "votes": top_votes,
                "total_votes": total_votes,
                "alternatives": alternatives,
            })

        items.sort(
            key=lambda item: (
                item["tier"] != "strong",
                item["tier"] != "medium",
                -item["confidence"],
                item["cipher_letter"],
            )
        )

        return {
            "available": True,
            "items": items,
            "strong_count": sum(1 for item in items if item["tier"] == "strong"),
            "medium_count": sum(1 for item in items if item["tier"] == "medium"),
            "weak_count": sum(1 for item in items if item["tier"] == "weak"),
        }