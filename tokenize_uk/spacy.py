"""
spaCy integration: LanguageTool-grade Ukrainian tokenization as a
drop-in spaCy tokenizer and sentencizer.

Requires the ``spacy`` extra: ``pip install tokenize_uk[spacy]``.

Quick start::

    from tokenize_uk.spacy import blank_pipeline

    nlp = blank_pipeline()
    doc = nlp("Це проф. Артюхов. Він приїхав у м. Київ.")
    [token.text for token in doc]      # LT-grade word tokens
    [sent.text for sent in doc.sents]  # LT-grade sentences

Or wire into an existing pipeline::

    import spacy
    from tokenize_uk.spacy import UkrainianTokenizer

    nlp = spacy.blank("uk")
    nlp.tokenizer = UkrainianTokenizer(nlp.vocab)
    nlp.add_pipe("tokenize_uk_sentencizer")

Caveat: statistical components of pretrained pipelines (e.g.
``uk_core_news_sm``) were trained on spaCy's own tokenization; swapping
the tokenizer under them may degrade their accuracy. This integration
is primarily intended for blank/rule-based pipelines and for corpus
processing where LanguageTool-identical tokenization matters.
"""

import json
from typing import Iterator, List, Tuple

try:
    from spacy.language import Language
    from spacy.tokens import Doc
    from spacy.vocab import Vocab
except ImportError as error:  # pragma: no cover
    raise ImportError(
        "spaCy is required for tokenize_uk.spacy; "
        "install it with: pip install tokenize_uk[spacy]"
    ) from error

from .pipeline import (
    SENTENCE_LANGUAGE_CODE,
    _WORD_TOKENIZER,
    tokenize_sents_with_spans,
)
from . import legacy as _legacy


class UkrainianTokenizer:
    """
    A spaCy tokenizer backed by the LanguageTool word tokenizer port
    (or, with ``legacy=True``, the 2016 regex engine).

    ``doc.text`` always equals the input text exactly: the raw
    LanguageTool token stream concatenates back to the input, so token
    offsets are exact.
    """

    def __init__(self, vocab: Vocab, *, legacy: bool = False) -> None:
        self.vocab = vocab
        self.legacy = legacy

    def __call__(self, text: str) -> Doc:
        words, spaces = self._words_and_spaces(text)
        return Doc(self.vocab, words=words, spaces=spaces)

    def _words_and_spaces(self, text: str) -> Tuple[List[str], List[bool]]:
        words: List[str] = []
        spaces: List[bool] = []
        for token in self._raw_tokens(text):
            if token == " " and words and not spaces[-1]:
                # A single space after a token becomes its trailing
                # space, like spaCy's own tokenizer does.
                spaces[-1] = True
            else:
                words.append(token)
                spaces.append(False)
        return words, spaces

    def _raw_tokens(self, text: str) -> Iterator[str]:
        if self.legacy:
            # The legacy engine drops whitespace and some symbols; to
            # keep doc.text == text, emit the gaps as whitespace tokens.
            cursor = 0
            for match in _legacy.WORD_TOKENIZATION_RULES.finditer(text):
                if match.start() > cursor:
                    yield text[cursor : match.start()]
                yield match.group()
                cursor = match.end()
            if cursor < len(text):
                yield text[cursor:]
        else:
            yield from _WORD_TOKENIZER.tokenize(text)

    # --- minimal serialization so nlp.to_disk()/from_disk() work ---

    def _config(self) -> bytes:
        return json.dumps({"legacy": self.legacy}).encode("utf-8")

    def _load_config(self, data: bytes) -> None:
        self.legacy = bool(json.loads(data.decode("utf-8")).get("legacy", False))

    def to_bytes(self, **kwargs) -> bytes:
        return self._config()

    def from_bytes(self, data: bytes, **kwargs) -> "UkrainianTokenizer":
        self._load_config(data)
        return self

    def to_disk(self, path, **kwargs) -> None:
        with open(path, "wb") as file:
            file.write(self._config())

    def from_disk(self, path, **kwargs) -> "UkrainianTokenizer":
        with open(path, "rb") as file:
            self._load_config(file.read())
        return self


class TokenizeUkSentencizer:
    """
    Sets sentence boundaries from choppa's SRX segmentation (the same
    rules LanguageTool uses), aligned to token offsets.
    """

    def __init__(self, *, legacy: bool = False, language_code: str = SENTENCE_LANGUAGE_CODE) -> None:
        self.legacy = legacy
        self.language_code = language_code

    def __call__(self, doc: Doc) -> Doc:
        if self.legacy:
            spans = tokenize_sents_with_spans(doc.text, legacy=True)
        else:
            spans = tokenize_sents_with_spans(doc.text, language_code=self.language_code)
        starts = {start for _, start, _ in spans}
        for i, token in enumerate(doc):
            doc[i].is_sent_start = i == 0 or token.idx in starts
        return doc


try:
    from spacy.util import registry
except ImportError:  # pragma: no cover
    from spacy import registry


@registry.tokenizers("tokenize_uk.UkrainianTokenizer.v1")
def create_tokenizer(legacy: bool = False):
    """Registered factory so config-built pipelines (and spacy.load)
    can construct the tokenizer."""

    def make_tokenizer(nlp: Language) -> UkrainianTokenizer:
        return UkrainianTokenizer(nlp.vocab, legacy=legacy)

    return make_tokenizer


@Language.factory(
    "tokenize_uk_sentencizer",
    default_config={"legacy": False, "language_code": SENTENCE_LANGUAGE_CODE},
)
def create_sentencizer(
    nlp: Language, name: str, legacy: bool, language_code: str
) -> TokenizeUkSentencizer:
    return TokenizeUkSentencizer(legacy=legacy, language_code=language_code)


def blank_pipeline(
    *, legacy: bool = False, language_code: str = SENTENCE_LANGUAGE_CODE
) -> Language:
    """
    A ready-to-use blank Ukrainian pipeline with LanguageTool-grade
    tokenization and sentence segmentation.
    """
    import spacy

    nlp = spacy.blank(
        "uk",
        config={
            "nlp": {
                "tokenizer": {
                    "@tokenizers": "tokenize_uk.UkrainianTokenizer.v1",
                    "legacy": legacy,
                }
            }
        },
    )
    nlp.add_pipe(
        "tokenize_uk_sentencizer",
        config={"legacy": legacy, "language_code": language_code},
    )
    return nlp


__all__ = ["UkrainianTokenizer", "TokenizeUkSentencizer", "blank_pipeline"]
