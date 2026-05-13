from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from vna_chatbot import load_config, load_pages, answer_question


APP_TITLE = "VNA Policy Chatbot"
ASSETS_DIR = Path("assets")
DEFAULT_CONFIG = Path("config/chatbot.yaml")


def load_svg(name: str) -> str:
    path = ASSETS_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


CSS = """
/* Vietnam Airlines-like colors and clean layout */
.va-header { display:flex; align-items:center; gap:16px; }
.va-title { font-size:24px; color:#002663; font-weight:700; }
.va-sub { color:#4b5563; }
.chat-bubble { background:#f1f5f9; padding:12px; border-radius:8px; margin-bottom:8px; }
.chat-bubble.user { background:#e6f0ff; text-align:right; }
.source-link { font-size:12px; color:#1e40af; }
.app-container { padding: 12px; }
"""


def render_header(svg: str | None) -> None:
    cols = st.columns([1, 6])
    with cols[0]:
        if svg:
            st.markdown(svg, unsafe_allow_html=True)
        else:
            st.write("")
    with cols[1]:
        st.markdown(f'<div class="va-title">{APP_TITLE}</div>', unsafe_allow_html=True)
        st.markdown('<div class="va-sub">Trả lời dựa trên dữ liệu chính sách Vietnam Airlines</div>', unsafe_allow_html=True)


def init_session() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []


def show_chat() -> None:
    for item in st.session_state.history:
        role = item.get("role")
        text = item.get("text")
        if role == "user":
            st.markdown(f'<div class="chat-bubble user">{text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble">{text}</div>', unsafe_allow_html=True)
            sources = item.get("sources") or []
            if sources:
                for s in sources:
                    title = s.get("title") or s.get("url")
                    url = s.get("url")
                    st.markdown(f'<div class="source-link">• <a href="{url}" target="_blank">{title}</a></div>', unsafe_allow_html=True)


def main() -> None:
    load_dotenv()
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

    svg = load_svg("airplane.svg")
    render_header(svg)

    try:
        config = load_config(DEFAULT_CONFIG)
    except Exception:
        config = load_config()

    try:
        pages = load_pages(config.data_path)
    except Exception:
        pages = []

    init_session()

    left, right = st.columns([3, 1])
    with left:
        show_chat()
        question = st.text_area("Bạn:", height=80, key="input_box")
        send = st.button("Gửi")
        if send and question.strip():
            st.session_state.history.append({"role": "user", "text": question})
            with st.spinner("Đang truy vấn..."):
                try:
                    result = answer_question(question, config, pages)
                    answer = result.get("answer", "")
                    sources = result.get("sources", [])
                except Exception as exc:
                    answer = f"Lỗi khi trả lời: {exc}"
                    sources = []

            st.session_state.history.append({"role": "assistant", "text": answer, "sources": sources})
            st.rerun()

    with right:
        st.markdown("**Thông tin**")
        st.write("Số trang policy đã load: ", len(pages))
        st.markdown("---")
        st.caption("Sử dụng môi trường và keys để gọi LLM; nếu không, chatbot trả fallback text.")


if __name__ == "__main__":
    main()
