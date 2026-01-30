import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from typing import Dict, Any, List


REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "week-03" / "aws_raw_evidence" / "iam"
OUT_DIR = REPO_ROOT / "data" / "week-03" / "aws_normalised_evidence"

COLLECTOR = "aws_cli"
COLLECTOR_VERSION = "week-03-iam-extension-v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def aws_account_id() -> str:
    out = subprocess.check_output(["aws", "sts", "get-caller-identity"], text=True)
    return json.loads(out).get("Account", "unknown")


def aws_region() -> str:
    out = subprocess.check_output(["aws", "configure", "get", "region"], text=True).strip()
    return out or "unknown"


def wrap(evidence_object: str, evidence_type: str, related_assertions: List[str], payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "collected_at": utc_now_iso(),
        "collector": COLLECTOR,
        "collector_version": COLLECTOR_VERSION,
        "cloud_account": aws_account_id(),
        "region": aws_region(),
        "evidence_object": evidence_object,
        "evidence_type": evidence_type,
        "related_assertions": related_assertions,
        "raw_evidence": payload,
    }


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Aggregate: user -> attached managed policies
    user_attached: Dict[str, Any] = {}
    for p in RAW_DIR.glob("user_*_attached_policies.json"):
        # filename: user_<USER>_attached_policies.json
        name = p.name
        user = name[len("user_") : -len("_attached_policies.json")]
        user_attached[user] = load_json(p)

    # Aggregate: user -> MFA devices
    user_mfa: Dict[str, Any] = {}
    for p in RAW_DIR.glob("user_*_mfa_devices.json"):
        name = p.name
        user = name[len("user_") : -len("_mfa_devices.json")]
        user_mfa[user] = load_json(p)

    # Aggregate: role -> attached managed policies
    role_attached: Dict[str, Any] = {}
    for p in RAW_DIR.glob("role_*_attached_policies.json"):
        name = p.name
        role = name[len("role_") : -len("_attached_policies.json")]
        role_attached[role] = load_json(p)

    # Write normalised evidence objects
    (OUT_DIR / "iam_user_policy_attachments.normalized.json").write_text(
        json.dumps(
            wrap(
                evidence_object="iam_user_policy_attachments",
                evidence_type="configuration_state",
                related_assertions=["RAP-02", "RAP-01"],
                payload={"users": user_attached},
            ),
            indent=2,
        ),
        encoding="utf-8",
    )

    (OUT_DIR / "iam_user_mfa_devices.normalized.json").write_text(
        json.dumps(
            wrap(
                evidence_object="iam_user_mfa_devices",
                evidence_type="configuration_state",
                related_assertions=["MFA-01"],
                payload={"users": user_mfa},
            ),
            indent=2,
        ),
        encoding="utf-8",
    )

    (OUT_DIR / "iam_role_policy_attachments.normalized.json").write_text(
        json.dumps(
            wrap(
                evidence_object="iam_role_policy_attachments",
                evidence_type="configuration_state",
                related_assertions=["RAP-02"],
                payload={"roles": role_attached},
            ),
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Wrote:")
    print(f"- {OUT_DIR / 'iam_user_policy_attachments.normalized.json'}")
    print(f"- {OUT_DIR / 'iam_user_mfa_devices.normalized.json'}")
    print(f"- {OUT_DIR / 'iam_role_policy_attachments.normalized.json'}")


if __name__ == "__main__":
    main()
