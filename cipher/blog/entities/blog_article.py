import uuid
from datetime import datetime


class BlogArticle:
    def __init__(
        self,
        id=None,
        title="",
        slug="",
        summary="",
        content_html="",
        featured_image="",
        author="",
        status="draft",
        publication_date=None,
        last_updated=None,
        meta_title="",
        meta_description="",
        canonical_url="",
        og_title="",
        og_description="",
        og_image="",
        created_at=None,
        updated_at=None,
    ):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.slug = slug
        self.summary = summary
        self.content_html = content_html
        self.featured_image = featured_image
        self.author = author
        self.status = status
        self.publication_date = publication_date
        self.last_updated = last_updated
        self.meta_title = meta_title
        self.meta_description = meta_description
        self.canonical_url = canonical_url
        self.og_title = og_title
        self.og_description = og_description
        self.og_image = og_image
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @staticmethod
    def from_row(row):
        if not row:
            return None

        return BlogArticle(
            id=str(row.get("id")),
            title=row.get("title") or "",
            slug=row.get("slug") or "",
            summary=row.get("summary") or "",
            content_html=row.get("content_html") or "",
            featured_image=row.get("featured_image") or "",
            author=row.get("author") or "",
            status=row.get("status") or "draft",
            publication_date=row.get("publication_date"),
            last_updated=row.get("last_updated"),
            meta_title=row.get("meta_title") or "",
            meta_description=row.get("meta_description") or "",
            canonical_url=row.get("canonical_url") or "",
            og_title=row.get("og_title") or "",
            og_description=row.get("og_description") or "",
            og_image=row.get("og_image") or "",
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )