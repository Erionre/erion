from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Book:
    source: str
    source_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    description: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    published_year: Optional[int] = None
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    edition_count: Optional[int] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    canonical_url: Optional[str] = None
    thumbnail: Optional[str] = None
    popularity_score: Optional[float] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "source": self.source,
            "source_id": self.source_id,
            "title": self.title,
            "authors": self.authors,
            "description": self.description,
            "categories": self.categories,
            "published_year": self.published_year,
            "average_rating": self.average_rating,
            "ratings_count": self.ratings_count,
            "edition_count": self.edition_count,
            "isbn_10": self.isbn_10,
            "isbn_13": self.isbn_13,
            "canonical_url": self.canonical_url,
            "thumbnail": self.thumbnail,
            "popularity_score": self.popularity_score,
        }

    def dedupe_key(self) -> str:
        if self.isbn_13:
            return f"isbn13:{self.isbn_13.replace('-', '').strip()}"
        if self.isbn_10:
            return f"isbn10:{self.isbn_10.replace('-', '').strip()}"

        normalized_title = "".join(ch for ch in (self.title or "").lower() if ch.isalnum())
        primary_author = (self.authors[0] if self.authors else "").lower()
        normalized_author = "".join(ch for ch in primary_author if ch.isalnum())
        return f"title_author:{normalized_title}:{normalized_author}"
