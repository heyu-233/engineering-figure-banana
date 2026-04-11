#!/usr/bin/env python3
"""Generate or edit images with the Gemini generateContent API."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path


OFFICIAL_BASE_URL = "https://generativelanguage.googleapis.com"
OFFICIAL_HOSTNAME = "generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_TIMEOUT = 120
DEFAULT_AUTH_MODE = "google"
HIGHRES_HINTS = ("2k", "highres", "high-res", "high resolution", "final export", "final-export", "final quality")


def load_figure_templates() -> dict:
    template_path = Path(__file__).resolve().parent.parent / "references" / "engineering-figure-templates.json"
    return json.loads(template_path.read_text(encoding="utf-8"))


def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))


def resolve_lang(raw_prompt: str, requested_lang: str | None) -> str:
    if requested_lang:
        return requested_lang
    return "zh" if contains_chinese(raw_prompt) else "en"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate or edit images with Gemini generateContent.")
    parser.add_argument("prompt", nargs="?", help="Prompt text or scientific background for shortcut modes.")
    parser.add_argument(
        "--prompt-file",
        help="Read prompt text or scientific background from a text or markdown file.",
    )
    parser.add_argument(
        "--figure-template",
        choices=tuple(load_figure_templates().keys()),
        help="Use a built-in engineering-paper figure template.",
    )
    parser.add_argument(
        "--materials-figure",
        choices=tuple(load_figure_templates().keys()),
        help="Backward-compatible alias for --figure-template.",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh"),
        default=None,
        help="Template output language for shortcut modes. If omitted, Chinese prompts default to zh and others default to en.",
    )
    parser.add_argument(
        "--style-note",
        help="Optional extra style constraint appended after a shortcut template.",
    )
    parser.add_argument(
        "--input-image",
        action="append",
        default=[],
        help="Input image path. Repeat to provide multiple reference images.",
    )
    parser.add_argument("--out-dir", default="./output/nanobanana", help="Output directory.")
    parser.add_argument("--prefix", default="nanobanana", help="Saved filename prefix.")
    parser.add_argument(
        "--base-url",
        default=os.getenv("NANOBANANA_BASE_URL"),
        help=f"Gemini-compatible base URL. Must be set explicitly, e.g. {OFFICIAL_BASE_URL}.",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--highres",
        action="store_true",
        help="Use the configured higher-resolution model for this request.",
    )
    parser.add_argument(
        "--auth-mode",
        choices=("google", "bearer"),
        default=os.getenv("NANOBANANA_AUTH_MODE", DEFAULT_AUTH_MODE),
        help="Auth header mode. 'google' uses X-goog-api-key, 'bearer' uses Authorization: Bearer.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("NANOBANANA_API_KEY"),
        help="API key. Defaults to NANOBANANA_API_KEY.",
    )
    parser.add_argument(
        "--api-key-file",
        default=os.getenv("NANOBANANA_API_KEY_FILE"),
        help="Path to a file containing the API key. Preferred when you do not want the key shown in the command line.",
    )
    parser.add_argument(
        "--aspect-ratio",
        help="Official Gemini image aspect ratio, e.g. 1:1, 16:9, 3:2.",
    )
    parser.add_argument(
        "--image-size",
        help="Official Gemini image size, e.g. 512, 1K, 2K, 4K.",
    )
    parser.add_argument(
        "--text-only",
        action="store_true",
        help="Request only text output.",
    )
    parser.add_argument(
        "--include-thoughts",
        action="store_true",
        help="Request returned thoughts when the provider supports it.",
    )
    parser.add_argument(
        "--thinking-level",
        choices=("minimal", "high", "Minimal", "High"),
        help="Gemini 3.1 Flash Image thinking level.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("NANOBANANA_TIMEOUT", str(DEFAULT_TIMEOUT))),
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the resolved final prompt and exit without calling the API.",
    )
    parser.add_argument(
        "--allow-third-party",
        action="store_true",
        help="Explicitly allow sending API keys and input files to a non-official Gemini-compatible provider.",
    )
    return parser


def resolve_base_url(args: argparse.Namespace) -> str:
    base_url = args.base_url
    if not base_url:
        raise SystemExit(
            "Missing base URL. Set NANOBANANA_BASE_URL or pass --base-url explicitly. "
            f"Official Google example: {OFFICIAL_BASE_URL}"
        )

    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit(f"Invalid base URL: {base_url}. Use an explicit https URL such as {OFFICIAL_BASE_URL}.")
    return base_url.rstrip("/")


def assert_endpoint_allowed(base_url: str, args: argparse.Namespace) -> None:
    hostname = urllib.parse.urlparse(base_url).hostname or ""
    allow_third_party = args.allow_third_party or os.getenv("NANOBANANA_ALLOW_THIRD_PARTY") == "1"
    if hostname != OFFICIAL_HOSTNAME and not allow_third_party:
        raise SystemExit(
            "Refusing to send API keys or user-provided files to a third-party Gemini-compatible provider. "
            "If you intend to use a non-official endpoint, set NANOBANANA_ALLOW_THIRD_PARTY=1 "
            "or pass --allow-third-party. "
            f"Official Google endpoint: {OFFICIAL_BASE_URL}"
        )


def load_input_images(image_paths: list[str]) -> list[dict]:
    return [file_to_inline_part(path_str) for path_str in image_paths]


def file_to_inline_part(path_str: str) -> dict:
    path = Path(path_str)
    if not path.is_file():
        raise SystemExit(f"Input image not found: {path}")
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "inlineData": {
            "mimeType": mime_type,
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def resolve_prompt(args: argparse.Namespace) -> str:
    raw_prompt = args.prompt
    if args.prompt_file:
        path = Path(args.prompt_file)
        if not path.is_file():
            raise SystemExit(f"Prompt file not found: {path}")
        raw_prompt = path.read_text(encoding="utf-8")

    figure_template = args.figure_template or args.materials_figure
    if figure_template:
        if not raw_prompt:
            raise SystemExit("Provide technical background as the positional prompt when using --figure-template.")
        template_lang = resolve_lang(raw_prompt, args.lang)
        template = load_figure_templates()[figure_template][template_lang]
        prompt = template.format(background=raw_prompt.strip())
        if args.style_note:
            prompt = f"{prompt}\n\nAdditional Style Requirement:\n{args.style_note}"
        return prompt

    if not raw_prompt:
        raise SystemExit("Missing prompt.")
    return raw_prompt


def collect_highres_hint_text(args: argparse.Namespace) -> str:
    parts = [args.prompt or "", args.style_note or "", args.model or ""]
    if args.prompt_file:
        path = Path(args.prompt_file)
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts).lower()


def should_use_highres_model(args: argparse.Namespace) -> bool:
    if args.highres:
        return True

    combined = collect_highres_hint_text(args)
    return any(hint in combined for hint in HIGHRES_HINTS)


def is_explicit_highres_request(args: argparse.Namespace) -> bool:
    if args.highres:
        return True
    combined = collect_highres_hint_text(args)
    return any(hint in combined for hint in HIGHRES_HINTS)


def resolve_model(args: argparse.Namespace) -> str:
    if args.model:
        return args.model

    default_model = os.getenv("NANOBANANA_DEFAULT_MODEL") or os.getenv("NANOBANANA_MODEL") or DEFAULT_MODEL
    highres_model = os.getenv("NANOBANANA_HIGHRES_MODEL")

    if should_use_highres_model(args):
        if highres_model:
            return highres_model
        raise SystemExit(
            "This request clearly asks for the higher-resolution model, but NANOBANANA_HIGHRES_MODEL is not configured. "
            "Generation has been stopped intentionally. Do not silently downgrade to the default model. "
            "Ask the human whether to keep retrying high-resolution generation or explicitly allow fallback."
        )
    return default_model


def resolve_api_key(args: argparse.Namespace) -> str:
    if args.api_key:
        return args.api_key
    if args.api_key_file:
        path = Path(args.api_key_file)
        if not path.is_file():
            raise SystemExit(f"API key file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    raise SystemExit("Missing API key. Set NANOBANANA_API_KEY, NANOBANANA_API_KEY_FILE, or pass --api-key.")


def build_payload(args: argparse.Namespace) -> dict:
    parts = [{"text": resolve_prompt(args)}]
    parts.extend(load_input_images(args.input_image))

    payload = {
        "contents": [
            {
                "parts": parts,
            }
        ]
    }

    generation_config: dict = {}
    generation_config["responseModalities"] = ["TEXT"] if args.text_only else ["TEXT", "IMAGE"]

    image_config: dict = {}
    if args.aspect_ratio:
        image_config["aspectRatio"] = args.aspect_ratio
    if args.image_size:
        image_config["imageSize"] = args.image_size
    if image_config:
        generation_config["imageConfig"] = image_config

    thinking_config: dict = {}
    if args.thinking_level:
        thinking_config["thinkingLevel"] = args.thinking_level
    if args.include_thoughts:
        thinking_config["includeThoughts"] = True
    if thinking_config:
        generation_config["thinkingConfig"] = thinking_config

    if generation_config:
        payload["generationConfig"] = generation_config

    return payload


def request_json(args: argparse.Namespace) -> dict:
    base_url = resolve_base_url(args)
    assert_endpoint_allowed(base_url, args)
    api_key = resolve_api_key(args)
    resolved_model = resolve_model(args)
    encoded_model = urllib.parse.quote(resolved_model, safe="")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    }
    if args.auth_mode == "bearer":
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        headers["X-goog-api-key"] = api_key

    request = urllib.request.Request(
        f"{base_url}/v1beta/models/{encoded_model}:generateContent",
        data=json.dumps(build_payload(args)).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 429:
            if is_explicit_highres_request(args):
                raise SystemExit(
                    "The higher-resolution request was rate limited (HTTP 429). Generation has been stopped intentionally. "
                    "Do not silently downgrade to the default model. Ask the human whether to retry high-resolution generation "
                    "or explicitly allow fallback."
                ) from exc
            raise SystemExit(
                "Upstream rate limited this request (HTTP 429). Wait a bit and retry."
            ) from exc
        if is_explicit_highres_request(args):
            raise SystemExit(
                f"High-resolution generation failed with HTTP {exc.code}. Generation has been stopped intentionally. "
                "Do not silently downgrade to the default model. Ask the human whether to retry high-resolution generation "
                f"or explicitly allow fallback. Response body: {body}"
            ) from exc
        raise SystemExit(f"Request failed with HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        if is_explicit_highres_request(args):
            raise SystemExit(
                f"High-resolution generation failed due to a network or upstream error: {exc.reason}. "
                "Generation has been stopped intentionally. Do not silently downgrade to the default model. "
                "Ask the human whether to retry or explicitly allow fallback."
            ) from exc
        raise SystemExit(f"Request failed: {exc.reason}") from exc


def save_parts(response_json: dict, out_dir: Path, prefix: str) -> list[str]:
    candidates = response_json.get("candidates") or []
    if not candidates:
        raise SystemExit(f"Unexpected response shape: {json.dumps(response_json, ensure_ascii=False)}")

    parts = ((candidates[0].get("content") or {}).get("parts")) or []
    if not parts:
        raise SystemExit(f"Unexpected response shape: {json.dumps(response_json, ensure_ascii=False)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    image_index = 0
    text_index = 0

    for part in parts:
        text = part.get("text")
        if text:
            text_index += 1
            path = out_dir / f"{prefix}-text-{text_index}.txt"
            path.write_text(text, encoding="utf-8")
            outputs.append(str(path))
            continue

        inline_data = part.get("inlineData") or part.get("inline_data")
        if not inline_data:
            continue

        image_index += 1
        mime_type = inline_data.get("mimeType") or inline_data.get("mime_type") or "image/png"
        extension = mimetypes.guess_extension(mime_type) or ".png"
        path = out_dir / f"{prefix}-{image_index}{extension}"
        path.write_bytes(base64.b64decode(inline_data["data"]))
        outputs.append(str(path))

    if not outputs:
        raise SystemExit(f"No text or image parts found: {json.dumps(response_json, ensure_ascii=False)}")
    return outputs


def main() -> int:
    args = build_parser().parse_args()
    if args.print_prompt:
        print(resolve_prompt(args))
        return 0
    response_json = request_json(args)
    for output in save_parts(response_json, Path(args.out_dir), args.prefix):
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
