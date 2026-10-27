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
2. **Keep `LICENSE_NOTES.md`** (this file) in the repository for operators and contributors.
3. **Ship a single post-sign-in “Legal notices” page** at `/static/oss/oss.html` (title: *Legal notices*). That page holds:
   - the Apache License 2.0 notice and a link to `NOTICE.txt`;
   - the AGPLv3 notice and a link to `LICENSE.txt`;
   - the **AGPL §13 corresponding-source offer** (public repository link and/or written offer), because section 13 requires offering source to network users, not only on request.
4. **Do not show licence or upstream project names before sign-in.** Login, signup, footers, error pages, and email templates must not mention open-source licences, project names from the upstream stack, or link to Legal notices. The only product entry points to Legal notices are after sign-in:
   - Help menu → **Legal notices**
   - About dialog → *Astra Loop includes third-party software; see **Legal notices***
5. **Do not use Mattermost trademarks** in user-facing product surfaces. Astra Loop is intentionally rebranded so the Mattermost name, logo, and wordmark do not appear there.

## Where attribution appears in the product

| Surface | Content |
|---------|---------|
| Help menu (signed-in) | One link: **Legal notices** |
| About dialog (signed-in) | “Astra Loop includes third-party software; see Legal notices.” |
| `/static/oss/oss.html` | Legal notices page (Apache NOTICE, AGPLv3, AGPL §13 source offer, links to `LICENSE.txt` / `NOTICE.txt`) |
| Login / signup / pre-auth footer / emails / error pages | No licence links and no upstream project names |

The running build’s `BuildHash` / git SHA should remain reconcilable with the published corresponding source.
