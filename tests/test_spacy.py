"""Tests for the spaCy integration (skipped if spaCy is not installed)."""

import unittest

try:
    import spacy  # noqa: F401

    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False

from tokenize_uk import tokenize_sents, tokenize_words


@unittest.skipUnless(HAS_SPACY, "spaCy not installed")
class SpacyIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tokenize_uk.spacy import blank_pipeline

        cls.nlp = blank_pipeline()

    def test_doc_text_roundtrip(self):
        for text in [
            "Це проф. Артюхов. Він приїхав у м. Київ.",
            "а  б\tв\nг",
            " з пробілу",
            "12.03.2022 о 15:30 — і т. д.",
            "",
        ]:
            self.assertEqual(text, self.nlp(text).text)

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
        from tokenize_uk.spacy import blank_pipeline

        nlp = blank_pipeline(legacy=True)
        text = "Це €дивний\tтекст. Другий."
        doc = nlp(text)
        self.assertEqual(text, doc.text)
        self.assertEqual(2, len(list(doc.sents)))

    def test_serialization_roundtrip(self):
        import tempfile

        from tokenize_uk.spacy import UkrainianTokenizer

        with tempfile.TemporaryDirectory() as tmp:
            self.nlp.to_disk(tmp)
            nlp2 = spacy.load(tmp)
            self.assertIsInstance(nlp2.tokenizer, UkrainianTokenizer)
            text = "Перевірка. Другe речення."
            self.assertEqual(
                [t.text for t in self.nlp(text)], [t.text for t in nlp2(text)]
            )
