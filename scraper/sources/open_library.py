from typing import Dict, Iterable, List

from ..types import Book
from ..utils.http import get_json


SUBJECT_BASE = "https://openlibrary.org/subjects/{subject}.json"


def _parse_open_library_work(work: Dict[str, object], subject: str) -> Book:
    key = str(work.get("key") or "").strip("/")
    work_id = key.split("/")[-1] if key else ""
    title = str(work.get("title") or "").strip()
    authors = []
    for a in work.get("authors") or []:
        name = a.get("name") if isinstance(a, dict) else None
        if isinstance(name, str):
            authors.append(name)

    description_val = work.get("description")
    if isinstance(description_val, dict):
        description = description_val.get("value")
    else:
        description = description_val
    if not isinstance(description, str):
        description = None

    published_year = work.get("first_publish_year")
    if not isinstance(published_year, int):
        published_year = None

    edition_count = work.get("edition_count")
    if not isinstance(edition_count, int):
        edition_count = None

    cover_id = work.get("cover_id")
    thumbnail = None
    if isinstance(cover_id, int):
        thumbnail = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

    read_url = None
    # Open Library often provides readable editions; link to work page for reading/borrowing.
    if key:
        read_url = f"https://openlibrary.org/{key}"

    return Book(
        source="openlibrary",
        source_id=work_id,
        title=title,
        authors=authors,
        description=description,
        categories=[subject],
        published_year=published_year,
        edition_count=edition_count,
        canonical_url=f"https://openlibrary.org/{key}" if key else None,
        thumbnail=thumbnail,
        preview_url=f"https://openlibrary.org/{key}" if key else None,
        read_url=read_url,
    )


async def fetch_open_library_for_subject(subject: str, limit: int = 100) -> List[Book]:
    url = SUBJECT_BASE.format(subject=subject.replace(" ", "_").lower())
    books: List[Book] = []
    offset = 0
    page_size = 100

    while len(books) < limit:
        remaining = limit - len(books)
        limit_param = page_size if remaining > page_size else remaining
        params: Dict[str, object] = {
            "limit": limit_param,
            "offset": offset,
        }
        data = await get_json(url, params=params)
        works = data.get("works") or []
        if not works:
            break
        for w in works:
            try:
                books.append(_parse_open_library_work(w, subject))
            except Exception:
                continue
        offset += len(works)
        if len(works) < limit_param:
            break

    return books


async def fetch_open_library(subjects: Iterable[str], limit_per_subject: int = 100) -> List[Book]:
    all_books: List[Book] = []
    for subject in subjects:
        subject = str(subject).strip()
        if not subject:
            continue
        books = await fetch_open_library_for_subject(subject, limit=limit_per_subject)
        all_books.extend(books)
    return all_books
