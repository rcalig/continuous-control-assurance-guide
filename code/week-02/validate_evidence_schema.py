import json
import sys
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "data" / "week-02" / "evidence_schemas" / "schema_mfa_policy_state.json"
EVIDENCE_PATH = REPO_ROOT / "data" / "week-02" / "sample_evidence" / "mfa_policy_state.sample.json"

def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))

try:
    validate(instance=evidence, schema=schema)
    print("PASS: Evidence matches schema.")
    return 0
except ValidationError as e:
    print("FAIL: Evidence does not match schema.")
    print(f"Reason: {e.message}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

