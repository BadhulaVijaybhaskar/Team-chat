# Astra Loop deploy notes

Operator notes for running Astra Loop behind a reverse proxy. Product licence
placement and AGPL §13 process are documented in [`LICENSE_NOTES.md`](LICENSE_NOTES.md).

## Headers to strip at nginx

These response headers are emitted by the application and cannot be renamed or
removed safely in app code without breaking clients, sessions, or upstream
compatibility. Strip or rewrite them at the edge (nginx / ingress) if you do not
want build metadata or request correlation IDs visible in browser DevTools.

| Header | Value pattern (examples) | Why strip / rewrite at nginx |
|--------|--------------------------|------------------------------|
| `X-Version-Id` | `12.1.0.dev.<40-hex-hash>.false` or `12.1.0.<build>.<hash>.true` | Embeds a build/commit-style hash. Safe to drop or replace with a coarse product version (e.g. `12.1.0`) at the proxy. |
| `X-Request-Id` | 26-character lowercase id (e.g. `8ttr5dudk3dm8ftcy7a35t1m5o`) | Request correlation id. Optional to keep for support; strip if your threat model treats it as sensitive. |

### Example nginx snippet

```nginx
# Inside the location that proxies to Astra Loop (port 8065):
proxy_hide_header X-Version-Id;
proxy_hide_header X-Request-Id;
# Optional: advertise a coarse version instead of the upstream build hash
# add_header X-Version-Id "12.1.0" always;
```

Do **not** strip session cookies (`MMAUTHTOKEN`, `MMUSERID`, `MMCSRF`, `MMEMBED`) or
`X-Content-Type-Options` / `X-Frame-Options` / CSP-related headers — those are
required for security and session continuity.

## Static assets

Production web builds are configured to:

- omit source maps (`devtool: false`);
- omit extracted `*.js.LICENSE.txt` companion files (Terser `extractComments: false`).

Repo-root [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.txt`](NOTICE.txt) remain the
canonical licence texts and are also served from `/static/oss/` for the Legal
notices page. Do not delete those.
