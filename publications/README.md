# Local publication copies

This directory is for local-only downloaded copies of linked papers and reference pages.

The repository intentionally does not vendor full PDFs or copyrighted article text. Run the downloader to populate `publications/files/` on your own machine:

```bash
python3 tools/download_publications.py
```

The script reads `bibliography/articles.yaml`, downloads arXiv and direct PDF links as PDFs, uses `download_url` overrides where a public source is easier to fetch than the canonical publisher URL, saves other reference pages as HTML, and writes a local `publications/download-manifest.json` file with status, source URL, local filename, content type, and SHA-256 hash when available.

Generated downloads and the local manifest are ignored by git.
