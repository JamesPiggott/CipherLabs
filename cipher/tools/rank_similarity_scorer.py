import re
import string
from collections import Counter


class RankSimilarityScorer:
    LETTERS = string.ascii_uppercase

    @staticmethod
    def normalize_text(text):
        return "".join(
            char.upper()
            for char in text or ""
            if char.upper() in RankSimilarityScorer.LETTERS or char.isspace()
        )

    @staticmethod
    def normalize_letters_only(text):
        return "".join(
            char.upper()
            for char in text or ""
            if char.upper() in RankSimilarityScorer.LETTERS
        )

    @staticmethod
    def normalize_ranked_items(ranked_items):
        """
        Accepts either:
        - ["THE", "AND", "ING"]
        - {"THE": 1.0, "AND": 0.95}

        This keeps JSON profiles flexible without creating language-specific code paths.
        """
        if not ranked_items:
            return []

        if isinstance(ranked_items, dict):
            return [
                item.upper()
                for item, _weight in sorted(
                    ranked_items.items(),
                    key=lambda pair: pair[1],
                    reverse=True,
                )
            ]

        return [str(item).upper() for item in ranked_items]

    @staticmethod
    def rank_to_weights(ranked_items):
        normalized_items = RankSimilarityScorer.normalize_ranked_items(ranked_items)

        if not normalized_items:
            return {}

        total = len(normalized_items)

        return {
            item: (total - index) / total
            for index, item in enumerate(normalized_items)
        }

    @staticmethod
    def observed_ngrams(text, size):
        normalized = RankSimilarityScorer.normalize_letters_only(text)

        if len(normalized) < size:
            return []

        return [
            normalized[index:index + size]
            for index in range(len(normalized) - size + 1)
        ]

    @staticmethod
    def observed_ngram_counts(text, size):
        return Counter(RankSimilarityScorer.observed_ngrams(text, size))

    @staticmethod
    def score_weighted_ngrams(text, weighted_ngrams, size, top_limit=10):
        """
        Scores observed ngrams against weighted reference data.

        weighted_ngrams should be a dict such as:
        {
            "THE": 1.0,
            "AND": 0.92
        }
        """
        counter = RankSimilarityScorer.observed_ngram_counts(text, size)

        if not counter:
            return {
                "score": 0.0,
                "matched": 0,
                "total": 0,
                "coverage": 0.0,
                "top_matches": [],
            }

        normalized_weights = {
            str(item).upper(): float(weight)
            for item, weight in (weighted_ngrams or {}).items()
        }

        if not normalized_weights:
            return {
                "score": 0.0,
                "matched": 0,
                "total": sum(counter.values()),
                "coverage": 0.0,
                "top_matches": [],
            }

        total = sum(counter.values())
        matched = 0
        weighted_score = 0.0
        max_expected = max(normalized_weights.values()) or 1.0
        top_matches = []

        for ngram, count in counter.items():
            weight = normalized_weights.get(ngram)

            if weight is None:
                continue

            matched += count
            weighted_score += weight * count
            top_matches.append({
                "ngram": ngram,
                "count": count,
                "weight": round(weight, 4),
            })

        top_matches.sort(
            key=lambda item: (item["count"], item["weight"], item["ngram"]),
            reverse=True,
        )

        score = weighted_score / (total * max_expected) if total else 0.0
        coverage = matched / total if total else 0.0

        return {
            "score": round(score, 4),
            "matched": matched,
            "total": total,
            "coverage": round(coverage, 4),
            "top_matches": top_matches[:top_limit],
        }

    @staticmethod
    def score_ranked_ngrams(text, ranked_ngrams, size, top_limit=10):
        ngrams = RankSimilarityScorer.observed_ngrams(text, size)

        if not ngrams:
            return {
                "score": 0.0,
                "matched": 0,
                "total": 0,
                "coverage": 0.0,
                "top_matches": [],
            }

        weights = RankSimilarityScorer.rank_to_weights(ranked_ngrams)
        counter = Counter(ngrams)

        total = sum(counter.values())
        matched = 0
        weighted_score = 0.0
        top_matches = []

        for ngram, count in counter.items():
            if ngram in weights:
                matched += count
                weighted_score += weights[ngram] * count
                top_matches.append({
                    "ngram": ngram,
                    "count": count,
                    "weight": round(weights[ngram], 4),
                })

        top_matches.sort(
            key=lambda item: (item["count"], item["weight"]),
            reverse=True,
        )

        score = weighted_score / total if total else 0.0
        coverage = matched / total if total else 0.0

        return {
            "score": round(score, 4),
            "matched": matched,
            "total": total,
            "coverage": round(coverage, 4),
            "top_matches": top_matches[:top_limit],
        }

    @staticmethod
    def score_common_words(text, common_words, top_limit=10):
        normalized = RankSimilarityScorer.normalize_text(text)
        words = re.findall(r"[A-Z]+", normalized)

        if not words:
            return {
                "score": 0.0,
                "matched": 0,
                "total": 0,
                "coverage": 0.0,
                "top_matches": [],
            }

        weights = RankSimilarityScorer.rank_to_weights(common_words)
        counter = Counter(words)

        total = sum(counter.values())
        matched = 0
        weighted_score = 0.0
        top_matches = []

        for word, count in counter.items():
            if word not in weights:
                continue

            matched += count
            weighted_score += weights[word] * count
            top_matches.append({
                "word": word,
                "count": count,
                "weight": round(weights[word], 4),
            })

        top_matches.sort(
            key=lambda item: (item["count"], item["weight"], item["word"]),
            reverse=True,
        )

        score = weighted_score / total if total else 0.0
        coverage = matched / total if total else 0.0

        return {
            "score": round(score, 4),
            "matched": matched,
            "total": total,
            "coverage": round(coverage, 4),
            "top_matches": top_matches[:top_limit],
        }
