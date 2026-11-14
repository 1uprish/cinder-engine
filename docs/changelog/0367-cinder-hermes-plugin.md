# 0367 — 2026-11-14 — Package the CAD engine for Eve Cinder

- **Commit:** (this commit)
- **Date:** 2026-11-14
- **Author:** OpenAI Codex / Arvind

## Summary

The repository can now be installed directly as a Hermes portable Agent Plugin.
Its single `cinder` MCP server launches AgentCAD's existing MCP adapter and
stores configuration, projects, and runtime state in Hermes' profile-scoped
plugin data directory.

## Why

Eve should use AgentCAD's complete 109-tool CAD surface rather than grow a
second geometry engine or a permanent CAD toolset in Hermes core. The plugin
boundary preserves AgentCAD's upstream history and keeps the integration
independently upgradable.

## Changes

- Added Agent Plugins v1 `plugin.json` and `mcp.json` manifests.
- Added a strict launcher for the existing `agentcad mcp` command.
- Documented the Cinder/Eve ownership boundary and disabled-agent contract.
- Added executable launcher and manifest contract tests.

## Verification

The upstream baseline passed 6,441 tests with 48 skips before this fork delta.
The live MCP probe exposed 109 tools and built, revised, recovered, and exported
a real OCCT-backed part. This commit's focused tests cover the new launcher and
package contract.
