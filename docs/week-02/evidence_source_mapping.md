| Assertion ID | Evidence Type | Evidence Source Category | Frequency | Output | Notes |
|---|---|---|---|---|---|
| MFA-01 | configuration_state | SaaS IAM / IdP config | daily | JSON | interactive privileged access only |
| MFA-04 | audit_events | IdP audit logs | continuous | JSON | include actor, action, timestamp |
| RAP-01 | identity_inventory | IAM roles/groups | daily | JSON | identify permanent admin assignment |
| POS-02 | patch_inventory | endpoint/server inventory | daily | JSON | must include OS version + support status |
