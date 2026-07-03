# Local publication copies

This directory is for local-only downloaded copies of linked papers and reference pages.

Article PDFs are vendored in [`files/`](files/) for research convenience (see the list in the top-level `README.md`); copyright remains with the original authors and publishers. Non-PDF reference pages (HTML) and the download manifest are not committed.

Run the downloader to (re)populate `publications/files/` on your own machine:

```bash
python3 tools/download_publications.py
```

The script reads `bibliography/articles.yaml`, downloads arXiv and direct PDF links as PDFs, uses `download_url` overrides where a public source is easier to fetch than the canonical publisher URL, saves other reference pages as HTML, and writes a local `publications/download-manifest.json` file with status, source URL, local filename, content type, and SHA-256 hash when available.

Committed: the `*.pdf` files in `files/`. Ignored by git: HTML pages, JSON, and `publications/download-manifest.json`.
