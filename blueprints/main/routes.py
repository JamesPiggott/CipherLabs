from flask import Blueprint, Response, render_template, request, url_for
from tools.glossary_loader import load_glossary_terms
from tools.resource_loader import load_resources
from cipher.processor.cipher_message_processor import CipherMessageProcessor

main_blueprint = Blueprint("main", __name__)


def absolute_url(endpoint, **values):
    return url_for(endpoint, _external=True, **values)


@main_blueprint.route("/")
def index():
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "CipherLabs",
        "url": absolute_url("main.index"),
        "description": "An interactive cryptanalysis workbench for learning, analyzing, and solving classical ciphers.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": absolute_url("main.glossary") + "?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }

    return render_template(
        "index.html",
        seo_title="CipherLabs | Interactive Cryptanalysis Workbench",
        seo_description="CipherLabs is an interactive codebreaking workbench for learning, analyzing, and solving classical ciphers.",
        seo_canonical=absolute_url("main.index"),
        structured_data=structured_data,
    )


@main_blueprint.route("/glossary")
def glossary():
    query = request.args.get("q", "").strip().lower()
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = 20

    terms = load_glossary_terms()

    if query:
        terms = [
            term for term in terms
            if query in term["term"].lower()
            or query in term["definition"].lower()
            or any(query in tag.lower() for tag in term.get("tags", []))
        ]

    total = len(terms)
    start = (page - 1) * per_page
    end = start + per_page

    return render_template(
        "glossary.html",
        terms=terms[start:end],
        query=query,
        page=page,
        per_page=per_page,
        total=total,
        has_prev=page > 1,
        has_next=end < total,
        seo_title="Cryptography Glossary | CipherLabs",
        seo_description="A practical glossary of codebreaking, cryptanalysis, and classical cipher terminology.",
        seo_canonical=absolute_url("main.glossary"),
    )


@main_blueprint.route("/resources")
def resources():
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()

    resources = load_resources()

    categories = sorted({
        item.get("category", "Other")
        for item in resources
    })

    if category:
        resources = [
            item for item in resources
            if item.get("category") == category
        ]

    if query:
        resources = [
            item for item in resources
            if query in item.get("title", "").lower()
            or query in item.get("description", "").lower()
            or query in item.get("publisher", "").lower()
            or any(query in tag.lower() for tag in item.get("tags", []))
        ]

    return render_template(
        "resources.html",
        resources=resources,
        categories=categories,
        query=query,
        selected_category=category,
        seo_title="Codebreaking Resources | CipherLabs",
        seo_description="Curated codebreaking, cryptanalysis, cipher, Kryptos, Zodiac cipher, and classical cryptography resources.",
        seo_canonical=absolute_url("main.resources"),
    )


@main_blueprint.route("/robots.txt")
def robots_txt():
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {absolute_url('main.sitemap_xml')}",
        "",
    ])

    return Response(content, mimetype="text/plain")


@main_blueprint.route("/sitemap.xml")
def sitemap_xml():
    urls = [
        {
            "loc": absolute_url("main.index"),
            "priority": "1.0",
            "changefreq": "weekly",
        },
        {
            "loc": absolute_url("main.glossary"),
            "priority": "0.8",
            "changefreq": "monthly",
        },
        {
            "loc": absolute_url("main.resources"),
            "priority": "0.8",
            "changefreq": "monthly",
        },
        {
            "loc": absolute_url("ciphers.list_ciphers"),
            "priority": "0.7",
            "changefreq": "weekly",
        },
    ]

    try:
        ciphers = CipherMessageProcessor().list_ciphers()

        for cipher in ciphers:
            urls.append({
                "loc": absolute_url("ciphers.view_cipher", cipher_id=cipher.id),
                "priority": "0.6",
                "changefreq": "monthly",
            })

    except Exception:
        pass

    xml = render_template("sitemap.xml", urls=urls)

    return Response(xml, mimetype="application/xml")