# Agent marks used in the launch graphics

Standalone marks, rendered white on navy at one optical size by `stage.html`. All are used nominatively ("works with"), unmodified apart from color and size. Researched 2026-10-14; the full per-agent install research is in `docs/research/personal-agents-2026-10.md`.

| File | Product | Source | Notes |
| --- | --- | --- | --- |
| `chatgpt.svg` | ChatGPT (OpenAI) | OpenAI blossom geometry (simple-icons) | OpenAI brand rules: black or white only, do not modify, do not pair with the wordmark. |
| `claude.svg` | Claude (Anthropic) | Anthropic press kit, "Claude Spark" | Official file; shown white here. |
| `muse.svg` | Muse (Meta) | Wikimedia Commons `Muse_icon.svg` | Trademark of Meta; nominative use. No Muse entry in Meta's brand center yet. |
| `grok.svg` | Grok Bot (xAI) | grok.com header mark | Grok Bot has no standalone mark; the parent Grok mark is captioned "Grok Bot". |
| `instinct.svg` | Instinct | instinct.com favicon, card removed | No brand page exists. |
| `hermes.svg` | Hermes Agent (Nous Research) | `assets/nous-girl-white.svg` in the hermes-agent repo (MIT) | Official black/white mark. |
| `orchid.svg` | Orchid | orchid.ai/brand, "paper" symbol | Official. Write "Orchid", never "Orchid AI". |
| `tab.png` | Tab | tab.bot app icon | No SVG published; PNG shown unfiltered. |
| `openclaw.svg` | OpenClaw | openclaw.ai/favicon.svg | No brand kit published. |
| `poke.svg` | Poke (Interaction Co. / Cognition) | Inline SVG from poke.com | Recolored white. |

To change the row, edit the `LOGOS` list near the top of `stage.html`. Per-mark `h` scales a mark that is optically heavier or lighter than the others; `raw:true` skips the white filter.
