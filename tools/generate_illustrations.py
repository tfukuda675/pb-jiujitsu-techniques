#!/usr/bin/env python3
"""柔術の技ステップを表すSVG教材を一括生成するツール。

自分=青、相手=グレーで統一し、頭・胴・腕・脚・グリップ・力の方向を
明示する。解剖学的な写実性より、学習時に必要な「体の向き」「脚や腕の
かかり方」「崩す方向」を読み取れることを優先する。

技を追加したら SPEC に1行足して再実行:
    /opt/conda/bin/conda run --no-capture-output -n py313 python tools/generate_illustrations.py
"""

from __future__ import annotations

import html
import os

ME = "#2d6cdf"
ME_DARK = "#174a9c"
OPP = "#8a94a3"
OPP_DARK = "#586474"
MAT = "#f6f8fb"
LINE = "#c8d2dd"
INK = "#334155"
MUTED = "#64748b"
ARROW = "#e0552b"
WARN = "#c2410c"
W, H = 480, 360

ROOT = os.path.join(os.path.dirname(__file__), "..")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def points_attr(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def poly(points: list[tuple[float, float]], color: str, width: int, opacity: float = 0.9) -> str:
    return (
        f'<polyline points="{points_attr(points)}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'
    )


def dot(x: float, y: float, r: float, fill: str, stroke: str = "none", width: int = 0) -> str:
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def label(x: float, y: float, text: str, color: str = INK, size: int = 12, weight: int = 700) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="middle">{esc(text)}</text>'
    )


def limb(points: list[tuple[float, float]], color: str, width: int = 10, joints: bool = True) -> str:
    out = poly(points, color, width)
    if joints:
        for x, y in points[1:-1]:
            out += dot(x, y, width * 0.42, color)
        out += dot(points[-1][0], points[-1][1], width * 0.36, "#fff", color, 3)
    return out


def figure(
    head: tuple[float, float],
    hip: tuple[float, float],
    color: str,
    name: str,
    arms: list[list[tuple[float, float]]] | None = None,
    legs: list[list[tuple[float, float]]] | None = None,
    dark: str | None = None,
) -> str:
    dark = dark or color
    hx, hy = head
    px, py = hip
    out = ""
    for leg in legs or []:
        out += limb(leg, color, 12)
    out += poly([head, hip], color, 30, 0.86)
    out += dot(px, py, 13, color)
    for arm in arms or []:
        out += limb(arm, dark, 9)
    out += dot(hx, hy, 18, color)
    out += dot(hx, hy, 8, "#ffffff")
    out += label(hx, hy - 25, name, color, 12)
    return out


def grip(x: float, y: float, text: str | None = None) -> str:
    out = dot(x, y, 8, "#fff", "#111827", 2) + dot(x, y, 3, "#111827")
    if text:
        out += label(x, y - 13, text, "#111827", 11, 700)
    return out


def arrow(x1: float, y1: float, x2: float, y2: float, text: str | None = None) -> str:
    out = (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{ARROW}" stroke-width="5" stroke-linecap="round" marker-end="url(#ah)"/>'
    )
    if text:
        out += label((x1 + x2) / 2, (y1 + y2) / 2 - 10, text, ARROW, 12)
    return out


def zone(points: list[tuple[float, float]], color: str = "#fef3c7", opacity: float = 0.72) -> str:
    return (
        f'<polygon points="{points_attr(points)}" fill="{color}" opacity="{opacity}" '
        f'stroke="{WARN}" stroke-width="2" stroke-dasharray="5 4"/>'
    )


def mat_note(x: float, y: float, text: str) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="sans-serif" font-size="11" '
        f'font-weight="700" fill="{MUTED}" text-anchor="middle">{esc(text)}</text>'
    )


def closed_guard(kind: str = "control") -> str:
    me_arms = [[(112, 204), (166, 170), (244, 146)], [(112, 226), (168, 226), (262, 184)]]
    me_legs = [[(184, 196), (232, 128), (270, 139)], [(184, 219), (236, 203), (272, 188)]]
    opp_arms = [[(309, 137), (274, 145), (244, 146)], [(307, 158), (284, 177), (262, 184)]]
    opp_legs = [[(239, 154), (208, 128), (190, 102)], [(239, 177), (209, 205), (188, 238)]]
    out = figure((330, 145), (239, 166), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((88, 216), (184, 207), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(244, 146, "襟") + grip(262, 184, "袖")
    out += zone([(232, 128), (270, 139), (272, 188), (236, 203)], "#dbeafe", 0.58)
    out += mat_note(250, 118, "脚で腰を閉じる")
    if kind in {"pull", "cross3"}:
        out += arrow(292, 156, 226, 176, "引きつける")
    if kind in {"angle", "scissor_setup"}:
        out += arrow(166, 235, 128, 276, "横向き")
    if kind == "cross1":
        out += zone([(228, 128), (260, 132), (252, 158), (224, 154)], "#fee2e2", 0.7)
        out += mat_note(242, 106, "片手を首裏まで深く")
    if kind == "cross2":
        out += poly([(246, 146), (224, 165), (262, 184)], WARN, 6)
        out += mat_note(245, 114, "前腕を交差")
    return out


def scissor(kind: str) -> str:
    me_arms = [[(106, 192), (158, 158), (237, 143)], [(104, 218), (158, 218), (263, 184)]]
    me_legs = [[(168, 198), (220, 144), (285, 142)], [(168, 222), (225, 224), (286, 211)]]
    opp_arms = [[(307, 136), (274, 144), (237, 143)], [(307, 159), (284, 176), (263, 184)]]
    opp_legs = [[(240, 154), (212, 128), (192, 104)], [(240, 176), (212, 204), (193, 236)]]
    out = figure((330, 145), (240, 165), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((82, 208), (168, 210), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(237, 143, "襟") + grip(263, 184, "袖")
    out += zone([(215, 136), (288, 132), (292, 218), (222, 230)], "#dbeafe", 0.45)
    out += mat_note(252, 124, "上脚=押す / 下脚=刈る")
    if kind == "shape":
        out += arrow(242, 146, 170, 166, "崩す")
    if kind == "finish":
        out += arrow(280, 142, 340, 106, "押す") + arrow(278, 212, 337, 235, "刈る")
    return out


def mount(kind: str = "top") -> str:
    opp_arms = [[(142, 177), (176, 142), (214, 134)], [(142, 222), (176, 246), (218, 250)]]
    opp_legs = [[(246, 181), (288, 156), (326, 146)], [(246, 219), (292, 236), (330, 250)]]
    me_arms = [[(212, 122), (192, 151), (180, 176)], [(240, 122), (265, 150), (282, 178)]]
    me_legs = [[(214, 184), (190, 214), (166, 238)], [(242, 184), (270, 214), (296, 238)]]
    out = figure((94, 200), (246, 200), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((226, 88), (228, 176), ME, "自分", me_arms, me_legs, ME_DARK)
    out += zone([(174, 160), (282, 160), (300, 236), (160, 236)], "#dbeafe", 0.36)
    out += mat_note(228, 258, "腰で胸をまたぐ")
    if kind == "sweep_finish":
        out += arrow(138, 250, 270, 250, "上を取る")
    if kind == "arm_isolate":
        out += zone([(168, 136), (226, 126), (230, 148), (176, 160)], "#fee2e2", 0.7)
        out += grip(214, 134, "腕")
    if kind == "swing_leg":
        out += arrow(246, 178, 158, 126, "足を頭側へ")
    return out


def half_guard(kind: str = "lock") -> str:
    me_arms = [[(102, 198), (150, 166), (234, 150)], [(100, 226), (147, 228), (216, 212)]]
    me_legs = [[(176, 198), (224, 202), (268, 202)], [(176, 222), (222, 228), (268, 220)]]
    opp_arms = [[(310, 142), (270, 146), (234, 150)], [(310, 166), (272, 190), (226, 212)]]
    opp_legs = [[(238, 158), (262, 204), (292, 238)], [(238, 176), (205, 214), (178, 248)]]
    out = figure((334, 154), (238, 166), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((82, 214), (176, 210), ME, "自分", me_arms, me_legs, ME_DARK)
    out += zone([(222, 196), (270, 194), (272, 226), (220, 232)], "#dbeafe", 0.55)
    out += mat_note(247, 188, "片足を挟む")
    if kind in {"underhook", "old1"}:
        out += grip(234, 150, "アンダーフック")
    if kind == "shield":
        out += limb([(176, 198), (222, 158), (266, 150)], ME, 13)
        out += mat_note(236, 137, "ニーシールド")
    if kind == "far_leg":
        out += arrow(214, 212, 286, 238, "遠い足をすくう") + grip(286, 238, "足")
    if kind == "come_up":
        out += arrow(105, 208, 170, 165, "起き上がる")
    return out


def butterfly(kind: str = "base") -> str:
    me_arms = [[(128, 196), (176, 158), (232, 148)], [(126, 222), (166, 230), (220, 214)]]
    me_legs = [[(166, 226), (204, 192), (242, 178)], [(180, 242), (220, 220), (262, 204)]]
    opp_arms = [[(290, 126), (260, 142), (232, 148)], [(304, 150), (270, 182), (230, 212)]]
    opp_legs = [[(270, 188), (238, 220), (214, 252)], [(292, 190), (268, 230), (252, 268)]]
    out = figure((306, 104), (282, 184), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((104, 212), (174, 234), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(232, 148, "脇")
    out += zone([(204, 190), (262, 174), (272, 204), (218, 224)], "#dbeafe", 0.55)
    out += mat_note(236, 164, "足甲を内腿へ")
    if kind == "lift":
        out += arrow(236, 194, 278, 130, "持ち上げる") + arrow(280, 136, 332, 114, "横へ崩す")
    return out


def spider(kind: str = "base") -> str:
    me_arms = [[(112, 203), (165, 166), (258, 134)], [(112, 227), (168, 236), (270, 190)]]
    me_legs = [[(184, 196), (226, 154), (276, 138)], [(186, 222), (230, 206), (284, 192)]]
    opp_arms = [[(318, 130), (292, 134), (258, 134)], [(313, 154), (292, 176), (270, 190)]]
    opp_legs = [[(270, 176), (248, 222), (228, 260)], [(292, 176), (318, 220), (340, 260)]]
    out = figure((330, 106), (282, 172), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((88, 216), (184, 209), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(258, 134, "袖") + grip(270, 190, "袖")
    out += mat_note(274, 120, "足裏を上腕へ")
    if kind == "push_pull":
        out += arrow(276, 138, 322, 112, "押す") + arrow(270, 190, 208, 210, "引く")
    return out


def dlr(kind: str = "hook") -> str:
    me_arms = [[(112, 205), (166, 168), (282, 118)], [(112, 228), (164, 238), (284, 226)]]
    me_legs = [[(184, 202), (250, 170), (300, 204), (276, 226)], [(184, 224), (238, 228), (294, 236)]]
    opp_arms = [[(302, 82), (286, 112), (282, 118)], [(324, 82), (344, 122), (360, 154)]]
    opp_legs = [[(302, 166), (296, 212), (284, 258)], [(326, 166), (352, 210), (370, 252)]]
    out = figure((314, 48), (314, 160), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((88, 218), (184, 212), ME, "自分", me_arms, me_legs, ME_DARK)
    out += zone([(250, 170), (302, 162), (306, 214), (276, 226)], "#dbeafe", 0.55)
    out += mat_note(270, 154, "外から脚を巻く")
    if kind == "grips":
        out += grip(282, 118, "袖") + grip(284, 226, "かかと")
        out += arrow(284, 226, 238, 232, "引く")
    return out


def triangle(kind: str = "entry") -> str:
    me_arms = [[(112, 205), (166, 170), (244, 164)], [(112, 228), (168, 232), (268, 196)]]
    me_legs = [[(184, 198), (240, 128), (306, 150)], [(184, 222), (242, 198), (306, 150), (276, 126)]]
    opp_arms = [[(310, 154), (276, 164), (244, 164)], [(308, 178), (290, 192), (268, 196)]]
    opp_legs = [[(240, 172), (210, 144), (190, 118)], [(240, 190), (214, 220), (190, 250)]]
    out = figure((332, 166), (240, 182), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((88, 216), (184, 210), ME, "自分", me_arms, me_legs, ME_DARK)
    out += zone([(240, 128), (306, 150), (276, 126)], "#fee2e2", 0.78)
    out += mat_note(276, 114, "首＋片腕を脚で囲む")
    if kind == "entry":
        out += mat_note(260, 218, "片腕は内 / 片腕は外")
    if kind == "lock":
        out += grip(306, 150, "膝裏ロック")
    if kind == "angle":
        out += arrow(116, 240, 166, 276, "角度を切る")
    return out


def armbar(kind: str = "closed") -> str:
    opp_arms = [[(296, 160), (246, 158), (188, 160)], [(296, 184), (260, 208), (232, 236)]]
    opp_legs = [[(232, 172), (198, 144), (172, 118)], [(232, 190), (204, 222), (176, 250)]]
    me_arms = [[(178, 116), (178, 145), (188, 160)], [(204, 116), (218, 144), (188, 160)]]
    me_legs = [[(184, 176), (244, 132), (312, 132)], [(204, 180), (258, 194), (320, 204)]]
    out = figure((320, 172), (232, 182), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((190, 78), (194, 168), ME, "自分", me_arms, me_legs, ME_DARK)
    out += poly([(188, 160), (246, 158), (296, 160)], WARN, 7)
    out += grip(188, 160, "手首")
    out += zone([(176, 145), (216, 145), (218, 182), (176, 182)], "#dbeafe", 0.54)
    out += mat_note(200, 200, "両膝で腕を挟む")
    if kind == "swing":
        out += arrow(246, 132, 320, 116, "頭側の脚")
    if kind == "finish":
        out += arrow(194, 168, 194, 116, "腰を上げる")
        out += arrow(232, 160, 304, 160, "腕を伸ばす")
    return out


def pendulum(kind: str = "setup") -> str:
    out = closed_guard("control")
    out += grip(188, 238, "足")
    if kind == "swing":
        out += arrow(165, 245, 150, 146, "脚を振る")
    else:
        out += arrow(210, 222, 188, 238, "足を抱える")
    return out


def hip_bump(kind: str = "sit") -> str:
    me_arms = [[(152, 166), (196, 132), (252, 136)], [(152, 190), (204, 198), (264, 174)]]
    me_legs = [[(176, 220), (226, 218), (268, 198)], [(166, 234), (218, 246), (260, 238)]]
    opp_arms = [[(316, 136), (282, 136), (252, 136)], [(310, 160), (288, 174), (264, 174)]]
    opp_legs = [[(246, 158), (216, 130), (196, 102)], [(246, 182), (220, 210), (198, 242)]]
    out = figure((334, 148), (246, 170), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((130, 178), (170, 226), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(252, 136, "肩")
    if kind == "bump":
        out += arrow(170, 226, 262, 170, "腰をぶつける")
    if kind == "finish":
        out += arrow(130, 178, 252, 126, "覆い被さる")
    return out


def old_school(kind: str) -> str:
    if kind == "far_leg":
        return half_guard("far_leg")
    if kind == "come_up":
        return half_guard("come_up")
    return half_guard("old1")


def side_americana(kind: str = "pin") -> str:
    opp_arms = [[(142, 174), (190, 142), (244, 144)], [(142, 222), (176, 246), (218, 250)]]
    opp_legs = [[(246, 181), (288, 156), (326, 146)], [(246, 219), (292, 236), (330, 250)]]
    me_arms = [[(212, 122), (226, 138), (244, 144)], [(238, 126), (214, 154), (190, 142)]]
    me_legs = [[(236, 176), (280, 176), (320, 186)], [(230, 194), (276, 220), (316, 238)]]
    out = figure((94, 200), (246, 200), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((224, 84), (232, 182), ME, "自分", me_arms, me_legs, ME_DARK)
    out += poly([(244, 144), (190, 142), (214, 154), (244, 144)], WARN, 7)
    out += grip(244, 144, "手首")
    out += mat_note(214, 132, "腕を4の字")
    if kind == "key":
        out += grip(214, 154, "自分の手首")
    if kind == "finish":
        out += arrow(214, 154, 222, 126, "肘を上げる")
        out += arrow(244, 144, 252, 170, "手首は下")
    return out


def back_bow_arrow(kind: str = "collar") -> str:
    opp_arms = [[(236, 114), (232, 150), (226, 180)], [(260, 114), (270, 150), (282, 178)]]
    opp_legs = [[(236, 210), (214, 248), (196, 280)], [(260, 210), (290, 246), (316, 274)]]
    me_arms = [[(188, 120), (214, 106), (244, 92)], [(210, 120), (246, 168), (294, 250)]]
    me_legs = [[(190, 210), (224, 226), (254, 218)], [(210, 210), (250, 198), (282, 212)]]
    out = figure((248, 82), (248, 204), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((198, 86), (200, 204), ME, "自分", me_arms, me_legs, ME_DARK)
    out += grip(244, 92, "襟")
    out += zone([(190, 210), (254, 218), (282, 212), (210, 210)], "#dbeafe", 0.45)
    out += mat_note(236, 235, "両フックで背中を固定")
    if kind in {"leg", "finish"}:
        out += grip(294, 250, "足")
    if kind == "leg":
        out += arrow(294, 250, 332, 280, "足を引く")
    if kind == "finish":
        out += arrow(244, 92, 174, 92, "襟を引く")
        out += arrow(294, 250, 334, 282, "脚を引く")
    return out


def knee_slice(kind: str = "knee") -> str:
    opp_arms = [[(112, 188), (166, 154), (224, 148)], [(112, 226), (160, 244), (218, 230)]]
    opp_legs = [[(214, 190), (268, 180), (322, 166)], [(214, 218), (270, 236), (326, 254)]]
    me_arms = [[(326, 100), (300, 134), (258, 148)], [(350, 112), (328, 164), (276, 202)]]
    me_legs = [[(310, 182), (262, 196), (222, 212)], [(334, 184), (362, 222), (388, 256)]]
    out = figure((82, 208), (214, 204), OPP, "相手", opp_arms, opp_legs, OPP_DARK)
    out += figure((340, 70), (322, 176), ME, "自分", me_arms, me_legs, ME_DARK)
    out += zone([(262, 188), (314, 174), (326, 206), (252, 222)], "#dbeafe", 0.48)
    out += mat_note(294, 168, "膝を太ももに通す")
    if kind == "pressure":
        out += grip(258, 148, "襟") + grip(276, 202, "脇")
        out += arrow(326, 100, 268, 160, "頭を低く")
    if kind == "side":
        out += arrow(222, 212, 152, 250, "膝を抜く")
        out += arrow(322, 176, 232, 132, "サイドへ")
    return out


SCENES = {
    "closed_guard": closed_guard,
    "scissor": scissor,
    "mount": mount,
    "half_guard": half_guard,
    "butterfly": butterfly,
    "spider": spider,
    "dlr": dlr,
    "triangle": triangle,
    "armbar": armbar,
    "pendulum": pendulum,
    "hip_bump": hip_bump,
    "old_school": old_school,
    "americana": side_americana,
    "bow_arrow": back_bow_arrow,
    "knee_slice": knee_slice,
}


def render(scene: str, kind: str, num: int, label_text: str) -> str:
    body = SCENES[scene](kind)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label_text)}">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0 0L10 5L0 10z" fill="{ARROW}"/>
    </marker>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#0f172a" flood-opacity=".15"/>
    </filter>
  </defs>
  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="10" fill="{MAT}" stroke="{LINE}" stroke-width="2"/>
  <g filter="url(#shadow)">
    <circle cx="38" cy="38" r="20" fill="{ME}"/>
    <text x="38" y="45" font-family="sans-serif" font-size="20" font-weight="bold" fill="#fff" text-anchor="middle">{num}</text>
  </g>
  <g>
    <circle cx="368" cy="30" r="6" fill="{ME}"/><text x="380" y="34" font-family="sans-serif" font-size="11" fill="{MUTED}">自分</text>
    <circle cx="414" cy="30" r="6" fill="{OPP}"/><text x="426" y="34" font-family="sans-serif" font-size="11" fill="{MUTED}">相手</text>
  </g>
  {body}
  <text x="240" y="338" font-family="sans-serif" font-size="14" font-weight="700" fill="{INK}" text-anchor="middle">{esc(label_text)}</text>
</svg>
'''


SPEC = [
    ("scissor-sweep", [("closed_guard", "scissor_setup", "襟と袖を取り横向きに"), ("scissor", "shape", "スネと下脚でハサミを作る"), ("scissor", "finish", "押して刈りマウントへ")]),
    ("cross-collar-choke", [("closed_guard", "cross1", "片手を首裏まで深く"), ("closed_guard", "cross2", "反対の手を交差して握る"), ("closed_guard", "cross3", "肘を締めて胸へ引く")]),
    ("knee-slice-pass", [("knee_slice", "knee", "膝を太ももへスライス"), ("knee_slice", "pressure", "襟と脇を取り頭を低く"), ("knee_slice", "side", "膝を抜いてサイドへ")]),
    ("triangle-choke", [("triangle", "entry", "片腕を内・片腕を外に"), ("triangle", "lock", "首と片腕を三角で囲む"), ("triangle", "angle", "角度を切って絞める")]),
    ("armbar-closed", [("closed_guard", "pull", "片腕を抱えて崩す"), ("armbar", "swing", "頭側へ脚を回す"), ("armbar", "finish", "膝で挟み腰で極める")]),
    ("pendulum-sweep", [("pendulum", "setup", "袖と襟を取り片足を抱える"), ("pendulum", "swing", "脚を大きく振って勢いを作る"), ("mount", "sweep_finish", "横転させてマウント")]),
    ("hip-bump-sweep", [("hip_bump", "sit", "起き上がって肩を押さえる"), ("hip_bump", "bump", "腰をぶつけて後ろへ崩す"), ("hip_bump", "finish", "覆い被さってマウントへ")]),
    ("butterfly-sweep", [("butterfly", "base", "脇差しと両フックを作る"), ("butterfly", "lift", "横へ崩しフックで持ち上げる"), ("mount", "sweep_finish", "上を取る")]),
    ("old-school-sweep", [("old_school", "underhook", "横向きでアンダーフック"), ("old_school", "far_leg", "遠い足を腕ですくう"), ("old_school", "come_up", "起き上がってトップへ")]),
    ("mount-armbar", [("mount", "arm_isolate", "マウントで腕を分離する"), ("mount", "swing_leg", "片足を頭側へ回す"), ("armbar", "finish", "後ろへ倒れて腕を伸ばす")]),
    ("americana", [("americana", "pin", "手首をマットに固定"), ("americana", "key", "腕を4の字に組む"), ("americana", "finish", "手首を下げ肘を上げる")]),
    ("bow-and-arrow", [("bow_arrow", "collar", "バックから襟を深く握る"), ("bow_arrow", "leg", "相手の足を引っかける"), ("bow_arrow", "finish", "襟と脚を弓のように引く")]),
    ("guard-closed", [("closed_guard", "control", "脚を相手の腰でロック"), ("closed_guard", "pull", "襟と袖で姿勢を崩す")]),
    ("guard-half", [("half_guard", "lock", "相手の片足を脚で挟む"), ("half_guard", "shield", "アンダーフックとニーシールド")]),
    ("guard-butterfly", [("butterfly", "base", "座って両フックを内腿へ"), ("butterfly", "lift", "脇差しで横崩しの起点に")]),
    ("guard-spider", [("spider", "base", "両袖と足裏で腕を制御"), ("spider", "push_pull", "片足で押し袖を引く")]),
    ("guard-dlr", [("dlr", "hook", "前足の外からDLRフック"), ("dlr", "grips", "袖とかかとを取り崩す")]),
]


def main() -> None:
    n = 0
    for tid, steps in SPEC:
        d = os.path.join(ROOT, "images", tid)
        os.makedirs(d, exist_ok=True)
        for i, (scene, kind, label_text) in enumerate(steps, 1):
            svg = render(scene, kind, i, label_text)
            with open(os.path.join(d, f"{i:02d}.svg"), "w", encoding="utf-8") as f:
                f.write(svg)
            n += 1
    print(f"generated {n} svg files for {len(SPEC)} entries")


if __name__ == "__main__":
    main()
