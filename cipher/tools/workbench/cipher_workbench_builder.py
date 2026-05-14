from cipher.tools.workbench.workbench_widget import WorkbenchWidget


class CipherWorkbenchBuilder:
    PHASES = [
        {
            "id": "identify",
            "title": "1. Identify",
            "short_title": "Identify",
            "description": "Determine likely cipher family and language.",
        },
        {
            "id": "analyze",
            "title": "2. Analyze",
            "short_title": "Analyze",
            "description": "Inspect statistical and structural patterns.",
        },
        {
            "id": "solve",
            "title": "3. Solve",
            "short_title": "Solve",
            "description": "Use interactive tools to build a solution.",
        },
        {
            "id": "validate",
            "title": "4. Validate",
            "short_title": "Validate",
            "description": "Check whether the solution behaves like natural language.",
        },
        {
            "id": "notes",
            "title": "5. Notes",
            "short_title": "Notes",
            "description": "Save assumptions, observations, and rejected guesses.",
        },
    ]

    @staticmethod
    def normalize(value):
        return (value or "").strip().lower()

    @staticmethod
    def build(
            cipher,
            index_of_coincidence=None,
            repeated_sequences=None,
            cipher_classification=None,
    ):
        cipher_type = CipherWorkbenchBuilder.normalize(cipher.cipher_type)
        suspected_language = CipherWorkbenchBuilder.normalize(cipher.suspected_language)

        classification_type = ""
        classification_recommended_next_step = None

        if cipher_classification:
            classification_type = CipherWorkbenchBuilder.normalize(
                cipher_classification.get("primary_type")
            )
            classification_recommended_next_step = cipher_classification.get(
                "recommended_next_step"
            )

        ioc_value = 0

        if index_of_coincidence:
            ioc_value = index_of_coincidence.get("value", 0) or 0

        has_repeated_sequences = bool(repeated_sequences)

        looks_like_caesar = (
                "caesar" in cipher_type
                or "caesar" in classification_type
        )

        looks_like_substitution = (
                "substitution" in cipher_type
                or "monoalphabetic" in cipher_type
                or "aristocrat" in classification_type
                or "patristocrat" in classification_type
                or ioc_value >= 0.06
        )

        looks_like_polyalphabetic = (
                "vigenere" in cipher_type
                or "vigenère" in cipher_type
                or "polyalphabetic" in cipher_type
                or "polyalphabetic" in classification_type
                or ioc_value < 0.045
                or has_repeated_sequences
        )

        if looks_like_caesar:
            recommended_path = (
                "Start with Caesar brute force, then validate the best result using language hints."
            )
            primary_hypothesis = "Caesar shift"

        elif looks_like_substitution:
            if "aristocrat" in classification_type:
                primary_hypothesis = "Aristocrat"
                recommended_path = (
                    "Word boundaries appear to be preserved. Start with frequency analysis, "
                    "then use word patterns and the substitution assistant."
                )
            elif "patristocrat" in classification_type:
                primary_hypothesis = "Patristocrat"
                recommended_path = (
                    "Word boundaries appear to be missing. Start with frequency analysis, "
                    "then use substitution tools carefully because word-pattern analysis is less direct."
                )
            else:
                primary_hypothesis = "Monoalphabetic substitution"
                recommended_path = (
                    "Start with frequency and word patterns, then use the substitution assistant "
                    "to test candidate mappings."
                )

        elif looks_like_polyalphabetic:
            recommended_path = (
                "Start with repeated sequences and IoC. This may require a future Vigenère/Kasiski workflow."
            )
            primary_hypothesis = "Possible polyalphabetic cipher"

        else:
            recommended_path = (
                "Start with identification tools, then enable analysis widgets as patterns emerge."
            )
            primary_hypothesis = "Unknown"

        if classification_recommended_next_step:
            recommended_path = classification_recommended_next_step

        widgets = [
            WorkbenchWidget(
                widget_id="ciphertext",
                title="Ciphertext",
                template="ciphers/workbench/widgets/_ciphertext.html",
                phase="identify",
                description="Review the original message and known plaintext.",
                recommended=True,
                order=10,
                default_open=True,
            ),
            WorkbenchWidget(
                widget_id="cipher-classification",
                title="Cipher Classification",
                template="ciphers/workbench/widgets/_cipher_classification.html",
                phase="identify",
                description="Estimate the likely cipher family and starting strategy.",
                recommended=True,
                order=15,
                default_open=True,
            ),
            WorkbenchWidget(
                widget_id="basic-analysis",
                title="Basic Analysis",
                template="ciphers/workbench/widgets/_basic_analysis.html",
                phase="identify",
                description="Basic size, symbol, and IoC indicators.",
                recommended=True,
                order=20,
                default_open=True,
            ),
            WorkbenchWidget(
                widget_id="language-hints",
                title="Language Hints",
                template="ciphers/workbench/widgets/_language_hints.html",
                phase="identify",
                description="Compare letter frequency against language profiles.",
                recommended=True,
                order=30,
                default_open=True,
            ),
            WorkbenchWidget(
                widget_id="frequency-analysis",
                title="Frequency Analysis",
                template="ciphers/workbench/widgets/_frequency_analysis.html",
                phase="analyze",
                description="Inspect single-letter frequency distribution.",
                recommended=looks_like_substitution,
                order=10,
            ),
            WorkbenchWidget(
                widget_id="repeated-sequences",
                title="Repeated Sequences",
                template="ciphers/workbench/widgets/_repeated_sequences.html",
                phase="analyze",
                description="Find repeated sequences and distances.",
                recommended=looks_like_polyalphabetic,
                order=20,
            ),
            WorkbenchWidget(
                widget_id="word-patterns",
                title="Word Patterns",
                template="ciphers/workbench/widgets/_word_patterns.html",
                phase="analyze",
                description="Group cipher words by repeated-letter structure.",
                recommended=looks_like_substitution and "patristocrat" not in classification_type,
                order=30,
            ),
            WorkbenchWidget(
                widget_id="caesar",
                title="Caesar Brute Force",
                template="ciphers/workbench/widgets/_caesar.html",
                phase="solve",
                description="Try all Caesar shifts and rank likely plaintexts.",
                recommended=looks_like_caesar,
                order=10,
            ),
            WorkbenchWidget(
                widget_id="substitution-solver",
                title="Substitution Workspace",
                template="ciphers/workbench/widgets/_substitution_solver.html",
                phase="solve",
                description="Manually assign plaintext letters and preview the result.",
                recommended=looks_like_substitution,
                order=20,
            ),
            WorkbenchWidget(
                widget_id="partial-plaintext",
                title="Plaintext Reveal",
                template="ciphers/workbench/widgets/_partial_plaintext.html",
                phase="solve",
                description="Show the emerging plaintext from confirmed and high-confidence mappings.",
                recommended=looks_like_substitution,
                order=25,
            ),
            WorkbenchWidget(
                widget_id="substitution-assistant",
                title="Substitution Assistant",
                template="ciphers/workbench/widgets/_substitution_assistant.html",
                phase="solve",
                description="Rank candidate words and mapping suggestions.",
                recommended=looks_like_substitution and "patristocrat" not in classification_type,
                order=30,
            ),
            WorkbenchWidget(
                widget_id="mapping-confidence",
                title="Mapping Confidence",
                template="ciphers/workbench/widgets/_mapping_confidence.html",
                phase="solve",
                description="Show which suggested letter mappings have the strongest evidence.",
                recommended=looks_like_substitution,
                order=35,
            ),
            WorkbenchWidget(
                widget_id="substitution-key-tool",
                title="Substitution Key Tool",
                template="ciphers/workbench/widgets/_substitution_key_tool.html",
                phase="solve",
                description="Test a complete 26-letter substitution key.",
                recommended=False,
                order=40,
            ),
            WorkbenchWidget(
                widget_id="digram-similarity",
                title="Digram Similarity",
                template="ciphers/workbench/widgets/_digram_similarity.html",
                phase="validate",
                description="Compare digram distribution against language profiles.",
                recommended=bool(suspected_language),
                order=10,
            ),
            WorkbenchWidget(
                widget_id="notes",
                title="Workspace Notes",
                template="ciphers/workbench/widgets/_notes.html",
                phase="notes",
                description="Record assumptions, rejected guesses, and observations.",
                recommended=True,
                order=10,
                default_open=True,
            ),
        ]

        grouped_widgets = {}

        for phase in CipherWorkbenchBuilder.PHASES:
            grouped_widgets[phase["id"]] = []

        for widget in widgets:
            grouped_widgets.setdefault(widget.phase, []).append(widget)

        for phase_id in grouped_widgets:
            grouped_widgets[phase_id].sort(key=lambda item: item.order)

        recommended_widget_ids = [
            widget.id
            for widget in widgets
            if widget.recommended
        ]

        return {
            "phases": CipherWorkbenchBuilder.PHASES,
            "widgets": widgets,
            "grouped_widgets": grouped_widgets,
            "recommended_widget_ids": recommended_widget_ids,
            "recommended_path": recommended_path,
            "primary_hypothesis": primary_hypothesis,
            "looks_like_substitution": looks_like_substitution,
            "looks_like_caesar": looks_like_caesar,
            "looks_like_polyalphabetic": looks_like_polyalphabetic,
            "classification_type": classification_type,
        }