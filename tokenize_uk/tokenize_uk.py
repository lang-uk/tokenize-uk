#!env python
# -*- coding: utf-8 -*-

"""Ukrainian tokenization script based on `standard tokenization algorithm <https://github.com/lang-uk/ner-uk/blob/master/doc/tokenization.md>`_.

2016 (c) Vsevolod Dyomkin <vseloved@gmail.com>, Dmitry Chaplinsky <chaplinsky.dmitry@gmail.com>
"""

from __future__ import unicode_literals
import re
import six


ACCENT = six.unichr(769)
WORD_TOKENIZATION_RULES = re.compile(r"""
[\w""" + ACCENT + """]+://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+
|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+
|[0-9]+-[а-яА-ЯіїІЇ'’`""" + ACCENT + """]+
|[+-]?[0-9](?:[0-9,.-]*[0-9])?
|[\w""" + ACCENT + """](?:[\w'’`-""" + ACCENT + """]?[\w""" + ACCENT + """]+)*
|[\w""" + ACCENT + """].(?:\[\w""" + ACCENT + """].)+[\w""" + ACCENT + """]?
|[^\s]
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


def tokenize_words(string):
    """
    Tokenize input text to words.

    :param string: Text to tokenize
    :type string: str or unicode
    :return: words
    :rtype: list of strings
    """
    string = six.text_type(string)
    return re.findall(WORD_TOKENIZATION_RULES, string)


def tokenize_sents(string):
    """
    Tokenize input text to sentences.

    :param string: Text to tokenize
    :type string: str or unicode
    :return: sentences
    :rtype: list of strings
    """
    string = six.text_type(string)

    spans = []
    for match in re.finditer('[^\s]+', string):
        spans.append(match)
    spans_count = len(spans)

    rez = []
    off = 0

    for i in range(spans_count):
        tok = string[spans[i].start():spans[i].end()]
        if i == spans_count - 1:
            rez.append(string[off:spans[i].end()])
        elif tok[-1] in ['.', '!', '?', '…', '»']:
            tok1 = tok[re.search('[.!?…»]', tok).start()-1]
            next_tok = string[spans[i + 1].start():spans[i + 1].end()]
            if (next_tok[0].isupper()
                and not tok1.isupper()
                and not (tok[-1] != '.'
                         or tok1[0] == '('
                         or tok in ABBRS)):
                rez.append(string[off:spans[i].end()])
                off = spans[i + 1].start()

    return rez


def tokenize_text(string):
    """
    Tokenize input text to paragraphs, sentences and words.

    Tokenization to paragraphs is done using simple Newline algorithm
    For sentences and words tokenizers above are used

    :param string: Text to tokenize
    :type string: str or unicode
    :return: text, tokenized into paragraphs, sentences and words
    :rtype: list of list of list of words
    """
    string = six.text_type(string)
    rez = []
    for part in string.split('\n'):
        par = []
        for sent in tokenize_sents(part):
            par.append(tokenize_words(sent))
        if par:
            rez.append(par)
    return rez



__all__ = [
    "tokenize_words", "tokenize_text", "tokenize_sents"]
