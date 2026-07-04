# tokenize-uk

Ukrainian tokenization: paragraphs → sentences → words. Small, fast and
robust, now with LanguageTool-grade engines.

Since 2.0 the default engines are ports of what
[LanguageTool](https://languagetool.org) uses for Ukrainian, both
verified **byte-identical** to their Java originals on multi-million-token
real-world corpora:

- **words**: a port of LanguageTool's `UkrainianWordTokenizer` (Andriy
  Rysin's abbreviation-aware tokenizer) — verified on 3.87M tokens across
  four corpora, zero differences, faster than the Java original;
- **sentences**: [choppa-srx](https://pypi.org/project/choppa-srx/), the
  Python port of the Java `segment` SRX library with LanguageTool's rules.

The original 2016 regex engines are preserved and one argument away.

## Quick Start

```bash
pip install tokenize_uk
```

```python
import tokenize_uk

tokenize_uk.tokenize_words("Це проф. Артюхов.")
# ['Це', 'проф.', 'Артюхов', '.']

tokenize_uk.tokenize_sents("Це проф. Артюхов. Він приїхав у м. Київ.")
# ['Це проф. Артюхов.', 'Він приїхав у м. Київ.']

tokenize_uk.tokenize_text("Перший абзац. Ще речення.\nДругий абзац.")
# [[['Перший', 'абзац', '.'], ['Ще', 'речення', '.']], [['Другий', 'абзац', '.']]]
```

Command line:

```bash
echo "Це проф. Артюхов. Він приїхав у м. Київ." | tokenize-uk -l sents
```

## The two engines

Every function keeps the pre-2.0 signature and return shape. If the new
behavior breaks your pipeline, fall back per call:

```python
tokenize_uk.tokenize_words(text, legacy=True)   # 2016 regex engine
```

or import the old engines directly from `tokenize_uk.legacy`. The legacy
code is preserved byte-for-byte (regexes included) and covered by the
original test fixtures.

Differences you will notice with the default engine:

- abbreviations keep their dots and don't split (`проф.`, `т.`, `зв.`,
  `чл.-кор.`), and don't end sentences where they shouldn't;
- dates (`12.03.2022`), times (`15:30`), decimals (`10,5`) and web
  entities (`Цензор.НЕТ`) stay single tokens;
- sentence splitting follows LanguageTool's `segment.srx` rules instead
  of a punctuation-plus-uppercase heuristic.

For raw LanguageTool-compatible word tokens (including whitespace
tokens), use the class directly:

```python
from tokenize_uk import UkrainianWordTokenizer
UkrainianWordTokenizer().tokenize("а б")
# ['а', ' ', 'б']
```

## Verification and performance

The word tokenizer is compared byte-for-byte against LanguageTool
master's `UkrainianWordTokenizer` (compiled from source; harness in
`scripts/java-harness/`):

| corpus | lines | tokens | Java | tokenize-uk 2.0 | output |
|---|---|---|---|---|---|
| Militarny news | 100,004 | 1,736,362 | 7.4 s | 5.4 s | identical |
| uanews.dp.ua | 133,120 | 1,973,203 | 8.9 s | 7.8 s | identical |
| Liga.net | 5,982 | 69,695 | 0.5 s | 0.2 s | identical |

The sentence layer's own verification (byte-identity with the Java
segment library on ~136k segments) is documented in
[choppa's README](https://github.com/lang-uk/choppa#performance-and-verification).

Reproduce with `scripts/benchmark.py` (see `docs/design.md`).

## Documentation

- [API](docs/api.md) — functions, shapes, engines, CLI
- [Design](docs/design.md) — how the LT port works and how it's verified
- [History](docs/history.md) — 2016 origins, the LanguageTool ports

## Copyrights and kudos

- Vsevolod Dyomkin, [Dmytro Chaplynskyi](https://github.com/dchaplinsky) —
  original library, [lang-uk](https://lang.org.ua) project
- Andriy Rysin and the LanguageTool team — the original
  `UkrainianWordTokenizer` and the Ukrainian SRX rules
- [Jarek Lipski](https://github.com/loomchild) — the segment library
  behind the sentence layer

MIT licensed.
