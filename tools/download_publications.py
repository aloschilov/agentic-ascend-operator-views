#!/usr/bin/env python3
"""Download local-only copies of the linked publication sources.

The repository keeps only links and notes under version control. This helper
creates local files for personal offline reading and records what happened in a
machine-readable manifest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIBLIOGRAPHY = ROOT / "bibliography" / "articles.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "publications" / "files"
DEFAULT_MANIFEST = ROOT / "publications" / "download-manifest.json"


@dataclass(frozen=True)
class Source:
    category: str
    id: str
    title: str
    url: str
    status: str | None = None
    download_url: str | None = None
    download_kind: str | None = None


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_bibliography(path: Path) -> list[Source]:
    """Parse the small flat YAML subset used by bibliography/articles.yaml."""
    sources: list[Source] = []
    category: str | None = None
    current: dict[str, Any] | None = None

    def finish_current() -> None:
        if not current:
            return
        required = {"id", "title", "url"}
        missing = sorted(required - current.keys())
        if missing:
            raise ValueError(f"Missing {', '.join(missing)} in bibliography entry: {current!r}")
        sources.append(
            Source(
                category=str(current.get("category") or "uncategorized"),
                id=str(current["id"]),
                title=str(current["title"]),
                url=str(current["url"]),
                status=current.get("status"),
                download_url=current.get("download_url"),
                download_kind=current.get("download_kind"),
            )
        )

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        stripped = raw_line.strip()
        if raw_line.startswith("  ") and not raw_line.startswith("    ") and stripped.endswith(":"):
            finish_current()
            current = None
            category = stripped[:-1]
            continue

        if stripped.startswith("- id:"):
            finish_current()
            current = {"category": category or "uncategorized", "id": parse_scalar(stripped.split(":", 1)[1])}
            continue

        if current is not None:
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
            if match:
                key, value = match.groups()
                if key in {"title", "url", "status", "download_url", "download_kind"}:
                    current[key] = parse_scalar(value)

    finish_current()
    return sources


def arxiv_pdf_url(url: str) -> str | None:
    parsed = urlparse(url)
    if not parsed.netloc.endswith("arxiv.org"):
        return None

    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2 or parts[0] not in {"abs", "pdf"}:
        return None

    arxiv_id = parts[1]
    if arxiv_id.endswith(".pdf"):
        arxiv_id = arxiv_id[:-4]
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def target_for(source: Source) -> tuple[str, str, str]:
    selected_url = source.download_url or source.url
    selected_kind = source.download_kind

    pdf_url = None if source.download_url else arxiv_pdf_url(source.url)
    if pdf_url:
        return pdf_url, f"{source.id}.pdf", "pdf"

    if selected_kind == "pdf":
        return selected_url, f"{source.id}.pdf", "pdf"
    if selected_kind == "metadata":
        return selected_url, f"{source.id}.json", "metadata"

    parsed = urlparse(selected_url)
    path = parsed.path.lower()
    if path.endswith(".pdf"):
        return selected_url, f"{source.id}.pdf", "pdf"
    if path.endswith(".json"):
        return selected_url, f"{source.id}.json", "metadata"

    return selected_url, f"{source.id}.html", "html"


def download(url: str, timeout: int) -> tuple[bytes, str, str, int]:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; local-publication-downloader/1.0)",
            "Accept": "application/pdf,text/html,application/xhtml+xml,*/*;q=0.8",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type", "")
            final_url = response.geturl()
            status_code = getattr(response, "status", 200)
        return data, content_type, final_url, status_code
    except (HTTPError, URLError, TimeoutError):
        if shutil.which("curl"):
            return download_with_curl(url, timeout)
        raise


def download_with_curl(url: str, timeout: int) -> tuple[bytes, str, str, int]:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    try:
        completed = subprocess.run(
            [
                "curl",
                "-L",
                "--fail",
                "--silent",
                "--show-error",
                "--max-time",
                str(timeout),
                "--user-agent",
                "Mozilla/5.0 (compatible; local-publication-downloader/1.0)",
                "--header",
                "Accept: application/pdf,text/html,application/xhtml+xml,*/*;q=0.8",
                "--output",
                str(temp_path),
                "--write-out",
                "%{http_code}\t%{content_type}\t%{url_effective}",
                url,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            message = completed.stderr.strip() or completed.stdout.strip() or f"curl exited {completed.returncode}"
            raise RuntimeError(message)

        metadata = completed.stdout.strip().split("\t", 2)
        status_code = int(metadata[0]) if metadata and metadata[0].isdigit() else 200
        content_type = metadata[1] if len(metadata) > 1 else ""
        final_url = metadata[2] if len(metadata) > 2 else url
        return temp_path.read_bytes(), content_type, final_url, status_code
    finally:
        temp_path.unlink(missing_ok=True)


def write_manifest(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_bibliography": str(DEFAULT_BIBLIOGRAPHY.relative_to(ROOT)),
        "download_dir": str(DEFAULT_OUTPUT_DIR.relative_to(ROOT)),
        "records": records,
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bibliography", type=Path, default=DEFAULT_BIBLIOGRAPHY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--force", action="store_true", help="redownload files that already exist")
    args = parser.parse_args()

    sources = parse_bibliography(args.bibliography)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    ok_count = 0

    for source in sources:
        download_url, filename, kind = target_for(source)
        local_path = args.output_dir / filename
        record: dict[str, Any] = {
            "id": source.id,
            "title": source.title,
            "category": source.category,
            "status": source.status,
            "source_url": source.url,
            "download_url": download_url,
            "local_path": str(local_path.relative_to(ROOT)),
            "kind": kind,
        }
        if source.download_url:
            record["canonical_url"] = source.url

        if local_path.exists() and local_path.stat().st_size > 0 and not args.force:
            data = local_path.read_bytes()
            record.update(
                {
                    "result": "skipped_existing",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
            ok_count += 1
            records.append(record)
            print(f"ok existing  {source.id} -> {local_path}")
            continue

        try:
            data, content_type, final_url, status_code = download(download_url, args.timeout)
            if not data:
                raise ValueError("empty response body")
            local_path.write_bytes(data)
            record.update(
                {
                    "result": "downloaded",
                    "http_status": status_code,
                    "final_url": final_url,
                    "content_type": content_type,
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
            ok_count += 1
            print(f"ok          {source.id} -> {local_path}")
        except (HTTPError, URLError, TimeoutError, RuntimeError, ValueError, OSError) as exc:
            record.update({"result": "failed", "error": str(exc)})
            print(f"failed      {source.id}: {exc}", file=sys.stderr)

        records.append(record)

    write_manifest(args.manifest, records)
    print(f"\nDownloaded or found {ok_count}/{len(records)} sources.")
    print(f"Manifest: {args.manifest}")
    return 0 if ok_count == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
