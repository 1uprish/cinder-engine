"""Cinder's portable Hermes plugin launches the existing AgentCAD MCP server."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cinder_plugin_declares_one_lazy_mcp_surface() -> None:
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    mcp = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))

    assert manifest["name"] == "cinder-engine"
    assert set(mcp["mcpServers"]) == {"cinder"}
    server = mcp["mcpServers"]["cinder"]
    assert server["command"] == "./run-cinder-mcp"
    assert server["env"] == {
        "AGENTCAD_CONFIG": "${PLUGIN_DATA}/config.json",
        "AGENTCAD_STATE_DIR": "${PLUGIN_DATA}/state",
        "AGENTCAD_PROJECTS_DIR": "${PLUGIN_DATA}/projects",
    }


def test_cinder_launcher_uses_plugin_scoped_state_and_existing_mcp(tmp_path: Path) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    capture = tmp_path / "capture.json"
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        "#!/bin/sh\n"
        "python3 -c 'import json, os, sys; "
        "json.dump({\"argv\": sys.argv[1:], "
        "\"config\": os.environ[\"AGENTCAD_CONFIG\"], "
        "\"state\": os.environ[\"AGENTCAD_STATE_DIR\"], "
        "\"projects\": os.environ[\"AGENTCAD_PROJECTS_DIR\"]}, "
        "open(os.environ[\"CAPTURE\"], \"w\"))' \"$@\"\n",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    plugin_data = tmp_path / "data"
    env = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PLUGIN_ROOT": str(ROOT),
        "PLUGIN_DATA": str(plugin_data),
        "CAPTURE": str(capture),
    }

    subprocess.run([str(ROOT / "run-cinder-mcp")], env=env, check=True)

    launched = json.loads(capture.read_text(encoding="utf-8"))
    assert launched == {
        "argv": ["run", "--directory", str(ROOT), "agentcad", "mcp"],
        "config": str(plugin_data / "config.json"),
        "state": str(plugin_data / "state"),
        "projects": str(plugin_data / "projects"),
    }
