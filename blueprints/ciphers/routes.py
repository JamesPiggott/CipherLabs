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
from cipher.tools.word_pattern_analysis import WordPatternAnalysis

ciphers_blueprint = Blueprint("ciphers", __name__, template_folder="../../templates/ciphers")


@ciphers_blueprint.route("/")
def list_ciphers():
    ciphers = CipherMessageProcessor().list_ciphers()
    return render_template("ciphers/list.html", ciphers=ciphers)


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

    workspace = None

    if current_user.is_authenticated:
        workspace = UserWorkspaceProcessor().get_workspace(
            user_id=current_user.id,
            cipher_id=cipher.id,
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
