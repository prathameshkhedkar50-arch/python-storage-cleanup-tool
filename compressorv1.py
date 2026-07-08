#!/usr/bin/env python3
"""
compressor.py

Usage:
    python compressor.py compress <input_dir> <output_dir>
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterator

SUPPORTED_EXTENSIONS = frozenset({
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".c", ".cpp", ".cxx", ".h", ".hpp",
    ".cs", ".go", ".rs", ".php", ".kt", ".swift", ".rb",
    ".sh", ".sql", ".html", ".css",
    ".json", ".yaml", ".yml", ".xml",
    ".md", ".txt",
})

SEPARATORS = (
    " ", "=", ";", ":", "<", ">", "?",
    "(", ")", "{", "}", "[", "]",
    "\n", "#", "-", '"', "'", ".", ",", "|",
    "&", "*", "+", "\t", "%", "^", "!", "@",
    "\\", "\r", "/",
)

SEP_PATTERN = re.compile("(" + "|".join(re.escape(s) for s in SEPARATORS) + ")")
SEP_SET = set(SEPARATORS)


def alias_stream() -> Iterator[str]:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    for ch in digits:
        yield ch
    for ch in letters:
        yield ch
    n = 10
    while n < 100:
        yield str(n)
        n += 1
    width = 2
    while True:
        from itertools import product
        for combo in product(letters, repeat=width):
            yield "".join(combo)
        width += 1


def iter_files(root: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield fpath


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def split(text: str) -> list[str]:
    return SEP_PATTERN.split(text)


def compress(args: argparse.Namespace) -> None:
    src = Path(args.input_dir).resolve()
    dst = Path(args.output_dir).resolve()

    if not src.is_dir():
        print(f"ERROR: '{src}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    if dst == src:
        print("ERROR: output_dir must differ from input_dir.", file=sys.stderr)
        sys.exit(1)

    # Pass 1: count token frequency
    freq: dict[str, int] = defaultdict(int)
    for fpath in iter_files(src):
        text = read_text(fpath)
        if text is None:
            continue
        for part in split(text):
            if part and part not in SEP_SET:
                freq[part] += 1

    # Pass 2: sort by frequency descending, assign aliases by rank
    sorted_tokens = sorted(freq, key=lambda t: freq[t], reverse=True)
    gen = alias_stream()
    token_to_alias: dict[str, str] = {}
    alias_to_token: dict[str, str] = {}
    for token in sorted_tokens:
        alias = next(gen)
        token_to_alias[token] = alias
        alias_to_token[alias] = token

    # Pass 3: write compressed files
    dst.mkdir(parents=True, exist_ok=True)
    for fpath in iter_files(src):
        text = read_text(fpath)
        if text is None:
            continue
        parts = split(text)
        out = "".join(
            token_to_alias[p] if (p and p not in SEP_SET and p in token_to_alias) else p
            for p in parts
        )
        rel = fpath.relative_to(src)
        out_path = dst / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")

    # Save mappings
    (dst / "token_to_alias.json").write_text(
        json.dumps(token_to_alias, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (dst / "alias_to_token.json").write_text(
        json.dumps(alias_to_token, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Done. Compressed files written to '{dst}'.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="compressor.py")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("compress")
    p.add_argument("input_dir")
    p.add_argument("output_dir")
    args = parser.parse_args()
    if args.command == "compress":
        compress(args)


if __name__ == "__main__":
    main()