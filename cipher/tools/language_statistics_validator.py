from cipher.reference.language_profiles import LanguageProfileLoader
from cipher.tools.index_of_coincidence import IndexOfCoincidence
from cipher.tools.rank_similarity_scorer import RankSimilarityScorer


class LanguageStatisticsValidator:
    @staticmethod
    def score_ioc(ioc_value, expected_ioc):
        if expected_ioc is None:
            return {
                "available": False,
                "score": 0.0,
                "display": "N/A",
                "reason": "No Index of Coincidence reference is available for this language yet.",
            }

        if not ioc_value:
            return {
                "available": True,
                "score": 0.0,
                "display": "0.0000",
                "reason": "",
            }

        distance = abs(ioc_value - expected_ioc)
        score = max(0.0, 1.0 - (distance / expected_ioc))

        return {
            "available": True,
            "score": round(score, 4),
            "display": str(round(ioc_value, 4)),
            "reason": "",
        }

    @staticmethod
    def unavailable_ngram_score(label, ranked=False):
        prefix = "ranked " if ranked else ""
        return {
            "available": False,
            "score": 0.0,
            "coverage": 0.0,
            "matched": 0,
            "total": 0,
            "top_matches": [],
            "display": "N/A",
            "reason": f"No {prefix}{label} data is available for this language yet.",
        }

    @staticmethod
    def score_frequency_ngrams(text, profile, key, size, label):
        data = profile.get(key)

        if not data:
            return LanguageStatisticsValidator.unavailable_ngram_score(label)

        result = RankSimilarityScorer.score_weighted_ngrams(
            text=text,
            weighted_ngrams=data,
            size=size,
        )

        result["available"] = True
        result["display"] = f"{round(result['coverage'] * 100)}%"
        result["reason"] = ""

        return result

    @staticmethod
    def score_ranked_ngrams(text, profile, key, size, label):
        ranked_items = profile.get(key)

        if not ranked_items:
            return LanguageStatisticsValidator.unavailable_ngram_score(
                label=label,
                ranked=True,
            )

        result = RankSimilarityScorer.score_ranked_ngrams(
            text=text,
            ranked_ngrams=ranked_items,
            size=size,
        )

        result["available"] = True
        result["display"] = f"{round(result['coverage'] * 100)}%"
        result["reason"] = ""

        return result

    @staticmethod
    def score_common_words(text, profile):
        common_words = profile.get("common_words")

        if not common_words:
            return {
                "available": False,
                "score": 0.0,
                "coverage": 0.0,
                "matched": 0,
                "total": 0,
                "top_matches": [],
                "display": "N/A",
                "reason": "No common-word list is available for this language yet.",
            }

        result = RankSimilarityScorer.score_common_words(
            text=text,
            common_words=common_words,
        )

        result["available"] = True
        result["display"] = f"{result['matched']} / {result['total']}"
        result["reason"] = ""

        return result

    @staticmethod
    def combine_scores(scores):
        weighted_scores = [
            (scores["digrams"], 0.15),
            (scores["ranked_digrams"], 0.10),
            (scores["trigrams"], 0.20),
            (scores["ranked_trigrams"], 0.20),
            (scores["quadgrams"], 0.15),
            (scores["ranked_quadgrams"], 0.15),
            (scores["common_words"], 0.03),
            (scores["ioc"], 0.02),
        ]

        available_weight = 0.0
        total_score = 0.0

        for score_data, weight in weighted_scores:
            if not score_data.get("available"):
                continue

            available_weight += weight
            total_score += score_data.get("score", 0.0) * weight

        if available_weight == 0:
            return 0.0

        return round(total_score / available_weight, 4)

    @staticmethod
    def build_signals(scores):
        signals = []

        signal_rules = [
            ("digrams", 0.05, "Exact digram matches were observed."),
            ("ranked_digrams", 0.05, "Ranked digram matches were observed."),
            ("trigrams", 0.03, "Exact trigram matches were observed."),
            ("ranked_trigrams", 0.03, "Ranked trigram matches were observed."),
            ("quadgrams", 0.02, "Exact quadgram matches were observed."),
            ("ranked_quadgrams", 0.02, "Ranked quadgram matches were observed."),
        ]

        for key, threshold, message in signal_rules:
            if scores[key].get("available") and scores[key].get("coverage", 0.0) >= threshold:
                signals.append(message)

        if scores["common_words"].get("available") and scores["common_words"].get("matched", 0) > 0:
            signals.append("Common words were found.")

        if scores["ioc"].get("available") and scores["ioc"].get("score", 0.0) >= 0.75:
            signals.append("Index of Coincidence is close to the language reference.")

        return signals

    @staticmethod
    def analyze(text):
        if not text:
            return []

        profiles = LanguageProfileLoader.load_profiles()

        if not profiles:
            return []

        ioc_result = IndexOfCoincidence.calculate(text)
        ioc_value = ioc_result.get("value", 0) if ioc_result else 0

        results = []

        for language, profile in profiles.items():
            scores = {
                "digrams": LanguageStatisticsValidator.score_frequency_ngrams(
                    text=text,
                    profile=profile,
                    key="digrams",
                    size=2,
                    label="digram",
                ),
                "ranked_digrams": LanguageStatisticsValidator.score_ranked_ngrams(
                    text=text,
                    profile=profile,
                    key="ranked_digrams",
                    size=2,
                    label="digram",
                ),
                "trigrams": LanguageStatisticsValidator.score_frequency_ngrams(
                    text=text,
                    profile=profile,
                    key="trigrams",
                    size=3,
                    label="trigram",
                ),
                "ranked_trigrams": LanguageStatisticsValidator.score_ranked_ngrams(
                    text=text,
                    profile=profile,
                    key="ranked_trigrams",
                    size=3,
                    label="trigram",
                ),
                "quadgrams": LanguageStatisticsValidator.score_frequency_ngrams(
                    text=text,
                    profile=profile,
                    key="quadgrams",
                    size=4,
                    label="quadgram",
                ),
                "ranked_quadgrams": LanguageStatisticsValidator.score_ranked_ngrams(
                    text=text,
                    profile=profile,
                    key="ranked_quadgrams",
                    size=4,
                    label="quadgram",
                ),
                "common_words": LanguageStatisticsValidator.score_common_words(
                    text=text,
                    profile=profile,
                ),
                "ioc": LanguageStatisticsValidator.score_ioc(
                    ioc_value=ioc_value,
                    expected_ioc=profile.get("ioc"),
                ),
            }

            combined_score = LanguageStatisticsValidator.combine_scores(scores)

            available_datasets = sum(
                1 for item in scores.values()
                if item.get("available")
            )

            missing_datasets = sum(
                1 for item in scores.values()
                if not item.get("available")
            )

            results.append({
                "language": language,
                "score": combined_score,
                "score_percent": int(round(combined_score * 100)),
                "digrams_score": scores["digrams"],
                "ranked_digrams_score": scores["ranked_digrams"],
                "trigrams_score": scores["trigrams"],
                "ranked_trigrams_score": scores["ranked_trigrams"],
                "quadgrams_score": scores["quadgrams"],
                "ranked_quadgrams_score": scores["ranked_quadgrams"],
                "common_word_score": scores["common_words"],
                "ioc_score": scores["ioc"],
                "ioc_value": round(ioc_value, 4),
                "available_datasets": available_datasets,
                "missing_datasets": missing_datasets,
                "signals": LanguageStatisticsValidator.build_signals(scores),
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        return results
