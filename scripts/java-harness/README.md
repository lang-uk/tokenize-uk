# Java ground-truth harness

Compiles LanguageTool's `UkrainianWordTokenizer` from source (against a
stubbed one-method `Tokenizer` interface — no Maven, no LT jars) so the
Python port can be byte-diffed against the exact upstream revision.

## Provenance

The port and its verification are synced to:

- Upstream file: `languagetool-language-modules/uk/src/main/java/org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java`
- Commit: see [`LT_COMMIT`](LT_COMMIT) (the machine-readable pin used by CI and the drift watchdog)
- License: LGPL-2.1 (LanguageTool) — which is why the file is fetched on
  demand rather than committed into this MIT repository.

Fetch it (pinned to the sync commit):

```bash
mkdir -p org/languagetool/tokenizers/uk
curl -sfL -o org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java \
  "https://raw.githubusercontent.com/languagetool-org/languagetool/$(cat LT_COMMIT)/languagetool-language-modules/uk/src/main/java/org/languagetool/tokenizers/uk/UkrainianWordTokenizer.java"
```

When re-syncing the port with a newer LT revision, update `LT_COMMIT`,
re-fetch, and re-run the differential.

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
