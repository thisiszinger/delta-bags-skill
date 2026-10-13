# Launch kit

Everything needed to post about Delta Bags. Assets live in [`assets/`](../assets).

## Assets

| File | Use |
| --- | --- |
| `assets/launch.png` (1600×900) | Primary static graphic for X; also the README hero |
| `assets/social-preview.png` (1280×640) | GitHub repository social preview (Settings › General › Social preview › Upload) |
| `assets/demo.mp4` (1920×1080, ~30 s) | Attach to the launch post; video outperforms images for skill launches |
| `assets/demo.gif` (960 wide) | README or reply embed |
| `assets/launch-source.html` | Editable source; render with headless Chrome at 1600×900 |

## Posting pattern

Observed across recent well-performing skill launches (Anatomy, universal-modder, grill-me, Claude Mods):

- Lead with the outcome in one plain sentence, not the technology.
- Put the video in the first post. Keep the install command and repo link in the first reply, then pin it.
- Name compatible agents as a short text list.
- Keep the beta and unofficial disclaimer visible; honesty is rewarded and overclaiming gets Community Noted.
- Post Tuesday to Friday, US mid-morning.
- For a small account, amplifier reposts and the README matter more than the post itself, so make the clip and one-liner easy to copy.

## Post options

**A (outcome hook)**

> Delta owes you 2,500 SkyMiles if your checked bag takes >20 min. Almost nobody files the form.
>
> Quick ship: Delta Bags, an open-source agent skill. Say "my Delta bags were late", confirm once, it files the claim. Works in Claude Code, Codex, Gemini CLI, Cursor, OpenClaw + more. Beta, unofficial.

**B (builder voice)**

> Quick ship this week: an Agent Skill that files Delta's 20-Minute Bag Guarantee for you.
>
> "my bags were late" → one confirmation → 2,500 SkyMiles request filed.
>
> One SKILL.md, runs in Claude Code / Codex / Gemini CLI / Cursor / Hermes / OpenClaw. Beta, not affiliated with Delta. Repo below.

**C (self-deprecating)**

> I kept forgetting to claim Delta's 2,500-mile late-bag guarantee (2-hour window!). So I made my agent do it.
>
> Delta Bags: open-source portable skill, works in Claude Code, Codex, Gemini CLI, Cursor, OpenClaw and ~70 other agents. Tell it your bag was late, confirm once, done. Beta + unofficial. Quick ship.

**Reply (pin this)**

> Install in any agent:
> `npx skills add thisiszinger/delta-bags-skill --skill delta-bags`
>
> Or paste into your agent: "Install the Agent Skill delta-bags from github.com/thisiszinger/delta-bags-skill"
>
> https://github.com/thisiszinger/delta-bags-skill
>
> Beta. Not affiliated with Delta. Fails closed if it can't verify Delta's live terms. PRs welcome.

## Checklist

1. Merge the release PR and tag `v0.2.0` (`gh release create v0.2.0 --generate-notes`).
2. Upload `assets/social-preview.png` as the GitHub social preview.
3. Run `npx skills add thisiszinger/delta-bags-skill --skill delta-bags` once from a clean machine so skills.sh re-indexes the new description.
4. Post, reply with the install command, pin the reply.
