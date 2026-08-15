# 0001: Keep a portable skill core

- Status: Accepted
- Date: 2026-08-15
- Issue: [#1](https://github.com/thisiszinger/delta-bags-skill/issues/1)

## Context

Agent Skills standardizes the instruction and resource container, but agent hosts expose email, calendar, browser, authentication, and private storage differently. Binding the workflow to one host would simplify its first integration while preventing the open-source skill from degrading usefully elsewhere. Building wrappers for every host before testing them would create unverified compatibility claims.

## Decision

Keep the canonical implementation in `skills/delta-bags/` with standard `SKILL.md` frontmatter, plain Markdown references, and semantic capability names.

Treat all external capabilities as optional. Ask for missing fields, prepare a browser handoff, or use an optional local state helper when a host lacks the corresponding integration.

Include OpenAI UI metadata without making the core workflow depend on it. Add host-specific plugin wrappers or connector declarations only after validating those packages on the target host.

Keep Delta-specific policy and form details localized, but wait for a second remotely automatable airline before introducing a provider registry or airline-adapter abstraction.

## Consequences

- The same skill directory can be installed by multiple Agent Skills hosts.
- Full automation depends on capabilities supplied by the host and user environment.
- Documentation must distinguish native skill loading from validated end-to-end automation.
- The beta ships no universal one-click plugin or bundled email/calendar/browser connector.
- A future second airline may require refactoring, but the implementation does not pay for a hypothetical abstraction today.
