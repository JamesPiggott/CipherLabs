from flask import Blueprint, render_template, request, redirect, url_for, abort, flash

from cipher.blog.processor.blog_article_processor import BlogArticleProcessor


admin_blog_blueprint = Blueprint(
    "admin_blog",
    __name__,
    url_prefix="/admin/blog"
)

article_processor = BlogArticleProcessor()


@admin_blog_blueprint.route("/articles")
def articles():
    article_list = article_processor.get_articles(limit=100)

    return render_template(
        "admin/blog/articles.html",
        articles=article_list
    )


@admin_blog_blueprint.route("/articles/add", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        article_processor.create_article(request.form)
        flash("Article created successfully.", "success")
        return redirect(url_for("admin_blog.articles"))

    return render_template(
        "admin/blog/article_form.html",
        article=None,
        form_action=url_for("admin_blog.add_article")
    )


@admin_blog_blueprint.route("/articles/edit/<article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    article = article_processor.get_article_by_id(article_id)

    if not article:
        abort(404)

    if request.method == "POST":
        article_processor.update_article(article_id, request.form)
        flash("Article updated successfully.", "success")
        return redirect(url_for("admin_blog.articles"))

    return render_template(
        "admin/blog/article_form.html",
        article=article,
        form_action=url_for("admin_blog.edit_article", article_id=article_id)
    )


@admin_blog_blueprint.route("/articles/delete/<article_id>", methods=["POST"])
def delete_article(article_id):
    article_processor.delete_article(article_id)
    flash("Article deleted successfully.", "success")
    return redirect(url_for("admin_blog.articles"))


@admin_blog_blueprint.route("/articles/publish/<article_id>", methods=["POST"])
def publish_article(article_id):
    article_processor.publish_article(article_id)
    flash("Article published.", "success")
    return redirect(url_for("admin_blog.articles"))


@admin_blog_blueprint.route("/articles/unpublish/<article_id>", methods=["POST"])
def unpublish_article(article_id):
    article_processor.unpublish_article(article_id)
    flash("Article unpublished.", "success")
    return redirect(url_for("admin_blog.articles"))