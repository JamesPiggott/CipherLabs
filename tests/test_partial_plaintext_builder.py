# tests/test_partial_plaintext_builder.py

from cipher.tools.partial_plaintext_builder import PartialPlaintextBuilder


def test_builds_plaintext_from_workspace_mapping():
    result = PartialPlaintextBuilder.build(
        ciphertext="ABC XYZ",
        workspace_mapping={
            "A": "T",
            "B": "H",
            "C": "E",
        },
        include_confident_suggestions=False,
    )

    assert result["plaintext"] == "THE ___"
    assert result["confirmed_letters"] == 3
    assert result["suggested_letters"] == 0


def test_uses_confident_suggestions():
    result = PartialPlaintextBuilder.build(
        ciphertext="ABC",
        workspace_mapping={},
        mapping_confidence={
            "available": True,
            "items": [
                {
                    "cipher_letter": "A",
                    "plain_letter": "T",
                    "confidence": 0.9,
                }
            ],
        },
        include_confident_suggestions=True,
    )

    assert result["plaintext"] == "T__"
    assert result["suggested_letters"] == 1