// 学習進捗をブラウザの localStorage に保存する共通モジュール。
// データ構造: { [techniqueId]: { status, lastStudied } }
//   status: "new" | "learning" | "mastered"
//   lastStudied: ISO文字列
// ※ localStorage はこのブラウザ内だけに保存されます（端末間では同期されません）。

const STORE_KEY = "pb-jj-progress";

// 復習をうながす日数のしきい値（簡易SRS）
const REVIEW_DAYS = { learning: 3, mastered: 14 };

export const STATUS_LABELS = {
  new: "未学習",
  learning: "学習中",
  mastered: "習得",
};

export function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY)) || {};
  } catch {
    return {};
  }
}

export function getStatus(id) {
  const p = loadProgress()[id];
  return p ? p.status : "new";
}

export function getEntry(id) {
  return loadProgress()[id] || { status: "new", lastStudied: null };
}

export function setStatus(id, status) {
  const all = loadProgress();
  all[id] = { status, lastStudied: new Date().toISOString() };
  localStorage.setItem(STORE_KEY, JSON.stringify(all));
}

// 復習が必要か（学習中/習得だが、最終学習から一定日数が経過）
export function needsReview(id) {
  const e = getEntry(id);
  if (!e.lastStudied || e.status === "new") return false;
  const days = (Date.now() - new Date(e.lastStudied).getTime()) / 86400000;
  return days >= (REVIEW_DAYS[e.status] ?? 9999);
}

export function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`;
}
