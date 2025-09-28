from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable, List

from .types import Book


def compute_popularity_score(book: Book) -> float:
    rating = book.average_rating or 0.0
    ratings_count = float(book.ratings_count or 0)
    edition_weight = float(book.edition_count or 0) * 0.1
    base = rating * min(ratings_count, 10000) ** 0.5
    return base + edition_weight


def merge_books(primary: Book, secondary: Book) -> Book:
    authors = primary.authors or secondary.authors
    categories = list({*primary.categories, *secondary.categories})
    published_year = primary.published_year or secondary.published_year
    average_rating = primary.average_rating or secondary.average_rating
    ratings_count = primary.ratings_count or secondary.ratings_count
    edition_count = primary.edition_count or secondary.edition_count
    isbn_10 = primary.isbn_10 or secondary.isbn_10
    isbn_13 = primary.isbn_13 or secondary.isbn_13
    canonical_url = primary.canonical_url or secondary.canonical_url
    thumbnail = primary.thumbnail or secondary.thumbnail
    description = primary.description or secondary.description

    merged = replace(
        primary,
        authors=authors,
        categories=categories,
        published_year=published_year,
        average_rating=average_rating,
        ratings_count=ratings_count,
        edition_count=edition_count,
        isbn_10=isbn_10,
        isbn_13=isbn_13,
        canonical_url=canonical_url,
        thumbnail=thumbnail,
        description=description,
    )
    return merged


def normalize_and_rank(books: Iterable[Book]) -> List[Book]:
    by_key: Dict[str, Book] = {}
    for book in books:
        key = book.dedupe_key()
        if key in by_key:
            by_key[key] = merge_books(by_key[key], book)
        else:
            by_key[key] = book

    normalized: List[Book] = []
    for b in by_key.values():
        b.popularity_score = compute_popularity_score(b)
        normalized.append(b)

    normalized.sort(
        key=lambda b: (
            b.popularity_score or 0.0,
            (b.ratings_count or 0),
            (b.edition_count or 0),
        ),
        reverse=True,
    )
    return normalized
