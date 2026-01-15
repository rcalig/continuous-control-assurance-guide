# Essential Eight – Maturity Translation

Purpose:
To translate maturity levels into enforceable control expectations.

## Multi-Factor Authentication
### Base Assertions
MFA-01: All privileged user accounts require multi-factor authentication for interactive access.
MFA-02: Multi-factor authentication enforcement cannot be bypassed for privileged user accounts.
MFA-03: Only cryptographically strong authentication factors are permitted for multi-factor authentication.
MFA-04: All changes to multi-factor authentication configuration are logged centrally.

### Maturity Level 1
- MFA is enforced for privileged user accounts.
- MFA configuration exists and is active for privileged access.
- MFA configuration changes are logged centrally.

### Maturity Level 2
- MFA is enforced for privileged and remote user access.
- MFA enforcement cannot be bypassed through exclusions or conditional rules.
- Only strong authentication factors are permitted for MFA.

### Maturity Level 3
- MFA is enforced for all interactive users.
- MFA enforcement is centrally governed and immutable by end users.
- MFA failures, changes, and anomalies generate alerts and are monitored continuously.

## Restrict Administrative Privileges
### Base Assertions
RAP-01: No user accounts have permanent administrative privileges.
RAP-02: Administrative access is granted only through role-based mechanisms.
RAP-03: All administrative role assignments are logged centrally.
RAP-04: Administrative access configurations cannot be modified without approval.

### Maturity Level 1
- Administrative privileges are assigned using role-based mechanisms.
- Direct user-based administrative privilege assignments are not permitted.
- Administrative role assignment events are logged centrally.

### Maturity Level 2
- Administrative privileges are time-bound or session-based.
- Administrative roles are scoped to specific functions.
- Administrative access configuration changes are centrally controlled and logged.

### Maturity Level 3
- Administrative privileges are ephemeral by default.
- Standing administrative access is technically prevented.
- Unexpected administrative privilege use generates alerts and is monitored continuously.

## Patch Operating Systems
### Base Assertions
POS-01: All supported operating systems have current security patches installed within a defined timeframe.
POS-02: No unsupported or end-of-life operating systems are in use.
POS-03: Operating system patch sources are restricted to trusted update mechanisms.
POS-04: Operating system patch failures are detected and recorded.

### Maturity Level 1
- Security patches are applied to supported operating systems within a defined timeframe.
- Unsupported or end-of-life operating systems are identified.
- Operating systems use trusted update mechanisms.
- Patch failures are recorded.

### Maturity Level 2
- Security patches are applied within a tighter, consistently enforced timeframe.
- Unsupported or end-of-life operating systems are actively remediated.
- Patch sources are technically restricted and cannot be overridden by users.
- Patch failures are detected and tracked for remediation.

### Maturity Level 3
- Operating system patch compliance is evaluated continuously.
- Newly introduced unsupported or end-of-life operating systems are detected automatically.
- Patch source integrity is continuously validated.
- Patch failures generate alerts and are monitored continuously.
