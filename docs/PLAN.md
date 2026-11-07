# GTR 4 connectivity-first implementation plan

## Goal and limits

Use the existing GTR 4 to validate a push-to-talk remote AI workflow before purchasing Balance 2. First milestone: tap a button and display a response from the Mac. No AI dependency is needed to prove transport.

Target architecture:

```text
Watch Device App ↔ Bluetooth messaging ↔ Zepp Side Service on phone
                                         ↕ HTTP(S)
                                      Mac endpoint
                                         ↓ later
                               transcription → restricted agent
```

The phone Side Service, not the watch itself, makes the network request. Watch Wi-Fi hardware and built-in voice assistants do not establish third-party network or microphone access.

## Current scaffold

- Implemented: dependency-free Mac `/ping` probe; loopback default; integration tests.
- Pending: official Zepp project generation, watch UI, phone messaging/fetch, hardware testing.
- Not implemented: audio, STT, agent calls, remote networking, voice playback.
- Source conversations remain unchanged and are excluded from Git alongside attachments, recordings and generated watch output. Use local Git checkpoints before generating or changing the watch project; no remote or automatic commits are required.

## Stage 0 — confirm the environment and API contract

Record before generating the watch app:

- Exact watch model (GTR 4 versus Limited Edition), firmware, Zepp OS version, region.
- Android or iOS, phone OS version, Zepp app version, developer-mode availability.
- Mac Python and Node versions; current official Zepp CLI requirements.
- Whether phone and Mac can share a trusted Wi-Fi network without client isolation.

Check primary documentation rather than relying on the exported conversations:

- Device targets/API levels: https://docs.zepp.com/docs/reference/related-resources/device-list/
- Architecture: https://docs.zepp.com/docs/guides/architecture/arc/
- Recorder: https://docs.zepp.com/docs/reference/device-app-api/newAPI/media/Recorder/
- TransferFile: https://docs.zepp.com/docs/reference/device-app-api/newAPI/transfer-file/TransferFile/
- Side Service fetch: https://docs.zepp.com/docs/v2/reference/side-service-api/fetch/

Verify current equivalents of these links, supported messaging mechanism, fetch response shape, HTTP/HTTPS restrictions, permissions, device target and simulator/deployment instructions. Verify API-level requirements and device exclusions separately for audio and transfer. Do not assume an API-level threshold guarantees hardware support.

Acceptance: fill in the environment facts and select an official compatible starter. If development installation is unavailable, resolve that before building features.

## Stage 1 — prove phone → Mac

1. Run `python3 -m unittest discover -s tests -v`.
2. Run `python3 mac/server.py`; verify `/ping` locally.
3. On trusted Wi-Fi, restart with `--host 0.0.0.0`.
4. Find the Mac's active LAN address in Network settings. Open `http://<Mac-IP>:8765/ping` on the phone.
5. If blocked, check active interface, firewall, VPN routing and Wi-Fi client isolation. Do not disable the firewall globally.

Acceptance: phone displays `pong from Mac`. Record address/port and network conditions, not secrets. Browser success proves reachability only; Side Service fetch is a separate check.

### Stage 1b — trusted HTTPS before Side Service testing

LAN HTTP above is a diagnostic only, not a promise that Zepp fetch permits cleartext. Mobile app policy depends on Zepp's configuration; a browser opening the URL does not establish sandbox compatibility. Do not weaken certificate validation or assume a self-signed certificate works.

Prefer a stable, trusted HTTPS hostname through private networking, for example Tailscale Serve forwarding to the loopback probe. Verify current setup, certificate prerequisites, phone VPN routing and tailnet access rules before using it; do not enable public Funnel. Tailscale is an optional installation requiring operator approval, not a scaffold dependency. Verify Zepp Side Service fetch against the HTTPS URL before investing in audio. Private TLS does not replace application authentication for later uploads/jobs.

If private networking cannot work inside Zepp, choose another explicitly approved authenticated HTTPS route or mark transport blocked. Use a stable hostname rather than compiling changing LAN addresses into each build. Confirm DNS and connectivity after a network change.

## Stage 2 — watch → phone → Mac → watch

Generate the official project inside `watch/` only after Stage 0. Keep its generated conventions and supported dependencies. Avoid a custom Android app.

Implement only:

- Device App: one readable, accessible **Ping Mac** button and status text.
- States: idle → sending → success or actionable error; suppress duplicate taps while pending.
- Side Service: receive a ping, fetch the configured Mac `/ping`, validate successful status and the expected string response, return a small result.
- Use a bounded request timeout supported by the tooling; if fetch cannot be cancelled, ignore late replies after timeout using request correlation.
- Show disconnected, timeout and network/server failures instead of an endless spinner. Do not log credentials.
- Configure the Mac URL in the simplest supported local configuration; no settings UI unless needed.

Do not import newer voice keyboard APIs into the GTR 4 build. Do not invent manifest permissions or device identifiers.

Acceptance on real hardware:

- Ten sequential taps each display the returned text; record latency and failures.
- Phone Bluetooth off results in an error and the next attempt succeeds after reconnecting.
- Mac server stopped gives an error; restarting permits recovery.
- Establish a foreground baseline. Then leave the phone locked with Zepp backgrounded for 15 minutes and complete five consecutive watch pings without unlocking it; record timing and results. Repeat after another idle period to expose suspension after the first wakeup.
- Failure of that locked-phone test blocks the pocket/hands-free workflow and Stages 3–5 on that architecture. Diagnose documented OS battery/background settings without assuming they guarantee operation. A foreground-only demo may continue only as an explicitly reduced goal.
- Simulated messaging/fetch tests cover valid response, malformed response, failed request and timeout. Simulator success alone is insufficient.

Exit gate: save the firmware, phone state, tool versions and measured results before adding audio.

## Stage 3 — microphone and file transfer

1. Verify supported recorder permissions, output format/path and recording lifecycle on the actual firmware.
2. Record a deliberately short clip (initial target: five seconds); stop cleanly on user action/page exit and surface permission/device failures.
3. First confirm a nonempty file exists; then test watch → Side Service transfer using the documented API.
4. Confirm Side Service can read and upload transferred bytes without corruption. Check available buffer, encoding and fetch APIs; do not assume browser `Blob` or `FormData`. Use Base64 JSON if supported and binary upload is unavailable; account for roughly one-third encoding overhead and device memory. Compare decoded byte count/hash with the source where accessible.
5. Only then add a Mac upload endpoint with authentication, encoded-body and decoded-byte limits, timeout, safe server-generated filenames and a fixed storage directory. Never trust client paths. Use the asynchronous job contract below, not blocking STT inside the request handler.
6. Inspect the first transferred file's header bytes and container metadata before selecting a decoder. An `.opus` extension does not prove Ogg Opus; custom framing is a hypothesis to inspect, not an established device fact. Test standard decoding first; write a frame converter only against verified format evidence and a small fixture test. Remove temporary recordings after each test; obtain consent before retaining speech.

Acceptance: intelligible clip reaches Mac repeatedly, with bytes/duration and transfer latency recorded. Test cancellation, empty recording, disconnected transfer and oversized upload. No streaming audio or continuous recording.

Timebox: spend at most one focused two-hour session on initial recorder/transfer debugging, then record the blocker. Mac-recorded samples can validate the STT/agent backend separately, but do not count as a watch-audio pass or override the locked-phone gate.

### Stages 3–5 — asynchronous job contract (planned, not implemented)

- Authenticated `POST /jobs` accepts a bounded audio payload (or a text request when testing the backend independently) with an `Idempotency-Key`. Validate and admit the job before returning `202` with `job_id`; return an explicit error if admission fails. STT and agent work run outside the HTTP handler, with bounded queue size/concurrency and subprocess deadlines.
- Scope keys/jobs to the authenticated client. The same key and payload returns the existing job; the same key with a different payload returns `409`. Retain deduplication records for a documented retry window. Never blindly retry an expired submission, especially an agent task.
- Authenticated `GET /jobs/{job_id}` returns `queued`, `running`, `succeeded` or `failed`, plus bounded result/error data. Unknown/expired IDs return an explicit error. Check authorization on reads as well as writes.
- Persist the active job ID and retry key using verified supported watch/phone storage. Poll only while the app is active (initial target: every two seconds, backing off to ten seconds after transient failures). Stop after a bounded session; resume the same job on reopen rather than resubmitting. Polling does not keep a suspended Side Service alive.
- Verify the watch's supported screen-awake API and maximum duration; use it only during a bounded user-visible active session, and release it on exit. Correctness must not depend on keeping the display on: completed results remain retrievable after wrist drop/reopen.
- For the prototype, an in-memory bounded job store is sufficient if Mac restart explicitly means job loss and the UI never automatically resubmits lost work. Set and document result/deduplication expiry before implementation. Add persistence only if restart recovery becomes a requirement.
- Tests must cover duplicate submissions, conflicting keys, queue full, worker timeout/failure, unauthorized reads, expiry/restart and resumed polling. A deliberately slow job must not block `/ping` or status requests. `ThreadingHTTPServer` already provides threaded request handling, but threads alone do not bound work or prevent resource exhaustion.

## Stage 4 — transcription

Choose one local STT tool after inspecting a real watch sample, or use a clearly labeled Mac-recorded fallback sample if Stage 3 is blocked; verify decoding. Return transcript text through job status before involving an agent. Set input-size/duration limits and execution timeouts. Keep private audio and transcripts out of logs/source control.

Acceptance: three short spoken phrases produce readable transcripts on the watch; failures are visible and retryable. Record end-to-end latency and language accuracy.

## Stage 5 — restricted AI task

Choose Pi or Hermes integration after transport works; verify its documented interface at that time. Start with one fixed read-only task, not arbitrary shell execution. Treat dictated prompts as untrusted input. Require authentication before enabling this stage; keep agent credentials on Mac only, restrict accessible files/tools, bound execution time and response size, and require explicit confirmation for destructive actions.

Acceptance: a fixed read-only request returns a short result; unauthenticated requests are rejected; duplicate submissions do not launch repeated tasks. Do not expose a raw agent or shell port.

## Stage 6 — optional playback and off-LAN validation

Playback is separate from text replies: verify codec support, file transfer back to the watch, speaker output, cleanup and interruption behavior. Test an existing small audio file before adding TTS.

Trusted HTTPS was established in Stage 1b. Now repeat the locked-phone gate and job-resumption tests on mobile data/off-LAN; do not assume LAN success proves remote routing or background reliability. No router port forwarding or public unauthenticated endpoint.

## Results log template

For each hardware run record:

- Date; watch/firmware; phone OS/Zepp version; project/tool version.
- Stage and exact action; Wi-Fi/Bluetooth/background conditions.
- Expected versus observed result; repeated successes/attempts; latency.
- Error text; workaround; pass/fail/blocked and next smallest experiment.

Do not record tokens, personal audio, or private agent output in this log.

## Balance 2 purchase gate

Make the purchase decision using separate evidence: shared messaging/network/backend feasibility, and device-specific voice input. Verify current Balance 2 system voice-to-text API availability, firmware, language/region and third-party permissions independently; if supported, it may bypass recorder/file transfer entirely. Do not make solving GTR 4 audio framing a prerequisite for buying Balance 2. Reuse Mac services and the protocol where compatible, but validate the Balance 2 target, audio, newer voice APIs, background behavior and battery independently. A GTR 4-specific failure neither proves nor disproves Balance 2 support.

## Deferred deliberately

No custom phone app, cloud backend, database, framework, CI, agent SDK, streaming microphone, TTS or production deployment yet. Git tracking is established now; trusted HTTPS is brought forward, with network installation/configuration still requiring approval. Add only what the next proven stage needs.
