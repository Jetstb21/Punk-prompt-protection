from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

GENESIS_HASH = "GENESIS"


def canonical_json(payload: Dict[str, Any]) -> str:
    """Stable JSON encoding for deterministic hashing."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def event_hash(event_without_hash: Dict[str, Any]) -> str:
    return sha256_text(canonical_json(event_without_hash))


def build_event(
    *,
    event_index: int,
    event_type: str,
    input_text: str,
    decision: Dict[str, Any],
    previous_hash: str = GENESIS_HASH,
    created_utc: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if event_index < 0:
        raise ValueError("event_index must be non-negative")
    if not event_type:
        raise ValueError("event_type is required")

    base = {
        "event_index": event_index,
        "created_utc": created_utc or datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "input_sha256": sha256_text(input_text),
        "decision": decision,
        "previous_hash": previous_hash,
        "metadata": metadata or {},
    }
    base["event_hash"] = event_hash(base)
    return base


def append_event(
    path: str | Path,
    *,
    event_type: str,
    input_text: str,
    decision: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    events = load_events(ledger_path) if ledger_path.exists() else []
    previous_hash = events[-1]["event_hash"] if events else GENESIS_HASH

    event = build_event(
        event_index=len(events),
        event_type=event_type,
        input_text=input_text,
        decision=decision,
        previous_hash=previous_hash,
        metadata=metadata,
    )

    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(canonical_json(event) + "\n")

    return event


def load_events(path: str | Path) -> List[Dict[str, Any]]:
    ledger_path = Path(path)
    if not ledger_path.exists():
        return []

    events: List[Dict[str, Any]] = []
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL ledger line {line_number}") from exc
    return events


def verify_event(event: Dict[str, Any]) -> bool:
    if "event_hash" not in event:
        return False
    expected = event["event_hash"]
    payload = dict(event)
    payload.pop("event_hash", None)
    return event_hash(payload) == expected


def verify_chain(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(events)
    failures: List[Dict[str, Any]] = []
    previous_hash = GENESIS_HASH

    for expected_index, event in enumerate(rows):
        event_index = event.get("event_index")
        event_hash_value = event.get("event_hash")

        if event_index != expected_index:
            failures.append({"event_index": event_index, "failure": "BAD_INDEX", "expected_index": expected_index})

        if event.get("previous_hash") != previous_hash:
            failures.append({"event_index": event_index, "failure": "BAD_PREVIOUS_HASH", "expected_previous_hash": previous_hash})

        if not verify_event(event):
            failures.append({"event_index": event_index, "failure": "BAD_EVENT_HASH"})

        previous_hash = event_hash_value or "MISSING_HASH"

    return {
        "valid": len(failures) == 0,
        "event_count": len(rows),
        "head_hash": rows[-1]["event_hash"] if rows else GENESIS_HASH,
        "failures": failures,
    }


def verify_ledger_file(path: str | Path) -> Dict[str, Any]:
    return verify_chain(load_events(path))
