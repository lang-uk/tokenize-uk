# API

Public API: everything importable from `tokenize_uk`, plus the
`tokenize-uk` CLI. Function signatures and return shapes are stable
since 0.x; the `legacy` keyword was added in 2.0.

## Functions

```python
tokenize_words(string, legacy=False) -> list[str]
```
Words and punctuation tokens, no whitespace tokens. Default engine: the
LanguageTool `UkrainianWordTokenizer` port with whitespace tokens
filtered out. `legacy=True`: the 2016 regex rules.

```python
tokenize_sents(string, legacy=False, language_code="uk_two") -> list[str]
```
Sentences, stripped of surrounding whitespace. Default engine: choppa's
`SrxTextIterator` with LanguageTool's `segment.srx`. `language_code`
selects the SRX key: `uk_two` (paragraphs end at two line breaks, the
LanguageTool default) or `uk_one` (every line break ends a paragraph).
`legacy=True`: the 2016 punctuation-plus-uppercase heuristic.
All keyword arguments are keyword-only.

```python
tokenize_text(string, legacy=False) -> list[list[list[str]]]
```
Paragraphs → sentences → words. Paragraphs are split on single newlines
(historical behavior); empty paragraphs are dropped.

## Classes and modules

```python
from tokenize_uk import UkrainianWordTokenizer

UkrainianWordTokenizer().tokenize(text) -> list[str]
```
The raw LanguageTool-compatible word tokenizer: tokens **include**
whitespace runs and concatenate back to the exact input. Byte-identical
to LT master's Java implementation (see [design.md](design.md)).

`tokenize_uk.legacy` — the 2016 engines (`tokenize_words`,
`tokenize_sents`, `tokenize_text`), preserved byte-for-byte.

## CLI

```
tokenize-uk [input-file] [-l words|sents|text] [--legacy]
```

`words`/`sents` print one token/sentence per line; `text` prints the
3-level structure as JSON.

## Notes

- Importing the package compiles the word-tokenizer patterns (~15 ms);
  the first sentence call additionally parses the bundled SRX rules via
  choppa (~0.2-0.4 s, cached module-wide). choppa itself is imported
  lazily, so `import tokenize_uk` stays fast.
- Only the package-level API is stable: since 2.0,
  `from tokenize_uk.tokenize_uk import tokenize_words` (the 0.x physical
  path) no longer works — import from `tokenize_uk` directly.
- Instances of `UkrainianWordTokenizer` are stateless and thread-safe;
  the pipeline caches are write-once.
- Dependencies: `regex` (variable-length lookbehind, Unicode classes)
  and `choppa-srx` (sentence layer).
