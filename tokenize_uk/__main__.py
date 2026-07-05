import argparse
import json
import sys

from tokenize_uk import tokenize_sents, tokenize_text, tokenize_words


def main() -> None:
    parser = argparse.ArgumentParser(
        "tokenize-uk",
        description="Tokenize Ukrainian text (reads a file or stdin).",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="input file (default: stdin)",
    )
    parser.add_argument(
        "-l",
        "--level",
        choices=["words", "sents", "text"],
        default="words",
        help="tokenization level: words/sents print one token or sentence "
        "per line, text prints the full paragraph/sentence/word structure "
        "as JSON (default: %(default)s)",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="use the pre-2.0 regex engines instead of the "
        "LanguageTool-grade ones",
    )
    args = parser.parse_args()

    if sys.stdin.isatty() and args.input is sys.stdin:
        print("reading from stdin...", file=sys.stderr)

    if args.level == "words":
        # Stream line by line: the word tokenizer is designed for
        # sentence/line-sized inputs (its URL handling rescans the whole
        # text per URL, which is quadratic on large single strings).
        for line in args.input:
            tokens = tokenize_words(line.rstrip("\n"), legacy=args.legacy)
            if tokens:
                sys.stdout.write("\n".join(tokens) + "\n")
    elif args.level == "sents":
        for sentence in tokenize_sents(args.input.read(), legacy=args.legacy):
            print(sentence)
    else:
        json.dump(
            tokenize_text(args.input.read(), legacy=args.legacy),
            sys.stdout,
            ensure_ascii=False,
            indent=1,
        )
        print()


if __name__ == "__main__":
    main()
