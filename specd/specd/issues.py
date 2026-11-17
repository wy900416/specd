"""Shared issue type for validation and fitness checks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Issue:
    severity: str  # "error" | "warning" | "info"
    code: str
    message: str
    path: str = ""

    def __str__(self) -> str:
        location = f" [{self.path}]" if self.path else ""
        return f"{self.severity.upper():7} {self.code:8} {self.message}{location}"

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


def has_errors(issues: list[Issue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def counts(issues: list[Issue]) -> dict[str, int]:
    result = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        result[issue.severity] = result.get(issue.severity, 0) + 1
    return result
