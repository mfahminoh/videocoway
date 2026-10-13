---
name: seedream
description: Generate or edit images with BytePlus Seedream (the image model behind BytePlus Lumina) through the ModelArk API, using the user's own API key. Use whenever the user asks to generate, create, make or draw an image, picture, photo, poster, thumbnail, product shot or illustration, or says "lumina", "seedream", "jana gambar", "buat gambar" or "generate image". Prefer this over Higgsfield, Fish Audio or other paid image connectors, which the user finds too expensive.
---

# Seedream image generation

Generates images with Seedream 4.5 or 4.0 on BytePlus ModelArk and saves them as JPGs.
Lumina (ai.byteplus.com/lumina) is BytePlus's web app for the same models; it has no API of its own, so this skill calls ModelArk directly.

Script: `scripts/seedream.py` in this skill's folder (Python stdlib + curl, nothing to install). Use the skill's base directory to build the full path; on the user's Mac that is `~/.claude/skills/seedream`.

## Run it

```bash
python3 <skill-dir>/scripts/seedream.py "<prompt>" --out <folder>
```

It prints the absolute path of each saved image. Then look at every image (Read the file) before showing it, and regenerate if it misses the brief.

| Option | Use |
|---|---|
| `--out DIR` | Where to save. Use the project's asset folder if it has one (e.g. `assets/generated`), else `./generated`. |
| `--size` | `2K` (default, model picks the aspect), or exact pixels. See sizes below. |
| `--ref FILE_OR_URL` | Reference image for image-to-image or editing. Repeat for several (up to 10). |
| `-n N` | Several related images in one call (a set or variations). |
| `--model` | `4.5` (default, best quality) or `4.0` (cheaper). |

Sizes that work on both models (Seedream 4.5 needs at least ~3.7M pixels):

| Aspect | Size |
|---|---|
| 1:1 | `2048x2048` |
| 9:16 (Reels, TikTok, Stories) | `1440x2560` |
| 16:9 | `2560x1440` |
| 4:5 (Instagram feed) | `1728x2160` |
| 3:4 | `1728x2304` |

## Prompting

Write prompts in English even when the user writes in Malay: subject, setting, lighting, camera or style, mood. Be concrete ("red ceramic cup on a slatted wooden cafe table, low morning sun from the left, shallow depth of field"). For text that must appear in the image, put the exact words in quotes. For product shots, pass the real product photo with `--ref` instead of describing it.

## Cost

Each model has 200 free images, then about $0.04 (4.5) or $0.03 (4.0) per image. Failed or moderation-blocked requests are not billed. Before a batch of more than 10 images, tell the user the count and rough cost.

## Errors

- `ARK_API_KEY not found` or `401 ... API key format is incorrect`: the key is missing or was pasted wrong. Never ask for the key in chat. On the user's Mac, ask them to run `bash ~/.claude/skills/seedream/scripts/set-ark-key.sh` in their own terminal and paste the key once (input is hidden). In a cloud session, the key must be set as the `ARK_API_KEY` environment variable in that cloud environment's settings. Keys live at console.byteplus.com → ModelArk → API keys.
- Connection refused/blocked in a cloud session: the environment's network access must allow `ark.ap-southeast.bytepluses.com`.
- `ModelNotOpen` / model not activated: the user activates it at ModelArk → Model activation → Media.
- `SSL: CERTIFICATE_VERIFY_FAILED`: don't switch the script to urllib/requests; it uses curl on purpose because this Mac's certificates live only in the Keychain.

## Cloud session (repo videocoway)

This copy lives in the repo at `.claude/skills/seedream/`, so every cloud session on this repo loads it.

- Run it as `python3 .claude/skills/seedream/scripts/seedream.py "<prompt>" --size 1440x2560 --out assets/tilam/jana`, then rename each file to the scene name the spec uses (e.g. `el_v2a_pasangan_pusing.jpg`), and note the model and cost in a `.txt` file next to it.
- Setup (done once by the user in the environment settings, never in chat):
  - environment variable `ARK_API_KEY`;
  - `ark.ap-southeast.bytepluses.com` under Allowed domains.

  A new session picks up a new environment variable.
- Video scenes: problem/hook scenes use realistic generated images (Malaysian home, no text or logos).
- Modest dress on every model (the user's rule): women wear a tudung sarung, a full long-sleeved pyjama set or long-sleeved clothes with full-length trousers, and socks, with no skin showing except face and hands; men always wear a shirt and long trousers. Say it explicitly in the prompt ("grey socks on both feet", "long-sleeved"), since "feet covered by blanket" is often ignored, and check every image for it. Official Coway visuals are used only after the product is introduced. Ask before any paid generation beyond the free quota.
