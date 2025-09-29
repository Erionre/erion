## Book Popularity Scraper (Fantasy, Romance, Thriller)

This project scrapes popular books in the genres of fantasy, romance, and thriller using public APIs (Google Books and Open Library), normalizes and deduplicates the results, ranks them by a composite popularity score, and exports to JSON and CSV.

### Features
- Fetches from Google Books and Open Library
- Supports multiple genres at once
- Normalizes and deduplicates entries (prefer ISBN-13, then title+author)
- Popularity scoring combines ratings, ratings count, and edition count
- Exports JSON and CSV with ranking

### Requirements
- Python 3.9+
- Dependencies in `requirements.txt`

### Install
```bash
pip install -r requirements.txt
```

### Usage
```bash
python scrape.py \
  --genres fantasy romance thriller \
  --sources google openlibrary \
  --limit-per-source 100 \
  --output-json output/books.json \
  --output-csv output/books.csv
```

Arguments:
- `--genres` (list): Genres to fetch. Default: `fantasy romance thriller`
- `--sources` (list): Sources to use. Choices: `google`, `openlibrary`. Default: both
- `--limit-per-source` (int): Max books per source per genre. Default: 100
- `--top` (int, optional): Keep top N after de-dup; if omitted, keep all
- `--output-json` (path): JSON output file. Default: `output/books.json`
- `--output-csv` (path): CSV output file. Default: `output/books.csv`

Environment variables:
- `GOOGLE_API_KEY` (optional): If set, used to increase Google Books quota and stability

### Notes
- This project uses public APIs and honors their usage terms. For high-volume or commercial use, obtain proper API keys and review each provider's terms.
- Popularity ranking is a heuristic combining available metrics; it is not an official list.

### View the Web UI
After generating `output/books.json`, you can open the static UI:

1. Ensure the file exists:
   ```bash
   ls -l output/books.json
   ```
2. Serve the `/workspace` folder with any static server (examples):
   ```bash
   # Python 3
   python3 -m http.server --directory /workspace 8080
   # Or BusyBox
   busybox httpd -f -p 8080 -h /workspace
   ```
3. Open the UI at `http://localhost:8080/web/`. The left sidebar includes a link to `Project Gutenberg` for legal free downloads. Each book card has:
   - **Details**: opens the source page (Google/OpenLibrary)
   - **Free copy**: searches Project Gutenberg by title/author
   - **OpenLibrary**: opens Open Library work page when available
# erion