# Examples

Before → after edits that show the rules in practice. Every pair comes from a real hacks.guide review or commit. The ones set in software docs are the same edit transposed (marked *transposed*). A real run of steps from the guides is at the end.

## Steps

**Give every action its own step.** A step that assumes setup the reader hasn't done fails silently. *(transposed)*

```markdown
4. Copy `settings.yaml` to the `~/.acme/plugins/` folder.
```
```markdown
1. Install the CLI with `npm install -g acme-cli`.
1. Run `acme init` to create the `~/.acme/` folder.
1. Extract `plugins.zip` to the `~/.acme/` folder.
1. Copy `settings.yaml` to the `~/.acme/plugins/` folder.
```

**Split a conditional extra action out of the main step**, so skimmers can't miss it. *(transposed)*

```markdown
1. When the installer finishes, select `Finish`. If you are offered `Add acme to PATH`, select that as well.
```
```markdown
1. When the installer finishes, select `Finish`.
1. If you are offered `Add acme to PATH`, select it.
```

**The numbered line is the action; the result is a checkpoint under it, named exactly.** *(transposed)*

```markdown
1. Run `docker compose up -d`. It should start the web and db containers.
```
```markdown
1. Run `docker compose up -d`.
    - The output should end with `Container app-web-1  Started` and `Container app-db-1  Started`.
```

**A failure note is not a step.** Nest it under the step where the failure happens, and describe what the reader sees.

```markdown
6. If you are stuck being unable to acquire the am:u service, power off your 3DS and try again
```
```markdown
   + If it freezes while attempting svchax, power off your 3DS by holding the power button and try again (this can take many tries)
```

## Precision

**Name the one file the reader needs, not "the contents of" an archive.** *(transposed)*

```markdown
1. Extract the contents of `acme-tools.zip` to your `bin` folder.
```
```markdown
1. Copy `acme.exe` from `acme-tools.zip` to your `bin` folder.
```

**Define a placeholder by what it looks like and where the reader got it.** *(transposed)*

```markdown
   + The `<TOKEN>` will be the same one that you used earlier
```
```markdown
   + `<TOKEN>` is the 40-character string starting with `ghp_` that you copied in Section II
```

**When a step sets several values, list them as labelled sub-bullets.**

```markdown
1. Go to `Advanced Settings`. Set your primary DNS to `95.217.77.181`, and your secondary DNS to `1.1.1.1`.
```
```markdown
1. Go to `Advanced Settings` and set your DNS to the following:
    * Primary DNS: `95.217.77.181`
    * Secondary DNS: `1.1.1.1` (Cloudflare)
```

**When the download differs by OS, tell each OS which asset to pick.** *(transposed)*

```markdown
* The latest release of [acme-cli](https://example.com/acme-cli/releases/latest)
```
```markdown
* The latest release of [acme-cli](https://example.com/acme-cli/releases/latest) (the asset marked `windows-x64` if you use Windows, or `darwin-arm64` if you use an Apple Silicon Mac)
```

## Checkpoints

**Gate "once it's done" on a visible signal.** *(transposed)*

```markdown
1. Once the migration completes, restart the server
```
```markdown
1. Once the migration completes and the terminal prints `Migrations applied: 12`, restart the server
```

## Failures

**Replace a vague trigger with a threshold the reader can check.** *(transposed)*

```markdown
   + The dashboard should load after a short delay. If you get a *persistent* blank page, [follow this troubleshooting guide](troubleshooting#blank-dashboard)
```
```markdown
   + The dashboard should load after a short delay. If the page stays blank for longer than 2 minutes, [follow this troubleshooting guide](troubleshooting#blank-dashboard)
```

**Replace a guessed cause with a check the reader can perform.** *(transposed)*

```markdown
   - If the container keeps restarting, you may be out of memory.
```
```markdown
   - If the container keeps restarting, run `docker logs app-web-1` and check the last lines. If you see `OOMKilled`, increase the memory limit.
```

**When a method fails, say exactly where to go next.** *(transposed)*

```markdown
1. If `acme login` hangs, you will not be able to use SSO. You will instead need to use an API token
```
```markdown
   + If `acme login` hangs for more than 30 seconds, you cannot use SSO. Return to [Authentication](authentication) and select "API token".
```

**Title a troubleshooting entry by the symptom, short and impersonal.** *(transposed)*

```markdown
<summary>My app does not show any of my environment variables after deploying</summary>
```
```markdown
<summary>Environment variables missing after deploy</summary>
```

## Warnings

**State the concrete consequence of skipping the precaution.** *(transposed)*

```markdown
If you have a VPN running, you must turn it off for these steps. You can turn it back on afterwards.
```
```markdown
If you have a VPN running, you must turn it off for these steps, or you will get a `TLS handshake timeout` error. You can turn it back on afterwards.
```

**Merge overlapping warnings into one rule the reader can act on.** *(transposed)*

```markdown
acme-agent versions before 3.0 do not support ARM. Installing versions before 2.4 on ARM will corrupt the package cache.
```
```markdown
Do not install any acme-agent version before 3.0 on ARM, or it will corrupt the package cache.
```

## One path

**Recommend one choice; fold the known error and its fix under it.** *(transposed)*

```markdown
1. Run the installer. It will ask which backend to use. If you have Postgres installed, use `postgres`, or else use `sqlite`. If the former gives a `connection refused` error, restart Postgres, run the installer again, then try `postgres-legacy`.
```
```markdown
1. Run the installer. When it asks which backend to use, select `sqlite`.
    - If you get `connection refused`, restart the installer and try again.
```

**Keep readers on the main path.** Cut side links that only serve curiosity.

```markdown
Select the exploit that matches your console. If the recommended option does not work for you, or if you are curious about other exploits, check out [Legacy Exploits](legacy-exploits).
```
```markdown
Select the exploit that matches your console.
```

## Why

**Say what a requirement is for when it is not obvious.** *(transposed)*

```markdown
* The latest release of [acme-codecs](https://example.com/acme-codecs/releases/latest)
```
```markdown
* The latest release of [acme-codecs](https://example.com/acme-codecs/releases/latest). This allows exported videos to have audio.
```

**Give a precaution's reason as its consequence**, in a sub-bullet under the step *(adapted from a step a reviewer trimmed)*:

```markdown
1. Copy `NANDmin.bin` and `NANDmin.bin.sha` from the `/gm9/out/` folder to a safe location on your computer
   + This backup will save you from a brick if anything goes wrong in the future
```

## Wording

**Cut trailing clauses that give the reader nothing to do.** *(transposed)*

```markdown
For now, only the `.env` file is required, however the other files in the folder can be useful to you for other things.
```
```markdown
For now, only the `.env` file is required.
```

**Use the short present form.** *(transposed)*

```markdown
1. Once the build has been completed, run `make install`
```
```markdown
1. Once the build is complete, run `make install`
```

**Use one noun for one thing, everywhere.** *(transposed)*

```markdown
1. Restart your machine
1. Reconnect the drive to your computer
1. Power on your system
```
```markdown
1. Restart your computer
1. Reconnect the drive to your computer
1. Power on your computer
```

**Write instructions as bare imperatives.** Drop "please", "just" and "simply". *(transposed)*

```markdown
To find the right image tag, please just enter the version you noted in Section I.
```
```markdown
To find the right image tag, enter the version you noted in Section I.
```

**Make the descriptive phrase the link text.** *(transposed)*

```markdown
* Docker Desktop installed ([install guide here](https://docs.docker.com/desktop/))
```
```markdown
* [Docker Desktop installed](https://docs.docker.com/desktop/)
```

## A real run of steps

From 3ds.hacks.guide (`installing-boot9strap-(mset9-cli).md`). It shows the moves working together:
- the section intro states the goal
- the danger box sits where the risk starts
- each step is one action
- every result, fork and fix hangs under its step

```markdown
### Section II - MSET9

In this section, you will trigger MSET9 to launch SafeB9SInstaller (the custom firmware installer).

::: danger

These instructions must be followed **EXACTLY**, so double-check EVERYTHING you are doing to avoid errors!

:::

1. Power on your console, ensuring System Settings is selected
    + If System Settings is not selected, hover over the System Settings icon using the D-Pad, power your console off, then back on
1. Press (A) to launch System Settings
1. Navigate to `Data Management` -> `Nintendo 3DS` -> `Extra Data`
1. **Do not press any buttons or touch the screen**
1. **With the console STILL ON, and without pressing any buttons or touching the screen**, remove your SD card from your console
    + The menu will refresh and say that no SD card is inserted, which is expected
1. Insert your SD card into your computer
1. In the MSET9 window, type `3`, then press Enter to inject MSET9
    + You should see "MSET9 successfully injected!"
1. Reinsert your SD card into your console **without pressing any buttons or touching the screen**
1. If the exploit was successful, you will have booted into SafeB9SInstaller
    + If you get a red screen or the console gets stuck on a loading screen for more than 10 seconds, follow the [troubleshooting guide](troubleshooting-mset9)
```
