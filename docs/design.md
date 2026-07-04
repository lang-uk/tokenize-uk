# Design

## The word tokenizer port

`tokenize_uk/tokenize_uk.py` is a line-by-line port of LanguageTool's
[`UkrainianWordTokenizer.java`](https://github.com/languagetool-org/languagetool/blob/master/languagetool-language-modules/uk/src/main/java/org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java)
(synced to LT master as of 2026-04-07), keeping the original's
structure: a battery of pre-processing regexes hides characters that
must not split tokens (decimal commas, dots in dates and abbreviations,
colons in times, slashes in `с/г`, ...) behind private-use Unicode
placeholders (`U+E001`–`U+E120`), the text is split with one big
`SPLIT_CHARS` alternation, and the placeholders are restored in each
token.

Porting notes:

- The `regex` package is required: the patterns use variable-length
  lookbehind (e.g. the apostrophe rules) which stdlib `re` rejects.
- Java's `Pattern.UNICODE_CHARACTER_CLASS` flags are no-ops in Python
  (str patterns are Unicode-aware by default).
- The port is intentionally *not* pythonized beyond naming: keeping the
  pattern-for-pattern correspondence with the Java source is what makes
  re-syncing with upstream (and reviewing the diff) tractable. Sync
  procedure: diff the Java file between the recorded sync commit and
  master, apply each hunk to the matching Python pattern, port the test
  drift, re-run the corpus differential.

## Verification

Three layers, mirroring [choppa](https://github.com/lang-uk/choppa)'s
methodology (see its `docs/design.md` for the rationale):

1. **LT's own unit tests**, ported from `UkrainianWordTokenizerTest.java`
   (15 test methods, in `tests/test_word_tokenizer.py`).
2. **Corpus-level byte-diff against the Java original.**
   `scripts/java-harness/` contains LT master's
   `UkrainianWordTokenizer.java` compiled against a stubbed one-method
   `Tokenizer` interface plus a tiny driver — no Maven, no LT jars, and
   the ground truth is exactly master, not a lagging release:

   ```bash
   cd scripts/java-harness
   javac -encoding UTF-8 Driver.java org/languagetool/tokenizers/Tokenizer.java \
       org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java
   java -cp . Driver < corpus.txt > java.txt
   python ../benchmark.py corpus.txt --java java.txt
   ```

   Result at 2.0.0: **3,871,085 tokens across four corpora (Militarny,
   uanews.dp.ua, Liga.net news, one 5k-line sample), zero differences**,
   with the Python side 1.3–4x faster than the Java driver.
3. **The pipeline's legacy engines** are pinned by the original 0.x
   fixtures (`tests/cases/*.json`), guaranteeing `legacy=True` output
   never drifts.

## The dual-engine pipeline

The 2.0 decision: default to the LanguageTool-grade engines but never
strand a 0.x user — same function names, same return shapes, and
`legacy=True` reproduces the old output exactly. The shape parity is
achieved by post-processing the LT engines' richer output (whitespace
tokens dropped for words, segments stripped for sentences) rather than
by changing the engines, so `UkrainianWordTokenizer` remains available
untouched for anyone who needs LT-identical tokens.

Paragraph splitting stays at "one line = one paragraph" (the 0.x
behavior) even though choppa could handle multi-line paragraphs — the
return shape of `tokenize_text` is the API contract here.
