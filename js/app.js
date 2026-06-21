import { getStatus, needsReview, STATUS_LABELS } from "./store.js";

const els = {
  profile: document.getElementById("profile"),
  position: document.getElementById("filter-position"),
  type: document.getElementById("filter-type"),
  mastery: document.getElementById("filter-mastery"),
  search: document.getElementById("search"),
  grid: document.getElementById("grid"),
  empty: document.getElementById("empty"),
  count: document.getElementById("count"),
};

let TECHNIQUES = [];

init();

async function init() {
  const [profile, data] = await Promise.all([
    fetch("data/profile.json").then((r) => r.json()),
    fetch("data/techniques.json").then((r) => r.json()),
  ]);

  renderProfile(profile);
  TECHNIQUES = data.techniques;

  fillOptions(els.position, data.positions);
  fillOptions(els.type, [...new Set(data.techniques.map((t) => t.type))]);

  [els.position, els.type, els.mastery].forEach((s) =>
    s.addEventListener("change", render)
  );
  els.search.addEventListener("input", render);

  render();
}

function renderProfile(p) {
  els.profile.innerHTML = [
    `${p.belt}`,
    `${p.height}cm`,
    `${p.weight}kg`,
    `筋力:${p.strength}`,
    p.style,
  ]
    .map((t) => `<span>${t}</span>`)
    .join("");
}

function fillOptions(select, values) {
  values.forEach((v) => {
    const o = document.createElement("option");
    o.value = v;
    o.textContent = v;
    select.appendChild(o);
  });
}

function render() {
  const pos = els.position.value;
  const type = els.type.value;
  const mastery = els.mastery.value;
  const q = els.search.value.trim().toLowerCase();

  const list = TECHNIQUES.filter((t) => {
    if (pos && t.from !== pos) return false;
    if (type && t.type !== type) return false;
    if (mastery === "review" && !needsReview(t.id)) return false;
    if (mastery && mastery !== "review" && getStatus(t.id) !== mastery) return false;
    if (q && !(`${t.name} ${t.nameEn}`.toLowerCase().includes(q))) return false;
    return true;
  });

  els.grid.innerHTML = list.map(card).join("");
  els.empty.hidden = list.length > 0;
  els.count.textContent = `${list.length} 技`;
}

function card(t) {
  const status = getStatus(t.id);
  const review = needsReview(t.id);
  const thumb = t.images?.[0]?.src ?? "";
  return `
    <a class="card" href="technique.html?id=${encodeURIComponent(t.id)}">
      <div class="thumb"><img src="${thumb}" alt="${t.name}" loading="lazy"></div>
      <div class="body">
        <div class="name">${t.name}</div>
        <div class="name-en">${t.nameEn ?? ""}</div>
        <div class="route">${t.to ? `${t.from} → ${t.to}` : t.from}</div>
        <div class="tags">
          <span class="tag">${t.type}</span>
          <span class="mastery"><span class="dot ${status}"></span>${STATUS_LABELS[status]}</span>
          ${review ? '<span class="review-flag">復習</span>' : ""}
        </div>
      </div>
    </a>`;
}
