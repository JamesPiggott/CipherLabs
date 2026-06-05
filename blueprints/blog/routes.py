from flask import Blueprint, render_template, request, abort

from cipher.blog.processor.blog_article_processor import BlogArticleProcessor


blog_blueprint = Blueprint(
    "blog",
    __name__,
    url_prefix="/blog"
)

article_processor = BlogArticleProcessor()


@blog_blueprint.route("/")
def blog_index():
    page = request.args.get("page", 1, type=int)
    limit = 24
    offset = (page - 1) * limit

    articles = article_processor.get_published_articles(limit=limit, offset=offset)

    return render_template(
        "blog/index.html",
        articles=articles,
        page=page
    )


@blog_blueprint.route("/<slug>")
def blog_article(slug):
    article = article_processor.get_article_by_slug(slug)

    if not article or article.status != "published":
        abort(404)

    seo = article_processor.get_article_seo(article)

    return render_template(
        "blog/article.html",
        article=article,
        seo=seo
    )


@blog_blueprint.route("/search")
def blog_search():
    query = request.args.get("q", "").strip()
    articles = []

    if query:
        articles = article_processor.search_published_articles(query)

    return render_template(
        "blog/search.html",
        query=query,
        articles=articles
    )