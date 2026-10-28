/* The browser displays only reviewed data shipped with this static site. */
(function () {
  "use strict";
  const grid = document.getElementById("project-grid");
  if (!grid) return;

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function externalUrl(value) {
    try {
      const parsed = new URL(value);
      return parsed.protocol === "https:" ? parsed.href : null;
    } catch (_) { return null; }
  }
  function localPath(value) {
    if (typeof value !== "string") return null;
    if (!/^(assets|projects)\/[a-zA-Z0-9_./-]+$/.test(value)) return null;
    if (value.split("/").some(function (part) { return part === ".."; })) return null;
    return "./" + value;
  }
  function card(project) {
    const article = element("article", "project-card");
    const media = element("div", "project-media");
    const imagePath = localPath(project.cover);
    if (imagePath) {
      const img = document.createElement("img");
      img.src = imagePath;
      img.alt = project.cover_alt || ("Photo of " + project.title);
      img.loading = "lazy";
      media.appendChild(img);
    } else {
      const mark = element("span", "project-placeholder", "E.");
      mark.setAttribute("aria-hidden", "true");
      media.appendChild(mark);
    }
    article.appendChild(media);
    const body = element("div", "project-body");
    body.appendChild(element("div", "project-meta", [project.category || "Project", project.status].filter(Boolean).join(" / ")));
    body.appendChild(element("h3", "", project.title));
    body.appendChild(element("p", "", project.summary));
    const tags = element("div", "project-tags");
    (project.tags || []).slice(0, 6).forEach(function (tag) { tags.appendChild(element("span", "project-tag", tag)); });
    body.appendChild(tags);
    const links = element("div", "project-actions");
    const page = localPath(project.page);
    if (page) {
      const a = element("a", "", "View project ↗");
      a.href = page;
      links.appendChild(a);
    }
    const repo = externalUrl(project.repository_url);
    if (repo) {
      const a = element("a", "", "Repository ↗");
      a.href = repo;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      links.appendChild(a);
    }
    body.appendChild(links);
    article.appendChild(body);
    return article;
  }
  fetch("./data/projects.json", { cache: "no-cache" })
    .then(function (response) { if (!response.ok) throw Error("Project data unavailable"); return response.json(); })
    .then(function (projects) {
      if (!Array.isArray(projects) || !projects.length) return;
      grid.replaceChildren();
      projects.filter(function (p) { return p && p.published === true; }).forEach(function (p) { grid.appendChild(card(p)); });
      if (!grid.children.length) {
        grid.appendChild(element("p", "", "Projects are being prepared for publication."));
      }
    })
    .catch(function () { /* Keep the meaningful static fallback visible. */ });
})();
