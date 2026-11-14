# 0368 — 2026-11-14 — Add the Eve-owned Cinder workbench mode

- **Commit:** (this commit)
- **Date:** 2026-11-14
- **Author:** OpenAI Codex / Arvind

## Summary

AgentCAD now has an explicit `?embed=cinder` workbench mode for Eve. It keeps
the complete CAD workspace and hides AgentCAD's optional chat and generation
entry points, because Eve owns the conversation. Project and part focus work
through both URL parameters and the existing `ui_open` event protocol.

## Changes

- Added a small, pure Cinder embed/focus contract.
- Added `workbench` to the existing `ui_open` registry.
- Added deep links for `project` and `part` without introducing a second
  viewport protocol.
- Suppressed the built-in Generate action and chat dock only in embed mode.
- Added Node-backed behavior tests for query parsing and focus ordering.

## Verification

The tests prove project-before-part focus, safe refusal when a project cannot
open, and that ordinary standalone AgentCAD URLs remain outside embed mode.
Browser verification is performed against the live service from Eve after the
host integration lands.

`make test-fast`: **6,446 passed, 48 skipped**. The first full run reached
6,434 passed and exposed only the twelve repository acceptance checks requiring
this newest changelog entry to cite the run; the recorded rerun is green.
