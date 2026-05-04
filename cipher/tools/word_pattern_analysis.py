import re
from collections import defaultdict

from cipher.reference.word_patterns import get_word_pattern


class WordPatternAnalysis:
    WORD_PATTERN = re.compile(r"[A-Za-z]+")

    @staticmethod
    def extract_words(text):
        return WordPatternAnalysis.WORD_PATTERN.findall(text.upper())

    @staticmethod
    def analyze(text):
        words = WordPatternAnalysis.extract_words(text)

        pattern_map = defaultdict(list)

        for word in words:
            pattern = get_word_pattern(word)

            if word not in pattern_map[pattern]:
                pattern_map[pattern].append(word)

        results = []

        for pattern, pattern_words in pattern_map.items():
            results.append({
                "pattern": pattern,
                "word_length": len(pattern.split(".")),
                "words": pattern_words,
                "word_count": len(pattern_words),
            })

        results.sort(
            key=lambda item: (
                item["word_count"],
                item["word_length"],
            ),
            reverse=True,
        )

        return results[:30]