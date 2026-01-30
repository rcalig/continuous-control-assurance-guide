import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "week-03" / "aws_raw_evidence"
OUT_DIR = REPO_ROOT / "data" / "week-03" / "aws_normalised_evidence"

COLLECTOR = "aws_cli"
COLLECTOR_VERSION = "week-03-lab3.2-v1"
EVIDENCE_TYPE = "configuration_state"

# [Unverified] Update these to match your Week 1 assertion IDs
RELATED_ASSERTIONS = ["RAP-01", "RAP-02", "RAP-03", "MFA-01"]

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def aws_account_id() -> str:
    out = subprocess.check_output(["aws", "sts", "get-caller-identity"], text=True)
    return json.loads(out).get("Account", "unknown")

def aws_region() -> str:
    out = subprocess.check_output(["aws", "configure", "get", "region"], text=True).strip()
    return out or "unknown"

def wrap(raw_filename: str) -> dict:
    payload = json.loads((RAW_DIR / raw_filename).read_text(encoding="utf-8"))
    return {
        "collected_at": utc_now_iso(),
        "collector": COLLECTOR,
        "collector_version": COLLECTOR_VERSION,
        "cloud_account": aws_account_id(),
        "region": aws_region(),
        "evidence_object": raw_filename.replace(".json", ""),
        "evidence_type": EVIDENCE_TYPE,
        "related_assertions": RELATED_ASSERTIONS,
        "raw_evidence": payload,
    }

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    mapping = {
        "iam_users.json": "iam_users.normalized.json",
        "iam_roles.json": "iam_roles.normalized.json",
        "iam_policies.json": "iam_policies.normalized.json",
        "iam_account_summary.json": "iam_account_summary.normalized.json",
    }

    for in_file, out_file in mapping.items():
        out_path = OUT_DIR / out_file
        out_path.write_text(json.dumps(wrap(in_file), indent=2), encoding="utf-8")
        print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
