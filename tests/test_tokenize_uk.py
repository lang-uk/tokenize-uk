#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tokenize_uk
----------------------------------

Tests for `tokenize_uk` module.
"""
from __future__ import unicode_literals
import glob
import json
from codecs import open
import unittest
from tokenize_uk import tokenize_text, tokenize_words, tokenize_sents


class TestTokenize_uk(unittest.TestCase):
    def test_full_text(self):
        files = glob.glob("tests/cases/*.json")
        assert len(files) > 0

        for case_file in files:
            with open(case_file, "r", encoding="utf-8") as fp:
                case = json.load(fp)
                assert tokenize_text(case["source"]) == case["result"]

    def test_word_tokenization(self):
        assert tokenize_words("Геогра́фія або земле́пис") == [
            "Геогра́фія", "або", "земле́пис"]

        assert tokenize_words("Комп'ютер") == [
            "Комп'ютер"]

    def test_sent_tokenization(self):
        assert len(tokenize_sents("""Результати цих досліджень опубліковано в таких колективних працях, як «Статистичні параметри
        стилів», «Морфемна структура слова», «Структурна граматика української мови Проспект», «Частотний словник сучасної української художньої прози», «Закономірності структурної організації науково-реферативного тексту», «Морфологічний аналіз наукового тексту на ЕОМ», «Синтаксичний аналіз наукового тексту на ЕОМ», «Використання ЕОМ у лінгвістичних дослідженнях» та ін. за участю В.І.Перебийніс,
        М.М.Пещак, М.П.Муравицької, Т.О.Грязнухіної, Н.П.Дарчук, Н.Ф.Клименко, Л.І.Комарової, В.І.Критської,
        Т.К.Пуздирєвої, Л.В.Орлової, Л.А.Алексієнко, Т.І.Недозим.""")) == 1
