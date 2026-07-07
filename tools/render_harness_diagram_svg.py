#!/usr/bin/env python3
"""Render the editable SVG version of the AI-agentic harness slide."""

from __future__ import annotations

import html
import math
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures" / "01-harness-operator-code-analysis-programming-model.ru.svg"

W, H = 1536, 1024


COLORS = {
    "ink": "#071225",
    "muted": "#283754",
    "blue": "#0b4fb3",
    "blue2": "#1a63c7",
    "green": "#1f7f35",
    "orange": "#f06b00",
    "purple": "#6b37b2",
    "teal": "#0f8b94",
    "gray": "#56687d",
    "line": "#295eab",
    "soft_blue": "#eef5ff",
    "soft_green": "#edf8ee",
    "soft_orange": "#fff5e6",
    "soft_purple": "#f6efff",
    "soft_teal": "#eaf9fa",
    "border": "#8fb4e8",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


class SVG:
    def __init__(self) -> None:
        self.parts: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = "none",
        stroke: str = "#000",
        sw: float = 1,
        rx: float = 6,
        opacity: float | None = None,
    ) -> None:
        op = "" if opacity is None else f' opacity="{opacity}"'
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:.1f}"{op}/>'
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = "#000",
        sw: float = 1.5,
        dash: str | None = None,
        marker: str | None = None,
    ) -> None:
        d = "" if dash is None else f' stroke-dasharray="{dash}"'
        m = "" if marker is None else f' marker-end="url(#{marker})"'
        self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw:.1f}" fill="none"{d}{m}/>'
        )

    def path(
        self,
        d: str,
        stroke: str = "#000",
        sw: float = 1.5,
        fill: str = "none",
        dash: str | None = None,
        marker: str | None = None,
    ) -> None:
        dash_attr = "" if dash is None else f' stroke-dasharray="{dash}"'
        marker_attr = "" if marker is None else f' marker-end="url(#{marker})"'
        self.add(
            f'<path d="{d}" stroke="{stroke}" stroke-width="{sw:.1f}" fill="{fill}"'
            f'{dash_attr}{marker_attr}/>'
        )

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: float = 12,
        fill: str = "#000",
        weight: int | str = 400,
        anchor: str = "start",
        family: str | None = None,
        style: str = "",
    ) -> None:
        fam = "" if family is None else f' font-family="{esc(family)}"'
        style_attr = "" if not style else f' style="{esc(style)}"'
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{fam}{style_attr}>{esc(value)}</text>'
        )

    def text_lines(
        self,
        x: float,
        y: float,
        lines: list[str],
        size: float = 10,
        fill: str = "#000",
        weight: int | str = 400,
        anchor: str = "start",
        leading: float | None = None,
    ) -> None:
        if not lines:
            return
        leading = leading or size * 1.32
        spans = []
        for idx, line in enumerate(lines):
            dy = 0 if idx == 0 else leading
            spans.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{esc(line)}</tspan>')
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}">' + "".join(spans) + "</text>"
        )

    def wrapped(
        self,
        x: float,
        y: float,
        text: str,
        chars: int,
        size: float = 10,
        fill: str = "#000",
        weight: int | str = 400,
        leading: float | None = None,
        bullet: str | None = None,
    ) -> float:
        leading = leading or size * 1.32
        lines = textwrap.wrap(text, chars, break_long_words=False, replace_whitespace=False)
        if bullet and lines:
            lines[0] = f"{bullet} {lines[0]}"
            for idx in range(1, len(lines)):
                lines[idx] = f"  {lines[idx]}"
        self.text_lines(x, y, lines, size=size, fill=fill, weight=weight, leading=leading)
        return y + max(len(lines), 1) * leading


def begin_svg() -> SVG:
    s = SVG()
    s.add(
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["blue2"]}"/>
    </marker>
    <marker id="arrow-gray" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["gray"]}"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{COLORS["green"]}"/>
    </marker>
    <filter id="soft-shadow" x="-6%" y="-6%" width="112%" height="112%">
      <feDropShadow dx="0" dy="1.2" stdDeviation="1.5" flood-color="#335" flood-opacity="0.10"/>
    </filter>
  </defs>
  <style>
    .font {{ font-family: Arial, Helvetica, "DejaVu Sans", sans-serif; }}
    .mono {{ font-family: Menlo, Consolas, "Liberation Mono", monospace; }}
    .cap {{ letter-spacing: .2px; }}
  </style>
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <g class="font">
'''
    )
    return s


def finish_svg(s: SVG) -> str:
    s.add("  </g>\n</svg>\n")
    return "\n".join(s.parts)


def card(s: SVG, x: float, y: float, w: float, h: float, title: str, color: str, fill: str) -> None:
    s.rect(x, y, w, h, "#ffffff", color, 1.0, 7)
    s.rect(x, y, w, 27, fill, color, 1.0, 7)
    s.line(x, y + 27, x + w, y + 27, color, 1.0)
    s.text(x + w / 2, y + 19, title, 13, color, 800, "middle")


def mini_icon(s: SVG, x: float, y: float, kind: str, color: str, size: float = 30) -> None:
    cx, cy = x + size / 2, y + size / 2
    if kind == "target":
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size*.42:.1f}" fill="none" stroke="{color}" stroke-width="2.0"/>')
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size*.27:.1f}" fill="none" stroke="{color}" stroke-width="1.6"/>')
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size*.10:.1f}" fill="{color}"/>')
        s.line(cx + 2, cy - 2, x + size * .95, y + size * .05, color, 1.8)
    elif kind == "checklist":
        s.rect(x + 5, y + 4, size - 10, size - 7, "none", color, 1.6, 3)
        for i in range(3):
            yy = y + 11 + i * 8
            s.path(f"M {x+10:.1f} {yy:.1f} l 3 3 l 5 -6", color, 1.4)
            s.line(x + 21, yy + 1, x + size - 8, yy + 1, color, 1.2)
    elif kind == "doc":
        s.rect(x + 7, y + 4, size - 12, size - 7, "none", color, 1.4, 2)
        s.path(f"M {x+size-11:.1f} {y+4:.1f} v 8 h 8", color, 1.2)
        for i in range(3):
            s.line(x + 11, y + 14 + i * 6, x + size - 9, y + 14 + i * 6, color, 1.1)
    elif kind == "code":
        s.rect(x + 3, y + 6, size - 6, size - 12, "none", color, 1.4, 3)
        s.text(cx, y + size * .63, "</>", size * .30, color, 800, "middle", family="Menlo")
    elif kind == "network":
        pts = [(cx, y + 6), (x + 7, y + size - 8), (x + size - 7, y + size - 8)]
        for a, b in [(0, 1), (0, 2), (1, 2)]:
            s.line(pts[a][0], pts[a][1], pts[b][0], pts[b][1], color, 1.2)
        for px, py in pts:
            s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.7" fill="#fff" stroke="{color}" stroke-width="1.4"/>')
    elif kind == "robot":
        s.rect(x + 5, y + 9, size - 10, size - 9, "#f7fbff", color, 1.7, 8)
        s.line(cx, y + 9, cx, y + 4, color, 1.4)
        s.add(f'<circle cx="{cx:.1f}" cy="{y+3.5:.1f}" r="2.4" fill="{color}"/>')
        s.add(f'<circle cx="{x+size*.38:.1f}" cy="{y+size*.56:.1f}" r="2.4" fill="{color}"/>')
        s.add(f'<circle cx="{x+size*.62:.1f}" cy="{y+size*.56:.1f}" r="2.4" fill="{color}"/>')
        s.line(x + size * .38, y + size * .72, x + size * .62, y + size * .72, color, 1.2)
    elif kind == "chart":
        s.line(x + 6, y + size - 6, x + size - 4, y + size - 6, color, 1.3)
        for i, bh in enumerate([9, 16, 24]):
            bx = x + 9 + i * 8
            s.rect(bx, y + size - 7 - bh, 5, bh, "none", color, 1.2, 1)
        s.path(f"M {x+7:.1f} {y+size-15:.1f} C {x+15:.1f} {y+size-23:.1f}, {x+19:.1f} {y+size-23:.1f}, {x+size-5:.1f} {y+8:.1f}", color, 1.4)
    elif kind == "gear":
        for a in range(0, 360, 45):
            r = math.radians(a)
            s.line(cx + math.cos(r) * 9, cy + math.sin(r) * 9, cx + math.cos(r) * 13, cy + math.sin(r) * 13, color, 1.6)
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9.5" fill="none" stroke="{color}" stroke-width="1.6"/>')
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.4" fill="none" stroke="{color}" stroke-width="1.4"/>')
    elif kind == "db":
        s.add(f'<ellipse cx="{cx:.1f}" cy="{y+8:.1f}" rx="{size*.38:.1f}" ry="5.0" fill="#eef3fb" stroke="{color}" stroke-width="1.2"/>')
        s.rect(x + size * .12, y + 8, size * .76, size - 14, "#eef3fb", color, 1.2, 0)
        for yy in [y + 8, y + size * .48, y + size - 6]:
            s.add(f'<ellipse cx="{cx:.1f}" cy="{yy:.1f}" rx="{size*.38:.1f}" ry="5.0" fill="none" stroke="{color}" stroke-width="1.2"/>')
    elif kind == "brain":
        for dx, dy in [(0, 0), (-7, 1), (7, 1), (-4, -7), (4, -7), (-2, 8), (5, 7)]:
            s.add(f'<circle cx="{cx+dx:.1f}" cy="{cy+dy:.1f}" r="5.5" fill="#fff" stroke="{color}" stroke-width="1.2"/>')
        s.path(f"M {cx-8:.1f} {cy+10:.1f} C {cx-5:.1f} {cy+17:.1f}, {cx+8:.1f} {cy+17:.1f}, {cx+10:.1f} {cy+7:.1f}", color, 1.2)
    elif kind == "cube":
        s.path(f"M {cx:.1f} {y+4:.1f} L {x+size-5:.1f} {y+11:.1f} L {cx:.1f} {y+18:.1f} L {x+5:.1f} {y+11:.1f} Z", color, 1.2, "#f9fbff")
        s.path(f"M {x+5:.1f} {y+11:.1f} L {x+5:.1f} {y+size-8:.1f} L {cx:.1f} {y+size-2:.1f} L {cx:.1f} {y+18:.1f}", color, 1.2)
        s.path(f"M {x+size-5:.1f} {y+11:.1f} L {x+size-5:.1f} {y+size-8:.1f} L {cx:.1f} {y+size-2:.1f}", color, 1.2)
    elif kind == "clock":
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size*.38:.1f}" fill="none" stroke="{color}" stroke-width="1.6"/>')
        s.line(cx, cy, cx, y + size * .30, color, 1.4)
        s.line(cx, cy, x + size * .68, y + size * .58, color, 1.4)
        for a in range(0, 360, 45):
            r = math.radians(a)
            s.line(cx + math.cos(r) * 10, cy + math.sin(r) * 10, cx + math.cos(r) * 12, cy + math.sin(r) * 12, color, 1.0)
    elif kind == "stars":
        s.text(cx, cy + 5, "☆☆☆☆☆", size * .54, "#f2a000", 700, "middle")
    elif kind == "spark":
        s.path(f"M {cx:.1f} {y+3:.1f} L {cx+5:.1f} {cy-2:.1f} L {x+size-3:.1f} {cy:.1f} L {cx+5:.1f} {cy+2:.1f} L {cx:.1f} {y+size-3:.1f} L {cx-5:.1f} {cy+2:.1f} L {x+3:.1f} {cy:.1f} L {cx-5:.1f} {cy-2:.1f} Z", color, 1.2, "#fffaf0")
    else:
        s.rect(x + 4, y + 4, size - 8, size - 8, "none", color, 1.4, 4)


def section_one(s: SVG) -> None:
    x, y, w, h = 17, 84, 294, 315
    color = COLORS["blue"]
    card(s, x, y, w, h, "1. ЦЕЛЬ И КЛЮЧЕВЫЕ ЗАДАЧИ", color, COLORS["soft_blue"])
    mini_icon(s, x + 13, y + 49, "target", color, 34)
    s.text(x + 62, y + 49, "Цель", 12, color, 800)
    s.wrapped(
        x + 62,
        y + 67,
        "Дать AI-агенту структурированные знания об операторе и целевой архитектуре, чтобы он мог анализировать, модифицировать и оптимизировать код с большей эффективностью и надёжностью.",
        39,
        9.3,
        COLORS["ink"],
        leading=12.4,
    )
    mini_icon(s, x + 13, y + 139, "checklist", color, 34)
    s.text(x + 62, y + 149, "Ключевые задачи", 12, color, 800)
    tasks = [
        "Извлечь из компилятора и профайлера полезные представления (views).",
        "Построить AI-friendly IR и набор допустимых преобразований.",
        "Передать агенту знания, контекст и ограничения.",
        "Агент предлагает изменения в коде/модели.",
        "Компиляция, проверка корректности и измерение производительности.",
        "Обучение и накопление опыта (skill/motif bank).",
    ]
    yy = y + 169
    for i, t in enumerate(tasks, 1):
        yy = s.wrapped(x + 50, yy, f"{i}. {t}", 42, 8.3, COLORS["ink"], leading=11.5)


def section_two(s: SVG) -> None:
    x, y, w, h = 320, 84, 860, 215
    color = COLORS["blue"]
    card(s, x, y, w, h, "2. ОБЩАЯ АРХИТЕКТУРА HARNESS", color, "#f7fbff")
    cols = [
        (x + 10, 115, 165, "Исходные артефакты", ["C++/AscendC код оператора", "Host-side tiling код", "Описание оператора (shape/dtype/layout)", "Тесты и референс-реализация"], ["doc", "code", "network", "doc"]),
        (x + 190, 115, 155, "Компиляторный пайплайн\n(Ascend toolchain)", ["Компиляция (AscendC/C++)", "Генерация двоичных файлов", "IR/дампы, логи, диагностика"], ["code", "doc", "gear"]),
        (x + 370, 115, 165, "Экстрактор представлений\n(Static & Program Analysis)", ["Статический анализ", "Извлечение IR и графов", "Построение AI-friendly views"], ["network", "network", "doc"]),
        (x + 550, 115, 155, "AI-Агент\n(Анализ и модификация)", ["Понимание контекста", "Планирование изменений", "Генерация патчей/кода/DSL"], ["robot"]),
        (x + 720, 115, 130, "Верификация и оценка", ["Компиляция и прогоны", "Проверка корректности", "Профилирование", "Оценка качества изменений"], ["clock", "chart"]),
    ]
    for idx, (cx, cy, cw, title, bullets, icons) in enumerate(cols):
        title_lines = title.split("\n")
        s.text_lines(cx + cw / 2, cy + 17, title_lines, 9.3, COLORS["ink"], 800, "middle", 12)
        ix = cx + 2
        for kind in icons:
            mini_icon(s, ix, cy + 45, kind, COLORS["gray"], 34)
            ix += 42
        if idx == 1:
            s.rect(cx + 8, cy + 42, cw - 16, 52, "#ffffff", COLORS["border"], 1, 5)
            s.text(cx + 26, cy + 72, "BiSheng", 9, COLORS["ink"], 800)
            s.text(cx + 77, cy + 72, "CANN", 9, COLORS["ink"], 800)
            s.text(cx + 121, cy + 72, "ATC", 9, COLORS["ink"], 800)
        yy = cy + 107
        for b in bullets:
            yy = s.wrapped(cx + 6, yy, b, max(20, int(cw / 5.2)), 8.0, "#111", leading=12, bullet="•")
        if idx < len(cols) - 1:
            s.line(cx + cw + 6, cy + 67, cx + cw + 26, cy + 67, COLORS["gray"], 2.0, marker="arrow-gray")


def section_three(s: SVG) -> None:
    x, y, w, h = 1194, 84, 324, 410
    color = COLORS["green"]
    card(s, x, y, w, h, "3. ПРЕДСТАВЛЕНИЯ (VIEWS) ДЛЯ АГЕНТА", color, COLORS["soft_green"])
    rows = [
        ("doc", "Semantic View (что делает оператор)", "op type, shape/dtype/layout, семантика, broadcast, редукции, точность, численные ограничения"),
        ("checklist", "Tiling View (разбиение работы)", "оси, размеры тайлов, split по ядрам, tail policy, объём данных, локальная память"),
        ("gear", "Pipeline View (CopyIn–Compute–CopyOut)", "стадии, очереди (TQue/TPipe), зависимости (events), перекрытие стадий, double-buffering"),
        ("doc", "Memory View", "пространства памяти (GM/UB/L1/L0/LOC), буферы, выравнивания, liveness, конфликты банков"),
        ("network", "Dependence View", "граф зависимостей данных и управления, def-use, alias/эффекты"),
        ("clock", "Performance View", "счётчики и метрики: время, загрузка AI Core, BW, stalls, IPC, bottlenecks, roofline"),
        ("spark", "Transformation Space", "допустимые преобразования и их предикаты, оценки стоимости и риски"),
    ]
    yy = y + 42
    row_h = 53
    for kind, title, desc in rows:
        s.line(x, yy - 8, x + w, yy - 8, "#9fd2aa", 0.8)
        mini_icon(s, x + 10, yy, kind, color, 27)
        s.text(x + 45, yy + 10, title, 9.8, "#0f5f23", 800)
        s.wrapped(x + 45, yy + 24, desc, 47, 8.1, "#111", leading=10.4)
        yy += row_h


def section_four(s: SVG) -> None:
    x, y, w, h = 17, 423, 294, 303
    color = COLORS["purple"]
    card(s, x, y, w, h, "4. ИНДУСТРИАЛЬНЫЕ ТЕХНИКИ АНАЛИЗА", color, COLORS["soft_purple"])
    rows = [
        ("network", "Dataflow Analysis (Kildall, 1973)", "reaching defs, liveness, const propagation и др."),
        ("clock", "Dependence Analysis (PDG)", "data/control зависимости, графы зависимостей"),
        ("doc", "Alias & Effect Analysis", "алиасы, побочные эффекты, память"),
        ("gear", "Abstract Interpretation", "диапазоны, формы, выравнивания, безопасность"),
        ("network", "Polyhedral Analysis (Affine)", "петли, аффинные доступы, векторизация, тайлинг, перестановки"),
        ("network", "Program Slicing & Pattern Mining", "выделение повторяющихся структур (motifs)"),
        ("gear", "E-Graphs & Equality Saturation (egg/Babble)", "поиск равноcильных программных форм"),
    ]
    yy = y + 43
    for kind, title, desc in rows:
        s.line(x, yy - 8, x + w, yy - 8, "#c7afe5", 0.8)
        mini_icon(s, x + 12, yy - 1, kind, color, 25)
        s.text(x + 47, yy + 9, title, 9.6, "#45238a", 800)
        s.wrapped(x + 47, yy + 22, desc, 43, 8.1, "#111", leading=9.8)
        yy += 40


def section_five(s: SVG) -> None:
    color = COLORS["blue"]
    s.text(768, 326, "5. AI-AGENT LOOP", 15, color, 900, "middle")
    s.rect(696, 344, 144, 23, "#f1f6ff", COLORS["border"], 1, 3)
    s.text(768, 361, "Действия агента", 10, color, 800, "middle")

    s.path("M 538 353 C 640 318, 880 321, 951 357", color, 1.6, marker="arrow-blue")
    s.path("M 947 533 C 825 570, 624 574, 532 535", color, 1.6, marker="arrow-blue")

    x1, y1, w1, h1 = 456, 363, 151, 163
    s.rect(x1, y1, w1, h1, "#f8fbff", "#8fb4e8", 1, 5, opacity=0.98)
    s.rect(x1, y1, w1, 27, "#eef5ff", "#8fb4e8", 1, 5)
    s.text(x1 + w1 / 2, y1 + 19, "Вход для агента", 10, color, 800, "middle")
    for i, kind in enumerate(["brain", "cube", "doc"]):
        mini_icon(s, x1 + 18 + i * 42, y1 + 42, kind, COLORS["gray"], 31)
    yy = y1 + 88
    for b in ["Все views (п.3)", "История изменений", "Результаты прошлых запусков", "Ограничения и цели", "Примеры/документация API"]:
        yy = s.wrapped(x1 + 14, yy, b, 28, 8.0, "#111", leading=12, bullet="•")

    x2, y2, w2, h2 = 650, 373, 191, 163
    s.rect(x2, y2, w2, h2, "#f2fbf0", "#91c59b", 1, 5)
    actions = [
        "Изменение тайлинга",
        "Перестановка циклов",
        "Включение double-buffering",
        "Изменение количества очередей",
        "Векторизация / unroll",
        "Fusion / fission",
        "Изменение размещения данных",
        "Изменение точности",
        "Генерация DSL/IR патча",
        "Рефакторинг кода",
    ]
    yy = y2 + 18
    for b in actions:
        yy = s.wrapped(x2 + 14, yy, b, 32, 8.0, "#111", leading=13, bullet="•")
    mini_icon(s, x2 + w2 - 36, y2 + 11, "gear", COLORS["green"], 27)
    mini_icon(s, x2 + w2 - 36, y2 + 47, "gear", COLORS["green"], 27)

    x3, y3, w3, h3 = 886, 363, 143, 163
    s.rect(x3, y3, w3, h3, "#f8fbff", "#8fb4e8", 1, 5)
    s.rect(x3, y3, w3, 27, "#eef5ff", "#8fb4e8", 1, 5)
    s.text(x3 + w3 / 2, y3 + 19, "Выход агента", 10, color, 800, "middle")
    for i in range(3):
        mini_icon(s, x3 + 12 + i * 39, y3 + 36, "code", color, 34)
    yy = y3 + 89
    for b in ["Патчи кода / новый код", "Параметры запуска", "Изменения в host/tiling коде", "Новые аннотации/директивы"]:
        yy = s.wrapped(x3 + 14, yy, b, 26, 8.0, "#111", leading=12, bullet="•")

    s.line(x1 + w1 + 8, y1 + 73, x2 - 18, y1 + 73, COLORS["blue2"], 2.4, marker="arrow-blue")
    s.line(x3 - 8, y1 + 73, x2 + w2 + 16, y1 + 73, COLORS["blue2"], 2.4, marker="arrow-blue")


def section_six(s: SVG) -> None:
    x, y, w, h = 425, 590, 628, 108
    color = COLORS["blue"]
    s.rect(x, y, w, h, "#ffffff", "#a9c4e8", 1, 7)
    s.text(x + w / 2, y + 18, "6. ВЕРИФИКАЦИЯ И ОБРАТНАЯ СВЯЗЬ", 14, color, 900, "middle")
    items = [
        ("gear", "Компиляция", "(AscendC/ATC)"),
        ("checklist", "Корректность", "(сравнение с референсом)"),
        ("clock", "Профилирование", "(msProf)\nсбор метрик"),
        ("chart", "Анализ производительности", "(roofline, bottlenecks)"),
        ("stars", "Оценка качества", "(скорость, стабильность,\nиспользование ресурсов)"),
    ]
    bw = 108
    for i, (kind, title, sub) in enumerate(items):
        bx = x + 10 + i * 128
        s.rect(bx, y + 30, bw, 75, "#fafcff", "#c5d5eb", 1, 4)
        s.text(bx + bw / 2, y + 43, title, 8.4, "#111", 800, "middle")
        s.text_lines(bx + bw / 2, y + 56, sub.split("\n"), 7.2, "#111", 400, "middle", 9)
        mini_icon(s, bx + 42, y + 73, kind, COLORS["gray"], 28)

    sx, sy, sw, sh = 553, 711, 390, 74
    s.rect(sx, sy, sw, sh, "#f8fbff", "#a9c4e8", 1, 6)
    mini_icon(s, sx + 9, sy + 9, "db", COLORS["gray"], 63)
    s.text(sx + 92, sy + 17, "База опыта (Experience / Motif / Skill Bank)", 9.6, color, 800)
    yy = sy + 32
    for b in ["Успешные паттерны оптимизаций", "Анти-паттерны и причины неудач", "Связь: изменение → эффект (метрики)", "Кодовые сниппеты, аннотации, рецепты"]:
        yy = s.wrapped(sx + 93, yy, b, 52, 7.6, "#111", leading=10.3, bullet="•")


def section_seven(s: SVG) -> None:
    x, y, w, h = 1145, 508, 373, 264
    color = COLORS["orange"]
    card(s, x, y, w, h, "7. ПРОГРАММНАЯ МОДЕЛЬ И ЕЁ МОДИФИКАЦИЯ", color, COLORS["soft_orange"])
    mini_icon(s, x + 12, y + 45, "network", color, 36)
    s.text(x + 48, y + 52, "Как сделать модель AI-дружественной", 10.2, "#111", 800)
    yy = y + 68
    for b in [
        "Явные примитивы и семантика (pipeline, memory, sync)",
        "Декларативные аннотации и контракты",
        "Ограничения и проверяемые свойства",
        "Метрики и cost-модель как часть модели",
        "Структурированный IR/DSL слой над кодом",
    ]:
        yy = s.wrapped(x + 60, yy, b, 55, 8.4, "#111", leading=12.2, bullet="•")
    s.line(x, y + 137, x + w, y + 137, "#efb56f", 0.9)
    mini_icon(s, x + 12, y + 151, "doc", color, 33)
    s.text(x + 48, y + 158, "Что можно модифицировать/расширять", 10.2, "#111", 800)
    yy = y + 174
    for b in [
        "Новый DSL/IR слой (операторы высокого уровня)",
        "Новые примитивы (copy_async, stage, barrier, etc.)",
        "Аннотации и атрибуты (buffer, align, reuse, etc.)",
        "Правила lowering в AscendC/ISA",
        "Верификаторы и статические проверки",
    ]:
        yy = s.wrapped(x + 60, yy, b, 55, 8.4, "#111", leading=12.2, bullet="•")


def section_eight(s: SVG) -> None:
    x, y, w, h = 17, 793, 364, 160
    color = COLORS["teal"]
    card(s, x, y, w, h, "8. ИНСТРУМЕНТЫ И ИСТОЧНИКИ ДАННЫХ", color, COLORS["soft_teal"])
    items = [
        ("doc", "BiSheng", "компиляция и сборка"),
        ("code", "msProf", "профилирование"),
        ("doc", "msobjdump", "разбор ELF/дампов"),
        ("network", "msKPP", "моделирование производит., автотюнинг"),
        ("code", "Ascend C API", "(AscendC/C++ Runtime)"),
        ("doc", "Тесты и датасеты", "формы, точности, нагрузки"),
    ]
    for i, (kind, title, desc) in enumerate(items):
        col = i % 3
        row = i // 3
        ix = x + 12 + col * 122
        iy = y + 44 + row * 60
        mini_icon(s, ix, iy, kind, color, 27)
        s.text(ix + 35, iy + 9, title, 8.5, "#111", 800)
        s.wrapped(ix + 35, iy + 23, desc, 18, 6.8, "#111", leading=8.4)


def section_nine(s: SVG) -> None:
    x, y, w, h = 395, 795, 737, 157
    color = COLORS["blue"]
    card(s, x, y, w, h, "9. ПРИМЕР ПОТОКА ДЛЯ ОДНОГО ОПЕРАТОРА", color, "#f9fcff")
    steps = [
        ("brain", "Оператор\n(RMSNorm)"),
        ("checklist", "Исходный\nкод"),
        ("gear", "Компиляция\n(BiSheng/ATC)"),
        ("doc", "Извлечение\nviews"),
        ("gear", "Агент\nпредлагает\nизменения"),
        ("code", "Новый код/\nпараметры"),
        ("db", "Компиляция\nи прогоны"),
        ("code", "Метрики\nи анализ"),
        ("checklist", "Улучшение?"),
        ("spark", "Да"),
        ("db", "Сохранить в\nбазу опыта"),
    ]
    sx = x + 18
    gap = 67
    yy = y + 49
    centers = []
    for i, (kind, label) in enumerate(steps):
        cx = sx + i * gap
        if i == 9:
            cx -= 8
        if i == 10:
            cx -= 16
        centers.append((cx + 15, yy + 15))
        mini_icon(s, cx, yy, kind, COLORS["gray"] if i not in {8, 9} else COLORS["green"], 31)
        if i == 9:
            s.text(cx + 15, yy - 3, "Да", 7.5, "#111", 700, "middle")
        else:
            s.text_lines(cx + 15, yy + 48, label.split("\n"), 7.4, "#111", 400, "middle", 8.8)
    for i in range(len(centers) - 1):
        x1, y1 = centers[i]
        x2, y2 = centers[i + 1]
        s.line(x1 + 17, y1, x2 - 18, y2, COLORS["gray"] if i < 8 else COLORS["green"], 1.6, marker="arrow-gray" if i < 8 else "arrow-green")
    s.path(f"M {centers[8][0]:.1f} {centers[8][1]+22:.1f} V {y+139:.1f} H {centers[3][0]:.1f}", COLORS["gray"], 1.1, marker="arrow-gray")
    s.text((centers[3][0] + centers[8][0]) / 2, y + 145, "Нет", 7.5, COLORS["gray"], 700, "middle")


def section_ten(s: SVG) -> None:
    x, y, w, h = 1149, 793, 369, 160
    color = COLORS["green"]
    card(s, x, y, w, h, "10. ВЫГОДЫ И ОЖИДАЕМЫЕ ЭФФЕКТЫ", color, COLORS["soft_green"])
    yy = y + 42
    items = [
        "Агент понимает оператора на структурном уровне, а не только по тексту кода.",
        "Снижение пространства поиска и числа ошибок.",
        "Более стабильные и объяснимые оптимизации.",
        "Накопление переиспользуемых паттернов (Skill Bank).",
        "Эволюция программной модели под домен и архитектуру.",
    ]
    for b in items:
        s.text(x + 18, yy, "☑", 12, color, 700)
        yy = s.wrapped(x + 38, yy, b, 55, 9.0, "#111", leading=13.2)
        yy += 2


def connectors(s: SVG) -> None:
    purple = COLORS["purple"]
    gray = "#36455d"
    s.path("M 404 301 V 411 H 457", purple, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 384 392 H 320", purple, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 384 392 V 302", purple, 1.3, dash="2 4")
    s.path("M 384 564 H 320", purple, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 384 564 V 392", purple, 1.3, dash="2 4")
    s.path("M 1086 302 V 411 H 1030", gray, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 1028 639 H 1107 V 414 H 1190", gray, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 1110 750 H 945", gray, 1.3, dash="2 4", marker="arrow-gray")
    s.path("M 370 640 H 425", COLORS["blue2"], 1.2, dash="2 4", marker="arrow-blue")
    s.path("M 369 640 V 746 H 553", COLORS["blue2"], 1.2, dash="2 4", marker="arrow-blue")


def bottom_key(s: SVG) -> None:
    x, y, w, h = 266, 967, 986, 39
    s.rect(x, y, w, h, "#fffaf0", "#e9b943", 0.9, 5)
    s.text(x + 45, y + 18, "КЛЮЧЕВАЯ ИДЕЯ:", 10.5, "#111", 900)
    s.text(
        x + 165,
        y + 18,
        "Компиляторные инструменты + статический анализ + структурированные представления + ограничения программной модели",
        10.0,
        "#111",
        700,
    )
    s.text(
        x + w / 2,
        y + 32,
        "позволяют AI-агенту эффективно анализировать и оптимизировать код операторов с доказуемой корректностью и измеримым выигрышем в производительности.",
        9.8,
        "#111",
        500,
        "middle",
    )


def main() -> None:
    s = begin_svg()

    s.text(
        W / 2,
        35,
        "Harness for AI Agentic Operator Code Analysis & Programming Model",
        30,
        COLORS["ink"],
        900,
        "middle",
    )
    s.text(
        W / 2,
        59,
        "Архитектура: как использовать инструменты компилятора, статический анализ и модификации программной модели для агентного тюнинга операторов",
        14,
        COLORS["muted"],
        400,
        "middle",
    )

    section_one(s)
    section_two(s)
    section_three(s)
    section_four(s)
    section_five(s)
    section_six(s)
    section_seven(s)
    section_eight(s)
    section_nine(s)
    section_ten(s)
    connectors(s)
    bottom_key(s)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(finish_svg(s), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
