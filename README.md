# 🥋 pb-jiujitsu-techniques

柔術（**Giのみ・青帯レベル**）の技を、**イラスト + 手順 + 相手の体型別の注意点**で覚えるための静的Webサイト。
GitHub Pages でそのまま公開できます。サーバー不要（HTML / CSS / JavaScript のみ）。

## 特長

- ポジション（クローズドガード等）・種別・技名で絞り込み／検索
- 技だけでなく **ガードの解説**（クローズド／ハーフ／バタフライ／スパイダー／デラヒーバ）も掲載
- 各技に **手順イラスト（SVG・自動生成の模式図）**・手順テキスト・コツ・よくあるミスを掲載
- **相手の体型別の注意点**（重くて力が強い / 大きい / 小柄ですばやい / 体が硬い）
  …自分の体格（175cm / 65kg / 普通の筋力）を基準にした相対的な目線で記載
- **習得状況の記録 + 簡易SRS**：「未学習 / 学習中 / 習得」をブラウザに保存し、一定期間たつと「復習」フラグを表示

## ディレクトリ構成

| パス | 説明 |
|------|------|
| `index.html` | トップ（技一覧・フィルタ・検索） |
| `technique.html` | 技の詳細ページ（`?id=技ID`） |
| `css/style.css` | スタイル |
| `js/store.js` | 学習進捗の保存（localStorage・簡易SRS） |
| `js/app.js` | 一覧ページのロジック |
| `js/technique.js` | 詳細ページのロジック |
| `data/profile.json` | 自分の体格プロフィール |
| `data/techniques.json` | 技データ本体（ここに追記して技を増やす） |
| `images/<技ID>/` | その技の手順イラスト（SVG/PNG） |
| `tools/generate_illustrations.py` | 概念図イラスト（SVG）を一括生成するツール |

## ローカルで確認する

ES Modules と `fetch` を使うため、`file://` で直接開くと動きません。簡易サーバーを立ててください。

```bash
# Python があれば
python3 -m http.server 8000
# → ブラウザで http://localhost:8000 を開く
```

## GitHub Pages で公開する

1. このリポジトリに push する
2. GitHub の **Settings → Pages** を開く
3. **Build and deployment → Source** を「Deploy from a branch」にする
4. Branch を `main` / フォルダを `/ (root)` にして **Save**
5. 数分後、`https://<ユーザー名>.github.io/pb-jiujitsu-techniques/` で公開される

> `.nojekyll` を置いているため、Jekyll の処理をスキップして素の静的ファイルとして配信されます。

## 技を追加する手順

1. `data/techniques.json` の `techniques` 配列に1件追記する（下のテンプレート参照）
2. `images/<技ID>/` にイラスト（`01.svg`, `02.svg` …）を置く
   - 既存のSVGは「自分=青 / 相手=グレー」の**模式図**です。位置関係・グリップ・動く方向を表します
   - より分かりやすくしたい場合は **自分の手描きイラストに差し替え**てください（SVG推奨。PNG/JPGも可）
3. push すれば反映される

### イラストを自動生成する

模式図は `tools/generate_illustrations.py` でまとめて作れます。技を増やすときは、スクリプト末尾の `SPEC` に
`(技ID, [(シーン名, バリエーション名, 短いラベル), ...])` を1行足して再実行してください。

```bash
python3 tools/generate_illustrations.py
```

現在のシーン名: `closed_guard` / `scissor` / `mount` / `half_guard` / `butterfly` / `spider` /
`dlr` / `triangle` / `armbar` / `pendulum` / `hip_bump` / `old_school` / `americana` /
`bow_arrow` / `knee_slice`

### 技データのテンプレート

```json
{
  "id": "技ID（半角英数・ハイフン。画像フォルダ名と一致させる）",
  "name": "技名",
  "nameEn": "English Name",
  "from": "開始ポジション（positions のいずれか）",
  "to": "終了ポジション or サブミッション",
  "type": "スイープ / 絞め技 / 関節技 / パスガード / エスケープ など",
  "belt": "青",
  "images": [
    { "src": "images/技ID/01.svg", "caption": "① …" },
    { "src": "images/技ID/02.svg", "caption": "② …" }
  ],
  "steps": ["手順1", "手順2"],
  "tips": "一番大事なコツ",
  "commonMistakes": ["よくあるミス1"],
  "opponentNotes": {
    "heavy_strong": "重くて力が強い相手への注意点",
    "tall_big": "自分より大きい・背が高い相手への注意点",
    "small_fast": "小柄・すばやい相手への注意点",
    "stiff": "体が硬い相手への注意点"
  }
}
```

相手タイプ（`opponentNotes` のキー）と `positions` の一覧は `data/techniques.json` の先頭で定義しています。増やしたい場合はそこを編集してください。

## メモ

- 学習進捗は **このブラウザの localStorage** に保存されます。別の端末・ブラウザとは同期されません。
- 技データ自体は全員共通（JSON）なので、複数端末で同じ技集を見られます。同期が必要になったら、進捗のエクスポート/インポートや外部サービス連携を後から追加できます。
