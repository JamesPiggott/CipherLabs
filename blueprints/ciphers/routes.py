from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from flask_login import login_required

from cipher.processor.cipher_message_processor import CipherMessageProcessor
from cipher.processor.user_workspace_processor import UserWorkspaceProcessor
from cipher.tools.basic_text_analysis import BasicTextAnalysis
from cipher.tools.caesar_bruteforce import CaesarBruteForce
from cipher.tools.frequency_analysis import FrequencyAnalysis
from cipher.tools.index_of_coincidence import IndexOfCoincidence
from cipher.tools.repeated_sequences import RepeatedSequences
from cipher.tools.language_frequency_match import LanguageFrequencyMatch
from cipher.tools.substitution_mapping_confidence import SubstitutionMappingConfidence
from cipher.tools.word_pattern_analysis import WordPatternAnalysis
from cipher.tools.digram_similarity import DigramSimilarity
from cipher.tools.substitution_cipher import SubstitutionCipher
from cipher.tools.substitution_mapping_assistant import SubstitutionMappingAssistant
from cipher.tools.workbench.cipher_workbench_builder import CipherWorkbenchBuilder
from cipher.tools.cipher_classifier import CipherClassifier
from cipher.tools.partial_plaintext_builder import PartialPlaintextBuilder

ciphers_blueprint = Blueprint("ciphers", __name__, template_folder="../../templates/ciphers")


@ciphers_blueprint.route("/")
def list_ciphers():
    ciphers = CipherMessageProcessor().list_ciphers()
    return render_template(
        "ciphers/list.html",
        ciphers=ciphers,
        seo_title="Public Cipher Archive | CipherLabs",
        seo_description="Browse public cipher messages and analyze them with CipherLabs cryptanalysis tools.",
        seo_canonical=url_for("ciphers.list_ciphers", _external=True),
    )


@ciphers_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_cipher():
    if request.method == "POST":
        title = request.form.get("title", "")
        ciphertext = request.form.get("ciphertext", "")
        plaintext = request.form.get("plaintext", "")
        status = request.form.get("status", "unsolved")
        cipher_type = request.form.get("cipher_type", "")
        suspected_language = request.form.get("suspected_language", "")
        source = request.form.get("source", "")

        try:
            CipherMessageProcessor().create_cipher(
                title=title,
                ciphertext=ciphertext,
                plaintext=plaintext,
                status=status,
                cipher_type=cipher_type,
                suspected_language=suspected_language,
                source=source,
                user_id=current_user.id,
            )
            flash("Cipher added.", "success")
            return redirect(url_for("ciphers.list_ciphers"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("ciphers/add.html")


@ciphers_blueprint.route("/<cipher_id>/delete", methods=["POST"])
@login_required
def delete_cipher(cipher_id):
    try:
        CipherMessageProcessor().delete_cipher(
            cipher_id=cipher_id,
            user_id=current_user.id,
            is_admin=getattr(current_user, "is_admin", False),
        )
        flash("Cipher deleted.", "success")

    except PermissionError as error:
        flash(str(error), "danger")

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(url_for("ciphers.list_ciphers"))


@ciphers_blueprint.route("/<cipher_id>")
def view_cipher(cipher_id):
    cipher = CipherMessageProcessor().get_cipher(cipher_id)

    if not cipher:
        flash("Cipher not found.", "danger")
        return redirect(url_for("ciphers.list_ciphers"))

    basic_analysis = BasicTextAnalysis.analyze(cipher.ciphertext)
    frequency_analysis = FrequencyAnalysis.analyze(cipher.ciphertext)
    index_of_coincidence = IndexOfCoincidence.calculate(cipher.ciphertext)
    repeated_sequences = RepeatedSequences.find_sequences(cipher.ciphertext)
    caesar_results = CaesarBruteForce.brute_force(cipher.ciphertext)
    caesar_best_guess = CaesarBruteForce.best_guess(cipher.ciphertext)
    language_frequency_matches = LanguageFrequencyMatch.analyze(cipher.ciphertext)
    word_pattern_analysis = WordPatternAnalysis.analyze(cipher.ciphertext)
    digram_similarity = DigramSimilarity.analyze(cipher.ciphertext)

    cipher_classification = CipherClassifier.classify(
        text=cipher.ciphertext,
        declared_cipher_type=cipher.cipher_type,
    )

    workbench = CipherWorkbenchBuilder.build(
        cipher=cipher,
        index_of_coincidence=index_of_coincidence,
        repeated_sequences=repeated_sequences,
        cipher_classification=cipher_classification,
    )

    workspace = None
    workspace_mapping = {}

    if current_user.is_authenticated:
        workspace = UserWorkspaceProcessor().get_workspace(
            user_id=current_user.id,
            cipher_id=cipher.id,
        )

        if workspace and workspace.substitution_mapping:
            workspace_mapping = workspace.substitution_mapping

    substitution_mapping_assistant = SubstitutionMappingAssistant.analyze(
        message=cipher.ciphertext,
        language=cipher.suspected_language,
        current_mapping=workspace_mapping,
        candidate_limit=8,
    )

    mapping_confidence = SubstitutionMappingConfidence.build_from_assistant(
        substitution_mapping_assistant
    )

    partial_plaintext = PartialPlaintextBuilder.build(
        ciphertext=cipher.ciphertext,
        workspace_mapping=workspace_mapping,
        mapping_confidence=mapping_confidence,
        include_confident_suggestions=True,
        minimum_confidence=0.75,
    )

    return render_template(
        "ciphers/detail.html",
        cipher=cipher,
        basic_analysis=basic_analysis,
        frequency_analysis=frequency_analysis,
        index_of_coincidence=index_of_coincidence,
        repeated_sequences=repeated_sequences,
        caesar_results=caesar_results,
        caesar_best_guess=caesar_best_guess,
        workspace=workspace,
        language_frequency_matches=language_frequency_matches,
        word_pattern_analysis=word_pattern_analysis,
        digram_similarity=digram_similarity,
        substitution_mapping_assistant=substitution_mapping_assistant,
        cipher_classification=cipher_classification,
        mapping_confidence=mapping_confidence,
        partial_plaintext=partial_plaintext,
        workbench=workbench,
        seo_title=f"{cipher.title} | Cipher Analysis | CipherLabs",
        seo_description=(
            f"Analyze the cipher message '{cipher.title}' using CipherLabs cryptanalysis tools, "
            "including frequency analysis, Index of Coincidence, word patterns, and substitution solving."
        ),
        seo_type="article",
        seo_canonical=url_for("ciphers.view_cipher", cipher_id=cipher.id, _external=True),
        structured_data={
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": cipher.title,
            "description": (
                f"Cipher analysis page for {cipher.title}, including cryptanalysis tools "
                "and guided solving workflows."
            ),
            "url": url_for("ciphers.view_cipher", cipher_id=cipher.id, _external=True),
            "author": {
                "@type": "Organization",
                "name": "CipherLabs",
            },
            "publisher": {
                "@type": "Organization",
                "name": "CipherLabs",
            },
        },
    )


@ciphers_blueprint.route("/<cipher_id>/workspace/save", methods=["POST"])
@login_required
def save_workspace(cipher_id):
    data = request.get_json() or {}

    substitution_mapping = data.get("substitution_mapping", {})
    notes = data.get("notes", "")

    workspace = UserWorkspaceProcessor().save_workspace(
        user_id=current_user.id,
        cipher_id=cipher_id,
        substitution_mapping=substitution_mapping,
        notes=notes,
    )

    return jsonify({
        "success": True,
        "message": "Workspace saved.",
        "updated_at": str(workspace.updated_at),
    })


@ciphers_blueprint.route("/<cipher_id>/substitution/apply", methods=["POST"])
@login_required
def apply_substitution_key(cipher_id):
    data = request.get_json() or {}

    key = data.get("key", "")
    mode = data.get("mode", "decrypt")

    cipher = CipherMessageProcessor().get_cipher(cipher_id)

    if not cipher:
        return jsonify({
            "success": False,
            "message": "Cipher not found.",
        }), 404

    try:
        if mode == "encrypt":
            output = SubstitutionCipher.encrypt(key, cipher.ciphertext)
        else:
            output = SubstitutionCipher.decrypt(key, cipher.ciphertext)

        return jsonify({
            "success": True,
            "output": output,
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error),
        }), 400
