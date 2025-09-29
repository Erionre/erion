(function () {
  const BOOKS_URL = '/output/books.json';
  const statusEl = document.getElementById('status');
  const listEl = document.getElementById('books');
  const reloadBtn = document.getElementById('reloadBtn');

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text || '';
  }

  function openInNewTab(url) {
    if (!url) return;
    window.open(url, '_blank', 'noopener,noreferrer');
  }

  function buildGutenbergSearchUrl(title, authors) {
    const q = [title || '', (authors && authors[0]) || ''].filter(Boolean).join(' ');
    return 'https://www.gutenberg.org/ebooks/search/?query=' + encodeURIComponent(q);
  }

  function renderBooks(books) {
    listEl.innerHTML = '';
    if (!books || books.length === 0) {
      const empty = document.createElement('div');
      empty.textContent = 'No books found.';
      empty.style.color = '#9aa3b2';
      listEl.appendChild(empty);
      return;
    }

    for (const b of books) {
      const card = document.createElement('article');
      card.className = 'book';

      const img = document.createElement('img');
      img.alt = 'Cover';
      img.loading = 'lazy';
      img.src = b.thumbnail || 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="72" height="110"><rect width="100%" height="100%" fill="%230e1224"/></svg>';

      const meta = document.createElement('div');
      meta.className = 'meta';

      const title = document.createElement('h3');
      title.className = 'title';
      title.textContent = b.title || '(Untitled)';

      const authors = document.createElement('div');
      authors.className = 'authors';
      authors.textContent = (b.authors && b.authors.length) ? b.authors.join(', ') : 'Unknown author';

      const cats = document.createElement('div');
      cats.className = 'cats';
      cats.textContent = (b.categories && b.categories.length) ? b.categories.join(', ') : '';

      const score = document.createElement('div');
      score.className = 'score';
      const parts = [];
      if (b.popularity_score != null) parts.push('Score ' + b.popularity_score.toFixed(1));
      if (b.average_rating != null) parts.push('Rating ' + b.average_rating);
      if (b.ratings_count != null) parts.push('Ratings ' + b.ratings_count);
      if (b.edition_count != null) parts.push('Editions ' + b.edition_count);
      score.textContent = parts.join(' • ');

      const buttons = document.createElement('div');
      buttons.className = 'buttons';

      // Details button
      const detailsBtn = document.createElement('button');
      detailsBtn.type = 'button';
      detailsBtn.textContent = 'Details';
      detailsBtn.addEventListener('click', () => {
        const url = b.canonical_url || (b.source === 'google' ? ('https://books.google.com/books?id=' + encodeURIComponent(b.source_id || '')) : (b.source === 'openlibrary' ? ('https://openlibrary.org/works/' + encodeURIComponent(b.source_id || '')) : ''));
        if (url) openInNewTab(url);
      });

      // Free copy search button (Project Gutenberg)
      const freeBtn = document.createElement('button');
      freeBtn.type = 'button';
      freeBtn.textContent = 'Free copy';
      freeBtn.addEventListener('click', () => {
        const url = buildGutenbergSearchUrl(b.title, b.authors);
        openInNewTab(url);
      });

      // OpenLibrary button (if applicable)
      const olBtn = document.createElement('a');
      olBtn.textContent = 'OpenLibrary';
      const olUrl = (b.source === 'openlibrary') ? (b.canonical_url || ('https://openlibrary.org/works/' + encodeURIComponent(b.source_id || ''))) : null;
      if (olUrl) {
        olBtn.href = olUrl;
        olBtn.target = '_blank';
        olBtn.rel = 'noopener noreferrer';
      } else {
        olBtn.href = '#';
        olBtn.addEventListener('click', (e) => e.preventDefault());
        olBtn.style.opacity = '0.6';
        olBtn.style.pointerEvents = 'none';
      }

      buttons.appendChild(detailsBtn);
      buttons.appendChild(freeBtn);
      buttons.appendChild(olBtn);

      meta.appendChild(title);
      meta.appendChild(authors);
      meta.appendChild(cats);
      meta.appendChild(score);
      meta.appendChild(buttons);

      card.appendChild(img);
      card.appendChild(meta);
      listEl.appendChild(card);
    }
  }

  async function loadBooks() {
    try {
      setStatus('Loading books...');
      const res = await fetch(BOOKS_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      const books = Array.isArray(data) ? data : [];
      // Sort by popularity_score desc if present
      books.sort((a, b) => (b.popularity_score || 0) - (a.popularity_score || 0));
      renderBooks(books);
      setStatus('Loaded ' + books.length + ' books.');
    } catch (err) {
      console.error(err);
      setStatus('Failed to load books. Make sure /output/books.json exists.');
      renderBooks([]);
    }
  }

  if (reloadBtn) reloadBtn.addEventListener('click', loadBooks);
  // Auto-load on page ready
  loadBooks();
})();
