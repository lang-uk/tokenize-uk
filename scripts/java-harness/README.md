# Java ground-truth harness

Compiles LanguageTool's `UkrainianWordTokenizer` from source (against a
stubbed one-method `Tokenizer` interface — no Maven, no LT jars) so the
Python port can be byte-diffed against the exact upstream revision.

## Provenance

The port and its verification are synced to:

- Upstream file: `languagetool-language-modules/uk/src/main/java/org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java`
- Commit: `0761ec3ecea3e1030fcc391246a8c23d48c91e8d` (2026-04-07)
- License: LGPL-2.1 (LanguageTool) — which is why the file is fetched on
  demand rather than committed into this MIT repository.

Fetch it (pinned to the sync commit):

```bash
curl -sL -o org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java \
  https://raw.githubusercontent.com/languagetool-org/languagetool/0761ec3ecea3e1030fcc391246a8c23d48c91e8d/languagetool-language-modules/uk/src/main/java/org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java
```

When re-syncing the port with a newer LT revision, update the commit
hash here (and in `docs/design.md`'s sync procedure), re-fetch, and
re-run the differential.

## Build and run

```bash
javac -encoding UTF-8 Driver.java org/languagetool/tokenizers/Tokenizer.java \
    org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java
java -cp . Driver < corpus.txt > java.txt
python ../benchmark.py corpus.txt --java java.txt
```

## Output contract

Consumed by `scripts/benchmark.py`: one output line per input line,
tokens joined with U+0001. Result at 2.0.0: 3,871,085 tokens across
four corpora, zero differences.
