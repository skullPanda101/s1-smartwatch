# Implementation handoff

## Current checkpoint — Stage 0 CLI startup resolved; starter build pending

Stage 0 documentation/toolchain reconnaissance is complete. Operator reports GTR 4 running Zepp OS 3.5, paired with Android HyperOS 3.0.3, and version 7.6.0.2 (whether this is watch firmware or phone app version needs clarification). Template selection remains pending. Stage 1 Mac tests pass, but phone/network and all watch gates are untested. Do not jump to audio or AI.

## Implemented

- Mac standard-library `ThreadingHTTPServer` with loopback-default `GET /ping` and two integration tests.
- Phase plan in `docs/PLAN.md`; original exports/attachments moved to ignored `research/`.
- `AGENTS.md` requires this handoff to be updated after every phase/session.
- Git initialized; private remote `skullPanda101/s1-smartwatch`; baseline commit `5f1ef02`. No credentials or recordings belong in tracked files.
- No Zepp project, jobs API, authentication, audio pipeline or AI integration implemented.

## Verified in this session (2026-11-07)

- Python `3.14.4`; Node `v26.5.0`; npm `11.17.0`.
- `zeus` not found on PATH. npm registry reports `@zeppos/zeus-cli` version `1.9.3`; no engines metadata returned by the query.
- `tailscale` binary exists; login, routing, Serve and certificate configuration were NOT inspected or changed.
- `python3 -m unittest discover -s tests -v`: 2 tests passed. No server left running.
- `pyright tests/test_server.py --project pyrightconfig.json`: 0 errors/warnings. Active LSP check of `tests/test_server.py` and `mac/server.py`: 0 diagnostics; previous import-resolution blocker is resolved.

## Primary documentation findings

Retrieved official pages below in this session; facts describe documentation, not the operator's firmware:

- Device list: GTR 4 latest API level **3.6**, Zepp OS **3.5**, **466×466**, deviceSource values `7930112` (Mainland China), `7930113`, `7864577`. Confirm exact variant before selecting target.
  https://docs.zepp.com/docs/reference/related-resources/device-list/
- Environment guide recommends Node LTS and Zeus CLI; currently illustrates Node 24. Installed Node 26 compatibility is not proven. Do not replace global Node automatically.
  https://docs.zepp.com/docs/guides/quick-start/environment/
- Official starter workflow: `zeus create <name>` followed by interactive selection. Generate into a temporary sibling first or otherwise preserve `watch/README.md`; do not blindly overwrite an existing directory.
  https://docs.zepp.com/docs/guides/quick-start/create/
- Watch preview: `zeus preview` compiles a QR code; paired Zepp app installs via developer Scan. Documented developer mode: Profile → Settings → About → tap Zepp icon seven times. Actual app UI may differ.
  https://docs.zepp.com/docs/guides/quick-start/preview/
- Side Service fetch differs from browser fetch: object options support `url`, `method`, `headers`, `body`; sample consumes `res.body` (parse if string), NOT `res.json()`. Status field and timeout/cancellation behavior still need verification before implementation.
  https://docs.zepp.com/docs/reference/side-service-api/fetch/

## Latest implementation attempt

- Operator confirmed Zepp **Developer Mode → Scan** is available. Developer-mode availability is no longer a blocker; physical installation remains untested.
- Ran `npx --yes @zeppos/zeus-cli@1.9.3 --help` to inspect the official CLI without a global installation.
- Failed with `Error: Cannot find module 'zeppos-app-utils'`; npm also reported deprecated transitive dependencies. No watch project was generated and no preview QR exists. CLI startup failure on Node 26 does not itself prove Node is the cause.
- Investigation: npm tarball dry-run lists 981 bundled private-module files, including the missing implementation. Thus the published tarball is NOT missing it; the npx extraction inspected locally contained only its package.json. Earlier claim of a broken published package was incorrect.
- Direct clean extraction to `/tmp/s1-zeus-clean/package` plus explicit module-alias registration using cached dependencies successfully displayed CLI 1.9.3 `--help` on Node 26. This demonstrates startup compatibility only, not a reproducible installed toolchain or build.
- Added root `package.json` pinning CLI 1.9.3 with `npm run zeus`. Local npm installation attempts timed out; no lockfile or functional local executable exists yet. Do not claim this scaffold command works yet.
- Ignored `.tools/` contains incomplete extracted third-party investigation files, not authored project source. Do not repair vendor diagnostics. Cross-volume move to /tmp failed; files remain ignored locally. No global Node/npm configuration was changed.
- RESOLVED: full install on local filesystem succeeded. Working pinned CLI is at `$HOME/.cache/s1-smartwatch-zeus`; `tools/zeus.cjs` explicitly registers the CLI's bundled module alias. `npm run zeus -- --help` / `--version` are the project entrypoints; setup is in `tools/README.md`. Root package.json has no dependencies; do not run a large install on the mount.
- Verified launcher help and version: Node 26.5.0, Zeus 1.9.3, zpm 3.4.2. Normal bin startup still fails alias resolution even with a complete install, so explicit registration is necessary here. No global config or vendor code was patched.
- Incomplete `.tools` files were moved outside the repo to sibling `../s1-smartwatch-cli-investigation`. Prior notes about their remaining inside the repo are superseded. No project node_modules or lockfile is required.
- Next action: use the launcher to inspect create/build commands and generate a compatible starter on the fast local filesystem before copying authored project files into watch/. No preview or watch installation has occurred.

## Blocking questions for operator

1. GTR 4 / Zepp OS 3.5 confirmed by operator; exact regional variant still unknown (no serial number needed).
2. Android HyperOS 3.0.3 confirmed; clarify what version 7.6.0.2 identifies and Zepp developer Scan is confirmed available.
3. Can phone and Mac share trusted Wi-Fi? Is private HTTPS/Tailscale wanted and available on the phone?

## Operator screenshots reviewed (2026-11-07)

Screenshots were read from operator-provided local files, not copied into tracked source. Store listings are claims, not successful hardware tests.

- **Voice AI**, author **alex**, 1.01 MB, in-app purchases: listing advertises hold-to-talk, Grok voice replies through watch speaker, on-screen answers and Zepp-side settings. No evidence of custom endpoint support or actual GTR 4 recording/transfer behavior. Candidate for comparison, not a proven Mac bridge; consider third-party speech privacy before testing.
- **HA Companion Free**, author **Aguacatec**, 2.30 MB: listing advertises Home Assistant device control. Changelog explicitly limits voice assistant to **Zepp OS 4 or higher**, so do not plan its voice feature on GTR 4 OS 3.5. Permission dialog requests extensive sensor/health/user-data access; do not grant merely to test ping.
- **Voice Memo** screen shows a 28.08-second item marked not transferred. Transfer prompt says phone connects to watch via Wi-Fi, leaves its current Wi-Fi network, then reconnects afterward. This stock transfer route is NOT proof of mini-app BLE transfer support; LAN Mac connectivity may be interrupted during that operation.
- Store grid also shows Zepp Flow, TranslateGo, Dudu, Walkie Talkie and others; functionality/compatibility not investigated.
- Operator says watch is connected to Mac; connection type and developer accessibility are unverified. Normal Zepp deployment still uses the paired phone/QR workflow unless another supported route is established.

## Next smallest actions

1. Obtain those answers; record only non-sensitive compatibility facts.
2. Verify official messaging/framework/configuration docs for a GTR 4-compatible starter and choose Node LTS execution if needed. Install pinned project-local tooling rather than unrequested global changes; do not authenticate as the user.
3. Finish Stage 0 by building the compatible starter; distinguish build success from physical install success.
4. Stage 1: operator runs the probe and opens it from the phone. HTTPS Stage 1b must be verified in actual Side Service before relying on fetch. Do not weaken TLS or expose a public endpoint.
5. Stage 2: implement ping and test errors, reconnect and five pings after 15 minutes locked. Only hardware evidence passes the pocket-workflow gate.

## Deliberate limits

No new dependencies installed, no phone/device tests, no microphone tests, no network changes. Documentation research is not proof of runtime support. Continue updating this file with results, blockers and next actions at every phase boundary.
