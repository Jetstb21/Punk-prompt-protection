from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .ledger import append_event, verify_ledger_file
from .policy import check


def _print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="punk-prompt-protection",
        description="Deterministic prompt guard with tamper-evident ledger support.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check_parser = sub.add_parser("check", help="Evaluate one prompt string.")
    check_parser.add_argument("prompt", help="Prompt text to evaluate.")
    check_parser.add_argument(
        "--ledger",
        help="Optional JSONL ledger path. When supplied, the check result is appended to the ledger.",
    )

    verify_parser = sub.add_parser("verify-ledger", help="Verify a JSONL ledger file.")
    verify_parser.add_argument("ledger", help="Path to the JSONL ledger file.")

    args = parser.parse_args()

    if args.command == "check":
        result = check(args.prompt)
        if args.ledger:
            event = append_event(
                Path(args.ledger),
                event_type="PROMPT_CHECK",
                input_text=args.prompt,
                decision=result["verdict"],
                metadata={"source": "cli"},
            )
            result = {"check": result, "ledger_event": event}
        _print_json(result)
        return 0 if result.get("check", result)["verdict"]["allowed"] else 1

    if args.command == "verify-ledger":
        result = verify_ledger_file(Path(args.ledger))
        _print_json(result)
        return 0 if result["valid"] else 1

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
