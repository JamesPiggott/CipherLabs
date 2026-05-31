import json
from functools import lru_cache
from pathlib import Path


class LanguageProfileLoader:
    PROFILE_DIR = Path(__file__).resolve().parent / "language_profiles"

    @staticmethod
    @lru_cache(maxsize=1)
    def load_profiles():
        profiles = {}

        if not LanguageProfileLoader.PROFILE_DIR.exists():
            return profiles

        for path in LanguageProfileLoader.PROFILE_DIR.glob("*.json"):
            with path.open("r", encoding="utf-8") as file:
                profile = json.load(file)

            language = profile.get("language")

            if language:
                profiles[language] = profile

        return profiles

    @staticmethod
    def get_languages():
        return sorted(LanguageProfileLoader.load_profiles().keys())

    @staticmethod
    def get_profile(language):
        return LanguageProfileLoader.load_profiles().get(language)