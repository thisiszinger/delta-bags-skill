# Delta Bags

Delta Bags is an unofficial Agent Skill for handling Delta Air Lines' 20-Minute Bag Guarantee Request. Tell a capable agent that your checked bag took more than 20 minutes, review one concise confirmation, and let the agent submit the public Delta form.

The project is in beta. Its instruction and fallback-state paths are tested, but the complete browser flow remains unvalidated until a genuine eligible late-bag event occurs.

## What it handles

- Finds the Affected Flight from calendar and Delta email when those capabilities are available.
- Re-checks Delta's live policy and public form before every request.
- Supports a Default Traveler and separately attested companions in a Request Batch.
- Uses one confirmation before submitting a separate form for each Requesting Traveler.
- Reports Delta's exact result without treating receipt as approval.
- Falls back to asking for the seven form fields or preparing a manual handoff when integrations are unavailable.
- Optionally retains Traveler Profiles and a 30-day duplicate ledger outside the repository.

The canonical portable skill is [skills/delta-bags](skills/delta-bags). It follows the [Agent Skills specification](https://agentskills.io/specification) and uses semantic capabilities instead of binding its workflow to one host's tool names.

## Install

Delta Bags is [listed on skills.sh](https://skills.sh/thisiszinger/delta-bags-skill/delta-bags). Install it with the cross-agent `skills` CLI; no clone or global CLI installation is required:

```sh
npx skills add thisiszinger/delta-bags-skill --skill delta-bags
```

The interactive installer detects supported agents and asks whether to install for the current project or for the current user. To install globally for both Claude Code and Codex without prompts, run:

```sh
npx skills add thisiszinger/delta-bags-skill --skill delta-bags --global --agent claude-code --agent codex --yes
```

Verify or update the global installation later with:

```sh
npx skills list --global
npx skills update delta-bags --global --yes
```

For a project-only installation, omit `--global`. The installer writes the appropriate agent directories and records the source in `skills-lock.json` so updates remain traceable.

GitHub CLI users can install the latest tagged release instead. Repeat with `--agent claude-code` for Claude Code, or add `--pin v0.1.0` for a reproducible version:

```sh
gh skill install thisiszinger/delta-bags-skill delta-bags --agent codex --scope user
```

### ChatGPT and Codex

The installer places the skill where Codex can discover it. Invoke it as `$delta-bags`, or describe a late Delta baggage delivery and allow implicit matching.

For a manual installation, copy or symlink `skills/delta-bags` to `~/.agents/skills/delta-bags` for personal use or `.agents/skills/delta-bags` inside a repository. Standalone skills are also supported by the ChatGPT desktop app. See the official [ChatGPT and Codex skills documentation](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

The installer places the skill in Claude Code's skills directory. Invoke `/delta-bags` or use natural language.

For a manual installation, copy or symlink `skills/delta-bags` to `~/.claude/skills/delta-bags` for personal use or `.claude/skills/delta-bags` for a project. See [Claude Code skills](https://code.claude.com/docs/en/skills).

Claude Code users can alternatively install the native plugin directly from this repository:

```sh
claude plugin marketplace add thisiszinger/delta-bags-skill
claude plugin install delta-bags@delta-bags-skill
```

The plugin-scoped invocation is `/delta-bags:delta-bags`; natural-language matching also works.

### Gemini CLI

Install the skill directory from this repository:

```sh
gemini skills install https://github.com/thisiszinger/delta-bags-skill --path skills/delta-bags
```

See [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/).

### Cursor and GitHub Copilot

Copy or symlink the directory to a supported project or user skills location. Cursor supports `.agents/skills` and `.cursor/skills`; GitHub Copilot supports `.github/skills`, `.agents/skills`, and `.claude/skills` in documented environments.

- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

## Discovery and marketplaces

- **skills.sh:** the public listing is live. There is no separate submission form; public installs through the `skills` CLI provide the anonymous aggregate data used for search and ranking.
- **Claude:** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` make the repository installable as a native Claude Code plugin today. A maintainer must still submit it through [Anthropic's plugin form](https://platform.claude.com/plugins/submit) for centralized discovery; [issue #2](https://github.com/thisiszinger/delta-bags-skill/issues/2) tracks that human review step. Approval places it in the `claude-community` catalog; Anthropic curates its separate official catalog independently.
- **ChatGPT and Codex:** `.codex-plugin/plugin.json` packages the same skill as an OpenAI skills-only plugin. A verified publisher must still submit the bundle, listing assets, policy URLs, prompts, and review tests through the [OpenAI plugin portal](https://platform.openai.com/plugins); [issue #3](https://github.com/thisiszinger/delta-bags-skill/issues/3) tracks the prerequisites. Once approved and published, it appears in the shared ChatGPT and Codex Plugins Directory.

The manifests are distribution wrappers only. They both point at the canonical `skills/` directory, so marketplace installs and direct skill installs use the same implementation.

See [the distribution research](docs/research/skill-distribution-and-discovery.md) for the verified channel requirements, paths, and source links.

## Capability support

The Agent Skills standard packages instructions and resources; it does not install email, calendar, browser, authentication, or private-storage connectors.

| Host | Skill loading | Full workflow status |
| --- | --- | --- |
| ChatGPT desktop | Standalone skill | Works with available equivalent capabilities; end-to-end beta validation pending |
| Codex CLI / IDE | Native `.agents/skills` discovery | Works with available equivalent capabilities; end-to-end beta validation pending |
| Claude Code | Native `.claude/skills` discovery | Works with equivalent tools; end-to-end beta validation pending |
| Gemini CLI | Native Agent Skills support | Works with equivalent tools; end-to-end beta validation pending |
| Cursor | Native Agent Skills support | Guided or automated according to available tools; end-to-end beta validation pending |
| GitHub Copilot | Native Agent Skills support in documented surfaces | Usually a prepared/manual handoff without an authenticated interactive browser |

Every host can use the manual field fallback. A host without browser interaction must stop after preparing verified values and the official form link.

## Private state

Prefer the agent host's existing private store. If none exists, the optional standard-library helper stores plaintext JSON in platform-native per-user locations:

| Platform | Profiles | Duplicate ledger |
| --- | --- | --- |
| Linux | `~/.config/delta-bags/profiles.json` | `~/.local/state/delta-bags/submissions.json` |
| macOS | `~/Library/Application Support/delta-bags/profiles.json` | `~/Library/Application Support/delta-bags/submissions.json` |
| Windows | `%APPDATA%\delta-bags\profiles.json` | `%LOCALAPPDATA%\delta-bags\submissions.json` |

The helper never stores a Confirmation Number. See [the storage reference](skills/delta-bags/references/storage.md) for schemas and commands.

## Develop

Run the local test suite:

```sh
python -m unittest discover -s tests -v
```

Run the skill validator from OpenAI's `skill-creator` when available:

```sh
python /path/to/skill-creator/scripts/quick_validate.py skills/delta-bags
```

Run the opt-in live smoke check only when you want to verify Delta's public content:

```sh
python skills/delta-bags/scripts/live_smoke.py
```

The smoke check performs two public GET requests and has no submission code. Automated CI uses local fixtures only; the networked workflow is manual.

Development is tracked in [GitHub Issues](https://github.com/thisiszinger/delta-bags-skill/issues). The initial beta specification is [issue #1](https://github.com/thisiszinger/delta-bags-skill/issues/1).

## Disclaimer

Delta Bags is an independent open-source project. It is not affiliated with, endorsed by, or sponsored by Delta Air Lines. Delta determines eligibility and awards. Policies and forms can change without notice, so the skill fails closed when it cannot verify the live terms.

## License

[MIT](LICENSE)
