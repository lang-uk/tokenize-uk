#!/usr/bin/env python3
"""
Benchmark the word tokenizer and (optionally) diff against the Java
LanguageTool UkrainianWordTokenizer output.

Java ground truth (driver around LT master source, see docs):
    java Driver < corpus.txt > java.txt   # one line per input line,
                                          # tokens separated by \\x01

    python scripts/benchmark.py corpus.txt --java java.txt
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tokenize_uk.tokenize_uk import UkrainianWordTokenizer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--java", type=Path, help="Java driver output to diff against")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    tokenizer = UkrainianWordTokenizer()
    lines = args.corpus.read_text(encoding="utf-8").splitlines()

    started = time.perf_counter()
    tokenized = [tokenizer.tokenize(line) for line in lines]
    elapsed = time.perf_counter() - started

    n_tokens = sum(len(t) for t in tokenized)
    mb = args.corpus.stat().st_size / 1e6
    print(f"{len(lines)} lines, {n_tokens} tokens in {elapsed:.2f}s ({mb / elapsed:.2f} MB/s)")

    if not (args.out or args.java):
        return 0

    rendered = ["\x01".join(t) for t in tokenized]

    if args.out:
        args.out.write_text("\n".join(rendered) + "\n", encoding="utf-8")

    if args.java:
        expected = args.java.read_text(encoding="utf-8").splitlines()
        if expected == rendered:
            print(f"IDENTICAL to Java ({n_tokens} tokens)")
            return 0
        print(f"DIFFERS from Java: {len(expected)} vs {len(rendered)} lines")
        shown = 0
        for i, (e, r) in enumerate(zip(expected, rendered)):
            if e != r and shown < 10:
                shown += 1
                print(f"line {i + 1}:")
                print(f"  java   | {e.replace(chr(1), '|')[:160]}")
                print(f"  python | {r.replace(chr(1), '|')[:160]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
