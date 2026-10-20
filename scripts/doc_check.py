#!/usr/bin/env python3
"""Flag wall-of-text patterns in markdown docs. Usage: doc_check.py FILE..."""
import re
import sys

STEP_MAX_WORDS = 25
PARA_MAX_WORDS = 60
CALLOUT_MAX_WORDS = 60
RUN_MAX_STEPS = 20
CALLOUT_KINDS = {"tip", "info", "note", "warning", "danger", "caution", "important", "success"}

STEP_RE = re.compile(r"^(\d+)\.\s+(.*)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CALLOUT_OPEN_RE = re.compile(r"^\s*(:{3,})\s*(\w+)|^\s*(!!!|\?\?\?)\s*(\w+)|^\s*>\s*\[!(\w+)\]")
CALLOUT_CLOSE_RE = re.compile(r"^\s*:{3,}\s*$")
STRUCTURAL_RE = re.compile(r"^\s*([-*+]\s|\d+\.\s|#|\||<|>|!\[|---|___|:::|!!!|\?\?\?|===)")


def words(text):
    text = re.sub(r"\]\([^)]*\)", "]", text)  # drop link targets
    text = re.sub(r"<[^>]+>", " ", text)
    return len(text.split())


def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return [""] * (i + 1) + lines[i + 1:]
    return lines


def without_code(lines):
    out, in_fence = [], False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def check_steps(lines, flag):
    run, run_start = 0, 0
    for n, line in enumerate(lines, 1):
        m = STEP_RE.match(line)
        if m:
            body = m.group(2)
            if words(body) > STEP_MAX_WORDS:
                flag(n, f"step is {words(body)} words; keep one action, move the rest to sub-bullets")
            prose = re.sub(r"`[^`]*`|\"[^\"]*\"|\[[^\]]*\]\([^)]*\)", "X", body)  # quoted UI text and link titles may contain periods
            if words(body) > 15 and re.search(r"[.!?]\s+[A-Z]", prose.rstrip(".")):
                flag(n, "step has several sentences; one action per step")
            if run == 0:
                run_start = n
            run += 1
        elif line.startswith("#") or CALLOUT_CLOSE_RE.match(line) or "<details" in line or "</details>" in line:
            run = 0
        if run == RUN_MAX_STEPS + 1:
            flag(run_start, f"over {RUN_MAX_STEPS} steps without a heading; split into Section I/II")


VAGUE_REF_RE = re.compile(r"\b(the (step|steps|section) above|(the )?previous (step|steps|section)|an earlier step"
                          r"|the step before|(do|repeat) what you did (earlier|before))\b", re.I)


def check_references(lines, flag):
    for n, line in enumerate(lines, 1):
        m = VAGUE_REF_RE.search(line)
        if m:
            flag(n, f'"{m.group(0)}" is a vague back-reference; name the section and step ("Section I, step 14")')


def check_list_breaks(lines, flag):
    in_run, broken_at = False, None
    for n, line in enumerate(lines, 1):
        if STEP_RE.match(line):
            if broken_at:
                flag(broken_at, "unindented block between numbered steps restarts the list at 1; "
                                "indent it under the step above (4 spaces) or end the list here")
                broken_at = None
            in_run = True
        elif line.startswith("#") or line.startswith("---"):
            in_run, broken_at = False, None
        elif in_run and line.strip() and not line[:1].isspace() and broken_at is None:
            broken_at = n


def check_paragraphs(lines, flag):
    para, start, in_callout = [], 0, False
    for n, line in enumerate(lines + [""], 1):
        if CALLOUT_OPEN_RE.match(line) or CALLOUT_CLOSE_RE.match(line):
            in_callout = not CALLOUT_CLOSE_RE.match(line)
        prose = line.strip() and not STRUCTURAL_RE.match(line) and not line.startswith("    ")
        if prose and not in_callout:
            if not para:
                start = n
            para.append(line)
            continue
        if para and words(" ".join(para)) > PARA_MAX_WORDS:
            flag(start, f"paragraph is {words(' '.join(para))} words; cut to 3 sentences or use bullets/table/fold")
        para = []


def check_callouts(lines, flag):
    for n, line in enumerate(lines, 1):
        m = CALLOUT_OPEN_RE.match(line)
        if not m:
            continue
        kind = next(g for g in (m.group(2), m.group(4), m.group(5)) if g).lower()
        if kind not in CALLOUT_KINDS or line.lstrip().startswith(">"):
            continue  # GitHub alerts are checked as paragraphs
        body = []
        if m.group(1):  # ::: container, closed by the same colon count
            close = re.compile(r"^\s*" + m.group(1) + r"\s*$")
            for later in lines[n:]:
                if close.match(later):
                    break
                body.append(later)
        else:  # !!! / ??? admonition, body is the indented block
            for later in lines[n:]:
                if later.strip() and not later.startswith("    "):
                    break
                body.append(later)
        if words(" ".join(body)) > CALLOUT_MAX_WORDS:
            flag(n, f"{kind} callout is {words(' '.join(body))} words; keep callouts to 1-3 sentences")


RESPONDING_RE = re.compile(
    r"^(Run|Install|Boot|Reboot|Connect|Sign in|Log in|Flash|Deploy|Upgrade|Execute|Pair|Apply|Inject"
    r"|Update)\b|`(sudo|docker|npm|pnpm|yarn|pip|uv"
    r"|python|curl|git|cargo|brew|apt|systemctl|fastboot|adb|kubectl)\b", re.I)
OUTCOME_RE = re.compile(r"\bshould\b|\byou (will )?see\b|\bappears?\b|\bshows?\b|\bprints?\b|\breturns?\b"
                        r"|\bdisplays?\b|^\s*[-*+]\s+If\b|troubleshoot", re.I)
RESPONDING_MIN = 3


def check_failure_sweep(lines, flag):
    steps = [i for i, l in enumerate(lines) if STEP_RE.match(l)]
    responding, bare = 0, []
    for i in steps:
        body = STEP_RE.match(lines[i]).group(2)
        if not RESPONDING_RE.search(body):
            continue
        responding += 1
        under = [body]
        for later in lines[i + 1:]:
            if STEP_RE.match(later) or (later.strip() and not later[:1].isspace()):
                break
            under.append(later)
        if not any(OUTCOME_RE.search(u) for u in under):
            bare.append(i + 1)
    if responding >= RESPONDING_MIN and len(bare) * 2 > responding:
        flag(bare[0], f"{len(bare)} of {responding} steps that wait on the system have no checkpoint or "
                      "failure branch under them; run the failure sweep")


def check_page(lines, flag, path):
    if "/_" in path or path.startswith("_"):
        return  # include partials are fragments, not pages
    h1 = [n for n, l in enumerate(lines, 1) if re.match(r"^#\s", l)]
    if len(h1) > 1 or (not h1 and not path_has_title(path)):
        flag(h1[1] if len(h1) > 1 else 1, f"page has {len(h1)} H1 headings; use exactly one")
    has_steps = any(STEP_RE.match(l) for l in lines)
    tail = [l for l in lines if l.strip() and not CALLOUT_CLOSE_RE.match(l)][-8:]
    if has_steps and not any("](" in l for l in tail):
        flag(len(lines), "page with steps ends without a signpost link (Continue to / Return to)")


def path_has_title(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(2000)
    return head.startswith("---") and re.search(r"^(title|layout):", head, re.M) is not None


def check_file(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read().splitlines()
    lines = without_code(strip_frontmatter(raw))
    flags = []

    def flag(n, msg):
        flags.append((n, msg))

    for check in (check_steps, check_paragraphs, check_callouts, check_references, check_list_breaks):
        check(lines, flag)
    h1 = next((l for l in lines if l.startswith("# ")), "")
    if "troubleshoot" not in (path + h1).lower():  # fix lists there are remedies, not walkthroughs
        check_failure_sweep(lines, flag)
    check_page(lines, flag, path)
    for n, msg in sorted(set(flags)):
        print(f"{path}:{n}: {msg}")
    return len(set(flags))


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    total = sum(check_file(p) for p in sys.argv[1:])
    print("clean" if total == 0 else f"{total} flag(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
