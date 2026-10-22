"""Read-only GitHub API update checker for this repository.

Run: python github_version_check.py --repo YulenJade/polymarket-whale-monitor
Optional: --known-sha <previously recorded SHA> to detect changes.
"""
import argparse
import json
import os
import urllib.error
import urllib.request


def fetch_latest_commit(repo, branch=None, token=None, timeout=10):
    """Fetch the latest commit on a branch using GitHub's public REST API."""
    if not repo or repo.count("/") != 1:
        raise ValueError("repo must have owner/name format")
    owner, name = repo.split("/")
    if not all(part.replace("-", "").replace("_", "").replace(".", "").isalnum() for part in (owner, name)):
        raise ValueError("invalid GitHub repository name")
    from urllib.parse import quote
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(name)}/commits"
    if branch:
        url += "?sha=" + quote(branch, safe="")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "YulenJade-whale-monitor-update-check", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API HTTP {exc.code}; check repository, rate limits and permissions") from exc
    if not isinstance(data, list) or not data or not isinstance(data[0], dict) or not data[0].get("sha"):
        raise RuntimeError("Unexpected GitHub API response")
    return {"repo": repo, "sha": data[0]["sha"], "url": data[0].get("html_url"), "branch": branch or "default"}


def main():
    parser = argparse.ArgumentParser(description="Check latest GitHub commit (read-only)")
    parser.add_argument("--repo", default="YulenJade/polymarket-whale-monitor")
    parser.add_argument("--branch", default=None)
    parser.add_argument("--known-sha", default=None, help="Previously recorded full or abbreviated SHA")
    args = parser.parse_args()
    result = fetch_latest_commit(args.repo, args.branch, os.getenv("GITHUB_TOKEN"))
    if args.known_sha:
        result["update_available"] = not result["sha"].startswith(args.known_sha)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
