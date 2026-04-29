#!/usr/bin/env node

const { spawnSync } = require('node:child_process');
const path = require('node:path');
const os = require('node:os');

const args = process.argv.slice(2);

if (args[0] === '--help' || args[0] === '-h') {
  console.log('Usage: gsd-sdk query <command> [args]');
  console.log('Compatibility shim for Codex on Windows. Forwards to gsd-tools.cjs.');
  process.exit(0);
}

if (args[0] !== 'query') {
  console.error('Usage: gsd-sdk query <command> [args]');
  process.exit(1);
}

const queryArgs = args.slice(1);
if (queryArgs.length === 0) {
  console.error('Usage: gsd-sdk query <command> [args]');
  process.exit(1);
}

const command = queryArgs[0];
const rest = queryArgs.slice(1);
const expanded = command.includes('.') ? command.split('.').filter(Boolean) : [command];
const gsdTools = path.join(os.homedir(), '.codex', 'get-shit-done', 'bin', 'gsd-tools.cjs');

const result = spawnSync(process.execPath, [gsdTools, ...expanded, ...rest], {
  cwd: process.cwd(),
  env: process.env,
  stdio: 'inherit',
  windowsHide: true,
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
