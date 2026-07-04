# Changelog

## 2.0.0 (2026-07-04)

- **New default engines, same API.** `tokenize_words`, `tokenize_sents`
  and `tokenize_text` keep their signatures and return shapes but are now
  backed by LanguageTool-grade engines: a port of LT's
  `UkrainianWordTokenizer` for words (synced to LT master 2026-04-07,
  byte-identical to the Java original on 3.87M tokens from four real
  corpora) and [choppa-srx](https://pypi.org/project/choppa-srx/) for
  sentences (LT's own SRX rules).
- **Legacy engines preserved.** Pass `legacy=True` to any function, or
  import `tokenize_uk.legacy`, for the exact 2016 behavior (regexes kept
  byte-for-byte, now with type hints, docstrings and tests).
- `UkrainianWordTokenizer` exposed for raw LT-compatible tokenization
  (whitespace tokens included).
- `tokenize-uk` console script (`-l words|sents|text`, `--legacy`).
- `tokenize_words_with_spans` / `tokenize_sents_with_spans`: character
  offsets into the input for NER-style alignment, both engines.
- Note: only the package-level import path is preserved —
  `from tokenize_uk import tokenize_words` works as before, but the 0.x
  physical path `from tokenize_uk.tokenize_uk import tokenize_words`
  now refers to the word-tokenizer module instead.
- Modern packaging (`pyproject.toml`, py.typed, Python 3.9–3.14), CI,
  tag-triggered trusted publishing; benchmark script and the Java
  ground-truth harness ship in `scripts/`.

## 0.2.0 and earlier (2016–2017)

Original regex-based tokenizers by Vsevolod Dyomkin and Dmytro
Chaplynskyi, following the lang-uk
[tokenization spec](https://github.com/lang-uk/ner-uk/blob/master/doc/tokenization.md).
