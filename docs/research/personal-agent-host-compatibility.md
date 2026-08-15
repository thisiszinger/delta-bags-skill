# Personal-agent host compatibility

Research date: 2026-08-15

This report covers the products most plausibly meant by “Hermes Agent,”
“OpenClaw,” and “the new Grok Bot.” It uses first-party documentation,
first-party repositories, and local CLI verification only.

## Executive conclusion

| Host | Can use the current portable skill? | Best install/discovery path | Delta Bags capability fit |
| --- | --- | --- | --- |
| Hermes Agent | Yes. Hermes follows the Agent Skills format and can install the repository's nested skill from skills.sh or GitHub. | `hermes skills install skills-sh/thisiszinger/delta-bags-skill/delta-bags` | Strong: browser automation, Google email/calendar integration, local files, memory, and interactive clarification are available after setup. |
| OpenClaw | Yes. The tested cross-agent installer copies the complete bundle into an OpenClaw skill root. | Today: `npx skills add ... --agent openclaw`. For first-class native discovery and updates: publish to ClawHub. | Strongest personal-agent fit: persistent browser profile, Gmail/Calendar tooling, persistent workspace/memory, and conversational approval. |
| Grok Bot | Not as a documented one-click external package. Grok Bot has private skills, but xAI does not document importing an Agent Skills repository or submitting one to a public Bot catalog. | Ask a Bot to create a private skill from the repository's instructions; monitor xAI for an external package/import surface. | Excellent runtime fit: persistent cloud browser/computer, connectors, durable `/workspace`, memory/preferences, and approval/takeover flows. Distribution is the blocker. |
| Grok Build | Yes, but it is a separate terminal agent, not Grok Bot. The existing `.claude-plugin` wrapper validates and installs without changes. | `grok plugin install thisiszinger/delta-bags-skill@v0.1.0 --trust`; submit a pinned catalog entry to xAI's plugin-marketplace repository for discovery. | Partial by default; browser and email/calendar access depend on plugins or MCP configuration. |

The highest-value distribution addition is **ClawHub**. It makes the skill
native to OpenClaw and also gives Hermes another indexed source. A Grok Build
marketplace pull request is useful, but it does not make the skill installable
in Grok Bot.

## Product identity and ambiguity

### Hermes Agent

This report means the open-source agent maintained at
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent),
whose official documentation is at `hermes-agent.nousresearch.com`. Search
results also expose mirrors and unrelated projects with similar names; those
are not treated as authoritative.

### OpenClaw

This report means [`openclaw/openclaw`](https://github.com/openclaw/openclaw),
the local-first agent and personal assistant. Its public skill registry is the
separate first-party [`openclaw/clawhub`](https://github.com/openclaw/clawhub)
project.

### Grok Bot versus Grok, Grok Skills, and Grok Build

xAI currently documents three different skill-bearing surfaces:

- **Grok Bot** is a persistent named cloud agent with its own computer,
  browser, files, memory, connectors, and routines. It is currently accessed
  through the Grok Bot desktop/iOS product and uses a Cursor account and
  eligible plan. [Grok Bot overview](https://docs.x.ai/grok-bot/overview),
  [getting started](https://docs.x.ai/grok-bot/get-started)
- **Grok web/mobile Skills** are private or shared skills created through
  conversation, writing, or file upload on grok.com, iOS, and Android.
  [xAI announcement](https://x.ai/news/grok-skills)
- **Grok Build** is xAI's terminal agent. It has filesystem Agent Skills,
  installable plugins, and a Git-backed public plugin marketplace.
  [Grok Build overview](https://docs.x.ai/build/overview),
  [skills and plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces)

An installation that works in Grok Build must not be described as a Grok Bot
installation.

## Hermes Agent

### Observed format and installation support

Hermes says its skills are compatible with the Agent Skills open standard.
Each skill is a directory containing `SKILL.md`, with optional `references/`,
`scripts/`, `templates/`, `assets/`, and `examples/`. Third-party installs copy
the `SKILL.md` plus the support files explicitly referenced by it. Installed
skills live under `$HERMES_HOME/skills` (normally `~/.hermes/skills`) and become
slash commands. [Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)

The current Delta Bags layout is compatible:

```text
skills/delta-bags/
├── SKILL.md
├── references/
└── scripts/
```

The skill already references every runtime reference and `scripts/state.py`.
`scripts/live_smoke.py` is intentionally not needed at runtime.

The shortest native install command is:

```sh
hermes skills install skills-sh/thisiszinger/delta-bags-skill/delta-bags
```

Verified observations with Hermes Agent v0.20.0:

- `hermes skills search delta-bags --source skills-sh --json` returned the
  `delta-bags` entry with identifier
  `skills-sh/thisiszinger/delta-bags-skill/delta-bags`.
- `hermes skills tap add thisiszinger/delta-bags-skill` successfully recognized
  the repository as a tap whose default root is `skills/`.
- Fetching
  `thisiszinger/delta-bags-skill/skills/delta-bags` resolved the skill and all
  referenced runtime files from the public repository.
- The first published build was blocked by a false-positive security rule on a
  broad `os.environ` read. Narrowing the helper to four literal path-variable
  lookups made the same Hermes scanner return `SAFE`. That fix should be
  released before presenting the command as frictionless; users should not be
  told to bypass a scanner when the source can avoid the false positive.

An optional repository-source setup is:

```sh
hermes skills tap add thisiszinger/delta-bags-skill
hermes skills install thisiszinger/delta-bags-skill/skills/delta-bags
```

The skills.sh route is preferable because it is already searchable without
requiring every user to add the repository as a tap.

### Public discovery

No new Hermes-specific marketplace submission is required for baseline
discovery. Hermes searches skills.sh, direct GitHub sources, ClawHub, and
other registries through its Skills Hub. The current skill is already returned
by its skills.sh search adapter. Hermes's own guidance says specialized or
community skills belong in a Skills Hub rather than its bundled catalog.
[Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)

Publishing to ClawHub would provide a second Hermes discovery source because
Hermes includes a ClawHub adapter. Optional `version`, `author`, and
`metadata.hermes.tags` frontmatter can improve source-specific display, but
they are not required for loading.

### Capability fit

- **Browser:** native browser tools navigate, snapshot, click, type, and fill
  forms. Backends include local Chromium/CDP and multiple cloud providers.
  A headed local browser can preserve a login across turns and allow human
  intervention. [Hermes Browser Automation](https://hermes-agent.nousresearch.com/docs/user-guide/features/browser)
- **Email and calendar:** Hermes ships a Google Workspace skill covering Gmail
  search/read and Calendar event lookup through OAuth. It is a separately
  configured integration, not something Delta Bags installs.
  [Hermes Google Workspace skill](https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace)
- **Persistent/private state:** Hermes has persistent memory, local file tools,
  and a durable `$HERMES_HOME`. Its bounded `MEMORY.md`/`USER.md` stores are too
  small and semantically wrong for a structured duplicate ledger, so Delta
  Bags' existing platform-native JSON fallback is appropriate.
  [Hermes Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/)
- **Confirmation:** the built-in `clarify` tool works in the CLI and messaging
  gateways. Delta Bags can obtain its required one-time pre-submit
  confirmation conversationally. Hermes's dangerous-command approval system
  does not itself guarantee an approval before a browser click, so the skill's
  explicit confirmation rule remains necessary.
  [Hermes tools](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/)

### Compatibility caveat

Hermes substitutes `${HERMES_SKILL_DIR}` with the installed skill's absolute
path. The portable skill now tells agents to resolve `scripts/state.py`
relative to the loaded skill directory and shows `${HERMES_SKILL_DIR}` as the
Hermes example rather than relying on the current working directory.

## OpenClaw

### Observed format and installation support

OpenClaw follows the Agent Skills format. It loads skills from, in descending
precedence, a workspace `skills/`, workspace `.agents/skills`, personal
`~/.agents/skills`, managed `~/.openclaw/skills`, bundled skills, and configured
extra directories. A minimum skill needs the same `name` and `description`
frontmatter Delta Bags already has. [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)

This project-scoped command was tested successfully with the current public
repository and copied the full bundle into `skills/delta-bags`:

```sh
npx skills add thisiszinger/delta-bags-skill \
  --skill delta-bags \
  --agent openclaw \
  --yes \
  --copy
```

For a personal assistant installation visible across local OpenClaw agents:

```sh
npx skills add thisiszinger/delta-bags-skill \
  --skill delta-bags \
  --agent openclaw \
  --global \
  --yes \
  --copy
```

The project command is directly tested. The global variant follows the same
installer's documented scope switch and writes to a personal skill root that
OpenClaw scans.

There is a version skew worth documenting:

- OpenClaw's current source documentation describes
  `openclaw skills install skills-sh:owner/repo/slug`.
- The latest published npm CLI tested here, OpenClaw `2026.7.1-2`, rejected
  `skills-sh:thisiszinger/delta-bags-skill/delta-bags` as an invalid slug.

Until a release containing that source feature is available, use the tested
Vercel `skills` command or ClawHub. The native Git installer is not a one-line
replacement because OpenClaw currently expects `SKILL.md` at the Git source
root, while this repository intentionally keeps its canonical skill under
`skills/delta-bags`.

### Public discovery through ClawHub

ClawHub is OpenClaw's first-party public registry. It stores versioned
`SKILL.md` bundles, changelogs, tags, downloads, stars, and scan summaries.
After publication, users get native search, install, verification, and updates:

```sh
openclaw skills search "delta bags"
openclaw skills install @thisiszinger/delta-bags --global
openclaw skills verify @thisiszinger/delta-bags --card --global
openclaw skills update @thisiszinger/delta-bags --global
```

The documented publisher flow is:

```sh
npm install --global clawhub
clawhub login
clawhub skill publish skills/delta-bags \
  --slug delta-bags \
  --name "Delta Bags" \
  --version 0.1.0 \
  --changelog "Initial beta"
```

Use `--dry-run` first if desired. Publishing requires GitHub authentication
and an account old enough to pass ClawHub's upload gate. Most importantly,
ClawHub's official CLI documentation says publishing a skill releases it on
ClawHub under **MIT-0**. The repository itself is MIT-licensed, so the owner
should explicitly accept the no-attribution license difference before
publishing. [ClawHub overview](https://github.com/openclaw/clawhub/blob/main/docs/clawhub.md),
[ClawHub CLI](https://github.com/openclaw/clawhub/blob/main/docs/cli.md)

### Capability fit

- **Browser:** OpenClaw's built-in browser plugin controls a dedicated
  persistent Chrome-family profile and can open tabs, inspect snapshots,
  click, type, and take screenshots. Users can sign in manually once; the
  agent should hand over login, 2FA, and CAPTCHA steps.
  [OpenClaw browser](https://docs.openclaw.ai/browser),
  [browser login](https://docs.openclaw.ai/tools/browser-login)
- **Email and calendar:** OpenClaw's first-party `gogcli` project supplies a
  Google Workspace skill/CLI with Gmail and Calendar read operations and OAuth
  setup. These capabilities require separate installation and authentication.
  [`openclaw/gogcli` skill](https://github.com/openclaw/gogcli/blob/main/.agents/skills/gog/SKILL.md)
- **Persistent/private state:** the agent workspace and its files persist, and
  OpenClaw provides Markdown memory plus indexed retrieval. Delta Bags'
  structured JSON fallback can live outside the skill as designed.
  [OpenClaw memory](https://docs.openclaw.ai/concepts/memory),
  [agent workspace](https://docs.openclaw.ai/agent-workspace)
- **Confirmation:** ordinary personal-agent conversation can collect Delta
  Bags' pre-submit confirmation. OpenClaw also has exec approvals and supports
  approval checkpoints through workflow tooling, but those mechanisms do not
  automatically turn every browser submit into a host-enforced approval. Keep
  the skill-level confirmation boundary.

### Compatibility caveat

OpenClaw documents `{baseDir}` as the skill-directory placeholder. The
portable skill now tells every host to resolve the helper relative to the
loaded skill directory and shows `{baseDir}` as the OpenClaw example.

## Grok Bot

### What xAI documents

Grok Bot is unusually well matched to the actual late-bag workflow:

- Each account gets a persistent cloud computer with browser, terminal, and
  filesystem. Browser sessions, files, command-line credentials, memory, and
  preferences persist. All Bots for one user share that computer.
  [Grok Bot overview](https://docs.x.ai/grok-bot/overview)
- Bots can use connectors shown under **Settings → Plugins**. xAI's connector
  catalog includes separate OAuth-backed Gmail and Google Calendar connectors
  with search/read capabilities.
  [Grok Bot computer and apps](https://docs.x.ai/grok-bot/computer-and-apps),
  [Gmail and Google Calendar connector](https://docs.x.ai/grok/connectors/gmail-google-calendar)
- A Bot can ask the user to take over for passwords, passkeys, 2FA, CAPTCHA,
  payments, identity checks, or explicitly human-only steps. Auto Review can
  require approval for selected tool calls and computer actions.
  [Grok Bot approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy)
- Grok Bot skills are reusable instruction sets available across a user's
  Bots. Users create them from a completed task, written instructions, or
  teach-by-demonstration; they appear under **Settings → Plugins → Yours**.
  [Grok Bot skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)

### Missing external distribution surface

No current xAI Grok Bot document exposes any of the following:

- a CLI command to install a skill from GitHub;
- a documented `.skill`, `SKILL.md`, plugin-manifest, or archive import format;
- an API for creating/installing Bot skills;
- a publisher submission process for adding third-party packaged skills to the
  Grok Bot Plugins catalog; or
- a public Bot skill marketplace comparable to ClawHub or the Grok Build
  plugin marketplace.

The broader Grok web/mobile product announces that a user can create a skill
by describing it, uploading a file, or writing one and can “share” skills.
That announcement does not document repository/package installation, and xAI's
business management documentation says skills can be shared only up to the
organization level, not through public links. It therefore should not be
treated as a public package-distribution contract.
[Grok Skills announcement](https://x.ai/news/grok-skills),
[xAI sharing policy](https://docs.x.ai/grok/management)

### Current practical bridge (inference, not an install command)

A Grok Bot user can plausibly ask the Bot to read or clone this public
repository on its cloud computer and create a **private** Bot skill from the
canonical instructions. This follows xAI's documented “create a skill from
written instructions” flow, but xAI does not promise lossless import of the
references or scripts. A suitable request is:

```text
Read https://github.com/thisiszinger/delta-bags-skill and create a private
skill called Delta Bags from skills/delta-bags/SKILL.md and its referenced
files. Preserve the rule that the final Delta submission requires my explicit
confirmation. Keep durable Delta Bags data under /workspace/delta-bags.
```

This must be described as a manual adaptation, not a supported one-click
install. The user should review the generated private skill before first use.

### Storage adaptation

Grok Bot specifically documents `/workspace` as the place for durable files
and warns that temporary directories, manually installed packages, and other
uncommitted application state are replaceable. Delta Bags' Linux fallback
currently targets `~/.config/delta-bags` and `~/.local/state/delta-bags`.
Those locations may work in the cloud computer but are not documented as
durable. A Grok Bot-specific private adaptation should store profiles and the
duplicate ledger under `/workspace/delta-bags`, or use a future Bot-private
storage API if xAI publishes one. Also disclose that all Bots on the account
share the computer and can see those files.

## Grok Build (separate opportunity)

Grok Build directly supports Agent Skills in `.grok/skills`, `~/.grok/skills`,
enabled plugins, and configured extra paths. It also reads Claude Code plugins,
skills, and marketplaces without extra setup. [Grok Build skills and plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces)

The current repository is already compatible:

- `grok plugin validate .` returned a valid `delta-bags` v0.1.0 plugin with one
  skill directory.
- In an isolated `$GROK_HOME`, this exact versioned command installed the
  public repository and `grok plugin list --json` reported `delta-bags`:

```sh
grok plugin install thisiszinger/delta-bags-skill@v0.1.0 --trust
```

No `.grok-plugin/plugin.json` is required because Grok's documented Claude
compatibility accepts the existing `.claude-plugin/plugin.json` wrapper.

xAI operates a separate public Grok Build marketplace. Third-party authors add
a remote catalog entry, pin it to a full 40-character commit SHA, regenerate
the component index, validate the catalog, and submit a pull request to
[`xai-org/plugin-marketplace`](https://github.com/xai-org/plugin-marketplace).
This is the documented public submission route for Grok Build only.
[xAI marketplace announcement](https://x.ai/news/grok-plugin-marketplace)

Grok Build is primarily a terminal/coding agent. Full Delta Bags execution
would additionally need a browser-control plugin and email/calendar MCP
servers; those are not installed by the Delta Bags skill.

## Recommended rollout

1. Release the Hermes scanner false-positive fix, then document the native
   Hermes skills.sh command.
2. Add the tested `npx skills ... --agent openclaw` command to the README now.
3. Decide whether MIT-0 publication is acceptable. If yes, publish
   `skills/delta-bags` to ClawHub and add the native `openclaw skills install`
   command.
4. Keep the portability note that resolves helper scripts relative to the
   loaded skill directory, with Hermes `${HERMES_SKILL_DIR}` and OpenClaw
   `{baseDir}` examples.
5. Optionally submit the already-compatible plugin to xAI's Grok Build
   marketplace with a pinned commit.
6. For Grok Bot, document the private “create from these instructions” bridge
   and durable `/workspace/delta-bags` storage. Do not advertise one-click or
   public-marketplace support until xAI publishes an external import or
   submission contract.

## Unknowns to monitor

- When the released OpenClaw CLI will accept the documented `skills-sh:`
  source reference.
- Whether xAI will expose a lossless Grok Bot skill import/export format.
- Whether xAI will open Grok Bot's Plugins catalog to third-party packaged
  skills and, if so, whether that catalog will share the Grok Build manifest or
  require a separate package.
- Whether Grok Bot will document a Bot-private structured store instead of the
  account-shared `/workspace` filesystem.
