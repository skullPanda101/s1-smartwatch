# Zeus CLI setup

CLI dependencies live on the Mac's local filesystem, outside this mounted project. No global installation or Node switch is required.

```sh
npm install --prefix "$HOME/.cache/s1-smartwatch-zeus" --save-exact --ignore-scripts --no-audit --no-fund @zeppos/zeus-cli@1.9.3
npm run zeus -- --help
npm run zeus -- --version
```

`tools/zeus.cjs` explicitly registers the CLI's own bundled `zeppos-app-utils` module alias before startup. Normal CLI startup failed to resolve it in this environment. Do not install the separately published package with that name or edit vendor files. The tarball contains the bundled implementation; initial incomplete npx extraction was a separate misleading symptom.

The mount was too slow for local dependency extraction; interrupted files were moved to sibling `../s1-smartwatch-cli-investigation` outside the project. Those are disposable investigation files, not application source. The working installation is in the home cache above. Its transitive dependencies include deprecated packages; use it for development only.

Verified: help and version on Node 26.5.0, Zeus 1.9.3, zpm 3.4.2. Building/previewing a watch app remains a separate gate. Run the launcher by absolute path when working from a generated watch directory, so Zeus uses that directory as the project root. Login/preview may require the operator's Zepp authentication; never commit account state or QR images.
