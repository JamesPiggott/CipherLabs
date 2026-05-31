# tests/test_substitution_mapping_confidence.py

from cipher.tools.substitution_mapping_confidence import SubstitutionMappingConfidence


def test_builds_mapping_confidence_from_ranked_candidates():
    assistant_result = {
        "matched_words": [
            {
                "ranked_candidates": [
                    {
                        "mapping": {
                            "A": "T",
                            "B": "H",
                        }
                    },
                    {
                        "mapping": {
                            "A": "T",
                            "B": "E",
                        }
                    },
                ]
            }
        ],
        "suggested_mappings": [],
    }

    result = SubstitutionMappingConfidence.build_from_assistant(assistant_result)

    assert result["available"] is True
    assert result["items"]
    assert any(item["cipher_letter"] == "A" for item in result["items"])