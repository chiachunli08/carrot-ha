# Publishing and updates

[한국어](PUBLISH.md) | English | [Overview](../README.en.md)

Upload the repository source, not the entire local outputs directory or your databases.

## Initial publication (maintainer)

1. Sign in to GitHub as `helico717`.
2. If the repository does not exist, choose + → New repository → `carrot-ha` → Public → Create repository.
3. Sign in to GitHub Desktop and clone the repository using File → Clone repository.
4. Copy the release folder's **contents** into the clone. `README.md`, `hacs.json`, and `custom_components` must be at the repository root, not inside another release folder.
5. Review changed files. Exclude `connection.json`, `wrangler.json`, databases, logs, tokens, and personal vehicle images or routes.
6. Enter a commit summary, commit to main, and Push origin.
7. Check the repository's Actions results if workflows are present. Resolve failures before releasing.
8. Open Releases → Draft a new release. Use a tag matching `manifest.json` (for example `v0.4.1` for version `0.4.1`). Describe changes and unverified vehicle support. Test initial builds as pre-releases before publishing a stable release.

Users add the repository URL to HACS Custom repositories. This is separate from inclusion in the HACS default list.

## Subsequent releases

Change the code, increase the manifest version (for example to `0.4.2`), test, commit, and push. Publish the matching GitHub Release `v0.4.2`. HACS can then offer the update after refreshing its repository information. Include separate instructions for collector or Cloudflare changes. Documentation-only edits do not require a runtime version bump.

References: [HACS requirements](https://hacs.xyz/docs/publish/integration/) and [HA brand images](https://developers.home-assistant.io/docs/core/integration/brand_images/).
