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

import functools
from typing import List

from . import legacy as _legacy
from .tokenize_uk import HORIZONTAL_SPACE, VERTICAL_SPACE, UkrainianWordTokenizer

SENTENCE_LANGUAGE_CODE = "uk_two"

# Characters that do not count as token content: whitespace plus the
# invisible/format characters the LanguageTool engine emits as
# standalone tokens (ZWSP family, bidi controls, BOM, word joiners,
# soft hyphen). The 2016 engine never emitted such tokens, so they are
# stripped/dropped to keep the historical output shape.
NON_CONTENT_CHARS = (
    HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "\u200b\u200c\u200d\u200e\u200f"  # zero-width chars, directional marks
    + "\u202a\u202b\u202c\u202d\u202e"  # bidi embedding controls
    + "\u2060\u2061\u2062\u2063\u2064"  # word joiner, invisible operators
    + "\u2066\u2067\u2068\u2069"  # bidi isolates
    + "\u00ad\ufeff\u180e"  # soft hyphen, BOM, Mongolian vowel separator
)

_WORD_TOKENIZER = UkrainianWordTokenizer()


@functools.lru_cache(maxsize=1)
def _get_sentence_splitter():
    from choppa import DEFAULT_SRX_RULESET, SrxDocument, SrxTextIterator

    return SrxDocument(ruleset=DEFAULT_SRX_RULESET), SrxTextIterator


def tokenize_words(string: str, *, legacy: bool = False) -> List[str]:
    """
    Tokenize input text to words.

    With the default engine, whitespace and invisible-character tokens
    produced by the LanguageTool word tokenizer are dropped so the
    output shape matches the pre-2.0 API (words and punctuation only).

    :param string: Text to tokenize
    :param legacy: use the 2016 regex engine instead
    :return: words
    """
    if legacy:
        return _legacy.tokenize_words(string)
    tokens = _WORD_TOKENIZER.tokenize(str(string))
    return [token for token in tokens if token.strip(NON_CONTENT_CHARS)]


def tokenize_sents(
    string: str,
    *,
    legacy: bool = False,
    language_code: str = SENTENCE_LANGUAGE_CODE,
) -> List[str]:
    """
    Tokenize input text to sentences.

    The default engine is choppa's ``SrxTextIterator`` with
    LanguageTool's SRX rules. Sentences are stripped of surrounding
    whitespace, matching the pre-2.0 API.

    :param string: Text to tokenize
    :param legacy: use the 2016 heuristic engine instead
    :param language_code: SRX language key (default ``uk_two``:
        paragraphs end at two line breaks; use ``uk_one`` to make every
        line break end a paragraph, as in LanguageTool's
        single-line-break mode)
    :return: sentences
    """
    if legacy:
        return _legacy.tokenize_sents(string)
    document, iterator_class = _get_sentence_splitter()
    segments = iterator_class(document, language_code, str(string))
    return [stripped for segment in segments if (stripped := segment.strip())]


def tokenize_text(string: str, *, legacy: bool = False) -> List[List[List[str]]]:
    """
    Tokenize input text to paragraphs, sentences and words.

    Paragraphs are split on single newlines (as in the pre-2.0 API);
    sentences and words are tokenized with the engines described above.

    :param string: Text to tokenize
    :param legacy: use the 2016 engines instead
    :return: text tokenized into paragraphs, sentences and words
    """
    rez = []
    for part in str(string).split("\n"):
        par = []
        for sent in tokenize_sents(part, legacy=legacy):
            par.append(tokenize_words(sent, legacy=legacy))
        if par:
            rez.append(par)
    return rez


__all__ = ["tokenize_words", "tokenize_sents", "tokenize_text"]
