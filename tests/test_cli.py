"""In-process tests for the tokenize-uk CLI."""

import io
import json
import sys
import unittest
from unittest import mock

from tokenize_uk.__main__ import main


def run_cli(args, stdin_text):
    stdout = io.StringIO()
    stdin = io.StringIO(stdin_text)
    with mock.patch.object(sys, "argv", ["tokenize-uk"] + args), \
            mock.patch.object(sys, "stdin", stdin), \
            mock.patch.object(sys, "stdout", stdout):
        main()
    return stdout.getvalue()


class CliTest(unittest.TestCase):
    def test_words_streams_lines(self):
        out = run_cli([], "Це проф. Артюхов.\nДруга стрічка.\n")
        self.assertEqual(
            ["Це", "проф.", "Артюхов", ".", "Друга", "стрічка", "."],
            out.splitlines(),
        )

    def test_words_legacy(self):
        out = run_cli(["--legacy"], "і т. д.\n")
        self.assertEqual(["і", "т", ".", "д", "."], out.splitlines())

    def test_sents(self):
        out = run_cli(["-l", "sents"], "Це проф. Артюхов. Він приїхав у м. Київ.")
        self.assertEqual(
            ["Це проф. Артюхов.", "Він приїхав у м. Київ."], out.splitlines()
        )

    def test_text_json(self):
        out = run_cli(["-l", "text"], "Абзац один.\nАбзац два.")
        self.assertEqual(
            [[["Абзац", "один", "."]], [["Абзац", "два", "."]]], json.loads(out)
        )
