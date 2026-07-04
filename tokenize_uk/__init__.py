from .pipeline import (
    tokenize_words,
    tokenize_sents,
    tokenize_text,
    tokenize_words_with_spans,
    tokenize_sents_with_spans,
)
from .tokenize_uk import UkrainianWordTokenizer
from . import legacy

__author__ = "Vsevolod Dyomkin, Dmytro Chaplynskyi"
__email__ = "chaplinsky.dmitry@gmail.com"
__version__ = "2.0.0"

__all__ = [
    "tokenize_words",
    "tokenize_sents",
    "tokenize_text",
    "tokenize_words_with_spans",
    "tokenize_sents_with_spans",
    "UkrainianWordTokenizer",
    "legacy",
]
