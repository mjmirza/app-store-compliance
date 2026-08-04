# Security Policy

## What this repository is, and what it is not

This is a documentation and tooling playbook. It ships Markdown references, JSON data files, shell and Python scripts that read a project and report findings. It does not run a service, hold user data, or handle credentials.

That shapes what counts as a security issue here.

## Supported versions

The default branch is the only supported version. Fixes land on `master` and are not backported.

## Reporting a vulnerability

Report privately through GitHub's [Report a vulnerability](https://github.com/mjmirza/app-store-compliance/security/advisories/new) form. That opens a private advisory visible only to the maintainer.

Do not open a public issue for anything in the first list below.

Expect a first response within 7 days. If a fix is warranted, the advisory stays private until it lands, then it is published with credit unless you ask otherwise.

## Report privately

- Command injection or arbitrary code execution in any script under `scripts/` or `agent-os/hooks/`, for example a path or project name that reaches a shell unquoted
- Path traversal that lets an audited project write outside its own directory
- Any way a scanned project can make the guard exfiltrate data or reach the network unexpectedly
- A supply-chain problem in something the repository tells you to install or run
- Credentials or tokens committed anywhere in the tree or its history

## Open a normal public issue

- A wrong, stale, or missing guideline reference
- A rejection pattern that misfires or never fires
- A broken citation link
- A false positive or false negative from a monitor
- Anything about how a policy is worded or explained

Accuracy problems are the most valuable reports this project receives, and they belong in the open where others can see them.

## Running the tooling safely

The guard and the monitors read files and make outbound requests to official Apple, Google, and EU sources. Review any script before running it against a private codebase, as you would with any third-party tooling.

Reports produced in `--simulate` mode contain illustrative sample data, not live announcements. Never treat simulate output as a real requirement.
