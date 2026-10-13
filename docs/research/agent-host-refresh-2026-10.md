# Agent host refresh (2026-10-13)

Research date: 2026-10-13. First-party documentation only; nothing was installed or submitted. This updates the August reports in [skill-distribution-and-discovery.md](skill-distribution-and-discovery.md) and [personal-agent-host-compatibility.md](personal-agent-host-compatibility.md).

## Summary

- The Agent Skills specification is unchanged since August: `name`, `description`, `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. Only wording clarifications landed. ([spec](https://agentskills.io/specification), [commits](https://github.com/agentskills/agentskills/commits/main/docs/specification.mdx))
- The Vercel `skills` CLI (v1.7.2 tested locally) now targets about 75 agents and gained `npx skills use <owner/repo>@<skill>`, which prints a one-shot prompt containing the skill without installing it. ([README](https://github.com/vercel-labs/skills))
- `gh skill install` accepts about 48 `--agent` IDs. ([manual](https://cli.github.com/manual/gh_skill_install))
- ClawHub is live. OpenClaw installs with `openclaw skills install skills-sh:owner/repo/slug` or `@owner/slug`. ([docs](https://docs.openclaw.ai/tools/skills))
- Grok Build docs no longer show `grok plugin install`; plugins come from the Marketplace tab, `.grok/plugins/`, or `--plugin-dir`. Skills load from `.grok/skills/`, `~/.grok/skills/`, and `~/.agents/skills/`. Grok Bot still has no documented external package import. ([docs](https://docs.x.ai/build/features/skills-plugins-marketplaces))
- Gemini CLI docs say the Antigravity CLI replaced Gemini CLI for unpaid and Google One users on 2026-06-18; both read `.agents/skills/`. ([Gemini CLI](https://geminicli.com/docs/cli/skills/), [Antigravity](https://antigravity.google/docs/skills))
- Codex skill docs moved to [learn.chatgpt.com](https://learn.chatgpt.com/docs/build-skills). Discovery: `.agents/skills`, `~/.agents/skills`, `/etc/codex/skills`.
- `.agents/skills/` has become the de facto shared project path: Codex, Cursor, Copilot, Devin, Amp, OpenCode, Warp, Zed, Junie, Roo, Vibe, Hermes (after `hermes skills trust`), and Antigravity all read it. Claude Code does not; it reads `.claude/skills/`.

## Hosts with documented SKILL.md support (October 2026)

| Agent | Project path | User path | Install command or UI | Docs |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `claude plugin install` from a marketplace | [link](https://code.claude.com/docs/en/skills) |
| Claude.ai / Cowork | — | Upload zip | Customize › Skills › Upload | [link](https://support.claude.com/en/articles/12512180-use-skills-in-claude) |
| ChatGPT / Codex | `.agents/skills/` | `~/.agents/skills/` | `$skill-installer` | [link](https://learn.chatgpt.com/docs/build-skills) |
| Gemini CLI | `.agents/skills/`, `.gemini/skills/` | `~/.gemini/skills/` | `gemini skills install <git-url> --path` | [link](https://geminicli.com/docs/cli/skills/) |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` | `agy plugin install` | [link](https://antigravity.google/docs/skills) |
| Cursor | `.cursor/skills/`, `.agents/skills/` | `~/.agents/skills/` | — | [link](https://cursor.com/docs/context/skills) |
| GitHub Copilot | `.github/skills/`, `.agents/skills/` | `~/.copilot/skills/` | `gh skill install` | [link](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Hermes Agent | `.hermes/skills/`, `.agents/skills/` | `~/.hermes/skills/` | `hermes skills install skills-sh/...` | [link](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| OpenClaw | workspace skills | `~/.openclaw/skills/` | `openclaw skills install` | [link](https://docs.openclaw.ai/tools/skills) |
| Grok Build | `.grok/skills/` | `~/.grok/skills/`, `~/.agents/skills/` | Marketplace tab | [link](https://docs.x.ai/build/features/skills-plugins-marketplaces) |
| Amp | `.agents/skills/` | `~/.config/agents/skills/` | `amp skill add <source>` | [link](https://ampcode.com/docs/customize/skills) |
| OpenCode | `.opencode/skills/`, `.agents/skills/` | `~/.config/opencode/skills/` | — | [link](https://opencode.ai/docs/skills/) |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` | IDE import from GitHub URL | [link](https://kiro.dev/docs/skills/) |
| Devin | `.devin/skills/`, `.agents/skills/` | `~/.config/devin/skills/` | Cascade › Skills | [link](https://docs.devin.ai/cli/extensibility/skills/overview) |
| Factory Droid | `.factory/skills/`, `.agents/skills/` | `~/.factory/skills/` | `/skills` | [link](https://docs.factory.com/cli/configuration/skills) |
| Cline | `.cline/skills/` | `~/.cline/skills/` | Skills tab | [link](https://docs.cline.bot/features/skills) |
| Roo Code | `.roo/skills/`, `.agents/skills/` | `~/.roo/skills/` | — | [link](https://roocodeinc.github.io/Roo-Code/features/skills) |
| Warp | `.agents/skills/`, `.warp/skills/` | `~/.agents/skills/` | `/open-skill` | [link](https://docs.warp.dev/agent-platform/warp-agents/skills) |
| Zed | `.agents/skills/` | `~/.agents/skills/` | `agent: create skill from url` | [link](https://zed.dev/docs/ai/skills) |
| JetBrains Junie | `.junie/skills/`, `.agents/skills/` | `~/.junie/skills/` | `/skills` | [link](https://junie.jetbrains.com/docs/agent-skills.html) |
| Mistral Vibe | `.vibe/skills/`, `.agents/skills/` | `~/.vibe/skills/` | — | [link](https://docs.mistral.ai/vibe/code/cli/skills) |
| Manus | — | Upload | Skills › Add › Import from GitHub | [link](https://manus.im/docs/features/skills.md) |
| Perplexity Computer | — | Upload zip | Skills page (partly unverified) | [link](https://docs.perplexity.ai/docs/agent-api/skills) |

Not supported per docs: Google Jules (AGENTS.md only). Goose is a `skills` CLI target but its skills doc was unreachable.

## Frontmatter rules that matter cross-host

- Claude Code truncates description plus `when_to_use` at 1,536 characters and ignores `license`, `compatibility`, and `metadata`.
- Claude.ai and the API reject names containing "anthropic" or "claude" and descriptions over 1,024 characters.
- Codex budgets the skill list at 2% of context and shortens descriptions first.
- Zed and Roo enforce the spec's name and description limits exactly.
- Grok treats only the literal `true` as `user-invocable`.

The current `delta-bags` frontmatter (name, description under 400 characters, license) satisfies all of these.
