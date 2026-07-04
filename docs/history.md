# History

- **2016** — Vsevolod Dyomkin and Dmytro Chaplynskyi write the original
  regex-based tokenizers for the [lang-uk](https://lang.org.ua) project,
  following the lang-uk
  [tokenization spec](https://github.com/lang-uk/ner-uk/blob/master/doc/tokenization.md).
  Released on PyPI as `tokenize_uk` 0.x.
- **2022** — the LanguageTool ports begin: `UkrainianWordTokenizer` is
  ported to Python on the `languagetools` branch, and the sibling
  [choppa](https://github.com/lang-uk/choppa) project ports the Java
  `segment` SRX sentence splitter. Both stall before release — subtle
  differences from the Java originals resist diagnosis.
- **2026** — choppa ships as
  [choppa-srx](https://pypi.org/project/choppa-srx/) 1.0, byte-identical
  to Java (the culprit was an emulation-layer windowing bug; see its
  [history](https://github.com/lang-uk/choppa/blob/main/docs/history.md)).
  The same methodology — sync with upstream, port upstream's tests,
  byte-diff against a Java ground-truth harness on real corpora — is
  applied here: the word tokenizer is synced with 4 years of LT drift
  (27 upstream commits), verified on 3.87M tokens, and tokenize-uk 2.0
  ships with LanguageTool-grade engines by default and the 2016 engines
  preserved behind `legacy=True`.

Credits: Andriy Rysin (the LT Ukrainian tokenizer and rules), Jarek
Lipski (the segment library), the LanguageTool team.
