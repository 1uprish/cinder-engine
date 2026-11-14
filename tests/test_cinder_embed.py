"""The Eve embed keeps AgentCAD's workbench and delegates conversation to Eve."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


MODULE = Path(__file__).resolve().parents[1] / "frontend" / "js" / "cinder_embed.js"
pytestmark = pytest.mark.skipif(shutil.which("node") is None,
                                reason="node is not installed")


def run_js(body: str) -> object:
    prelude = (
        f'import * as cinder from {json.dumps(MODULE.resolve().as_uri())};\n'
        "const out = (value) => process.stdout.write(JSON.stringify(value));\n"
    )
    proc = subprocess.run(
        ["node", "--input-type=module", "--eval", prelude + body],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_embed_query_is_explicit_and_carries_workbench_focus() -> None:
    got = run_js("""
      out({
        cinder: cinder.readCinderContext("?embed=cinder&project=gearbox&part=shaft"),
        ordinary: cinder.readCinderContext("?project=gearbox"),
        args: cinder.readWorkbenchArgs({project: " gearbox ", part_id: " shaft "}),
      });
    """)
    assert got == {
        "cinder": {"embedded": True, "project": "gearbox", "part": "shaft"},
        "ordinary": {"embedded": False, "project": "gearbox", "part": None},
        "args": {"project": "gearbox", "part": "shaft"},
    }


def test_focus_loads_project_before_part_and_closes_dashboard() -> None:
    got = run_js("""
      let current = "old";
      const calls = [];
      const result = await cinder.focusCinderWorkbench(
        {project: "gearbox", part: "shaft"},
        {
          currentProject: () => current,
          loadProject: async (name) => { calls.push(["project", name]); current = name; },
          selectPart: async (name) => calls.push(["part", name]),
          closeDashboard: () => calls.push(["close"]),
        },
      );
      out({result, calls});
    """)
    assert got == {
        "result": {"ok": True, "project": "gearbox", "part": "shaft"},
        "calls": [["project", "gearbox"], ["close"], ["part", "shaft"]],
    }


def test_focus_refuses_to_select_when_project_did_not_open() -> None:
    got = run_js("""
      const calls = [];
      const result = await cinder.focusCinderWorkbench(
        {project: "missing", part: "shaft"},
        {
          currentProject: () => "old",
          loadProject: async (name) => calls.push(["project", name]),
          selectPart: async (name) => calls.push(["part", name]),
          closeDashboard: () => calls.push(["close"]),
        },
      );
      out({result, calls});
    """)
    assert got == {
        "result": {"ok": False, "reason": "project_not_open"},
        "calls": [["project", "missing"]],
    }
