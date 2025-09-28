import argparse
import asyncio
from typing import List

from scraper.aggregate import normalize_and_rank
from scraper.exporters import export_csv, export_json
from scraper.sources.google_books import fetch_google_books
from scraper.sources.open_library import fetch_open_library
from scraper.types import Book


async def run_scrape(
    genres: List[str],
    sources: List[str],
    limit_per_source: int,
    top_n: int | None,
) -> List[Book]:
    collected: List[Book] = []

    if "google" in sources:
        gb = await fetch_google_books(genres, limit_per_genre=limit_per_source)
        collected.extend(gb)

    if "openlibrary" in sources:
        ol = await fetch_open_library(genres, limit_per_subject=limit_per_source)
        collected.extend(ol)

    ranked = normalize_and_rank(collected)
    if top_n is not None:
        ranked = ranked[:top_n]
    return ranked


def main() -> None:
    parser = argparse.ArgumentParser(description="Popular books scraper")
    parser.add_argument(
        "--genres",
        nargs="+",
        default=["fantasy", "romance", "thriller"],
        help="Genres/subjects to fetch",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        default=["google", "openlibrary"],
        choices=["google", "openlibrary"],
        help="Sources to include",
    )
    parser.add_argument(
        "--limit-per-source",
        type=int,
        default=100,
        help="Max per source per genre",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Keep only top N after ranking",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="output/books.json",
        help="Path to JSON output",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="output/books.csv",
        help="Path to CSV output",
    )
    args = parser.parse_args()

    books = asyncio.run(
        run_scrape(
            genres=args.genres,
            sources=args.sources,
            limit_per_source=args.limit_per_source,
            top_n=args.top,
        )
    )

    export_json(books, args.output_json)
    export_csv(books, args.output_csv)
    print(f"Wrote {len(books)} books to {args.output_json} and {args.output_csv}")


if __name__ == "__main__":
    main()
