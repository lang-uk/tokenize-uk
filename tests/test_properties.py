"""
Property-based tests: structural invariants for arbitrary input.

The generation alphabet excludes surrogates (invalid in str), the
private-use area (reserved by the tokenizer's internal placeholder
scheme, as in the Java original) and the five characters the engine
canonicalizes 1:1 (apostrophe/quote variants), so that exact string
equality invariants hold.
"""

import unittest

from hypothesis import given, settings, strategies as st

from tokenize_uk import (
    UkrainianWordTokenizer,
    tokenize_sents_with_spans,
    tokenize_words,
    tokenize_words_with_spans,
)

SAFE_TEXT = st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Co"),
        blacklist_characters="’ʼ‘‚‑",
    ),
    max_size=200,
)

TOKENIZER = UkrainianWordTokenizer()


class WordTokenizerPropertiesTest(unittest.TestCase):
    @settings(deadline=None)
    @given(text=SAFE_TEXT)
    def test_raw_tokens_concatenate_to_input(self, text: str) -> None:
        self.assertEqual(text, "".join(TOKENIZER.tokenize(text)))

    @settings(deadline=None)
    @given(text=SAFE_TEXT)
    def test_word_spans_match_input_slices(self, text: str) -> None:
        for word, start, end in tokenize_words_with_spans(text):
            self.assertEqual(text[start:end], word)

    @settings(deadline=None)
    @given(text=SAFE_TEXT)
    def test_spans_agree_with_tokenize_words(self, text: str) -> None:
        self.assertEqual(
            tokenize_words(text),
            [word for word, _, _ in tokenize_words_with_spans(text)],
        )

    @settings(deadline=None, max_examples=50)
    @given(text=SAFE_TEXT)
    def test_sentence_spans_match_input_slices(self, text: str) -> None:
        for sentence, start, end in tokenize_sents_with_spans(text):
            self.assertEqual(text[start:end], sentence)

    @settings(deadline=None)
    @given(text=SAFE_TEXT)
    def test_legacy_word_spans_match_input_slices(self, text: str) -> None:
        for word, start, end in tokenize_words_with_spans(text, legacy=True):
            self.assertEqual(text[start:end], word)
