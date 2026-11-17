"""Smoke test: the workspace demo graph is valid and the engine imports."""

from __future__ import annotations

import unittest
from pathlib import Path

from specd.fitness import check_fitness
from specd.validate import validate


class DemoGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]

    def test_no_validation_errors(self) -> None:
        errors = [issue for issue in validate(self.root) if issue.severity == "error"]
        self.assertEqual(errors, [], "\n".join(str(issue) for issue in errors))

    def test_no_fitness_errors(self) -> None:
        errors = [issue for issue in check_fitness(self.root) if issue.severity == "error"]
        self.assertEqual(errors, [], "\n".join(str(issue) for issue in errors))


if __name__ == "__main__":
    unittest.main()
