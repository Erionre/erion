import csv
import json
from pathlib import Path
from typing import Iterable

from .types import Book


def export_json(books: Iterable[Book], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([b.to_dict() for b in books], f, ensure_ascii=False, indent=2)


def export_csv(books: Iterable[Book], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "title",
        "authors",
        "categories",
        "description",
        "published_year",
        "average_rating",
        "ratings_count",
        "edition_count",
        "isbn_10",
        "isbn_13",
        "source",
        "source_id",
        "canonical_url",
        "thumbnail",
        "popularity_score",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, b in enumerate(books, start=1):
            row = b.to_dict()
            row["rank"] = idx
            row["authors"] = ", ".join(b.authors)
            row["categories"] = ", ".join(b.categories)
            writer.writerow(row)
