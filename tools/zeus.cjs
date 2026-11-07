// Zeus 1.9.3 does not reliably locate its bundled alias from module-alias/register.
const path = require('node:path');
const { createRequire } = require('node:module');
const home = require('node:os').homedir();
const requireTool = createRequire(path.join(home, '.cache/s1-smartwatch-zeus/package.json'));
const root = path.dirname(requireTool.resolve('@zeppos/zeus-cli/package.json'));
requireTool('module-alias').addAlias('zeppos-app-utils', path.join(root, 'private-modules/zeppos-app-utils'));
requireTool(path.join(root, 'bin/main.js'));
