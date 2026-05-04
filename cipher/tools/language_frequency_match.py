from collections import Counter

from cipher.reference.language_frequencies import LANGUAGE_PROFILES


class LanguageFrequencyMatch:
    @staticmethod
    def normalize_text(text, alphabet):
        alphabet_set = set(alphabet.upper())

        return "".join(
            char.upper()
            for char in text
            if char.upper() in alphabet_set
        )

    @staticmethod
    def get_letter_count(text, alphabet):
        letter_count = {letter: 0 for letter in alphabet}

        for letter in text.upper():
            if letter in letter_count:
                letter_count[letter] += 1

        return letter_count

    @staticmethod
    def get_frequency_order(text, alphabet, etaoin):
        letter_to_freq = LanguageFrequencyMatch.get_letter_count(text, alphabet)

        freq_to_letters = {}

        for letter in alphabet:
            count = letter_to_freq[letter]

            if count not in freq_to_letters:
                freq_to_letters[count] = []

            freq_to_letters[count].append(letter)

        for frequency in freq_to_letters:
            freq_to_letters[frequency].sort(
                key=etaoin.find,
                reverse=True,
            )
            freq_to_letters[frequency] = "".join(freq_to_letters[frequency])

        freq_pairs = list(freq_to_letters.items())
        freq_pairs.sort(key=lambda item: item[0], reverse=True)

        frequency_order = []

        for _, letters in freq_pairs:
            frequency_order.append(letters)

        return "".join(frequency_order)

    @staticmethod
    def match_score(text, profile):
        alphabet = profile["alphabet"]
        etaoin = profile["etaoin"]

        normalized_text = LanguageFrequencyMatch.normalize_text(text, alphabet)

        if len(normalized_text) < 20:
            return {
                "score": 0,
                "max_score": 12,
                "normalized_length": len(normalized_text),
                "frequency_order": "",
                "note": "Text is probably too short for meaningful language frequency comparison.",
            }

        frequency_order = LanguageFrequencyMatch.get_frequency_order(
            normalized_text,
            alphabet,
            etaoin,
        )

        score = 0

        for common_letter in etaoin[:6]:
            if common_letter in frequency_order[:6]:
                score += 1

        for uncommon_letter in etaoin[-6:]:
            if uncommon_letter in frequency_order[-6:]:
                score += 1

        return {
            "score": score,
            "max_score": 12,
            "normalized_length": len(normalized_text),
            "frequency_order": frequency_order,
            "note": None,
        }

    @staticmethod
    def analyze(text):
        results = []

        for language, profile in LANGUAGE_PROFILES.items():
            result = LanguageFrequencyMatch.match_score(text, profile)

            results.append({
                "language": language,
                "score": result["score"],
                "max_score": result["max_score"],
                "normalized_length": result["normalized_length"],
                "frequency_order": result["frequency_order"],
                "note": result["note"],
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        return results