# tests/test_cipher_classifier.py

from cipher.tools.cipher_classifier import CipherClassifier


def test_classifies_caesar_when_declared():
    result = CipherClassifier.classify(
        text="KHOOR ZRUOG",
        declared_cipher_type="Caesar",
    )

    assert result["primary_type"] == "Caesar cipher"
    assert result["confidence"] >= 0.8
    assert result["next_actions"]


def test_classifies_patristocrat_without_spaces():
    result = CipherClassifier.classify(
        text="GSRHRHZHVXIVGNVHHZTVGSVXLWVYVVM",
    )

    assert result["primary_type"] in [
        "Patristocrat",
        "Possible polyalphabetic cipher",
        "Unknown",
    ]
    assert "signals" in result


def test_returns_unknown_for_short_text():
    result = CipherClassifier.classify(text="ABC")

    assert result["primary_type"] == "Unknown"