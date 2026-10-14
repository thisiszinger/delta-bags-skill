# Launch kit

Everything needed to post about Delta Bags. Assets live in [`assets/`](../assets). All of them come from one source, `assets/src/stage.html`, so a copy or logo change re-renders everywhere.

## Design

Delta-themed without Delta's trademarks: navy `#003268` / `#0B2A5B`, Delta red `#E3132C`, white. The hero is an iPhone showing an iMessage conversation with your agent, because the people this is for will use it from a personal agent on a phone, not a terminal. The eight logos are personal agents (Muse, ChatGPT, Grok Bot, Instinct, OpenClaw, Hermes, Orchid, Tab); coding agents are covered in the README install table instead. The conversation is labeled illustrative, and the last bubble quotes Delta's real success title ("Claim Successful") rather than inventing an approval.

Three themes exist. **Light** (white field, navy panel, condensed red imperative) is the default for both X and the GitHub social preview; it reads as "Delta" fastest at feed size. **Navy** and **Miles** (editorial 2,500 numeral) are in `assets/options/` as drop-in alternatives.

## Assets

| File | Size | Use |
| --- | --- | --- |
| `assets/launch.png` | 1600×900 (2× export) | X post image, README hero. 16:9 shows uncropped in the feed. |
| `assets/social-preview.png` | 1280×640 (2× export) | GitHub › Settings › Social preview. Also the X link card (2:1). |
| `assets/demo.mp4` | 1920×1080, 17 s, loops | Attach to the launch post. Static copy on the left, animated phone on the right with zooms. |
| `assets/demo.gif` | 960 wide | Reply embeds, README fallback. |
| `assets/loop.mp4` | 1920×1080, 17 s, loops | Phone-only loop with heavier zooms; use as the OG video, a second post, or the README. |
| `assets/loop.gif` | 960 wide | README "How it works". |
| `assets/options/` | | Navy and Miles themes: launch PNG, OG PNG, and split MP4 each. |
| `assets/src/` | | `stage.html` (all layouts and themes), `render.mjs` (Playwright + ffmpeg), the eight logos with sourcing notes in `logos/README.md`. |

X limits that matter: images under 5 MB, video under 512 MB and 2:20, 16:9 or 1:1. Everything here is well under.

Re-render after a copy change:

```bash
cd assets/src && npm install
npm run stills   # launch.png + social-preview.png (Light theme)
npm run video    # demo.mp4 (Light split) + loop.mp4 (phone only)
THEME=navy node render.mjs still launch ../options/launch-navy.png
```

Each `render.mjs video` call drives system Chrome frame by frame, so a 17-second clip takes a couple of minutes.

## Posting pattern

Observed across recent well-performing skill and agent launches:

- Lead with the outcome in one plain sentence, not the technology.
- Video in the first post. Install command and repo link in the first reply, then pin it.
- Name the agents people already use, as plain text, so they see themselves in the list.
- Keep the beta and unofficial disclaimer visible; overclaiming gets Community Noted.
- Post Tuesday to Friday, US mid-morning.
- For a small account, the clip and one-liner being easy to copy matter more than the post itself.

## Post options

**A (outcome hook)**

> Delta owes you 2,500 SkyMiles if your checked bag takes more than 20 minutes. Almost nobody files the form.
>
> So I made it a text message. Delta Bags is an open-source skill for your personal agent: "bag took 40 min at LAX" → one confirmation → request filed on delta.com.
>
> Works with Hermes, OpenClaw, Muse, ChatGPT, Grok Bot and any agent that reads a SKILL.md. Beta, unofficial.

**B (builder voice)**

> Quick ship: an Agent Skill that files Delta's 20-Minute Bag Guarantee from a text.
>
> You: "bag took 40 min at LAX"
> Agent: finds the flight, checks Delta's live terms, confirms once, submits, tells you what Delta said.
>
> One SKILL.md, bring your own agent. Beta, not affiliated with Delta. Repo below.

**C (self-deprecating)**

> I kept forgetting to claim Delta's 2,500-mile late-bag guarantee (2-hour window!). So my agent does it now.
>
> Delta Bags: open-source skill, works in Hermes, OpenClaw, Muse, ChatGPT, Grok Bot and ~70 other agents. Text it that your bag was late, confirm once, done. Beta + unofficial.

**Reply (pin this)**

> Install in any agent:
> `npx skills add thisiszinger/delta-bags-skill --skill delta-bags`
>
> Or just paste into your agent: "Install the Agent Skill delta-bags from github.com/thisiszinger/delta-bags-skill"
>
> https://github.com/thisiszinger/delta-bags-skill
>
> Beta. Not affiliated with Delta. Fails closed if it can't verify Delta's live terms. PRs welcome.

## Checklist

1. Merge the release PR and tag `v0.2.0` (`gh release create v0.2.0 --generate-notes`).
2. Upload `assets/social-preview.png` as the GitHub social preview.
3. Run `npx skills add thisiszinger/delta-bags-skill --skill delta-bags` once from a clean machine so skills.sh re-indexes the new description.
4. Post with `assets/demo.mp4`, reply with the install command, pin the reply.

## Logo use

All eight marks are used nominatively ("works with"), unmodified apart from sizing in a rounded tile. `assets/src/logos/README.md` records each source and any published brand rule (Orchid: write "Orchid", never "Orchid AI"; OpenAI: do not recolor). Swap a logo by editing the `LOGOS` list at the top of `assets/src/stage.html`.
