"""
Tests for the tokenize_uk pipeline: the default LanguageTool-grade
engines and the preserved 2016 legacy engines.
"""

import glob
import json
import unittest

from tokenize_uk import tokenize_text, tokenize_words, tokenize_sents


class LegacyEngineTest(unittest.TestCase):
    """The 2016 engines must keep their historical behavior exactly."""

    def test_full_text(self):
        files = glob.glob("tests/cases/*.json")
        self.assertTrue(files)

        for case_file in files:
            with open(case_file, encoding="utf-8") as fp:
                case = json.load(fp)
                self.assertEqual(case["result"], tokenize_text(case["source"], legacy=True))

    def test_word_tokenization(self):
        self.assertEqual(
            ["Геогра́фія", "або", "земле́пис"],
            tokenize_words("Геогра́фія або земле́пис", legacy=True),
        )
        self.assertEqual(["Комп'ютер"], tokenize_words("Комп'ютер", legacy=True))

    def test_sent_tokenization(self):
        text = (
            "Результати цих досліджень опубліковано в таких колективних працях, як "
            "«Статистичні параметри стилів», «Частотний словник сучасної української "
            "художньої прози» та ін. за участю В.І.Перебийніс, М.М.Пещак, Т.І.Недозим."
        )
        self.assertEqual(1, len(tokenize_sents(text, legacy=True)))


class DefaultEngineTest(unittest.TestCase):
    """The 2.0 default: choppa sentences + LanguageTool word tokenizer."""

    def test_word_tokenization_drops_whitespace(self):
        self.assertEqual(
            ["Геогра́фія", "або", "земле́пис"],
            tokenize_words("Геогра́фія або земле́пис"),
        )
        self.assertEqual(["Комп'ютер"], tokenize_words("Комп'ютер"))

    def test_word_tokenization_beats_legacy(self):
        # Abbreviations with dots stay one token with the LT engine.
        self.assertEqual(
            ["Про", "це", "повідомив", "проф.", "Артюхов", "."],
            tokenize_words("Про це повідомив проф. Артюхов."),
        )
        self.assertEqual(["і", "т.", "д."], tokenize_words("і т. д."))

    def test_sent_tokenization(self):
        sents = tokenize_sents("Перше речення. Друге речення! А це — третє.")
        self.assertEqual(
            ["Перше речення.", "Друге речення!", "А це — третє."], sents
        )

    def test_sent_tokenization_abbreviations(self):
        # The LT rules know that "проф." does not end a sentence.
        sents = tokenize_sents("Це проф. Артюхов. Він приїхав у м. Київ.")
        self.assertEqual(
            ["Це проф. Артюхов.", "Він приїхав у м. Київ."], sents
        )

    def test_text_shape(self):
        result = tokenize_text("Перший абзац. Ще речення.\nДругий абзац.")
        self.assertEqual(
            [
                [
                    ["Перший", "абзац", "."],
                    ["Ще", "речення", "."],
                ],
                [
                    ["Другий", "абзац", "."],
                ],
            ],
            result,
        )

    def test_empty_lines_dropped(self):
        result = tokenize_text("Абзац.\n\n\nІнший.")
        self.assertEqual(2, len(result))


class InvisibleTokenTest(unittest.TestCase):
    """Invisible characters common in scraped web text must not leak
    into the word stream (shape parity with the 2016 engine, which
    never emitted them)."""

    def test_zero_width_space(self):
        self.assertEqual(
            ["слово", "друге"], tokenize_words("слово​друге")
        )
        self.assertEqual(
            tokenize_words("слово​друге", legacy=True),
            tokenize_words("слово​друге"),
        )

    def test_leading_bom(self):
        self.assertEqual(["Слово"], tokenize_words("﻿Слово"))

    def test_sentence_language_code(self):
        # uk_one: a single line break ends a paragraph.
        text = "Заголовок без крапки\nПерше речення."
        self.assertEqual(
            ["Заголовок без крапки", "Перше речення."],
            tokenize_sents(text, language_code="uk_one"),
        )

class LegacyModuleTest(unittest.TestCase):
    """tokenize_uk.legacy is public API on its own."""

    def test_legacy_tokenize_text_direct(self):
        from tokenize_uk import legacy

        result = legacy.tokenize_text("Речення одне. Речення два.\nДругий абзац.")
        self.assertEqual(
            [
                [["Речення", "одне", "."], ["Речення", "два", "."]],
                [["Другий", "абзац", "."]],
            ],
            result,
        )
        # The pipeline's legacy=True path must agree with the module.
        self.assertEqual(
            result, tokenize_text("Речення одне. Речення два.\nДругий абзац.", legacy=True)
        )


class NonBreakingSlashTest(unittest.TestCase):
    def test_ldnr(self):
        self.assertEqual(["бойовики", "Л/ДНР", "напали"], tokenize_words("бойовики Л/ДНР напали"))
