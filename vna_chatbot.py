from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import Iterable, Any, cast

import yaml
from dotenv import load_dotenv
from langsmith import Client
try:
    # try to import traceable and specific errors
    from langsmith import traceable
    from langsmith.utils import LangSmithError
    from requests import HTTPError
except Exception:
    traceable = None
    LangSmithError = Exception
    HTTPError = Exception


from typing import Any, cast


def safe_traceable(**kwargs):
    """Wrap LangSmith's traceable decorator to avoid raising on LangSmith failures.

    If `traceable` is unavailable or raises (e.g., 403 Forbidden), this
    decorator will call the wrapped function directly and print a brief warning.
    """
    ts = traceable
    if ts is None:
        def _noop(fn):
            return fn

        return _noop

    def _decorator(fn):
        wrapped = ts(**kwargs)(fn)

        def _safe(*args, **kw):
            try:
                return wrapped(*args, **kw)
            except Exception as exc:  # catch LangSmith/HTTP errors and fallback
                try:
                    msg = str(exc)
                except Exception:
                    msg = repr(exc)
                print(f"[langsmith-warning] tracing failed: {msg}; continuing without tracing")
                # attempt to run original function without the trace wrapper
                return fn(*args, **kw)

        return _safe

    return _decorator
from openai import OpenAI


DEFAULT_CONFIG_PATH = Path("config/chatbot.yaml")

STOPWORDS = {
    "và",
    "với",
    "của",
    "cho",
    "là",
    "theo",
    "trên",
    "trong",
    "một",
    "các",
    "được",
    "điều",
    "kiện",
    "vận",
    "chuyển",
    "thông",
    "tin",
    "điều lệ",
    "hành khách",
}


@dataclass
class ChatbotConfig:
    provider: str
    model: str
    temperature: float
    top_k: int
    data_path: str
    langsmith: dict
    ragas: dict


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> ChatbotConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ChatbotConfig(
        provider=raw.get("provider", "openai"),
        model=raw.get("model", "gpt-4o-mini"),
        temperature=float(raw.get("temperature", 0.2)),
        top_k=int(raw.get("top_k", 4)),
        data_path=raw.get("data_path", "data/vietnamairlines_public_policies.json"),
        langsmith=raw.get("langsmith", {}),
        ragas=raw.get("ragas", {}),
    )


def load_pages(data_path: str) -> list[dict]:
    return json.loads(Path(data_path).read_text(encoding="utf-8"))


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[\wÀ-ỹ]+", text.lower())
        if len(token) > 1 and token not in STOPWORDS
    }


def score_page(question_tokens: set[str], page: dict) -> int:
    title_tokens = tokenize(page.get("title", ""))
    body_tokens = tokenize(page.get("body_text", ""))
    slug_tokens = tokenize(page.get("url", ""))
    link_tokens = tokenize(" ".join(link.get("text", "") for link in page.get("links", [])))

    title_overlap = len(question_tokens & title_tokens)
    slug_overlap = len(question_tokens & slug_tokens)
    body_overlap = len(question_tokens & body_tokens)
    link_overlap = len(question_tokens & link_tokens)

    exact_bonus = 0
    normalized_query = " ".join(sorted(question_tokens))
    normalized_title = " ".join(sorted(title_tokens))
    if normalized_query and normalized_query in normalized_title:
        exact_bonus = 10

    return (title_overlap * 8) + (slug_overlap * 12) + body_overlap + (link_overlap * 2) + exact_bonus


def retrieve_pages(question: str, pages: list[dict], top_k: int = 4) -> list[dict]:
    question_tokens = tokenize(question)
    ranked = sorted(pages, key=lambda page: score_page(question_tokens, page), reverse=True)
    return ranked[:top_k]


def build_context(pages: Iterable[dict]) -> str:
    chunks: list[str] = []
    for page in pages:
        body = page.get("body_text") or page.get("body_markdown") or ""
        excerpt = body[:4000]
        chunks.append(
            f"[Nguồn] {page.get('title')}\nURL: {page.get('url')}\nNội dung trích:\n{excerpt}"
        )
    return "\n\n---\n\n".join(chunks)


def build_messages(question: str, context: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "Bạn là chatbot nội bộ cho dữ liệu chính sách Vietnam Airlines. "
                "Chỉ trả lời dựa trên ngữ cảnh được cung cấp. "
                "Nếu thiếu thông tin, hãy nói rõ là chưa đủ dữ liệu và gợi ý nguồn liên quan. "
                "Trả lời bằng tiếng Việt ngắn gọn, có thể liệt kê nguồn URL."
            ),
        },
        {
            "role": "user",
            "content": f"Câu hỏi: {question}\n\nNgữ cảnh:\n{context}",
        },
    ]


@safe_traceable(name="vna_chatbot_answer")
def answer_question(question: str, config: ChatbotConfig, pages: list[dict]) -> dict:
    sources = retrieve_pages(question, pages, top_k=config.top_k)
    context = build_context(sources)

    client = OpenAI()
    messages_payload = cast(Iterable[Any], build_messages(question, context))
    response = client.chat.completions.create(
        model=config.model,
        temperature=config.temperature,
        messages=messages_payload,
    )
    answer = response.choices[0].message.content or ""
    return {
        "answer": answer,
        "sources": [
            {"title": page.get("title"), "url": page.get("url"), "depth": page.get("depth", 0)}
            for page in sources
        ],
    }


def interactive_chat(config: ChatbotConfig) -> None:
    pages = load_pages(config.data_path)
    print(f"Loaded {len(pages)} policy pages from {config.data_path}")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Bạn: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            break

        result = answer_question(question, config, pages)
        print(f"\nChatbot: {result['answer']}\n")
        print("Nguồn:")
        for source in result["sources"]:
            print(f"- {source['title']} | {source['url']}")
        print()


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Vietnam Airlines policy chatbot")
    parser.add_argument("--question", help="Ask a single question and exit")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to chatbot config")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    pages = load_pages(config.data_path)

    if args.question:
        result = answer_question(args.question, config, pages)
        print(result["answer"])
        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source['title']} | {source['url']}")
        return

    interactive_chat(config)


if __name__ == "__main__":
    main()
