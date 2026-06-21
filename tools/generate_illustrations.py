#!/usr/bin/env python3
"""柔術の技ステップを表す概念図SVGを一括生成するツール。

- 自分=青 / 相手=グレー の2人を、ポジション（scene）ごとに配置
- グリップ点（白い丸）・力や動きの方向（矢印）を重ねる
- アナトミー的な正確さより「位置関係・グリップ・動く方向」を伝える模式図

技を追加したら下の SPEC に1行足して再実行すれば画像が増えます:
    python3 tools/generate_illustrations.py
"""
import math
import os

ME = "#2d6cdf"     # 自分（青の道着）
OPP = "#8a94a3"    # 相手（グレー）
ARROW = "#e0552b"  # 動き・力の方向
W, H = 400, 300

ROOT = os.path.join(os.path.dirname(__file__), "..")


# ---------- 基本パーツ ----------
def figure(hx, hy, ang, color, label, length=82, width=24):
    """頭（丸）+ 胴（太い丸キャップの線）で1人を描く。bodyは頭から角度angへ伸びる。"""
    rad = math.radians(ang)
    tx, ty = hx + math.cos(rad) * length, hy + math.sin(rad) * length
    r = round(width * 0.62)
    parts = [
        f'<line x1="{hx:.0f}" y1="{hy:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity="0.82"/>',
        f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{r}" fill="{color}"/>',
    ]
    if label:
        parts.append(
            f'<text x="{hx:.0f}" y="{hy - r - 5:.0f}" font-family="sans-serif" '
            f'font-size="11" font-weight="bold" fill="{color}" text-anchor="middle">{label}</text>'
        )
    return "".join(parts)


def grip(x, y):
    """グリップ点（道着をつかむ位置）。"""
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#fff" stroke="#1f2933" stroke-width="2"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2" fill="#1f2933"/>')


def arrow(x1, y1, x2, y2, text=None):
    s = (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
         f'stroke="{ARROW}" stroke-width="4" marker-end="url(#ah)"/>')
    if text:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s += (f'<text x="{mx:.0f}" y="{my - 8:.0f}" font-family="sans-serif" font-size="11" '
              f'font-weight="bold" fill="{ARROW}" text-anchor="middle">{text}</text>')
    return s


def legs(x1, y1, x2, y2, color):
    """脚・フック等を表す細い線。"""
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
            f'stroke="{color}" stroke-width="7" stroke-linecap="round" opacity="0.75"/>')


# ---------- シーン（ポジション）----------
def s_closed_guard(a=None):
    """クローズドガード: 自分が下で仰向け、相手が脚の間に。"""
    out = figure(120, 205, 0, ME, "自分", 92)
    out += figure(305, 150, 168, OPP, "相手", 92)
    out += legs(210, 200, 250, 150, ME) + legs(210, 215, 252, 178, ME)  # 相手腰を抱える脚
    out += grip(250, 150) + grip(262, 175)  # 襟・袖
    if a:
        out += a
    return out


def s_mount(a=None):
    out = figure(110, 195, 0, OPP, "相手", 105)
    out += figure(168, 120, 90, ME, "自分", 72)
    if a:
        out += a
    return out


def s_side(a=None):
    out = figure(110, 195, 0, OPP, "相手", 105)
    out += figure(150, 120, 28, ME, "自分", 95)
    if a:
        out += a
    return out


def s_back(a=None):
    out = figure(205, 150, 90, OPP, "相手", 85)
    out += figure(170, 138, 90, ME, "自分", 85)
    out += legs(178, 215, 232, 200, ME) + legs(178, 200, 232, 185, ME)  # フック
    out += grip(212, 150)
    if a:
        out += a
    return out


def s_butterfly(a=None):
    out = figure(150, 205, -68, ME, "自分", 82)
    out += figure(262, 120, 116, OPP, "相手", 82)
    out += legs(165, 175, 215, 175, ME)  # バタフライフック
    out += grip(232, 150)  # アンダーフック側
    if a:
        out += a
    return out


def s_half(a=None):
    out = figure(120, 200, -8, ME, "自分", 95)
    out += figure(300, 152, 172, OPP, "相手", 92)
    out += legs(205, 200, 250, 205, ME) + legs(218, 212, 250, 220, ME)  # 相手の片足を挟む
    out += grip(248, 168)
    if a:
        out += a
    return out


def s_spider(a=None):
    out = figure(115, 210, 0, ME, "自分", 90)
    out += figure(300, 120, 122, OPP, "相手", 92)
    out += legs(205, 205, 258, 150, ME) + legs(205, 218, 262, 175, ME)  # 足を相手のヒジ・腕へ
    out += grip(258, 150) + grip(262, 178)  # 両袖
    if a:
        out += a
    return out


def s_dlr(a=None):
    out = figure(115, 212, 0, ME, "自分", 90)
    out += figure(300, 95, 90, OPP, "相手", 100)
    out += legs(205, 210, 295, 150, ME)  # 相手の前足に絡むデラヒーバフック
    out += grip(292, 130)
    if a:
        out += a
    return out


def s_pass(a=None):
    """パス: 相手が下、自分が立ち or 圧をかける側。"""
    out = figure(110, 205, 0, OPP, "相手", 110)
    out += figure(300, 95, 100, ME, "自分", 100)
    if a:
        out += a
    return out


def s_triangle(a=None):
    out = figure(120, 210, 0, ME, "自分", 90)
    out += figure(300, 165, 172, OPP, "相手", 88)
    # 三角に組んだ脚
    out += legs(205, 205, 250, 150, ME) + legs(250, 150, 220, 185, ME)
    out += grip(240, 170)  # 相手の腕を内側に
    if a:
        out += a
    return out


def s_armbar(a=None):
    out = figure(300, 175, 180, OPP, "相手", 95)
    out += figure(180, 95, 90, ME, "自分", 80)
    out += legs(165, 120, 255, 150, ME) + legs(195, 120, 255, 170, ME)  # 相手の頭・胴をはさむ脚
    out += legs(250, 165, 185, 150, "#c23")  # 極める相手の腕
    out += grip(200, 150)
    if a:
        out += a
    return out


SCENES = {
    "closed_guard": s_closed_guard, "mount": s_mount, "side": s_side, "back": s_back,
    "butterfly": s_butterfly, "half": s_half, "spider": s_spider, "dlr": s_dlr,
    "pass": s_pass, "triangle": s_triangle, "armbar": s_armbar,
}


# ---------- ラッパー（枠・凡例・番号・ラベル）----------
def render(scene, num, label, extra=None):
    body = SCENES[scene](extra)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0L10 5L0 10z" fill="{ARROW}"/>
    </marker>
  </defs>
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="#f4f6f8" stroke="#c3ccd6" stroke-width="2"/>
  <circle cx="38" cy="38" r="20" fill="{ME}"/>
  <text x="38" y="45" font-family="sans-serif" font-size="20" font-weight="bold" fill="#fff" text-anchor="middle">{num}</text>
  <g>
    <circle cx="300" cy="30" r="6" fill="{ME}"/><text x="312" y="34" font-family="sans-serif" font-size="11" fill="#6b7888">自分</text>
    <circle cx="345" cy="30" r="6" fill="{OPP}"/><text x="357" y="34" font-family="sans-serif" font-size="11" fill="#6b7888">相手</text>
  </g>
  {body}
  <text x="200" y="288" font-family="sans-serif" font-size="13" fill="#46505c" text-anchor="middle">{label}</text>
</svg>
'''


# ---------- 各技のステップ → シーン ----------
# (技ID, [(scene, 画像下の短いラベル, 任意の追加SVG=矢印など), ...])
A = arrow  # 短縮
SPEC = [
    # 既存3技（新スタイルで再生成）
    ("scissor-sweep", [
        ("closed_guard", "襟と袖を取り横向きに", None),
        ("closed_guard", "ハサミの形を作る", A(235, 150, 150, 130, "崩す")),
        ("mount", "刈ってマウントへ", A(120, 250, 250, 250, "返す")),
    ]),
    ("cross-collar-choke", [
        ("closed_guard", "片手で深く襟を握る", None),
        ("closed_guard", "反対の手を交差", None),
        ("closed_guard", "肘を締めて絞める", A(260, 170, 230, 150, "引き込む")),
    ]),
    ("knee-slice-pass", [
        ("pass", "膝をスライスイン", None),
        ("pass", "襟と脇をコントロール", A(300, 130, 240, 170, "潰す")),
        ("side", "サイドへ回り込む", None),
    ]),
    # 追加の技
    ("triangle-choke", [
        ("closed_guard", "片腕を内・片腕を外に", None),
        ("triangle", "脚を三角に組む", A(250, 130, 230, 165, "首を挟む")),
        ("triangle", "角度を変えて絞める", A(120, 240, 170, 200, "ヒップを切る")),
    ]),
    ("armbar-closed", [
        ("closed_guard", "片腕を抱え込む", None),
        ("armbar", "頭側へ回り脚をかける", A(255, 165, 195, 150, None)),
        ("armbar", "ヒップを上げて極める", A(200, 200, 200, 120, "腕を伸ばす")),
    ]),
    ("pendulum-sweep", [
        ("closed_guard", "袖と襟を取り片足を抱える", None),
        ("closed_guard", "振り子で勢いをつける", A(150, 240, 150, 150, "脚を振る")),
        ("mount", "横転させてマウント", A(120, 250, 250, 250, "返す")),
    ]),
    ("hip-bump-sweep", [
        ("closed_guard", "起き上がり相手の肩に手を", None),
        ("closed_guard", "ヒップをぶつける", A(160, 200, 250, 160, "腰で押す")),
        ("mount", "覆い被さってマウント", None),
    ]),
    ("butterfly-sweep", [
        ("butterfly", "アンダーフックとバタフライフック", None),
        ("butterfly", "横に崩しフックで持ち上げる", A(232, 175, 280, 130, "すくい上げる")),
        ("mount", "上を取る", None),
    ]),
    ("old-school-sweep", [
        ("half", "アンダーフックを取る", None),
        ("half", "相手の足を確保", A(250, 205, 200, 205, "足をすくう")),
        ("side", "起き上がってトップへ", A(150, 240, 250, 240, "返す")),
    ]),
    ("mount-armbar", [
        ("mount", "マウントで相手の腕を狙う", None),
        ("armbar", "片足を相手の頭側へ回す", A(200, 110, 200, 90, "回転")),
        ("armbar", "後ろに倒れて極める", A(200, 130, 200, 200, "腕を伸ばす")),
    ]),
    ("americana", [
        ("side", "サイドで相手の手首を抑える", None),
        ("side", "図形（鍵の形）に肘を曲げる", A(230, 150, 210, 175, None)),
        ("side", "肩を極める", A(215, 175, 245, 175, "肘を上げる")),
    ]),
    ("bow-and-arrow", [
        ("back", "バックを取り襟を深く握る", None),
        ("back", "相手の足を引っかける", A(230, 200, 270, 230, "弓を引く")),
        ("back", "弓を引くように絞める", A(212, 150, 175, 150, "締める")),
    ]),
    # ガード解説
    ("guard-closed", [
        ("closed_guard", "脚を相手の腰でロック", None),
        ("closed_guard", "襟・袖をコントロール", None),
    ]),
    ("guard-half", [
        ("half", "相手の片足を脚で挟む", None),
        ("half", "アンダーフック/ニーシールドで防ぐ", None),
    ]),
    ("guard-butterfly", [
        ("butterfly", "座って両フックを内腿へ", None),
        ("butterfly", "アンダーフックで崩しの起点に", None),
    ]),
    ("guard-spider", [
        ("spider", "両袖を握り足裏を相手のヒジへ", None),
        ("spider", "押し引きで相手を操作", None),
    ]),
    ("guard-dlr", [
        ("dlr", "相手の前足にDLRフック", None),
        ("dlr", "袖/かかとを取り崩す", None),
    ]),
]


def main():
    n = 0
    for tid, steps in SPEC:
        d = os.path.join(ROOT, "images", tid)
        os.makedirs(d, exist_ok=True)
        for i, (scene, label, extra) in enumerate(steps, 1):
            svg = render(scene, i, label, extra)
            with open(os.path.join(d, f"{i:02d}.svg"), "w", encoding="utf-8") as f:
                f.write(svg)
            n += 1
    print(f"generated {n} svg files for {len(SPEC)} entries")


if __name__ == "__main__":
    main()
