
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IN_PATH = REPO_ROOT / "data" / "week-02" / "sample_evidence" / "mfa_policy_state.sample.json"
OUT_DIR = REPO_ROOT / "data" / "week-02" / "normalized_evidence"
OUT_PATH = OUT_DIR / "mfa_policy_state.normalized.json"

COLLECTOR_VERSION = "week-02-normalizer-v1"
COLLECTOR_NAME = "sample_collector"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.loads(IN_PATH.read_text(encoding="utf-8"))

    normalized = {
        "collected_at": utc_now_iso(),
        "collector": COLLECTOR_NAME,
        "collector_version": COLLECTOR_VERSION,
        "source": payload.get("source", "unknown"),
        "tenant_or_account": payload.get("tenant_or_account", "unknown"),
        "evidence_object": "mfa_policy_state",
        "payload": payload
    }

    OUT_PATH.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
    print(f"Wrote normalized evidence: {OUT_PATH}")

if __name__ == "__main__":
    main()
