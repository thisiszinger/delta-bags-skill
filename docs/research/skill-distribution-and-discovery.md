# Agent Skill Distribution and Discovery

Research checked: 2026-08-15. Sources are limited to current official Vercel, GitHub, Anthropic, and OpenAI documentation and source code. No skill was installed and no marketplace or directory submission was made.

## Current answer

`thisiszinger/delta-bags-skill` is already shaped correctly for standalone Agent Skill distribution: `skills/delta-bags/SKILL.md` has the required metadata, and the repository is public. It can be installed by the Vercel `skills` CLI today. It is also already indexed: its [direct skills.sh detail page](https://www.skills.sh/thisiszinger/delta-bags-skill/delta-bags) resolves as of the research date, although that does not establish that every search and ranking cache has refreshed.

The distribution systems should not be conflated:

| Channel | Is the existing skill tree sufficient? | How public discovery happens | Additional package or action |
| --- | --- | --- | --- |
| Vercel skills.sh | Yes | A successful, telemetry-enabled `npx skills add` from the public GitHub repository causes automatic indexing/ranking | None; `skills.sh.json` is optional display metadata |
| GitHub Agent Skills | Yes | Public repository conventions, the `agent-skills` topic, and optionally a tagged GitHub Release | `gh skill publish` can validate and create the topic/release, but does not submit elsewhere |
| Claude Code plugin directory | Yes for direct installation; review is still required for managed discovery | An own marketplace, or review into Anthropic's `claude-community` marketplace | This repo now includes the native manifest and marketplace; public-community submission is separate |
| OpenAI universal plugin directory | Yes for packaging; review is still required for listing | Review through the OpenAI submission portal | This repo now includes the OpenAI plugin manifest; portal materials and submission remain separate |

The implemented strategy retains `skills/delta-bags` as the canonical skill, documents the `npx skills` commands below, and wraps that same tree with thin Claude and OpenAI manifests. No `skills.sh.json` is needed for this single-skill repository.

## 1. Vercel skills.sh listing and ranking

### The listing trigger is install telemetry

Vercel's FAQ is explicit: skills appear automatically after users run `npx skills add <owner/repo>`; the anonymous install telemetry is what creates or updates leaderboard records. There is no documented skills.sh submission form, publisher registration step, or minimum install threshold. Ranking uses deduplicated install totals. ([skills.sh FAQ](https://www.skills.sh/docs/faq#how-do-i-get-my-skill-listed-on-the-leaderboard), [ranking documentation](https://www.skills.sh/docs#how-skills-are-ranked))

For a GitHub source, the CLI's current implementation sends install telemetry only after it has positively confirmed that the repository is public. The event includes the source, installed skill names, selected agents, scope, and skill-file mapping; telemetry can be disabled with `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1`. A telemetry-disabled install therefore installs the files but cannot provide the event that skills.sh documents as its listing trigger. ([Vercel install flow](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/add.ts#L1815-L1846), [telemetry implementation](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/telemetry.ts#L1-L21), [telemetry controls](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/README.md#telemetry))

The source must contain a discoverable `SKILL.md` whose YAML frontmatter has string `name` and `description` fields. The CLI searches standard locations including `skills/<name>/SKILL.md`; this repository satisfies those requirements. ([Vercel skill format and discovery](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/README.md#skill-format))

skills.sh may generate security audits after a skill's first install, and skills that fail every partner audit are excluded from public rankings. The docs publish cache intervals, but no guaranteed delay from the first telemetry event to search or leaderboard visibility. A resolvable detail-page URL should therefore not be treated as proof that every search and ranking surface has already refreshed. ([skills.sh About](https://www.skills.sh/about), [skills.sh API and caching](https://www.skills.sh/docs/api))

### What does not submit a skill to skills.sh

- A root `skills.sh.json` only controls how skills are grouped and described on an already-known repository page. Vercel says it is usually discovered after telemetry has seen the repository; it does not alter installation or `SKILL.md`. ([skills.sh customization](https://www.skills.sh/docs/customize))

- `gh skill publish` is a separate, public-preview GitHub CLI workflow. It validates skill structure and can guide the author through adding the `agent-skills` repository topic, creating a version tag, and creating a GitHub Release. GitHub does not describe it as a skills.sh, Claude, or OpenAI submission mechanism. ([GitHub `gh skill publish`](https://cli.github.com/manual/gh_skill_publish), [GitHub `gh skill` status](https://cli.github.com/manual/gh_skill))

- Vercel's “Official” skills view is a separately curated set of skills made by the organization responsible for the underlying technology. The official API documentation publishes no application route for that designation. ([skills.sh curated endpoint](https://www.skills.sh/docs/api#getapiv1skillscurated))

## 2. One-command installation for Claude Code and Codex

The official CLI supports multiple `--agent` flags, explicit `--skill` selection, project scope by default, `--global` for user scope, and `--yes` for noninteractive installation. ([Vercel CLI options](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/README.md#options))

Project scope:

```sh
npx skills add thisiszinger/delta-bags-skill \
  --skill delta-bags \
  --agent claude-code \
  --agent codex \
  --yes
```

User/global scope:

```sh
npx skills add thisiszinger/delta-bags-skill \
  --skill delta-bags \
  --agent claude-code \
  --agent codex \
  --global \
  --yes
```

With both agents selected and the default link mode, the current CLI uses one canonical copy and an agent-specific link:

| Scope | Canonical files used by Codex | Claude Code entry |
| --- | --- | --- |
| Project | `<project>/.agents/skills/delta-bags` | `<project>/.claude/skills/delta-bags` symlink to the canonical copy |
| Global | `$HOME/.agents/skills/delta-bags` | `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/delta-bags` symlink to the canonical copy |

This follows the CLI's canonical-store and install-mode implementation: Codex is classified as a universal `.agents/skills` consumer, while Claude Code targets `.claude/skills` and honors `CLAUDE_CONFIG_DIR` at global scope; selecting different target directories makes symlink mode the default. `--copy` creates independent copies at those effective paths instead, and the installer falls back to copying if linking fails. These path mechanics describe the two-agent commands above; a Claude-only installation can use a direct copy because it has only one target directory. ([agent definitions](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/agents.ts#L143-L151), [Codex/universal definitions](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/agents.ts#L210-L216), [canonical path logic](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/installer.ts#L98-L149), [mode selection](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/src/add.ts#L771-L800))

There is a documentation conflict here: Vercel's Supported Agents table says Codex's global path is `~/.codex/skills`, but the current CLI code routes universal Codex installs to `~/.agents/skills`. OpenAI's current documentation independently identifies `$HOME/.agents/skills` as the user-scope location and `.agents/skills` as the repository-scope location. The implementation and OpenAI documentation should take precedence over that Vercel table row. ([conflicting Vercel table](https://github.com/vercel-labs/skills/blob/c6f69c631292444cc541ac6d91e2226b0ff247da/README.md#supported-agents), [OpenAI skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills))

## 3. Claude Code plugin publication and discovery

Anthropic distinguishes standalone `.claude/skills` configuration from plugins: standalone skills suit personal or project use, while plugins are the shareable, versioned unit for community discovery. Plugin skills live at `skills/<skill>/SKILL.md`, next to a `.claude-plugin/plugin.json` manifest directory at the plugin root. ([Claude plugins versus standalone configuration](https://code.claude.com/docs/en/plugins#when-to-use-plugins-vs-standalone-configuration), [plugin structure](https://code.claude.com/docs/en/plugins-reference#plugin-directory-structure))

Two discovery routes exist:

1. An author can host an independent marketplace on GitHub by adding `.claude-plugin/marketplace.json`. Users register it with `/plugin marketplace add thisiszinger/delta-bags-skill` and then install `<plugin-name>@<marketplace-name>`. ([hosting a marketplace](https://code.claude.com/docs/en/plugin-marketplaces#host-on-github-recommended))

2. For Anthropic-managed public discovery, third-party authors submit to the `claude-community` marketplace through the Claude.ai or Console submission form. Anthropic directs authors to run `claude plugin validate`, applies automated safety screening, pins approved entries to a commit SHA, and refreshes the catalog nightly. The automatically registered `claude-plugins-official` marketplace is curated separately at Anthropic's discretion and has no application process. ([Anthropic community submission process](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace), [plugin discovery](https://code.claude.com/docs/en/discover-plugins))

This repository now includes `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. That makes the GitHub repository directly installable as the `delta-bags-skill` marketplace; it does not itself place the plugin in Anthropic's managed community catalog.

Current Anthropic product documentation conflicts with wording in the `anthropics/claude-plugins-official` repository README that describes the directory form as an official-marketplace submission route. The product docs explicitly say the form feeds `claude-community`, not `claude-plugins-official`; the current product docs are the safer authority for a submission decision. ([current submission documentation](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace), [conflicting repository README](https://github.com/anthropics/claude-plugins-official#submitting-plugins))

The Vercel `npx skills` install does not create a Claude plugin, register a marketplace, or make the package appear in `/plugin` discovery. Claude plugin metadata is independently required for those routes.

## 4. OpenAI standalone skill versus public plugin

OpenAI treats `SKILL.md` plus optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml` as a standalone skill. Standalone skills can be loaded locally by ChatGPT desktop, the Codex CLI, and the IDE extension. `agents/openai.yaml` supplies optional UI and dependency metadata; it is not a public-directory manifest. ([OpenAI skill format and metadata](https://learn.chatgpt.com/docs/build-skills))

OpenAI directs authors who need reusable public distribution to package the skill as a plugin. Plugins publish to a universal directory shared by supported ChatGPT and Codex surfaces; every native OpenAI plugin requires `.codex-plugin/plugin.json`, and a skills-only plugin points that manifest at the `skills/` directory. The IDE extension supports standalone skills but not plugins. ([skill distribution guidance](https://learn.chatgpt.com/docs/build-skills#distribute-skills-with-plugins), [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins))

Public submission is available as “Skills only” in the OpenAI portal. It requires Apps Management write permission, verified individual or business identity, listing details and assets, a final skill bundle, starter prompts, at least five positive and three negative test cases, availability information, and release notes; the uploaded bundle is scanned and reviewed. ([OpenAI submission workflow](https://developers.openai.com/plugins/deploy/submission))

OpenAI also accepts a skills-only Claude plugin archive containing `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md`; its portal converts the Claude manifest into `.codex-plugin/plugin.json`. Claude approval does not transfer, so OpenAI still performs its own review. This provides a packaging-reuse path, not a shared submission or approval path. ([OpenAI's Claude-plugin conversion guide](https://developers.openai.com/plugins/guides/submit-claude-plugin))

The repository now includes a native `.codex-plugin/plugin.json` pointing at the canonical `skills/` tree. It is therefore packaged for a skills-only submission, while public-directory discovery still requires the portal materials, review, approval, and publication described above.

## Conflicts and safe interpretation

| Apparent conflict | Safe interpretation |
| --- | --- |
| Telemetry versus a skills.sh submission form | Telemetry is the documented listing trigger; no form is documented. |
| skills.sh's short privacy summary versus emitted telemetry fields | The current CLI source shows agent, scope, URL/source, and skill-file metadata in addition to skill names; use the documented opt-outs if that distinction matters. |
| `skills.sh.json` versus publishing | The file customizes an existing repository page only. |
| `gh skill publish` versus marketplace publishing | It publishes GitHub topic/release metadata only. It does not submit to skills.sh, Claude, or OpenAI. |
| Vercel Codex path `~/.codex/skills` versus current code | Use `~/.agents/skills`; that matches both current CLI behavior and OpenAI documentation. |
| `npx skills` install versus vendor plugin discovery | The CLI installs standalone files. Claude and OpenAI directories require plugin packaging and their own review flows. |
| Claude “official” versus “community” form wording | Current product docs route third-party submissions to `claude-community`; `claude-plugins-official` remains discretionary. |
| Claude plugin approval versus OpenAI plugin approval | Packaging can be reused, but review and approval do not transfer. |
