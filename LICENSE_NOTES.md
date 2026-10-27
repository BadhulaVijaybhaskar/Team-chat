# Astra Loop licence notes

This repository is a rebranded fork of Mattermost team edition. Upstream licence
texts remain in [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt). This
file explains how those licences apply to Astra Loop and what operators must do.

## Which parts use which licence

| Tree | Licence | Notes |
|------|---------|--------|
| `webapp/` (and related admin tools / configuration files listed in `LICENSE.txt`, including `server/templates/`, `server/i18n/`, `server/public/`) | **Apache License 2.0** | Client UI and shared configuration/tooling. |
| `server/` (excluding the enterprise stub) | **GNU AGPLv3** | Networked server. Building and shipping a modified server triggers AGPL obligations. |
| `server/enterprise/` | **Mattermost Source Available** | Present as an upstream stub only. **Unused and untouched** in this Astra Loop fork. Do not enable or ship it without a separate commercial arrangement with Mattermost, Inc. |

Compiled binaries produced from this tree also follow the upstream compiled-licence story documented in `LICENSE.txt` / `server/build/MIT-COMPILED-LICENSE.md` where applicable.

## What we must do

1. **Keep `LICENSE.txt` and `NOTICE.txt`** in the repository and in shipped images/packages.
2. **Keep the in-app “Open-source licences” page** (`/static/oss/oss.html`), worded *“Astra Loop includes open-source software”*, linking to those files. That page is the only intentional place upstream licence attribution appears in the product UI.
3. **AGPL §13 (remote network interaction).** Because users interact with a modified AGPL server over a network, we must offer them the **corresponding source** of our server changes. Practical options:
   - a prominent link on the Open-source licences page to the public source repository (or a release tag / tarball that matches the running build); and/or
   - a written offer to provide that source on a durable medium, as AGPL §13 allows.
   The running build’s `BuildHash` / git SHA should be reconcilable with the published source.
4. **Do not use Mattermost trademarks.** Astra Loop is intentionally rebranded so the Mattermost name, logo, and wordmark do not appear in user-facing product surfaces. Trademark use remains subject to Mattermost, Inc.’s trademark policy; this fork avoids that use by shipping only Astra Loop branding.

## Where attribution appears in the product

- Help / About → **Open-source licences**
- Login footer → **Open-source licences**
- Static page: `/static/oss/oss.html` → `LICENSE.txt`, `NOTICE.txt`, and the public source offer

No other product chrome should carry Mattermost branding or trademarked wordmarks.
