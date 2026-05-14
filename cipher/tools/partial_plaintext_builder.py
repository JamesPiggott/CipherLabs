# cipher/tools/partial_plaintext_builder.py

import string


class PartialPlaintextBuilder:
    LETTERS = string.ascii_uppercase

    @staticmethod
    def normalize_mapping(mapping):
        normalized = {}

        if not mapping:
            return normalized

        for cipher_letter, plain_letter in mapping.items():
            cipher_letter = str(cipher_letter).strip().upper()
            plain_letter = str(plain_letter).strip().upper()

            if (
                len(cipher_letter) == 1
                and len(plain_letter) == 1
                and cipher_letter in PartialPlaintextBuilder.LETTERS
                and plain_letter in PartialPlaintextBuilder.LETTERS
            ):
                normalized[cipher_letter] = plain_letter

        return normalized

    @staticmethod
    def get_strong_confidence_mapping(mapping_confidence, minimum_confidence=0.75):
        mapping = {}

        if not mapping_confidence or not mapping_confidence.get("available"):
            return mapping

        for item in mapping_confidence.get("items", []):
            if item.get("confidence", 0) < minimum_confidence:
                continue

            cipher_letter = str(item.get("cipher_letter", "")).upper()
            plain_letter = str(item.get("plain_letter", "")).upper()

            if (
                cipher_letter in PartialPlaintextBuilder.LETTERS
                and plain_letter in PartialPlaintextBuilder.LETTERS
            ):
                mapping[cipher_letter] = plain_letter

        return mapping

    @staticmethod
    def build(
        ciphertext,
        workspace_mapping=None,
        mapping_confidence=None,
        include_confident_suggestions=True,
        minimum_confidence=0.75,
    ):
        ciphertext = ciphertext or ""

        confirmed_mapping = PartialPlaintextBuilder.normalize_mapping(workspace_mapping)

        suggested_mapping = {}

        if include_confident_suggestions:
            suggested_mapping = PartialPlaintextBuilder.get_strong_confidence_mapping(
                mapping_confidence=mapping_confidence,
                minimum_confidence=minimum_confidence,
            )

        combined_mapping = dict(suggested_mapping)
        combined_mapping.update(confirmed_mapping)

        output = []
        character_details = []

        total_letters = 0
        solved_letters = 0
        confirmed_letters = 0
        suggested_letters = 0

        for char in ciphertext:
            upper_char = char.upper()

            if upper_char not in PartialPlaintextBuilder.LETTERS:
                output.append(char)
                character_details.append({
                    "cipher_char": char,
                    "plain_char": char,
                    "type": "separator",
                    "source": "original",
                })
                continue

            total_letters += 1

            if upper_char in confirmed_mapping:
                plain_char = confirmed_mapping[upper_char]
                solved_letters += 1
                confirmed_letters += 1
                source = "confirmed"
            elif upper_char in suggested_mapping:
                plain_char = suggested_mapping[upper_char]
                solved_letters += 1
                suggested_letters += 1
                source = "suggested"
            else:
                plain_char = "_"
                source = "unknown"

            output.append(plain_char)
            character_details.append({
                "cipher_char": char,
                "plain_char": plain_char,
                "type": "letter",
                "source": source,
            })

        solve_percentage = 0

        if total_letters:
            solve_percentage = int(round((solved_letters / total_letters) * 100))

        return {
            "available": True,
            "plaintext": "".join(output),
            "characters": character_details,
            "total_letters": total_letters,
            "solved_letters": solved_letters,
            "unsolved_letters": total_letters - solved_letters,
            "confirmed_letters": confirmed_letters,
            "suggested_letters": suggested_letters,
            "solve_percentage": solve_percentage,
            "include_confident_suggestions": include_confident_suggestions,
            "minimum_confidence": minimum_confidence,
        }