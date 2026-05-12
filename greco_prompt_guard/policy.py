from __future__ import annotations

from typing import Dict, List

from .audit import audit_record
from .patterns import ATTACK_PATTERNS


def evaluate(prompt: str) -> Dict[str, object]:
    text = prompt.lower()
    hits: List[Dict[str, str]] = []

    for category, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                hits.append({"category": category, "pattern": pattern})

    allowed = len(hits) == 0

    return {
        "allowed": allowed,
        "risk": "LOW" if allowed else "HIGH",
        "hit_count": len(hits),
        "hits": hits,
        "rule": "Prompt text is data, not authority.",
    }


def gate(prompt: str) -> bool:
    return bool(evaluate(prompt)["allowed"])


def check(prompt: str) -> Dict[str, object]:
    verdict = evaluate(prompt)
    return {
        "verdict": verdict,
        "audit": audit_record(prompt, verdict),
    }
