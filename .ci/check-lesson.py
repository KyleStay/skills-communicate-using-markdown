#!/usr/bin/env python3
"""Run the retired course's four Markdown predicates locally; never edit course state."""
import argparse
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {"1": r"# [a-zA-Z0-9]", "2": r"\!\[.*](.*)", "3": r"```", "4": r"\- \[ ] "}


def check(step, text):
    return bool(re.search(PATTERNS[step], text))


class PredicateTests(unittest.TestCase):
    def test_original_header_predicate(self):
        self.assertTrue(check("1", "# Header"))
        self.assertFalse(check("1", "Header"))

    def test_original_image_predicate(self):
        self.assertTrue(check("2", "![sample](sample.png)"))
        self.assertFalse(check("2", "[sample](sample.png)"))

    def test_original_code_predicate(self):
        self.assertTrue(check("3", "```python\nprint(1)\n```"))
        self.assertFalse(check("3", "`inline code`"))

    def test_original_task_predicate(self):
        self.assertTrue(check("4", "- [ ] unfinished task"))
        self.assertFalse(check("4", "- [x] finished task"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", choices=PATTERNS)
    parser.add_argument("--file", type=Path, default=ROOT / "index.md")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return 0 if unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(PredicateTests)).wasSuccessful() else 1
    step = args.step or (ROOT / ".github/steps/-step.txt").read_text().strip()
    if step not in PATTERNS:
        print(f"Step {step} is a course lifecycle/merge event; no Markdown predicate exists. Complete it manually; no state was changed.")
        return 0
    if not args.file.is_file():
        print(f"Incomplete course step {step}: {args.file} is absent. Supply --file for the learner's local index.md.", file=sys.stderr)
        return 2
    if not check(step, args.file.read_text()):
        print(f"Incomplete course step {step}: original Markdown predicate did not match {args.file}.", file=sys.stderr)
        return 1
    print(f"Course step {step} Markdown predicate passed locally; no course state or remote files changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
