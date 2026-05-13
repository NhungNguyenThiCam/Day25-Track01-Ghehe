from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


BASE_URL = "https://www.vietnamairlines.com"
OUTPUT_DIR = Path("data")

POLICY_URLS = [
    "/vn/vi/legal/privacy-policy",
    "/vn/vi/legal/terms-and-conditions",
    "/vn/vi/legal/conditions-of-carriage",
    "/vn/vi/legal/cookies-policy",
    "/vn/vi/legal/quy-che-hoat-dong-san-tmdt",
    "/vn/vi/legal/conditions-of-online-booking",
    "/vn/vi/legal/conditions-of-check-in-cancellation",
    "/vn/vi/legal/conditions-of-website-and-mobile-app-usage",
    "/vn/vi/support/customer-service-plan",
]


@dataclass
class PolicyPage:
    url: str
    title: str
    slug: str
    body_markdown: str
    body_text: str
    links: list[dict[str, str]]
    word_count: int
    scraped_at: str


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def fetch_html(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", "ignore")


def slugify_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] or "index"
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", slug).strip("-")
    return slug or "index"


def choose_content_container(soup: BeautifulSoup):
    title_node = soup.find("h1")
    title_text = clean_text(title_node.get_text(" ", strip=True)) if title_node else ""

    search_root = soup.find("main") or soup.body or soup
    candidate_grid = None
    node = title_node
    while node is not None:
        classes = node.get("class") or []
        if node.name == "div" and any(cls.startswith("aem-Grid") for cls in classes):
            candidate_grid = node
            break
        node = node.parent

    if candidate_grid is not None:
        candidates = candidate_grid.find_all(recursive=False)
    else:
        candidates = search_root.find_all(recursive=False)

    def score(candidate) -> tuple[int, int]:
        text = clean_text(candidate.get_text(" ", strip=True))
        classes = " ".join(candidate.get("class") or []).lower()
        bonus = 0
        if title_text and title_text.lower() in text.lower():
            bonus += 3000
        if any(token in classes for token in ("breadcrumb", "footer", "header", "experiencefragment")):
            bonus -= 10000
        return len(text) + bonus, len(classes)

    best = None
    best_score = (-1, -1)
    for candidate in candidates:
        candidate_score = score(candidate)
        if candidate_score > best_score:
            best = candidate
            best_score = candidate_score

    return best or search_root


def extract_markdown(container) -> str:
    for tag in container.select("script, style, noscript"):
        tag.decompose()

    lines: list[str] = []
    seen: set[str] = set()
    block_tags = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "th", "td", "blockquote", "figcaption"}

    for element in container.find_all(block_tags):
        text = clean_text(element.get_text(" ", strip=True))
        if not text:
            continue

        key = text.lower()
        if key in seen:
            continue
        seen.add(key)

        if element.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = min(int(element.name[1]), 6)
            prefix = "#" * level
            lines.append(f"{prefix} {text}")
        elif element.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    return "\n\n".join(lines).strip()


def extract_links(container, base_url: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for anchor in container.find_all("a", href=True):
        text = clean_text(anchor.get_text(" ", strip=True))
        href = urljoin(base_url, anchor["href"])
        key = (text.lower(), href)
        if not text or key in seen:
            continue
        seen.add(key)
        links.append({"text": text, "href": href})
    return links


def build_policy_page(url: str) -> PolicyPage:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    title_node = soup.find("h1")
    title = clean_text(title_node.get_text(" ", strip=True)) if title_node else clean_text((soup.title.string if soup.title else ""))
    container = choose_content_container(soup)
    markdown = extract_markdown(container)
    links = extract_links(container, url)
    body_text = clean_text(BeautifulSoup(markdown.replace("\n", " "), "html.parser").get_text(" ", strip=True))
    return PolicyPage(
        url=url,
        title=title,
        slug=slugify_url(url),
        body_markdown=markdown,
        body_text=body_text,
        links=links,
        word_count=len(body_text.split()),
        scraped_at=datetime.now(timezone.utc).isoformat(),
    )


def write_outputs(pages: list[PolicyPage]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "html").mkdir(parents=True, exist_ok=True)

    payload = [asdict(page) for page in pages]
    (OUTPUT_DIR / "vietnamairlines_public_policies.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_parts = ["# Vietnam Airlines public policy scrape", ""]
    for page in pages:
        md_parts.extend(
            [
                f"## {page.title}",
                f"URL: {page.url}",
                f"Slug: {page.slug}",
                f"Word count: {page.word_count}",
                "",
                page.body_markdown or "(No body extracted)",
                "",
            ]
        )
    (OUTPUT_DIR / "vietnamairlines_public_policies.md").write_text("\n".join(md_parts).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    pages = []
    for relative_url in POLICY_URLS:
        full_url = urljoin(BASE_URL, relative_url)
        pages.append(build_policy_page(full_url))

    write_outputs(pages)
    print(f"Saved {len(pages)} policy pages to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
