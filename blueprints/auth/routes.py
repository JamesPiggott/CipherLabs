from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from core.users.processor.user_processor import UserProcessor

auth_blueprint = Blueprint("auth", __name__, template_folder="../../templates/auth")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        try:
            user = UserProcessor().create_user(
                username=username,
                email=email,
                password=password,
            )
            login_user(user)
            flash("Account created successfully.", "success")
            return redirect(url_for("main.index"))

        except ValueError as error:
            flash(str(error), "danger")

    return render_template("auth/register.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "")
        password = request.form.get("password", "")

        user = UserProcessor().authenticate(identifier, password)

        if user:
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))

        flash("Invalid username/email or password.", "danger")

    return render_template("auth/login.html")


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.index"))