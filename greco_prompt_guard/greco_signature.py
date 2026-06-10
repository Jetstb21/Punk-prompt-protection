"""GRECO signature computation for prompt evaluation.

Self-contained inline subset of the v3.2.2 hypotenuse chain and v3.3
token lineal calibration architecture, scaled down for the seed repo so
no external workshop import is needed. Produces a deterministic
geometric signature for any input prompt that downstream policy and
ledger code can include in audit records.

REPORT_ONLY by claim posture. The signature is descriptive geometry
(lineal length, alpha tag sum, hypotenuse chain values, bucket positions),
not a cryptographic primitive.

Schema produced per prompt:

    prompt_text              str   (original input, untruncated)
    word_count               int
    char_count               int
    alpha_a1_sum             int   (A1-Z26 sum across alphabetic chars)
    word_lineal_length_sum   float (per-word lineal lengths totalled)
    h_1_aggregate            float (sqrt(A_leg^2 + lineal^2) on aggregates)
    h_2_forward              float (sqrt(H_1^2 + K_kernel^2))
    h_2_mirror               float (sqrt(H_1^2 + K_mirror^2))
    volume_forward           float (17/12 * pi * H_2_fwd^3)
    volume_mirror            float (17/12 * pi * H_2_mir^3)
    bucket_path              list[int]   (11-bucket positions per word, -5..+5)
    signature_sha256         str   (16 hex of sha256 over canonical fields)
    per_word                 list[dict]  (word, tag, lineal, H_1, bucket)

The kernel K used here is a simple deterministic input-derived value
(char_count * 1000 + word_count * 100 + alpha_a1_sum), giving each
distinct prompt a distinct K. Digit-reverse for the mirror.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Dict, List

ALPHABET_INDEX = {chr(ord("A") + i): i + 1 for i in range(26)}

VOLUME_COEFF = 17.0 / 12.0


def _alpha_a1_sum(text: str) -> int:
    return sum(
        ALPHABET_INDEX[c.upper()]
        for c in text
        if c.upper() in ALPHABET_INDEX
    )


def _word_lineal_length(word: str) -> float:
    """Per-letter lineal increment matching the half-fold alphabet style:
    each letter contributes (index_a1) to a running cumulative total."""
    cumulative = 0.0
    for c in word:
        if c.upper() in ALPHABET_INDEX:
            cumulative += float(ALPHABET_INDEX[c.upper()])
    return cumulative


def _bucket_position_pm5(tag_sum: int) -> int:
    """Map an integer tag sum into the 11-bucket Father/Mother scaffold."""
    lane = tag_sum % 26
    edges = [3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 26]
    positions = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    for edge, pos in zip(edges, positions):
        if lane < edge:
            return pos
    return 5


def _reverse_int(n: int) -> int:
    return int(str(n)[::-1]) if n != 0 else 0


@dataclass(frozen=True)
class PerWord:
    word: str
    tag_a1_sum: int
    lineal_length: float
    h_1: float
    bucket_pm5: int


def compute_greco_signature(prompt: str) -> Dict[str, Any]:
    """Return a deterministic geometric signature for an input prompt.

    Pure function. No I/O, no side effects. Same prompt always yields
    the same signature (including the sha256 short hash).
    """
    words = [w for w in prompt.split() if w.strip()]
    word_count = len(words)
    char_count = len(prompt)
    alpha_total = _alpha_a1_sum(prompt)
    word_lineal_total = sum(_word_lineal_length(w) for w in words)

    h_1_aggregate = math.hypot(alpha_total, word_lineal_total)

    k_forward = char_count * 1000 + word_count * 100 + alpha_total
    k_mirror = _reverse_int(k_forward) if k_forward > 0 else 0

    h_2_forward = math.hypot(h_1_aggregate, k_forward)
    h_2_mirror = math.hypot(h_1_aggregate, k_mirror)
    volume_forward = VOLUME_COEFF * math.pi * (h_2_forward ** 3)
    volume_mirror = VOLUME_COEFF * math.pi * (h_2_mirror ** 3)

    per_word: List[PerWord] = []
    for w in words:
        tag = _alpha_a1_sum(w)
        lineal = _word_lineal_length(w)
        h1 = math.hypot(tag, lineal)
        bucket = _bucket_position_pm5(tag)
        per_word.append(PerWord(
            word=w,
            tag_a1_sum=tag,
            lineal_length=round(lineal, 6),
            h_1=round(h1, 6),
            bucket_pm5=bucket,
        ))
    bucket_path = [pw.bucket_pm5 for pw in per_word]

    per_word_seq = ",".join(f"{pw.tag_a1_sum}:{pw.bucket_pm5}" for pw in per_word)
    canonical = (
        f"{word_count}|{char_count}|{alpha_total}|{word_lineal_total:.9f}|"
        f"{h_2_forward:.9f}|{h_2_mirror:.9f}|{per_word_seq}"
    )
    signature_sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]

    return {
        "prompt_text": prompt,
        "word_count": word_count,
        "char_count": char_count,
        "alpha_a1_sum": alpha_total,
        "word_lineal_length_sum": round(word_lineal_total, 6),
        "h_1_aggregate": round(h_1_aggregate, 6),
        "k_forward": k_forward,
        "k_mirror": k_mirror,
        "h_2_forward": round(h_2_forward, 6),
        "h_2_mirror": round(h_2_mirror, 6),
        "volume_forward": round(volume_forward, 6),
        "volume_mirror": round(volume_mirror, 6),
        "bucket_path": bucket_path,
        "signature_sha256": signature_sha256,
        "per_word": [
            {
                "word": pw.word,
                "tag_a1_sum": pw.tag_a1_sum,
                "lineal_length": pw.lineal_length,
                "h_1": pw.h_1,
                "bucket_pm5": pw.bucket_pm5,
            }
            for pw in per_word
        ],
        "schema_version": "greco_signature_v0.1",
        "claim": "REPORT_ONLY_DETERMINISTIC_GEOMETRY",
    }
