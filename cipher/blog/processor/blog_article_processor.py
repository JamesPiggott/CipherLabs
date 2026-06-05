import re
from datetime import datetime

from cipher.blog.entities.blog_article import BlogArticle
from cipher.blog.database.blog_article_database import BlogArticleDatabase


class BlogArticleProcessor:
    def __init__(self):
        self.database = BlogArticleDatabase()

    def create_table(self):
        self.database.create_table()

    def generate_slug(self, title):
        slug = title.lower().strip()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug.strip("-")

    def ensure_unique_slug(self, slug, article_id=None):
        base_slug = slug
        counter = 2

        while self.database.slug_exists(slug, exclude_article_id=article_id):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def create_article(self, form_data):
        title = form_data.get("title", "").strip()
        slug = form_data.get("slug", "").strip()

        if not slug:
            slug = self.generate_slug(title)

        slug = self.ensure_unique_slug(slug)

        now = datetime.utcnow()

        article = BlogArticle(
            title=title,
            slug=slug,
            summary=form_data.get("summary", "").strip(),
            content_html=form_data.get("content_html", ""),
            featured_image=form_data.get("featured_image", "").strip(),
            author=form_data.get("author", "").strip(),
            status=form_data.get("status", "draft"),
            publication_date=now if form_data.get("status") == "published" else None,
            last_updated=now,
            meta_title=form_data.get("meta_title", "").strip(),
            meta_description=form_data.get("meta_description", "").strip(),
            canonical_url=form_data.get("canonical_url", "").strip(),
            og_title=form_data.get("og_title", "").strip(),
            og_description=form_data.get("og_description", "").strip(),
            og_image=form_data.get("og_image", "").strip(),
            created_at=now,
            updated_at=now,
        )

        self.database.insert_article(article)
        return article

    def update_article(self, article_id, form_data):
        article = self.database.retrieve_article_by_id(article_id)

        if not article:
            return None

        title = form_data.get("title", "").strip()
        slug = form_data.get("slug", "").strip()

        if not slug:
            slug = self.generate_slug(title)

        slug = self.ensure_unique_slug(slug, article_id=article_id)

        old_status = article.status
        new_status = form_data.get("status", "draft")
        now = datetime.utcnow()

        article.title = title
        article.slug = slug
        article.summary = form_data.get("summary", "").strip()
        article.content_html = form_data.get("content_html", "")
        article.featured_image = form_data.get("featured_image", "").strip()
        article.author = form_data.get("author", "").strip()
        article.status = new_status
        article.last_updated = now
        article.meta_title = form_data.get("meta_title", "").strip()
        article.meta_description = form_data.get("meta_description", "").strip()
        article.canonical_url = form_data.get("canonical_url", "").strip()
        article.og_title = form_data.get("og_title", "").strip()
        article.og_description = form_data.get("og_description", "").strip()
        article.og_image = form_data.get("og_image", "").strip()
        article.updated_at = now

        if old_status != "published" and new_status == "published":
            article.publication_date = now

        self.database.update_article(article)
        return article

    def publish_article(self, article_id):
        article = self.database.retrieve_article_by_id(article_id)

        if not article:
            return None

        now = datetime.utcnow()
        article.status = "published"
        article.publication_date = article.publication_date or now
        article.last_updated = now
        article.updated_at = now

        self.database.update_article(article)
        return article

    def unpublish_article(self, article_id):
        article = self.database.retrieve_article_by_id(article_id)

        if not article:
            return None

        now = datetime.utcnow()
        article.status = "draft"
        article.last_updated = now
        article.updated_at = now

        self.database.update_article(article)
        return article

    def delete_article(self, article_id):
        self.database.delete_article(article_id)

    def get_article_by_id(self, article_id):
        return self.database.retrieve_article_by_id(article_id)

    def get_article_by_slug(self, slug):
        return self.database.retrieve_article_by_slug(slug)

    def get_articles(self, limit=20, offset=0):
        return self.database.retrieve_articles(limit, offset)

    def get_published_articles(self, limit=20, offset=0):
        return self.database.retrieve_published_articles(limit, offset)

    def search_published_articles(self, query, limit=20, offset=0):
        return self.database.search_published_articles(query, limit, offset)

    def get_article_seo(self, article):
        canonical_url = article.canonical_url or f"/blog/{article.slug}"

        return {
            "seo_title": article.meta_title or f"{article.title} | CipherLabs Blog",
            "seo_description": article.meta_description or article.summary[:155],
            "seo_canonical": canonical_url,
            "seo_type": "article",
            "og_title": article.og_title or article.title,
            "og_description": article.og_description or article.summary[:155],
            "og_image": article.og_image or article.featured_image,
        }