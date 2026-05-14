from flask import Blueprint, render_template, request
from tools.glossary_loader import load_glossary_terms

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return render_template("index.html")


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
    )