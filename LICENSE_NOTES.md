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
   - a **written corresponding-source offer** (no public repository URL, no fork/build-hash pointers, and no “modified” wording in the product copy):  
     *Source code for open-source components of this service is available on request. Contact support@astraconnect.io.*
4. **Operate a `support@astraconnect.io` request process** that can fulfil AGPL §13 corresponding-source requests (and related source-on-request offers) within a reasonable time. The in-product Legal notices page depends on that mailbox being monitored and able to deliver source.
5. **Do not show licence or upstream project names before sign-in.** Login, signup, footers, error pages, and email templates must not mention open-source licences, project names from the upstream stack, or link to Legal notices. The only product entry points to Legal notices are after sign-in:
   - Help menu → **Legal notices**
   - About dialog → *Astra Loop includes third-party software; see **Legal notices***
6. **Do not use Mattermost trademarks** in user-facing product surfaces. Astra Loop is intentionally rebranded so the Mattermost name, logo, and wordmark do not appear there.
7. **About dialog** shows product version information only — not Build Hash / EE Build Hash (or other repo/commit pointers).

## Where attribution appears in the product

| Surface | Content |
|---------|---------|
| Help menu (signed-in) | One link: **Legal notices** |
| About dialog (signed-in) | “Astra Loop includes third-party software; see Legal notices.” Version lines only (no build hashes). |
| `/static/oss/oss.html` | Legal notices page (Apache NOTICE, AGPLv3, written source offer to `support@astraconnect.io`, links to `LICENSE.txt` / `NOTICE.txt`). No repo URLs. |
| Login / signup / pre-auth footer / emails / error pages | No licence links and no upstream project names |

## Decision: written offer instead of a public repo link

Product surfaces intentionally omit GitHub / repository / fork / build-hash pointers so the deployment does not advertise upstream project names or source locations in UI chrome. AGPL §13 is satisfied by the written offer on the Legal notices page plus an operational process at **support@astraconnect.io** that can provide corresponding source on request. Operators must not remove that offer or the support contact without replacing it with another compliant §13 mechanism.
