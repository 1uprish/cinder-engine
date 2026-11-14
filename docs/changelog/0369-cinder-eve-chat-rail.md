# 0369 — Add Eve chat to the Cinder workbench

- **Commit:** pending
- **Date:** 2026-11-15
- **Author:** OpenAI Codex / Arvind

## Summary

The Cinder embed now shows Eve's canonical Cinder conversation as a dedicated
right rail beside AgentCAD's existing inspector. AgentCAD continues to own the
CAD workbench while Eve remains the only conversational runtime.

## Changes

- Added a lazily loaded Eve chat iframe to the far-right edge of the workspace.
- Mounted that rail only for the explicit `?embed=cinder` product surface.
- Kept the existing Parameters, Code, Metrics, and Threads inspector unchanged.
- Added a regression test for embed-only chat mounting and documented the
  single-runtime ownership boundary.

## Files

- `frontend/index.html` — declares the Eve chat host.
- `frontend/css/app.css` — sizes and separates the right rail.
- `frontend/js/cinder_embed.js` — mounts the chat only in Cinder embed mode.
- `tests/test_cinder_embed.py` — proves the mount and ordinary-mode behavior.
- `docs/cinder-eve.md` — records the chat/runtime contract.

## Notes

The iframe URL is the existing Eve renderer development server at
`127.0.0.1:5174`; packaged endpoint discovery is intentionally not introduced
by this local integration slice.

`make test-fast`: **6447 passed, 48 skipped**. The first run reached 6435
passed and showed only the twelve acceptance checks that require this newest
entry to cite the completed suite count; the recorded rerun is green.
