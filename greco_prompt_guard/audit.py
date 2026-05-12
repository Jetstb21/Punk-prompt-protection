from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict


def audit_record(prompt: str, verdict: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "verdict": verdict,
    }
    payload["audit_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return payload
