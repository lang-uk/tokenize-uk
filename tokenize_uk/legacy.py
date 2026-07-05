"""
The original (2016) regex-based Ukrainian tokenizers, preserved verbatim.

Based on the `standard tokenization algorithm
<https://github.com/lang-uk/ner-uk/blob/master/doc/tokenization.md>`_.

2016 (c) Vsevolod Dyomkin <vseloved@gmail.com>,
         Dmytro Chaplynskyi <chaplinsky.dmitry@gmail.com>

These are the pre-2.0 engines behind :func:`tokenize_uk.tokenize_words`,
:func:`tokenize_uk.tokenize_sents` and :func:`tokenize_uk.tokenize_text`.
Since 2.0 the package defaults to the LanguageTool-grade engines; pass
``legacy=True`` to those functions (or import from this module directly)
if your pipeline depends on the historical behavior. The regular
expressions below are intentionally kept byte-for-byte identical to the
0.x releases, warts and all.
"""

import re
from typing import List

ACCENT = chr(769)

WORD_TOKENIZATION_RULES = re.compile(r"""
[\w""" + ACCENT + r"""]+://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+
|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+
|[0-9]+-[а-яА-ЯіїІЇ'’`""" + ACCENT + r"""]+
|[+-]?[0-9](?:[0-9,.-]*[0-9])?
|[\w""" + ACCENT + r"""](?:[\w'’`-""" + ACCENT + r"""]?[\w""" + ACCENT + r"""]+)*
|[\w""" + ACCENT + r"""].(?:\[\w""" + ACCENT + r"""].)+[\w""" + ACCENT + r"""]?
|["#$%&*+,/:;<=>@^`~…\(\)⟨⟩{}\[\|\]‒–—―«»“”‘’'№]
|[.!?]+
|-+
""", re.X | re.U)

ABBRS = """
ім.
о.
вул.
просп.
бул.
пров.
пл.
г.
р.
див.
п.
с.
м.
""".strip().split()


def tokenize_words(string: str) -> List[str]:
    """
    Tokenize input text to words using the 2016 regex rules.

    :param string: Text to tokenize
    :return: words (and standalone punctuation marks); whitespace is
        not included in the output
    """
    return re.findall(WORD_TOKENIZATION_RULES, str(string))


def tokenize_sents(string: str) -> List[str]:
    """
    Tokenize input text to sentences using the 2016 heuristic
    (sentence-final punctuation followed by an uppercase letter, with a
    small list of known abbreviations).

    :param string: Text to tokenize
    :return: sentences
    """
    string = str(string)

    spans = []
    for match in re.finditer(r"[^\s]+", string):
        spans.append(match)
    spans_count = len(spans)

    rez = []
    off = 0

    for i in range(spans_count):
        tok = string[spans[i].start():spans[i].end()]
        if i == spans_count - 1:
            rez.append(string[off:spans[i].end()])
        elif tok[-1] in [".", "!", "?", "…", "»"]:
            tok1 = tok[re.search("[.!?…»]", tok).start() - 1]
            next_tok = string[spans[i + 1].start():spans[i + 1].end()]
            if (next_tok[0].isupper()
                    and not tok1.isupper()
                    and not (tok[-1] != "."
                             or tok1[0] == "("
                             or tok in ABBRS)):
                rez.append(string[off:spans[i].end()])
                off = spans[i + 1].start()

    return rez


def tokenize_text(string: str) -> List[List[List[str]]]:
    """
    Tokenize input text to paragraphs, sentences and words using the
    2016 engines. Paragraphs are split on single newlines.

    :param string: Text to tokenize
    :return: text tokenized into paragraphs, sentences and words
    """
    string = str(string)
    rez = []
    for part in string.split("\n"):
        par = []
        for sent in tokenize_sents(part):
            par.append(tokenize_words(sent))
        if par:
            rez.append(par)
    return rez


__all__ = ["tokenize_words", "tokenize_sents", "tokenize_text"]
