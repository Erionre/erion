import os
from typing import Dict, Iterable, List

from ..types import Book
from ..utils.http import get_json


BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def _parse_google_book(item: Dict[str, object], genre: str) -> Book:
    volume_info = item.get("volumeInfo", {}) if isinstance(item, dict) else {}
    industry_ids = volume_info.get("industryIdentifiers", []) if isinstance(volume_info, dict) else []
    id_map = {i.get("type"): i.get("identifier") for i in industry_ids if isinstance(i, dict)}

    def parse_year(published_date: str) -> int | None:
        if not isinstance(published_date, str):
            return None
        parts = published_date.split("-")
        try:
            return int(parts[0])
        except Exception:
            return None

    access_info = item.get("accessInfo", {}) if isinstance(item, dict) else {}
    epub = access_info.get("epub", {}) if isinstance(access_info, dict) else {}
    pdf = access_info.get("pdf", {}) if isinstance(access_info, dict) else {}
    web_reader_link = access_info.get("webReaderLink") if isinstance(access_info, dict) else None

    preview_url = volume_info.get("previewLink") if isinstance(volume_info, dict) else None
    read_url = None
    if isinstance(epub, dict) and epub.get("isAvailable") and epub.get("downloadLink"):
        read_url = epub.get("downloadLink")
    elif isinstance(pdf, dict) and pdf.get("isAvailable") and pdf.get("downloadLink"):
        read_url = pdf.get("downloadLink")
    elif web_reader_link:
        read_url = web_reader_link

    return Book(
        source="google",
        source_id=str(item.get("id")),
        title=str(volume_info.get("title") or "").strip(),
        authors=[a for a in (volume_info.get("authors") or []) if isinstance(a, str)],
        description=str(volume_info.get("description") or "") or None,
        categories=[genre] + [c for c in (volume_info.get("categories") or []) if isinstance(c, str)],
        published_year=parse_year(volume_info.get("publishedDate")),
        average_rating=volume_info.get("averageRating"),
        ratings_count=volume_info.get("ratingsCount"),
        isbn_10=id_map.get("ISBN_10"),
        isbn_13=id_map.get("ISBN_13"),
        canonical_url=volume_info.get("infoLink"),
        thumbnail=(volume_info.get("imageLinks") or {}).get("thumbnail"),
        preview_url=preview_url,
        read_url=read_url,
    )


async def fetch_google_books_for_genre(genre: str, limit: int = 100) -> List[Book]:
    api_key = os.getenv("GOOGLE_API_KEY")
    books: List[Book] = []
    page_size = 40
    start_index = 0

    while len(books) < limit:
        remaining = limit - len(books)
        max_results = page_size if remaining > page_size else remaining
        params: Dict[str, object] = {
            "q": f"subject:{genre}",
            "orderBy": "relevance",
            "printType": "books",
            "langRestrict": "en",
            "maxResults": max_results,
            "startIndex": start_index,
        }
        if api_key:
            params["key"] = api_key

        data = await get_json(BASE_URL, params=params)
        items = data.get("items") or []
        if not items:
            break

        for item in items:
            try:
                books.append(_parse_google_book(item, genre))
            except Exception:
                continue

        start_index += len(items)
        if len(items) < max_results:
            break

    return books


async def fetch_google_books(genres: Iterable[str], limit_per_genre: int = 100) -> List[Book]:
    all_books: List[Book] = []
    for genre in genres:
        genre = str(genre).strip()
        if not genre:
            continue
        books = await fetch_google_books_for_genre(genre, limit=limit_per_genre)
        all_books.extend(books)
    return all_books
