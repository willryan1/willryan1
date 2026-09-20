"""Rewrites the activity section of the profile README from public GitHub events."""

import json
import os
import pathlib
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone

USER = "willryan1"
README = pathlib.Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!--START:activity-->", "<!--END:activity-->"
MAX_ENTRIES = 6


def fetch_events():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/events/public?per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def describe(event):
    """A short phrase for one event, or None for event types we don't surface.

    The public events API no longer includes commit counts in PushEvent payloads,
    so pushes are reported without a number.
    """
    kind, payload = event["type"], event.get("payload", {})
    if kind == "PushEvent":
        return "pushed"
    if kind == "PullRequestEvent":
        action = payload.get("action")
        if action == "closed" and payload.get("pull_request", {}).get("merged"):
            return "merged a pull request"
        if action == "opened":
            return "opened a pull request"
        return None
    if kind == "IssuesEvent" and payload.get("action") == "opened":
        return "opened an issue"
    if kind == "ReleaseEvent" and payload.get("action") == "published":
        return "published a release"
    if kind == "CreateEvent" and payload.get("ref_type") == "repository":
        return "created the repository"
    return None


def build_lines(events):
    """One line per repo, newest first, listing what happened there."""
    rows = OrderedDict()
    for event in events:
        phrase = describe(event)
        if not phrase:
            continue
        repo = event["repo"]["name"]
        when = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        row = rows.setdefault(repo, {"when": when, "notes": []})
        row["when"] = max(row["when"], when)
        if phrase not in row["notes"]:
            row["notes"].append(phrase)

    # Prefer the more interesting verbs when a repo has several.
    priority = {
        "merged a pull request": 0,
        "opened a pull request": 1,
        "published a release": 2,
        "opened an issue": 3,
        "created the repository": 4,
        "pushed": 5,
    }
    ordered = sorted(rows.items(), key=lambda kv: kv[1]["when"], reverse=True)
    lines = []
    for repo, row in ordered[:MAX_ENTRIES]:
        notes = sorted(row["notes"], key=lambda n: priority.get(n, 9))[:2]
        label = repo.split("/", 1)[1] if repo.startswith(f"{USER}/") else repo
        lines.append(
            f"[**{label}**](https://github.com/{repo}) · {', '.join(notes)}"
            f" · {row['when']:%b %-d}"
        )
    return lines


def main():
    try:
        events = fetch_events()
    except Exception as exc:  # never fail the workflow over a flaky API
        print(f"could not fetch events: {exc}")
        return
    lines = build_lines(events)
    if not lines:
        print("no surfaceable activity; leaving README alone")
        return

    text = README.read_text()
    if START not in text or END not in text:
        raise SystemExit("activity markers missing from README.md")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    body = "\n\n".join(lines)
    updated = f"{head}{START}\n\n{body}\n\n{END}{tail}"
    if updated != text:
        README.write_text(updated)
        print(f"updated {len(lines)} entries")
    else:
        print("no change")


if __name__ == "__main__":
    main()
