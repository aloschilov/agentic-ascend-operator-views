# Publication copies

This directory contains vendored publications and local offline downloads.

Article PDFs are vendored in [`files/`](files/) for research convenience (see the list in the top-level `README.md`); copyright remains with the original authors and publishers. Non-PDF reference pages (HTML) and the download manifest are not committed.

Run the downloader to (re)populate `publications/files/` on your own machine:

```bash
python3 tools/download_publications.py
```

The script reads `bibliography/articles.yaml`, downloads arXiv and direct PDF links as PDFs, uses `download_url` overrides where a public source is easier to fetch than the canonical publisher URL, saves other reference pages as HTML, and writes a local `publications/download-manifest.json` file with status, source URL, local filename, content type, and SHA-256 hash when available.

PDFs permitted for redistribution can be committed with attribution. Check each new source's licence; an arXiv download link alone does not establish republication permission. HTML pages, JSON, and `publications/download-manifest.json` are ignored.

The two September additions have pinned versions and SHA-256 values in `bibliography/articles.yaml`. Prism is vendored unchanged under CC BY 4.0. The spatiotemporal-composability PDF remains local-only and is explicitly ignored; its listed grant is to arXiv. See [attribution and scope](../notes/08-perspectives-and-composability.md).
