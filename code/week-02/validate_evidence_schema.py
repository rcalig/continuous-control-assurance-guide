import json
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = REPO_ROOT / "data" / "week-02" / "evidence_schemas" / "schema_mfa_policy_state.json"
EVIDENCE_PATH = REPO_ROOT / "data" / "week-02" / "sample_evidence" / "mfa_policy_state.sample.json"

def main() -> int:
    print("Validator started.")
    print(f"Schema path: {SCHEMA_PATH}")
    print(f"Evidence path: {EVIDENCE_PATH}")

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
    except Exception as e:
        print("ERROR: Unexpected exception.")
        print(str(e))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
