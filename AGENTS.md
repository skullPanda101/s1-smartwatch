# Agent working agreement

Read `docs/HANDOFF.md` first, then `docs/PLAN.md` and the files touched by the current phase.

- Work one phase at a time. Do not mark hardware or phone tests passed based on Mac tests or documentation.
- At the end of every work session/phase, update `docs/HANDOFF.md` with implemented changes, exact checks/results, open blockers and the next smallest action. Keep the plan's status consistent.
- Preserve local-only `research/`. Never add research exports, credentials, device/account identifiers, recordings or private endpoint configuration to Git. Inspect the staged diff before committing or pushing.
- Use official Zepp documentation/templates; verify target compatibility before generating the watch project. Do not guess manifests or browser API availability in Side Service.
- Keep dependencies minimal. Do not change global Node installations, log into accounts, configure VPN/Serve or expose network services without approval.
- Never enable agent execution before transport, authentication and the locked-phone gate pass. See the plan for explicitly labeled backend-only fallback tests.
- Do not leave servers running silently. Report anything the operator must start or stop.
