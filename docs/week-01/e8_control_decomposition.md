# Essential Eight – Control Decomposition

Purpose:
To decompose Essential Eight strategies into atomic,
machine-testable control assertions suitable for continuous assurance.

## Decomposition Rules

- One assertion represents one test
- Assertions must be objectively pass or fail
- Assertions must not rely on screenshots
- Assertions must be testable via configuration, logs, or events
- Assertions must avoid audit or policy language

## Restrict Administrative Privileges
### Control Intent
Prevent unauthorised or excessive administrative access
that could allow compromise of systems or data.
### Control Scope
- All systems with administrative capability
- All user and service identities
- Cloud and SaaS platforms
### Atomic Control Assertions
RAP-01: No user accounts have permanent administrative privileges.

RAP-02: Administrative access is granted only through role-based mechanisms.

RAP-03: All administrative role assignments are logged centrally.

RAP-04: Administrative access configurations cannot be modified without approval.

## Multi-Factor Authentication
### Control Intent
Reduce the risk of unauthorised access by ensuring authentication strength is sufficient for the sensitivity of access being granted.
### Control Scope
- All interactive human user accounts
- All privileged and administrative access paths
- All systems and applications capable of enforcing MFA
### Atomic Control Assertions
MFA-01: All privileged user accounts require multi-factor authentication for interactive access.

MFA-02: Multi-factor authentication enforcement cannot be bypassed for privileged user accounts.

MFA-03: Only cryptographically strong authentication factors are permitted for multi-factor authentication.

MFA-04: All changes to multi-factor authentication configuration are logged centrally.

## Patch Operating Systems
### Control Intent
Reduce exposure to known vulnerabilities by ensuring operating systems are maintained at a supported and current patch level.
### Control Scope
- All organisation-managed operating systems
- All servers and endpoints running supported OS versions
- All production and non-production environments
### Atomic Control Assertions
POS-01: All supported operating systems have current security patches installed within a defined timeframe.

POS-02: No unsupported or end-of-life operating systems are in use.

POS-03: Operating system patch sources are restricted to trusted update mechanisms.

POS-04: Operating system patch failures are detected and recorded.
