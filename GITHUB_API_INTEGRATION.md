# GitHub API update-check integration

This optional, read-only tool checks the latest repository commit using the **GitHub REST API** endpoint `GET /repos/{owner}/{repo}/commits`. It is independent of Polymarket trading, wallets, and Telegram, and does not change existing bot behavior.

## Run

```bash
python3 github_version_check.py --repo YulenJade/polymarket-whale-monitor
python3 github_version_check.py --repo YulenJade/polymarket-whale-monitor --known-sha YOUR_PREVIOUS_SHA
python3 -m unittest discover -s tests -p 'test_github_version_check.py' -v
```

The JSON result includes the latest SHA and its GitHub URL. When `--known-sha` is provided, `update_available` indicates whether the latest commit differs. This detects repository changes, **not** whether a release is newer or whether deployment is advisable.

Public repositories normally work without credentials, subject to GitHub API rate limits. Optionally set `GITHUB_TOKEN` locally for authenticated requests. Never commit tokens or private keys. The tool makes no writes and does not automatically deploy or restart anything.

## Developer Program relevance

This is a real integration with the GitHub REST API, but program acceptance is decided by GitHub. A support contact email and any other current eligibility requirements remain the account owner's responsibility.
