import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]

EVIDENCE_DIR = REPO_ROOT / "data" / "week-03" / "aws_normalised_evidence"
OUT_DIR = REPO_ROOT / "data" / "week-04" / "evaluation_results"

IAM_USERS_FILE = EVIDENCE_DIR / "iam_users.normalized.json"
IAM_POLICIES_FILE = EVIDENCE_DIR / "iam_policies.normalized.json"
IAM_ROLES_FILE = EVIDENCE_DIR / "iam_roles.normalized.json"

COLLECTOR = "week-04-evaluator"
COLLECTOR_VERSION = "week-04-lab4.2-v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_normalized(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_of(normalized: Dict[str, Any]) -> Dict[str, Any]:
    # Week 3 normalised evidence wrapper preserved raw payload under "raw_evidence"
    raw = normalized.get("raw_evidence")
    if raw is None:
        raise ValueError(f"Missing raw_evidence in {normalized.get('evidence_object', 'unknown')}")
    return raw


def iam_usernames(iam_users_payload: Dict[str, Any]) -> List[str]:
    # AWS iam list-users output usually has "Users": [ { "UserName": ... }, ...]
    users = iam_users_payload.get("Users", [])
    return [u.get("UserName") for u in users if u.get("UserName")]


def users_with_mfa_enabled(iam_users_payload: Dict[str, Any]) -> Set[str]:
    """
    [Unverified] AWS IAM 'list-users' does NOT include MFA device state.
    MFA device state usually comes from 'list-mfa-devices' per user.
    This function is a placeholder to keep Lab 4.2 structure consistent.

    For a working MFA-01 evaluator, you will need to add raw evidence collection:
      aws iam list-mfa-devices --user-name <user>   (for each user)
    and normalize those outputs in Week 3 or Week 4 evidence expansion.
    """
    return set()


def find_admin_equivalent_policies(iam_policies_payload: Dict[str, Any]) -> Set[str]:
    """
    Identify admin-equivalent policies by name.
    Deterministic and simple for Week 4: treat 'AdministratorAccess' as admin-equivalent.
    """
    policies = iam_policies_payload.get("Policies", [])
    admin_names = {"AdministratorAccess"}
    return {p.get("PolicyName") for p in policies if p.get("PolicyName") in admin_names}


def eval_rap_02() -> Dict[str, Any]:
    """
    RAP-02: Administrative access is granted only through role-based mechanisms.

    [Unverified] With only 'list-users', 'list-roles', and 'list-policies', we cannot
    deterministically prove direct policy attachments to users or role assumption paths.
    That requires:
      - aws iam list-attached-user-policies (per user)
      - aws iam list-user-policies (inline)
      - aws iam list-attached-role-policies (per role)
    So this evaluator will output INFORMATIONAL until that evidence exists.
    """
    users_norm = load_normalized(IAM_USERS_FILE)
    policies_norm = load_normalized(IAM_POLICIES_FILE)
    roles_norm = load_normalized(IAM_ROLES_FILE)

    users_payload = payload_of(users_norm)
    policies_payload = payload_of(policies_norm)
    _roles_payload = payload_of(roles_norm)

    admin_equiv = find_admin_equivalent_policies(policies_payload)
    all_users = iam_usernames(users_payload)

    result = {
        "assertion_id": "RAP-02",
        "evaluated_at": utc_now_iso(),
        "result": "INFORMATIONAL",
        "reason": (
            "Insufficient evidence to determine whether admin privileges are granted "
            "only via role-based mechanisms. Need user/role policy attachment evidence."
        ),
        "affected_objects": [],
        "evidence_refs": [
            IAM_USERS_FILE.name,
            IAM_POLICIES_FILE.name,
            IAM_ROLES_FILE.name,
        ],
        "metadata": {
            "admin_equivalent_policies_detected": sorted(list(admin_equiv)),
            "users_observed_count": len(all_users),
            "collector": COLLECTOR,
            "collector_version": COLLECTOR_VERSION,
        },
    }
    return result


def eval_mfa_01() -> Dict[str, Any]:
    """
    MFA-01: All privileged user accounts require MFA for interactive access.

    [Unverified] Privileged set depends on RAP-02 and/or attachment data.
    With current evidence, we cannot determine privileged users or MFA state deterministically.
    Output INFORMATIONAL until evidence is expanded.
    """
    users_norm = load_normalized(IAM_USERS_FILE)
    users_payload = payload_of(users_norm)

    all_users = iam_usernames(users_payload)
    mfa_enabled = users_with_mfa_enabled(users_payload)  # placeholder empty set

    result = {
        "assertion_id": "MFA-01",
        "evaluated_at": utc_now_iso(),
        "result": "INFORMATIONAL",
        "reason": (
            "Insufficient evidence to evaluate MFA for privileged users. Need privileged user "
            "identification (policy attachments) and MFA device state evidence."
        ),
        "affected_objects": [],
        "evidence_refs": [
            IAM_USERS_FILE.name,
        ],
        "metadata": {
            "users_observed_count": len(all_users),
            "users_with_mfa_evidence_count": len(mfa_enabled),
            "collector": COLLECTOR,
            "collector_version": COLLECTOR_VERSION,
        },
    }
    return result


def write_result(filename: str, obj: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / filename
    out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print(f"Wrote result: {out_path}")


def main() -> None:
    rap02 = eval_rap_02()
    mfa01 = eval_mfa_01()

    write_result("rap-02.result.json", rap02)
    write_result("mfa-01.result.json", mfa01)


if __name__ == "__main__":
    main()
