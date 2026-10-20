---
name: make-docs
description: Human-facing docs (guides, setup/install steps, READMEs, tutorials, FAQs, troubleshooting) written in the scannable hacks.guide style. Use when writing, rewriting or fixing docs, or when a doc reads like a wall of text. For docs agents read (AGENTS.md, skills), use writing-for-agents.
---

# Make docs

Write docs the way hacks.guide writes its console guides. A first-timer follows them without getting lost, and a returning reader scans straight to the step they need.

The style is not short writing. Its sentences and paragraphs are ordinary length. What changes is **where the words go**:
- actions sit in numbered steps
- results, variants and failures hang under the step they belong to
- background lives in a one-sentence intro or a fold the reader can skip

The result is fewer paragraphs, not shorter ones.

## Steps

1. **Name the reader, the goal and the doc type.** Write one sentence: who lands on the page, and what is true when they leave. Then pick each page's type by what the reader does with it:
   - follows it: **recipe** (numbered steps)
   - looks things up: **reference** (README, CLI flags, config, API). It uses tables and code blocks, with steps only in a quick start.
   - needs a mental model: **explainer**
   - is stuck: **troubleshooting**
   - has a question: **FAQ**
   - must choose a route: **router**
   - just arrived: **landing**

   If the goal won't fit in one sentence, plan a **path** of pages: landing → router (if readers diverge) → one recipe per stage → finishing page. Troubleshooting sits beside the path.
2. **Load the skeleton, renderer and examples.**
   - Read the matching type in [`page-types.md`](page-types.md).
   - Find the renderer (`.vitepress/`, `docusaurus.config.*` or `mkdocs.yml`; GitHub markdown if none) and read its section of [`formatting.md`](formatting.md).
   - Read [`examples.md`](examples.md) for how the rules look in real before → after edits.
3. **Draft** by the rules below.
4. **Verify the facts.** Know which mode you are in:
   - **Rewrite mode:** you were given the source, such as existing docs, notes, a spec or a fact sheet. The source is the truth. Every warning, reason, cause, step and link comes from it. When a step needs a fact the source lacks (a menu path, a success message, a reason), write the step without it and list the gap in your reply.
   - **Author mode:** you are the source. Write the complete doc from your knowledge: every step, checkpoint, failure and reason a reader needs. Check what you can against the tool itself (`--help`, `man`, its config or source) or its official docs. Where you can, run the procedure yourself (a VM, a container, a test account) and copy the exact labels and messages from the screen. When the doc needs pictures, read [`screenshots.md`](screenshots.md) before capturing any. List in your reply the specifics you could not check, such as exact messages, labels, defaults and versions.

   In both modes:
   - Check every command, flag, default, path, port, timeout and version the reader will act on.
   - Check that each step's preconditions hold on the reader's starting system: the package repo is added, the binary is on `PATH`, the port is open.
   - Give a reason only when you know it is true. A plausible-sounding guess is worse than no reason.
5. **Run the failure sweep.** Walk every step where the system responds: a command runs, something installs, boots, connects, signs in, flashes, pairs or upgrades. For each one:
   - Write down what the reader sees when it worked. That becomes a **checkpoint** sub-bullet.
   - Write down at least one way it fails: the exact error text, the hang, or the wrong screen. A one-line fix goes in a **fix** sub-bullet. A longer fix gets a troubleshooting entry titled with the exact error text, linked from the step.

   This sweep matters most: hacks.guide readers file issues over errors the guide never mentions, almost never over length.
   - In author mode, list every failure you know of for each step, not just one. Think of what a support channel would see in its first month: wrong version, missing dependency, permission denied, port in use, firewall, wrong OS variant, a stale cache, a typo the reader is likely to make.
   - In rewrite mode, cover every failure the source names.

   You're done when every responding step has a checkpoint and its failures are covered.
6. **Check.**
   - Run `python3 ~/.claude/skills/make-docs/scripts/doc_check.py <files...>`.
   - In rewrite mode, do a **fidelity pass** in both directions:
     - Reread every warning, reason, cause, consequence, definition, step number and link target, and point to its source. Delete or list in your reply anything without one.
     - Walk the source top to bottom and find each fact on the page, especially per-OS sub-steps, caveats and one-line outcomes. Restore anything missing, or name it in your reply as a deliberate cut.
   - In author mode, reread each step as the reader on a fresh system. Every precondition must be met, every responding step needs its failure, and the gaps go in your reply.
   - Walk the checklist at the bottom.

   You're done when the script prints `clean` (or you can name why each remaining flag is deliberate), the mode's pass comes out clean, and every checklist line holds.

## Rules

### Recipes

- **One action per step, verb first, about 5–15 words.** hacks.guide's median step is 9 words, and 90% are 20 words or under. Write every step as `1.` so markdown numbers them.
- Choose the verb by its target:

  | Target | Step |
  |---|---|
  | key or physical button | Press `Enter` / Press (A) |
  | menu path | Navigate to `Settings` -> `Network` |
  | control on screen | Select / Click (PC) / Tap (touch) `Save` |
  | program or app | Launch / Open / Close `App` |
  | command | Run `command` |
  | file | Copy `file` from `<source>` to `<destination>`, naming both ends |
  | waiting | Wait until `<observable condition>`, as its own step |

- Keep the step line a pure action. Under it, sub-bullets come in this order: **how** (detail on doing it) → **checkpoint** (what you should see now) → **fork** (`**macOS:** …`) → **fix** (`If you see <exact error>, …`). Put a **reassurance** ("The window closes on its own. **This is expected.**") before the fix that would otherwise alarm.
- Put multi-line content in a fenced code block indented under its step: a config file, a script, or commands meant to run together. Single commands stay inline in the step.
- Split procedures of more than about 8 steps, or ones that change place or tool, into `### Section I - <what happens>`. Open each section with one sentence: "In this section, you will <goal>." Add ", so that <reason>" when you know the reason. End each section on a checkpoint.
- When a procedure repeats (for example "run the script, choose your version"), write its steps out again in each place, or use the renderer's include. A link that sends the reader away and back loses their place.
- Put each note in the place the reader acts on it:
  - a warning goes above the step it protects
  - a skip note ("Already have X? Skip to step 5") goes above the steps it skips
  - a fix goes under the step where the reader first sees the failure
- Point every back-reference at an exact place: "return to Section I, step 14", linked to the section's anchor. Write these once the step numbering is final, then recount each one.

### Explanation

- Background has three homes:
  - the page intro: one sentence of about 25 words, "This page …", saying what it does and why
  - the section intro: one sentence with the goal, plus the reason when you know it
  - a fold titled `Technical details (optional)`
- Give reasons as consequences. Inside steps, give them as consequences: a trailing "so that …", or a sub-bullet "This keeps X from Y." / "Otherwise, Y."
- Write paragraphs of 1–3 complete sentences that a beginner can follow without guessing. A 30-word paragraph that explains beats a 10-word fragment that doesn't. Past three sentences, the content is really a list, a table or a fold.
- Define each term where it first appears: **term** (expansion), one plain sentence, and a comparison to something familiar ("comparable to administrator access"). After that, use it bare. Use one noun per thing everywhere.
- Explainers use question headings. Answer in three sentences or fewer, verdict first.

### Callouts

Keep each callout to 1–3 sentences, and place it at the step it concerns.

| Type | Job |
|---|---|
| **tip** | The signpost ("Continue to [Next](next)"), shortcuts ("Already have Node 20? Skip to Section II"), done-states |
| **info** | Neutral context, scope notes, the expected-result screenshot |
| **warning** | An easy-to-miss gotcha, a prerequisite gate, or a scope redirect ("This page is for macOS. On Windows, follow [Install (Windows)](install-windows) instead.") |
| **danger** | Irreversible outcomes only: data loss, wrong target, leaked secrets |
| **fold** | Anything skippable: background, alternative tools, long logs, every FAQ answer, every troubleshooting entry |

Every warning and danger follows one shape: **condition or instruction → consequence → what to do instead**. For example: "If you have a VPN running, turn it off for these steps, or you will get a `TLS handshake timeout` error." Put it before the risky step, and give each real risk exactly one box.

### Branches

Recommend one path. Readers follow whatever is offered, so put alternatives they don't need in a fold or on another page.

| The difference is… | Use |
|---|---|
| one or two steps | an inline fork sub-bullet (`**Windows:** …`) |
| the whole procedure, per OS or variant | tabs, each a full copy of requirements and steps. Without tabs, use pages titled `Title (Variant)` plus a chooser. |
| a choice the reader must make | a router: a table or cards, with the condition beside the link |
| the reader is on the wrong page | a warning at the top: "This page is for X. If Y, follow [Z](z) instead." |
| this method keeps failing | a fallback: "If this still fails after 3 tries, follow [Alternate](alt) instead." |
| two tools that do the same job (the user asked for options) | tabs, one per tool, each a full copy of the steps. Above them, "Pick **one** tool. Both do the same job.", then one line per tool on who it suits. |

### Inline formatting

- Put in `code` anything the reader types, sees on screen or finds on disk: file names, folders, commands, UI labels, error strings. Write menu paths as `Settings` -> `Network` -> `Proxy`.
- Use **bold** for the operative word of a warning, and for the one fact a skimmer must catch.
- Write placeholders as `<your-username>`, and say once what they look like and where the reader gets them.
- Give downloads by their exact asset: "The latest release of [Tool](…/releases/latest) (the `tool-linux-x64.tar.gz` file)".
- Make link text name the destination: "[Docker Desktop installed](…)".
- Embed an image where the reader could go wrong (the expected screen, the file layout, a hard-to-find button), right after its step: the reader compares against it without clicking. Write its alt text as what the reader should see there. Keep every screenshot your source provides embedded. A word-link ("until you see the [welcome screen](img/welcome.png)") is only for an optional second look that would otherwise crowd the steps.
- Use tables for lookups (version → method, error → meaning, flag → effect) and tree code blocks for folder layouts.

### Navigation

- Open with prerequisites as links: "This page assumes you have finished [Installing X](x)."
- End every page on a path with `---` and a tip signpost: "Continue to [Next Page](next)". Side pages end "Return to [Page](page)". The last page ends on a done-state followed by links to what readers usually do next.
- Give time estimates on the landing page and on slow steps ("This takes 10–60 minutes").
- At a dead end, say where to get help and what to bring: version, exact error text, what was already tried.

### Voice

- Address the reader as "you". Use bare imperatives in steps ("Enter the version") and the plain present in prose. Use "we" only for the guide's stance ("We recommend …").
- Write full forms ("do not", "it is"), and keep instructions free of "please", "just" and "simply".
- State outcomes with "will" ("The window will close"). Hedge only real uncertainty.
- Be calm about risk: state the risk and its consequence once. Predict outcomes that look scary but are normal before the reader meets them.

## Checklist

- [ ] Each page has one H1 and fits its doc type. Recipes walk; references look up.
- [ ] Every step is one verb-first action. Its how, checkpoint, fork and fix sit under it, in that order.
- [ ] Rewrite mode: every sentence traces to the source, and every source fact is on the page. Author mode: the doc is complete from your knowledge, verified where possible. Either way, gaps are listed in your reply.
- [ ] Every back-reference names an exact section and step, and matches the final numbering.
- [ ] Warnings and skip notes sit above their steps. Fixes sit under the step where the failure shows.
- [ ] The failure sweep is done: every step where the system responds has a checkpoint and a considered failure.
- [ ] Every section ends on an observable checkpoint.
- [ ] Background lives in intros and folds. Paragraphs are 1–3 complete sentences that a beginner can follow.
- [ ] Multi-line content is in code blocks under its step.
- [ ] Every warning states its consequence and sits before the risky step.
- [ ] Every page on a path ends with a signpost.
