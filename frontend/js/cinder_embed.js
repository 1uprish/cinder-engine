// Eve's Cinder host embeds this workbench; the CAD application remains usable
// on its own. Keep the host contract in query parameters and ui_open args so
// neither side needs a second geometry or viewport protocol.

function value(input) {
  return typeof input === "string" && input.trim() ? input.trim() : null;
}

export function readCinderContext(search) {
  const params = new URLSearchParams(search || "");
  return {
    embedded: params.get("embed") === "cinder",
    project: value(params.get("project")),
    part: value(params.get("part")),
  };
}

export function readWorkbenchArgs(args) {
  const input = args && typeof args === "object" ? args : {};
  return {
    project: value(input.project),
    part: value(input.part || input.part_id),
  };
}

export function applyCinderEmbed(doc, context) {
  const embedded = !!context.embedded;
  doc.body.classList.toggle("cinder-embed", embedded);

  const rail = doc.getElementById("eve-chat-rail");
  if (!rail) return;

  rail.hidden = !embedded;
  const frame = rail.querySelector("iframe");
  const source = frame?.dataset.src;
  if (embedded && frame && source && !frame.getAttribute("src")) {
    frame.setAttribute("src", source);
  }
}

export async function focusCinderWorkbench(context, deps) {
  const project = context.project || deps.currentProject();
  if (!project) return { ok: false, reason: "no_project" };

  if (deps.currentProject() !== project) await deps.loadProject(project);
  if (deps.currentProject() !== project) {
    return { ok: false, reason: "project_not_open" };
  }
  deps.closeDashboard();
  if (context.part) await deps.selectPart(context.part);
  return { ok: true, project, part: context.part };
}
