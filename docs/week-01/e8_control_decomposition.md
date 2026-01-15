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
### Control Scope
### Atomic Control Assertions

## Patch Operating Systems
### Control Intent
### Control Scope
### Atomic Control Assertions
