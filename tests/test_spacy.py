"""Tests for the spaCy integration (skipped if spaCy is not installed)."""

import tempfile
import unittest

import pytest

spacy = pytest.importorskip("spacy")

from tokenize_uk import tokenize_sents, tokenize_words
from tokenize_uk.spacy import UkrainianTokenizer, blank_pipeline


class SpacyIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlp = blank_pipeline()

    def test_doc_text_roundtrip(self):
        for text in [
            "Це проф. Артюхов. Він приїхав у м. Київ.",
            "а  б\tв\nг",
            " з пробілу",
            "12.03.2022 о 15:30 — і т. д.",
            "",
            # Characters the engine canonicalizes must survive verbatim:
            # typographic apostrophes, single low quote, non-breaking hyphen.
            "п’ять хвилин, мʼясо",
            "об‘єднати ‚так‘ і навпаки",
            "як‑небудь",
        ]:
            self.assertEqual(text, self.nlp(text).text)

    def test_token_text_is_verbatim_input(self):
        text = "п’ять"
        doc = self.nlp(text)
        self.assertEqual(["п’ять"], [t.text for t in doc])
        self.assertEqual(0, doc[0].idx)

    def test_tokens_match_tokenize_words(self):
        text = "Це проф. Артюхов, і т. д. — 12.03.2022!"
        doc = self.nlp(text)
        self.assertEqual(
            tokenize_words(text),
            [t.text for t in doc if not t.is_space],
        )

    def test_sentences_match_tokenize_sents(self):
        text = "Це проф. Артюхов. Він приїхав у м. Київ. І т. д. — далі буде."
        doc = self.nlp(text)
        self.assertEqual(
            tokenize_sents(text),
            [sent.text.strip() for sent in doc.sents],
        )

    def test_legacy_engine_roundtrip(self):
        nlp = blank_pipeline(legacy=True)
        text = "Це €дивний\tтекст. Другий."
        doc = nlp(text)
        self.assertEqual(text, doc.text)
        self.assertEqual(2, len(list(doc.sents)))

    def test_serialization_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.nlp.to_disk(tmp)
            nlp2 = spacy.load(tmp)
            self.assertIsInstance(nlp2.tokenizer, UkrainianTokenizer)
            text = "Перевірка. Другe речення."
            self.assertEqual(
                [t.text for t in self.nlp(text)], [t.text for t in nlp2(text)]
            )

    def test_fresh_process_load_via_entry_points(self):
        """spacy.load() must reconstruct the pipeline in a process that
        never imported tokenize_uk.spacy — this is exactly what the
        spacy_factories / spacy_tokenizers entry points promise, and it
        only works when the package is installed (pip install -e .)."""
        import importlib.metadata
        import subprocess
        import sys

        eps = importlib.metadata.entry_points(group="spacy_tokenizers")
        if not any(e.name == "tokenize_uk.UkrainianTokenizer.v1" for e in eps):
            self.skipTest("package not installed; entry points inactive")

        with tempfile.TemporaryDirectory() as tmp:
            self.nlp.to_disk(tmp)
            code = (
                "import spacy; nlp = spacy.load(%r); "
                "doc = nlp('Це проф. Артюхов. Він тут.'); "
                "print('|'.join(s.text for s in doc.sents))" % tmp
            )
            result = subprocess.run(
                [sys.executable, "-c", code], capture_output=True, text=True
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(
                "Це проф. Артюхов.|Він тут.", result.stdout.strip()
            )
