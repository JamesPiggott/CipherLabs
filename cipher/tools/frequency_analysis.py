from collections import Counter
import string


class FrequencyAnalysis:
    @staticmethod
    def normalize_text(text):
        return "".join(
            char.upper()
            for char in text
            if char.upper() in string.ascii_uppercase
        )

    @staticmethod
    def analyze(text):
        normalized_text = FrequencyAnalysis.normalize_text(text)
        total_letters = len(normalized_text)

        if total_letters == 0:
            return {
                "total_letters": 0,
                "frequencies": [],
            }

        counter = Counter(normalized_text)
        max_count = max(counter.values()) if counter else 0

        frequencies = []

        for letter in string.ascii_uppercase:
            count = counter.get(letter, 0)
            percentage = round((count / total_letters) * 100, 2)

            visual_percentage = 0
            if max_count > 0:
                visual_percentage = round((count / max_count) * 100, 2)

            frequencies.append({
                "letter": letter,
                "count": count,
                "percentage": percentage,
                "visual_percentage": visual_percentage,
            })

        frequencies.sort(key=lambda item: item["count"], reverse=True)

        return {
            "total_letters": total_letters,
            "frequencies": frequencies,
        }