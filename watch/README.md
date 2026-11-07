# Watch scaffold gate

This directory is intentionally not an installable Zepp project yet.

Before generation, confirm the exact GTR 4 model, firmware, phone OS, Zepp developer access and current official toolchain/device target. Follow Stage 0 in `../docs/PLAN.md`.

Generate the official compatible mini-app starter here, retaining its Device App, Side Service and manifest conventions. First feature: **Ping Mac**, with idle/pending/success/error states. The Side Service performs the network request; the watch sends a message and displays the returned text.

No voice keyboard, recorder, transfer API, agent dependency or guessed manifest entries belong in the initial ping app. Add those only after their respective hardware gates pass.
