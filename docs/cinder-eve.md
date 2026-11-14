# Cinder for Eve

Cinder is the Eve product surface built on this AgentCAD fork. AgentCAD remains
the CAD engine and workbench: build123d authors the parametric model, OCCT
builds and validates it, the existing browser renders it, and the existing MCP
server exposes the CAD operations.

Eve remains the only conversational agent. Do not configure
`ANTHROPIC_API_KEY` for the Cinder runtime; AgentCAD's optional built-in
generation loop is not part of the product path.

In local development, `?embed=cinder` keeps the AgentCAD editing surfaces and
adds Eve's chat-only renderer at the far right. The rail uses Eve's canonical
hidden Cinder session; AgentCAD does not send prompts or run a second agent.

## Hermes plugin contract

The repository root is an Agent Plugins v1 package. Hermes installs it as a
standalone plugin and starts `run-cinder-mcp` on demand. The launcher runs the
checked-out, lockfile-pinned AgentCAD application and keeps all mutable data in
Hermes' profile-scoped `PLUGIN_DATA` directory.

The MCP server is named `cinder`, so Hermes exposes its operations through the
existing lazy MCP/tool-search path. No CAD operation is duplicated in Eve and
none is added to Hermes' core tool schema.

For local development:

```bash
hermes plugins install /absolute/path/to/cinder-engine --no-enable
hermes plugins enable cinder-engine
```

Plugin changes take effect in a new Eve conversation unless explicitly
activated through Hermes' cache-aware reload flow.
