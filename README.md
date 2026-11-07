# GTR 4 → Mac connectivity experiment

Prove the Amazfit GTR 4 → Zepp phone Side Service → Mac → watch round trip before buying Balance 2 or adding AI.

## Status

Scaffold only. No watch app has been generated or installed; device compatibility is unverified. Original exported conversations and attachments are grouped in local-only `research/`, excluded from Git. They are research inputs, not authoritative specifications. Never place credentials in tracked project files.

- [Detailed implementation and hardware test plan](docs/PLAN.md)
- [Watch scaffold and prerequisites](watch/README.md)

## Mac probe (Python 3.9+; no dependencies)

```sh
python3 mac/server.py
```

In another terminal:

```sh
curl http://127.0.0.1:8765/ping
python3 -m unittest discover -s tests -v
```

Expected response: `{"message": "pong from Mac"}`.

The probe binds to loopback by default. For a trusted local Wi-Fi test only:

```sh
python3 mac/server.py --host 0.0.0.0
# On the phone, open http://<Mac-LAN-IP>:8765/ping
```

Allow Python through the macOS firewall only on a trusted network. Stop the server with Ctrl-C when finished. No port forwarding, public tunnels, agent execution, audio upload, or credentials are implemented.

## Layout

```text
mac/server.py     Standard-library HTTP ping probe
watch/README.md   Zepp app boundary and scaffold gate
docs/PLAN.md      Stages, acceptance checks, risks, and decisions
tests/            Mac probe integration tests
research/         Original exports and attachments (local only, ignored)
```

The watch source/configuration will be generated with the official Zepp tooling after checking the current GTR 4 target. Do not interpret the `watch/` placeholder as an installable mini app.
