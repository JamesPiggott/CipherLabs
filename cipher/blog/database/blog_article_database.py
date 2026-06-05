from cipher.blog.entities.blog_article import BlogArticle
from core.database.database import db


class BlogArticleDatabase:
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS blog_articles (
            id UUID PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            summary TEXT,
            content_html TEXT,
            featured_image TEXT,
            author TEXT,
            status TEXT NOT NULL DEFAULT 'draft',
            publication_date TIMESTAMP,
            last_updated TIMESTAMP,
            meta_title TEXT,
            meta_description TEXT,
            canonical_url TEXT,
            og_title TEXT,
            og_description TEXT,
            og_image TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """
        db.execute(query)

    def insert_article(self, article: BlogArticle):
        query = """
        INSERT INTO blog_articles (
            id, title, slug, summary, content_html, featured_image,
            author, status, publication_date, last_updated,
            meta_title, meta_description, canonical_url,
            og_title, og_description, og_image,
            created_at, updated_at
        )
        VALUES (
            %(id)s, %(title)s, %(slug)s, %(summary)s, %(content_html)s, %(featured_image)s,
            %(author)s, %(status)s, %(publication_date)s, %(last_updated)s,
            %(meta_title)s, %(meta_description)s, %(canonical_url)s,
            %(og_title)s, %(og_description)s, %(og_image)s,
            %(created_at)s, %(updated_at)s
        )
        """
        db.execute(query, article.__dict__)

    def update_article(self, article: BlogArticle):
        query = """
        UPDATE blog_articles
        SET title = %(title)s,
            slug = %(slug)s,
            summary = %(summary)s,
            content_html = %(content_html)s,
            featured_image = %(featured_image)s,
            author = %(author)s,
            status = %(status)s,
            publication_date = %(publication_date)s,
            last_updated = %(last_updated)s,
            meta_title = %(meta_title)s,
            meta_description = %(meta_description)s,
            canonical_url = %(canonical_url)s,
            og_title = %(og_title)s,
            og_description = %(og_description)s,
            og_image = %(og_image)s,
            updated_at = %(updated_at)s
        WHERE id = %(id)s
        """
        db.execute(query, article.__dict__)

    def delete_article(self, article_id):
        query = "DELETE FROM blog_articles WHERE id = %s"
        db.execute(query, (article_id,))

    def retrieve_article_by_id(self, article_id):
        query = "SELECT * FROM blog_articles WHERE id = %s"
        row = db.fetch_one(query, (article_id,))
        return BlogArticle.from_row(row)

    def retrieve_article_by_slug(self, slug):
        query = "SELECT * FROM blog_articles WHERE slug = %s"
        row = db.fetch_one(query, (slug,))
        return BlogArticle.from_row(row)

    def retrieve_articles(self, limit=20, offset=0):
        query = """
        SELECT *
        FROM blog_articles
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        rows = db.fetch_all(query, (limit, offset))
        return [BlogArticle.from_row(row) for row in rows]

    def retrieve_published_articles(self, limit=20, offset=0):
        query = """
        SELECT *
        FROM blog_articles
        WHERE status = 'published'
        ORDER BY publication_date DESC NULLS LAST, created_at DESC
        LIMIT %s OFFSET %s
        """
        rows = db.fetch_all(query, (limit, offset))
        return [BlogArticle.from_row(row) for row in rows]

    def slug_exists(self, slug, exclude_article_id=None):
        if exclude_article_id:
            query = """
            SELECT id
            FROM blog_articles
            WHERE slug = %s
            AND id != %s
            """
            row = db.fetch_one(query, (slug, exclude_article_id))
        else:
            query = """
            SELECT id
            FROM blog_articles
            WHERE slug = %s
            """
            row = db.fetch_one(query, (slug,))

        return row is not None

    def search_published_articles(self, search_query, limit=20, offset=0):
        like_query = f"%{search_query}%"

        query = """
        SELECT *
        FROM blog_articles
        WHERE status = 'published'
        AND (
            title ILIKE %s
            OR summary ILIKE %s
            OR content_html ILIKE %s
        )
        ORDER BY publication_date DESC NULLS LAST, created_at DESC
        LIMIT %s OFFSET %s
        """

        rows = db.fetch_all(
            query,
            (like_query, like_query, like_query, limit, offset)
        )

        return [BlogArticle.from_row(row) for row in rows]