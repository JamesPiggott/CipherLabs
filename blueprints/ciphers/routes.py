from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from cipher.processor.cipher_message_processor import CipherMessageProcessor
from cipher.tools.frequency_analysis import FrequencyAnalysis
from cipher.tools.basic_text_analysis import BasicTextAnalysis
from cipher.tools.index_of_coincidence import IndexOfCoincidence

ciphers_blueprint = Blueprint("ciphers", __name__, template_folder="../../templates/ciphers")


@ciphers_blueprint.route("/")
def list_ciphers():
    ciphers = CipherMessageProcessor().list_ciphers()
    return render_template("ciphers/list.html", ciphers=ciphers)


@ciphers_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_cipher():
    if request.method == "POST":
        title = request.form.get("title")
        ciphertext = request.form.get("ciphertext")

        try:
            CipherMessageProcessor().create_cipher(
                title=title,
                ciphertext=ciphertext,
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

    return render_template(
        "ciphers/detail.html",
        cipher=cipher,
        basic_analysis=basic_analysis,
        frequency_analysis=frequency_analysis,
        index_of_coincidence=index_of_coincidence,
    )


