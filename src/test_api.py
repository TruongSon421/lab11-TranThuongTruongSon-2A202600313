"""
Quick API connectivity test for Gemini and OpenAI.

Usage:
    python src/test_api.py
"""
from __future__ import annotations

import os
from pathlib import Path


def _load_env_file() -> None:
    """Load environment variables from src/.env."""
    env_path = Path(__file__).with_name(".env")
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_path, override=False)
        return
    except Exception:
        # Fallback parser when python-dotenv is not installed yet.
        if not env_path.exists():
            return

        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def test_gemini_api() -> bool:
    """Return True when Gemini API call succeeds."""
    try:
        from google import genai
    except Exception:
        print("[GEMINI] Missing package: google-genai")
        return False

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[GEMINI] Missing GOOGLE_API_KEY")
        return False

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="Reply with exactly: Gemini API OK",
        )
        print(f"[GEMINI] Success: {response.text}")
        return True
    except Exception as exc:
        print(f"[GEMINI] Failed: {exc}")
        return False


def test_openai_api() -> bool:
    """Return True when OpenAI API call succeeds."""
    try:
        from openai import OpenAI
    except Exception:
        print("[OPENAI] Missing package: openai")
        return False

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[OPENAI] Missing OPENAI_API_KEY")
        return False

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply with exactly: OpenAI API OK"}],
            max_tokens=20,
        )
        content = (response.choices[0].message.content or "").strip()
        print(f"[OPENAI] Success: {content}")
        return True
    except Exception as exc:
        print(f"[OPENAI] Failed: {exc}")
        return False


def main() -> None:
    _load_env_file()
    print("=== API TEST START ===")

    gemini_ok = test_gemini_api()
    openai_ok = test_openai_api()

    print("=== API TEST RESULT ===")
    print(f"Gemini: {'PASS' if gemini_ok else 'FAIL'}")
    print(f"OpenAI: {'PASS' if openai_ok else 'FAIL'}")


if __name__ == "__main__":
    main()
