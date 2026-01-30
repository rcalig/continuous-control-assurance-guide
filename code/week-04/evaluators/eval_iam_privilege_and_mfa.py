import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set


REPO_ROOT = Path(__file__).resolve().parents[3]

EVIDENCE_DIR = REPO_ROOT / "data" / "week-03" / "aws_normalised_evidence"
OUT_DIR = REPO_ROOT / "data" / "week-04" / "evaluation_results"

USER_ATTACH_FILE = EVIDENCE_DIR / "iam_user_policy_attachments.normalized.json"
USER_MFA_FILE = EVIDENCE_DIR / "iam_user_mfa_devices.normalized.json"
ROLE_ATTACH_FILE = EVIDENCE_DIR / "iam_role_policy_attachments.normalized.json"

COLLECTOR = "week-04-evaluator"
COLLECTOR_VERSION = "week-04-lab4.2-v2"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_normalized(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def payload_of(normalized: Dict[str, Any]) -> Dict[str, Any]:
    raw = normalized.get("raw_evidence")
    if raw is None:
        raise ValueError(f"Missing raw_evidence in {path}")
    return raw


def is_admin_equivalent_policy(policy_name: str, policy_arn: str) -> bool:
    # Deterministic starting point for RAP-02:
    # treat AWS-managed AdministratorAccess as admin-equivalent.
    if policy_name == "AdministratorAccess":
        return True
    if policy_arn.endswith(":policy/AdministratorAccess"):
        return True
    return False


def users_with_direct_admin_policies(user_attach_payload: Dict[str, Any]) -> Set[str]:
    offending: Set[str] = set()
    users = user_attach_payload.get("users", {})

    for username, attach_doc in users.items():
        attached = attach_doc.get("AttachedPolicies", [])
        for p in attached:
            name = p.get("PolicyName", "")
            arn = p.get("PolicyArn", "")
            if is_admin_equivalent_policy(name, arn):
                offending.add(username)
                break

    return offending


def users_with_mfa(user_mfa_payload: Dict[str, Any]) -> Set[str]:
    enabled: Set[str] = set()
    users = user_mfa_payload.get("users", {})

    for username, mfa_doc in users.items():
        devices = mfa_doc.get("MFADevices", [])
        if isinstance(devices, list) and len(devices) > 0:
            enabled.add(username)

    return enabled


def eval_rap_02(user_attach_payload: Dict[str, Any], role_attach_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    RAP-02: Administrative access is granted only through role-based mechanisms.

    PASS  -> no users have admin-equivalent policy directly attached
    FAIL  -> one or more users have admin-equivalent policy directly attached

    [Unverified] This evaluator checks direct user policy attachments only.
    It does not yet evaluate group-based admin or external IdP role assignment.
    """
    offenders = sorted(list(users_with_direct_admin_policies(user_attach_payload)))

    if offenders:
        result = "FAIL"
        reason = "Direct admin-equivalent privilege attached to user(s)"
        affected = offenders
    else:
        result = "PASS"
        reason = "No direct admin-equivalent privilege attached to any user"
        affected = []

    # role_attach_payload is loaded to keep evidence lineage explicit, even if not needed for PASS/FAIL yet.
    role_count = len(role_attach_payload.get("roles", {}))

    return {
        "assertion_id": "RAP-02",
        "evaluated_at": utc_now_iso(),
        "result": result,
        "reason": reason,
        "affected_objects": affected,
        "evidence_refs": [USER_ATTACH_FILE.name, ROLE_ATTACH_FILE.name],
        "metadata": {
            "roles_observed_count": role_count,
            "collector": COLLECTOR,
            "collector_version": COLLECTOR_VERSION,
        },
    }


def eval_mfa_01(user_attach_payload: Dict[str, Any], user_mfa_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MFA-01: All privileged user accounts require MFA for interactive access.

    Privileged users (Week 4 definition for determinism):
    - users with direct admin-equivalent policy attached

    PASS -> all privileged users have at least one MFA device
    FAIL -> any privileged user has zero MFA devices
    NOT_APPLICABLE -> no privileged users detected under this definition

    [Unverified] This definition does not include role-assumed or group-based admin users yet.
    """
    privileged = users_with_direct_admin_policies(user_attach_payload)
    if not privileged:
        return {
            "assertion_id": "MFA-01",
            "evaluated_at": utc_now_iso(),
            "result": "NOT_APPLICABLE",
            "reason": "No privileged users detected under current privileged-user definition",
            "affected_objects": [],
            "evidence_refs": [USER_ATTACH_FILE.name, USER_MFA_FILE.name],
            "metadata": {"collector": COLLECTOR, "collector_version": COLLECTOR_VERSION},
        }

    mfa_enabled = users_with_mfa(user_mfa_payload)
    lacking = sorted([u for u in privileged if u not in mfa_enabled])

    if lacking:
        result = "FAIL"
        reason = "Privileged user(s) lack MFA devices"
        affected = lacking
    else:
        result = "PASS"
        reason = "All privileged users have MFA devices"
        affected = []

    return {
        "assertion_id": "MFA-01",
        "evaluated_at": utc_now_iso(),
        "result": result,
        "reason": reason,
        "affected_objects": affected,
        "evidence_refs": [USER_ATTACH_FILE.name, USER_MFA_FILE.name],
        "metadata": {
            "privileged_user_count": len(privileged),
            "collector": COLLECTOR,
            "collector_version": COLLECTOR_VERSION,
        },
    }


def write_result(filename: str, obj: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / filename
    out_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print(f"Wrote result: {out_path}")


def main() -> None:
    user_attach_norm = load_normalized(USER_ATTACH_FILE)
    user_mfa_norm = load_normalized(USER_MFA_FILE)
    role_attach_norm = load_normalized(ROLE_ATTACH_FILE)

    user_attach_payload = user_attach_norm.get("raw_evidence", {})
    user_mfa_payload = user_mfa_norm.get("raw_evidence", {})
    role_attach_payload = role_attach_norm.get("raw_evidence", {})

    rap02 = eval_rap_02(user_attach_payload, role_attach_payload)
    mfa01 = eval_mfa_01(user_attach_payload, user_mfa_payload)

    write_result("rap-02.result.json", rap02)
    write_result("mfa-01.result.json", mfa01)


if __name__ == "__main__":
    main()
