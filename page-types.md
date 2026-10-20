# Page types

Every hacks.guide page is one of these types; SKILL.md step 1 says how to pick one. Copy the skeleton for each page you write, then fill it in. Skeleton sections are slots, not requirements: include a section (Compatibility notes, Technical details, a fold) only when you have real content for it. Callouts below use the VitePress `:::` syntax; translate them for your renderer with [`formatting.md`](formatting.md).

## Landing

The first page someone sees. It answers "what is this, is it for me, what do I need", then sends the reader onto the path.

```markdown
# <Project name>

<One sentence: what it is and who it's for.>

::: tip
Estimated time: 15 minutes.
:::

## What does this do?

- <outcome 1>
- <outcome 2>

## What do I need?

- <hardware / OS / account>
- <tool> <version> or later

## What should I know before starting?

::: danger
<The one irreversible risk, if there is one, plus its consequence.>
:::

- <placeholder convention, e.g. "`<angle brackets>` mean: replace with your own value">
- <where to get help>

---

::: tip
Continue to [Get Started](get-started)
:::
```

For a tool whose README is the whole doc, use the **Reference** type instead.

## Router

Use a router when readers need different paths. It finds out which path applies and sends the reader there. It does no work itself.

```markdown
# Get Started

<One sentence: we'll check X, then pick the right method.>

### Section I - Check your version

1. Run `tool --version`
    + You should see something like `tool 3.2.1`

### Section II - Pick a method

| If you have… | Follow |
|---|---|
| version 3.x on Linux or macOS | [Installing (Unix)](installing-unix) |
| version 3.x on Windows | [Installing (Windows)](installing-windows) |
| version 2.x or older | [Upgrading from 2.x](upgrading) |
```

## Recipe (the main type)

A recipe gets one stage done. On a path, each recipe is one stage.

```markdown
# <Verb-ing the thing> (<variant, if any>)

::: details Technical details (optional)
<What's happening under the hood. As long as it needs to be: nobody has to read it.>
:::

## Compatibility notes

<One sentence: which versions/OSes this works on.>

::: warning
This page is for <X>. If you <Y>, follow [<Sibling page>](sibling) instead.
:::

## What you need

- The latest release of [<Tool>](https://…/releases/latest) (the `<exact-asset>.zip` file)
- <Prereq>: if you don't have it yet, follow [<Page>](page) first

## Instructions

### Section I - Prep work

In this section, you will <goal of this section in one clause>.

1. <Verb> <object>
1. <Verb> <object>
    + <checkpoint: You should see `…`>
1. <Verb> <object>
    + **macOS:** <variant>
    + If you get `<exact error>`, <fix or [troubleshooting link](troubleshooting#anchor)>

### Section II - <What happens>

In this section, you will <goal>.

1. …
1. <Last step>
    + <checkpoint: the observable done-state>

---

::: tip
Continue to [<Next page>](next)
:::
```

### Worked example

```markdown
# Setting Up the Database (Docker)

## Compatibility notes

This page works on any machine with Docker 24 or later.

::: warning
This page uses Docker. If you'd rather install Postgres directly, follow [Setting Up the Database (Native)](database-native) instead.
:::

## What you need

- [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
- The project cloned to your computer. If you haven't cloned it yet, follow [Getting the Code](getting-the-code) first

## Instructions

### Section I - Starting Postgres

In this section, you will start a Postgres container that the app connects to.

1. Open a terminal in the project folder
1. Copy `.env.example` to `.env`
    + **Windows:** run `copy .env.example .env`
1. Run `docker compose up -d db`
    + The first run downloads about 150 MB, so it may take a few minutes
1. Run `docker compose ps`
    + You should see `db` with the status `running (healthy)`
    + If the status is `exited`, run `docker compose logs db` and check [Troubleshooting](troubleshooting#database-wont-start)

### Section II - Creating the tables

In this section, you will create the tables the app needs.

1. Run `npm run db:migrate`
    + You should see `All migrations applied`
    + If you see `ECONNREFUSED 127.0.0.1:5432`, wait 10 seconds and run it again. Postgres is still starting. **This is normal on the first run.**
1. Run `npm run db:seed` to add sample data
    + This step is optional

::: danger
`npm run db:reset` **deletes every row** in the database. Only run it on your local machine.
:::

---

::: tip
Continue to [Running the App](running-the-app)
:::
```

## Troubleshooting

Write one troubleshooting page per recipe, or one shared page grouped by stage. The entries come from the failure sweep.

- **Title** each entry with the exact error text (56% of hacks.guide entries). Use a short, impersonal symptom only when there is no error text ("Dashboard stays blank after login"). Readers find entries by pasting what they see.
- **Body:** give the cause in one sentence, then the fix (55% of entries). Use a numbered list once the fix takes more than about 3 actions. Order alternative fixes from easiest to hardest. End with where to get help if none of them works.
- **Length:** a median entry is about 55 words.
- **Folds or headings:** fold the entries (one `details` each) when the page has many of them, roughly 6 or more, so the reader scans titles. A page with only a few entries reads better as plain `##` headings with the fix beneath, since nothing needs hiding.

```markdown
# Troubleshooting (<Recipe name>)

This page covers common problems with [<Recipe name>](recipe). If yours isn't here, ask in [<support channel>](link). Include your version, the exact error and what you've already tried.

## Issues with <stage>

::: details `ECONNREFUSED 127.0.0.1:5432`
**Cause:** Postgres isn't running yet.

**Fix:**
1. Run `docker compose ps`
1. If `db` isn't `healthy`, wait 10 seconds and try again
:::

::: details The page loads but shows no data
…
:::

## Something else

::: details My problem isn't listed
<Where to get help, plus a numbered list of what to include.>
:::

---

::: tip
Go back to [<Recipe name>](recipe)
:::
```

For complex failures, split the fold into `#### Symptoms`, `#### Cause` and `#### Solutions`.

## FAQ

Group questions under `##` headings by stage (`## Before installing`, `## After installing`). Give each question its own fold, worded the way the reader would ask it ("Can I …?"). Open each answer with the verdict (91% of hacks.guide answers do). Follow it with one sentence on why, and name the one exception if there is one.

```markdown
::: details Can I use SQLite instead of Postgres?
**No.** The app relies on Postgres-only features (`jsonb`, `LISTEN/NOTIFY`).
:::
```

## Reference (README for a tool, CLI, config, API)

The reader looks things up instead of walking through. Use tables and code blocks freely, and keep numbered steps for the quick start and the install. Order the page by what readers reach for first.

```markdown
# <tool>

<One sentence: what it does and for whom.>

## Install

<One short block per method. Each install method gets its own command in a code block, plus a checkpoint ("Run `tool --version`; you should see `tool 1.4.0`").>

## Quick start

1. <3–8 steps to the first real result, each with a checkpoint>

## Usage

<Short examples in code blocks, one per common task, each introduced by one sentence that says what it does.>

## Options

| Flag | Default | What it does |
|---|---|---|
| `--dry-run` | off | Shows what would be deleted without deleting anything |

## Safety

<Anything destructive: what is irreversible, the safe default, and how to preview first. Put this before or beside the first destructive example, not at the end.>

## Exit codes / Troubleshooting

<Table of codes, then troubleshooting entries titled with exact error text.>
```

A glossary is the same shape: one `| Term | Definition |` table per topic. Each definition is one or two plain sentences, and links out for depth.

## Explainer

Use an explainer when the reader needs a mental model before they act. Write it as question headings, each answered in three sentences or fewer, with a diagram (a code-block flow chart or a table) when the idea has moving parts. End with a signpost to the recipe that applies it.

```markdown
## What is a reverse proxy?

A **reverse proxy** sits in front of your app and forwards requests to it. Think of it as a receptionist who takes every visitor and walks them to the right office. It also handles HTTPS, so your app doesn't have to.
```
