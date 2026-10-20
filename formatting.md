# Renderer syntax

**Anchors depend on the renderer:** a heading's anchor is its text lowercased, with punctuation dropped and spaces turned into `-`. They differ on repeated dashes:
- GitHub keeps every dash, so `### Section I - Prep Work` becomes `#section-i---prep-work`.
- Stock VitePress collapses repeats, so the same heading becomes `#section-i-prep-work`. hacks.guide's own VitePress setup keeps them.

When the site builds locally, check each link's anchor against the `id="…"` attributes in the built HTML.

**The site's own syntax wins.** When the site's existing pages or your source material show a syntax for callouts, tabs, buttons or includes (for example `::::: tabs` with `:::: tab Name`), copy it exactly, even where this file says otherwise. The sections below are defaults for sites with no established convention.

Read only the section for the renderer you found. The *jobs* (tip, info, warning, danger, fold, tabs, signpost) come from `SKILL.md`. This file only spells each job in a renderer's syntax.

## VitePress (`.vitepress/`)

- **Callouts:** `::: tip` / `::: info` / `::: warning` / `::: danger`, closed with `:::`.
- **Fold:** `::: details Title`.
- **Nesting:** give the outer container one more colon than the inner one (`:::: details` holding `::: info`).
- **Inside a list step:** indent callouts, code fences and sub-bullets 4 spaces, and images 3, so the list keeps going. A callout left at column 0 between two steps restarts the numbering.
- **Includes:** `<!--@include: ./_include/step-name.md-->` for steps several pages share.
- **Tabs:** need a plugin (`vitepress-plugin-tabs`: `:::tabs` then `== Windows`). Without the plugin, use separate pages plus a chooser.
- **Signpost button:** `[Continue to X →](x){.btn}`, if the theme styles `.btn`. Otherwise use a plain tip.
- **Frontmatter:** set `outline: deep` so the `Section I/II` headings show up in the page outline as a step map.

## Docusaurus (`docusaurus.config.*`)

- **Callouts:** `:::tip` / `:::info` / `:::warning` / `:::danger`, closed with `:::`. There is no space after the colons.
- **Fold:** `<details><summary>Title</summary>` … `</details>`. Leave a blank line after `<summary>`.
- **Tabs:** `import Tabs from '@theme/Tabs'; import TabItem from '@theme/TabItem';`, then `<Tabs groupId="os"><TabItem value="win" label="Windows">…</TabItem></Tabs>`. A shared `groupId` keeps every OS tab on the site in sync.

## MkDocs Material (`mkdocs.yml`)

- **Callouts:** `!!! tip`, `!!! info`, `!!! warning`, `!!! danger`. The body is indented 4 spaces.
- **Fold:** `??? note "Title"` (starts closed).
- **Tabs:** `=== "Windows"` with the body indented 4 spaces. Needs the `pymdownx.tabbed` extension.
- **Includes:** `--8<-- "_include/step.md"`, which needs `pymdownx.snippets`.

## GitHub-flavored markdown (default: READMEs, `docs/` folders)

- **Callouts:** GitHub alerts. Map the jobs like this:

  | Job | Syntax |
  |---|---|
  | tip | `> [!TIP]` |
  | info | `> [!NOTE]` |
  | warning | `> [!WARNING]` |
  | danger | `> [!CAUTION]` |
  | must-do prerequisite | `> [!IMPORTANT]` |

  Each line of the body starts with `> `.
- **Inside a list step:** alerts don't render there. Put the content in the sub-bullet itself and bold the operative word.
- **Fold:** `<details><summary>Title</summary>`, then a blank line, the markdown, a blank line, and `</details>`.
- **Tabs:** GitHub has no tabs. Use a fold per variant (`<details><summary>Windows</summary>`) or separate pages plus a chooser.
- **Inside a numbered step:** indent sub-bullets, code fences and images 3 spaces, to line up under the step's text. That keeps them nested in the step and the numbering keeps going.
- **Anchors:** fold titles can't be linked to. When steps link to troubleshooting entries, give each entry a `###` heading (exact error text) with the fix under it.

## Plain text / unknown renderer

Write callouts as a bold label on its own line ("**Warning:** …"). Write folds as a `##` heading marked `(optional)`. Keep every other rule.
