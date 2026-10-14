# Launch kit

Everything needed to post about Delta Bags. Assets live in [`assets/`](../assets). All of them render from one source, `assets/src/stage.html`, so a copy or logo change re-renders everywhere.

## Design

Navy field (`#0B2A5B`), white type, no Delta marks and no red-white-and-blue; the only Delta hint is the palette and one red luggage tag. Text is left-aligned on the left, the device on the right. The hero is an iPhone 16 Pro (a real device frame, see below) showing a clean messaging thread with the user's agent. The thread shows the work, not just the result: an activity card for the email and calendar lookup, landing and bag times, the live terms check on delta.com, and the SkyMiles profile, then a confirmation card, the user's "yes, file it", and Delta's real success title. Below the copy sit ten standalone agent marks (ChatGPT, Claude, Muse, Grok Bot, Instinct, Hermes, Orchid, Tab, OpenClaw, Poke) and a QR code to the repo for people reading on desktop. A clay-style luggage pile, rendered in three.js, is the only illustration.

The conversation is captioned as illustrative, and the agent never claims more than the skill does: it submits a request, and the last bubble quotes Delta's "Claim Successful" response verbatim.

## Assets

| File | Size | Use |
| --- | --- | --- |
| `assets/launch.png` | 1600×900, exported at 2× | X post image, README hero. 16:9 shows uncropped in the feed. |
| `assets/social-preview.png` | 1280×640, exported at 2× | GitHub › Settings › Social preview. Also the X link card (2:1). |
| `assets/demo.mp4` | 1920×1080, 60 fps, 19 s, loops | Attach to the launch post. Static copy on the left, the phone animating on the right with slow camera moves. |
| `assets/demo.gif` | 960 wide | Reply embeds. |
| `assets/loop.mp4` | 1920×1080, 60 fps, 19 s, loops | Phone-only loop with tighter zooms; a second post, the OG video, or the README. |
| `assets/loop.gif` | 960 wide | README "How it works". |
| `assets/src/` | | `stage.html` (all layouts), `luggage.js` (three.js pile), `render.mjs` (Playwright + ffmpeg), the ten logos, the QR SVG. |

X limits that matter: images under 5 MB, video under 512 MB and 2:20, 16:9 or 1:1. Everything here is well under.

### Re-rendering

```bash
cd assets/src && npm install
npm run frame    # downloads the iPhone 16 Pro frame PNG (not committed, see below)
npm run stills   # launch.png + social-preview.png
npm run video    # demo.mp4 + loop.mp4 (60 fps, a few minutes each)
```

The renderer drives system Chrome through Playwright with software WebGL for the luggage, so it needs `google-chrome` on the path and `ffmpeg`. Each video frame is a real screenshot, which is why a 19-second clip takes minutes.

**Device frame.** The phone is the iPhone 16 Pro Black Titanium frame from [fastlane's frameit-frames](https://github.com/fastlane/frameit-frames), which hosts the Facebook Design "Devices" frameset that Meta published free for mockups. It is not CC0 and must not be redistributed as our own asset, so it is downloaded at build time rather than committed. Screen cutout in that file: x 72, y 69, 1206×2622, corner radius 180 px.

**Logos.** Standalone marks, shown white at one optical size, used nominatively to say "works with". Sources and brand rules are in `assets/src/logos/README.md`. Grok Bot has no standalone mark, so the parent Grok mark is captioned "Grok Bot"; Tab only publishes a PNG.

## Posting pattern

Observed across recent well-performing skill and agent launches:

- Lead with the outcome in one plain sentence, not the technology.
- Video in the first post. Install prompt and repo link in the first reply, then pin it.
- Name the agents people already use, in the order people use them.
- Keep the beta and unofficial disclaimer visible; overclaiming gets Community Noted.
- Post Tuesday to Friday, US mid-morning.
- For a small account, the clip and one-liner being easy to copy matter more than the post itself.

## Post options

**A (outcome hook)**

> Delta owes you 2,500 SkyMiles if your checked bag takes more than 20 minutes. Almost nobody files the form.
>
> So I made it a text message. Delta Bags is an open-source skill for your personal agent: "bag took 40 min at LAX" → it finds the flight, checks Delta's live terms, confirms once, files the request.
>
> Works with ChatGPT, Claude, Muse, Grok Bot, Hermes, OpenClaw and friends. Beta, unofficial.

**B (builder voice)**

> Quick ship: an Agent Skill that files Delta's 20-Minute Bag Guarantee from a text.
>
> You: "bag took 40 min at LAX"
> Agent: pulls the flight from your email, checks the live terms, confirms once, submits on delta.com, tells you what Delta said.
>
> One SKILL.md, bring your own agent. Beta, not affiliated with Delta. Repo below.

**C (self-deprecating)**

> I kept forgetting to claim Delta's 2,500-mile late-bag guarantee (2-hour window!). So my agent does it now.
>
> Delta Bags: open-source skill that works with ChatGPT, Claude, Muse, Grok Bot, Hermes, OpenClaw and ~70 other agents. Text it that your bag was late, confirm once, done. Beta + unofficial.

**Reply (pin this)**

> Tell your agent:
> "Install the Agent Skill delta-bags from github.com/thisiszinger/delta-bags-skill and use it whenever I mention a late Delta bag."
>
> Terminal types: `npx skills add thisiszinger/delta-bags-skill --skill delta-bags`
>
> Which agents can actually install it, and how: https://github.com/thisiszinger/delta-bags-skill#personal-agents
>
> Beta. Not affiliated with Delta. Fails closed if it can't verify Delta's live terms. PRs welcome.

## Checklist

1. Merge the release PR and tag `v0.2.0` (`gh release create v0.2.0 --generate-notes`).
2. Upload `assets/social-preview.png` as the GitHub social preview.
3. Run `npx skills add thisiszinger/delta-bags-skill --skill delta-bags` once from a clean machine so skills.sh re-indexes the new description.
4. Post with `assets/demo.mp4`, reply with the install prompt, pin the reply.
