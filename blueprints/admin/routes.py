from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from core.auth.decorators import admin_required
from core.users.processor.user_processor import UserProcessor
from settings.processor.app_settings_processor import AppSettingsProcessor


admin_blueprint = Blueprint(
    "admin",
    __name__,
    template_folder="../templates/admin",
)


@admin_blueprint.route("/users")
@admin_required
def users():
    users = UserProcessor().retrieve_all_users()
    registration_enabled = AppSettingsProcessor().is_registration_enabled()

    return render_template(
        "admin/users.html",
        users=users,
        registration_enabled=registration_enabled,
    )


@admin_blueprint.route("/users/<user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    processor = UserProcessor()
    user = processor.retrieve_by_id(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        is_admin = request.form.get("is_admin") == "on"
        is_active = request.form.get("is_active") == "on"
        new_password = request.form.get("new_password", "")

        try:
            processor.update_user(
                user_id=user_id,
                username=username,
                email=email,
                is_admin=is_admin,
                is_active=is_active,
                current_user_id=current_user.id,
            )

            if new_password:
                processor.update_password(user_id, new_password)

            flash("User updated.", "success")
            return redirect(url_for("admin.users"))

        except ValueError as error:
            flash(str(error), "danger")

    return render_template("admin/edit_user.html", user=user)


@admin_blueprint.route("/users/<user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    try:
        UserProcessor().delete_user(
            user_id=user_id,
            current_user_id=current_user.id,
        )
        flash("User deleted.", "success")

    except ValueError as error:
        flash(str(error), "danger")

    return redirect(url_for("admin.users"))


@admin_blueprint.route("/registration/toggle", methods=["POST"])
@admin_required
def toggle_registration():
    enabled = request.form.get("registration_enabled") == "on"

    AppSettingsProcessor().set_registration_enabled(enabled)

    if enabled:
        flash("Registration enabled.", "success")
    else:
        flash("Registration disabled.", "warning")

    return redirect(url_for("admin.users"))