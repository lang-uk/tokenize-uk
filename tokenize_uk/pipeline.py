"""
The tokenize_uk pipeline: paragraphs -> sentences -> words.

Since 2.0 the default engines are LanguageTool-grade:

* sentences are split with `choppa-srx <https://pypi.org/project/choppa-srx/>`_
  (a Python port of the Java segment library, byte-identical to what
  LanguageTool uses, with LanguageTool's own SRX rules);
* words are split with :class:`tokenize_uk.UkrainianWordTokenizer`, a
  port of LanguageTool's ``UkrainianWordTokenizer`` verified
  byte-identical against the Java original on multi-million-token
  corpora.

Every function keeps the historical return shape, and every function
accepts ``legacy=True`` to fall back to the original 2016 regex engines
(see :mod:`tokenize_uk.legacy`) if the new behavior breaks your
pipeline.
"""

from typing import List, Optional

from . import legacy as _legacy
from .tokenize_uk import UkrainianWordTokenizer

SENTENCE_LANGUAGE_CODE = "uk_two"

_word_tokenizer: Optional[UkrainianWordTokenizer] = None
_srx_document = None


def _get_word_tokenizer() -> UkrainianWordTokenizer:
    global _word_tokenizer
    if _word_tokenizer is None:
        _word_tokenizer = UkrainianWordTokenizer()
    return _word_tokenizer


def _get_srx_document():
    global _srx_document
    if _srx_document is None:
        from choppa import DEFAULT_SRX_RULESET, SrxDocument

        _srx_document = SrxDocument(ruleset=DEFAULT_SRX_RULESET)
    return _srx_document


def tokenize_words(string: str, legacy: bool = False) -> List[str]:
    """
    Tokenize input text to words.

    With the default engine, whitespace tokens produced by the
    LanguageTool word tokenizer are dropped so the output shape matches
    the pre-2.0 API (words and punctuation only).

    :param string: Text to tokenize
    :param legacy: use the 2016 regex engine instead
    :return: words
    """
    if legacy:
        return _legacy.tokenize_words(string)
    tokens = _get_word_tokenizer().tokenize(str(string))
    return [token for token in tokens if token.strip()]


def tokenize_sents(string: str, legacy: bool = False) -> List[str]:
    """
    Tokenize input text to sentences.

    The default engine is choppa's ``SrxTextIterator`` with
    LanguageTool's SRX rules (language key ``uk_two``). Sentences are
    stripped of surrounding whitespace, matching the pre-2.0 API.

    :param string: Text to tokenize
    :param legacy: use the 2016 heuristic engine instead
    :return: sentences
    """
    if legacy:
        return _legacy.tokenize_sents(string)
    from choppa import SrxTextIterator

    document = _get_srx_document()
    segments = SrxTextIterator(document, SENTENCE_LANGUAGE_CODE, str(string))
    return [stripped for segment in segments if (stripped := segment.strip())]


def tokenize_text(string: str, legacy: bool = False) -> List[List[List[str]]]:
    """
    Tokenize input text to paragraphs, sentences and words.

    Paragraphs are split on single newlines (as in the pre-2.0 API);
    sentences and words are tokenized with the engines described above.

    :param string: Text to tokenize
    :param legacy: use the 2016 engines instead
    :return: text tokenized into paragraphs, sentences and words
    """
    if legacy:
        return _legacy.tokenize_text(string)
    rez = []
    for part in str(string).split("\n"):
        par = []
        for sent in tokenize_sents(part):
            par.append(tokenize_words(sent))
        if par:
            rez.append(par)
    return rez


__all__ = ["tokenize_words", "tokenize_sents", "tokenize_text"]
