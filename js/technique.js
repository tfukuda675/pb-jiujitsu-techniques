import { getEntry, setStatus, formatDate, STATUS_LABELS } from "./store.js";

const id = new URLSearchParams(location.search).get("id");
const contentEl = document.getElementById("content");
const profileEl = document.getElementById("profile");

let profile = null;

init();

async function init() {
  const [p, data] = await Promise.all([
    fetch("data/profile.json").then((r) => r.json()),
    fetch("data/techniques.json").then((r) => r.json()),
  ]);
  profile = p;
  renderProfile(p);

  const t = data.techniques.find((x) => x.id === id);
  if (!t) {
    contentEl.innerHTML = `<p class="empty">技が見つかりませんでした。</p>`;
    return;
  }
  document.title = `${t.name} | 柔術 技ノート`;
  contentEl.innerHTML = detail(t, data.opponentTypes);
  wireMastery(t.id);
}

function renderProfile(p) {
  profileEl.innerHTML = [`${p.belt}`, `${p.height}cm`, `${p.weight}kg`, `筋力:${p.strength}`]
    .map((x) => `<span>${x}</span>`)
    .join("");
}

function detail(t, opponentTypes) {
  return `
    <div class="detail-head">
      <h2>${t.name}</h2>
      <div class="en">${t.nameEn ?? ""}</div>
      <div class="route-badges">
        <span class="pos">${t.from}</span>
        ${t.to ? `<span class="arrow">→</span><span class="pos">${t.to}</span>` : ""}
        <span class="tag">${t.type}</span>
        <span class="tag">${t.belt}帯</span>
      </div>
    </div>

    <section class="block">
      <h3>${t.type === "ガード" ? "ポジション図" : "手順イラスト"}</h3>
      <div class="gallery">
        ${t.images
          .map(
            (im) => `
          <figure>
            <img src="${im.src}" alt="${im.caption}">
            <figcaption>${im.caption}</figcaption>
          </figure>`
          )
          .join("")}
      </div>
    </section>

    <section class="block">
      <h3>${t.type === "ガード" ? "セットアップ／キープのポイント" : "手順"}</h3>
      <ol class="steps">${t.steps.map((s) => `<li>${s}</li>`).join("")}</ol>
    </section>

    <section class="block">
      <h3>コツ</h3>
      <p class="tips"><strong>POINT:</strong> ${t.tips}</p>
      ${
        t.commonMistakes?.length
          ? `<p style="margin:14px 0 6px;font-weight:700;">よくあるミス</p>
             <ul class="mistakes">${t.commonMistakes.map((m) => `<li>${m}</li>`).join("")}</ul>`
          : ""
      }
    </section>

    <section class="block">
      <h3>相手の体型別の注意点</h3>
      <p class="opp-hint">自分（${profile.height}cm / ${profile.weight}kg / 筋力${profile.strength}）を基準にした目線です。</p>
      ${opponentTypes
        .filter((o) => t.opponentNotes?.[o.key])
        .map(
          (o) => `
        <div class="opp-note">
          <div class="label"><span class="icon">${o.icon}</span>${o.label}</div>
          <div>${t.opponentNotes[o.key]}</div>
        </div>`
        )
        .join("")}
    </section>

    <section class="block">
      <h3>習得状況</h3>
      <div class="mastery-controls" id="mastery">
        <button class="new" data-status="new">未学習</button>
        <button class="learning" data-status="learning">学習中</button>
        <button class="mastered" data-status="mastered">習得</button>
        <span class="last-studied" id="last-studied"></span>
      </div>
    </section>`;
}

function wireMastery(techId) {
  const wrap = document.getElementById("mastery");
  const lastEl = document.getElementById("last-studied");

  function refresh() {
    const e = getEntry(techId);
    wrap.querySelectorAll("button").forEach((b) => {
      b.classList.toggle("active", b.dataset.status === e.status);
    });
    lastEl.textContent =
      e.status === "new"
        ? "まだ記録なし"
        : `最終学習: ${formatDate(e.lastStudied)}（${STATUS_LABELS[e.status]}）`;
  }

  wrap.querySelectorAll("button").forEach((b) =>
    b.addEventListener("click", () => {
      setStatus(techId, b.dataset.status);
      refresh();
    })
  );
  refresh();
}
