import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


# -----------------------------
# Paths and constants
# -----------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]

EVIDENCE_DIR = REPO_ROOT / "data" / "week-03" / "aws_normalised_evidence"
OUT_DIR = REPO_ROOT / "data" / "week-04" / "evaluation_results"

CLOUDTRAIL_TRAILS_FILE = EVIDENCE_DIR / "cloudtrail_trails.normalized.json"
CLOUDTRAIL_STATUS_FILE = EVIDENCE_DIR / "cloudtrail_status.normalized.json"

COLLECTOR = "week-04-evaluator"
COLLECTOR_VERSION = "week-04-lab4.3-v1"


# -----------------------------
# Helpers
# -----------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_normalized(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_of(normalized: Dict[str, Any]) -> Dict[str, Any]:
    raw = normalized.get("raw_evidence")
    if raw is None:
        raise ValueError("Missing raw_evidence in normalised file")
    return raw


# -----------------------------
# RAP-03 evaluator
# -----------------------------

def eval_rap_03() -> Dict[str, Any]:
    """
    RAP-03: All administrative role assignments are logged centrally.

    Deterministic evaluation using CloudTrail presence and logging state.
    """

    trails_norm = load_normalized(CLOUDTRAIL_TRAILS_FILE)
    status_norm = load_normalized(CLOUDTRAIL_STATUS_FILE)

    trails_payload = payload_of(trails_norm)
    status_payload = payload_of(status_norm)

    trails = trails_payload.get("trailList", [])
    is_logging = status_payload.get("IsLogging", False)

    if not trails:
        result = "FAIL"
        reason = "No CloudTrail trails detected"
        affected = ["cloudtrail"]
    elif not is_logging:
        result = "FAIL"
        reason = "CloudTrail exists but logging is disabled"
        affected = ["cloudtrail"]
    else:
        result = "PASS"
        reason = "CloudTrail enabled and logging management events"
        affected = []

    return {
        "assertion_id": "RAP-03",
        "evaluated_at": utc_now_iso(),
        "result": result,
        "reason": reason,
        "affected_objects": affected,
        "evidence_refs": [
            CLOUDTRAIL_TRAILS_FILE.name,
            CLOUDTRAIL_STATUS_FILE.name,
        ],
        "metadata": {
            "trail_count": len(trails),
            "is_logging": is_logging,
            "collector": COLLECTOR,
            "collector_version": COLLECTOR_VERSION,
        },
    }


# -----------------------------
# Write result
# -----------------------------

def write_result(filename: str, obj: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / filename
    out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print(f"Wrote result: {out_path}")


def main() -> None:
    result = eval_rap_03()
    write_result("rap-03.result.json", result)


if __name__ == "__main__":
    main()
