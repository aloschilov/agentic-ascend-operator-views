#!/usr/bin/env python3
"""Render editable SVG variants for the three programming-model figures."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Iterable

from render_harness_diagram_svg import COLORS, W, SVG, begin_svg, finish_svg, mini_icon


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "assets" / "figures"


def out_path(name: str) -> Path:
    return FIG / name


def write(name: str, svg: SVG) -> None:
    path = out_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(finish_svg(svg), encoding="utf-8")
    print(path)


def title(s: SVG, main: str, subtitle: str, main_size: float = 27) -> None:
    s.text(W / 2, 34, main, main_size, COLORS["ink"], 900, "middle")
    s.text(W / 2, 58, subtitle, 14, COLORS["ink"], 400, "middle")


def panel(s: SVG, x: float, y: float, w: float, h: float, title_text: str, color: str, fill: str) -> None:
    s.rect(x, y, w, h, "#ffffff", color, 1.0, 7)
    s.rect(x, y, w, 27, fill, color, 1.0, 7)
    s.line(x, y + 27, x + w, y + 27, color, 1.0)
    raw_lines = []
    for part in title_text.split("\n"):
        raw_lines.extend(textwrap.wrap(part, max(16, int(w / 8.2)), break_long_words=False) or [""])
    longest = max((len(line) for line in raw_lines), default=0)
    size = 13.0
    if len(raw_lines) > 1:
        size = 8.2 if longest > 42 else 9.2
    elif longest > w / 6.0:
        size = 10.2
    start_y = y + 14 if len(raw_lines) > 1 else y + 19
    s.text_lines(x + w / 2, start_y, raw_lines, size, color, 900, "middle", min(9.7, size + 1.2))


def row_cards(
    s: SVG,
    x: float,
    y: float,
    w: float,
    entries: list[tuple[str, str]],
    color: str,
    fill: str,
    row_h: float,
    title_chars: int = 30,
    body_chars: int = 54,
) -> None:
    yy = y
    for name, desc in entries:
        s.rect(x, yy, w, row_h - 4, fill, "#c9d8e8" if color != COLORS["purple"] else "#d3b9ec", 0.9, 4)
        s.wrapped(x + 9, yy + 14, name, title_chars, 8.3, COLORS["ink"], 900, leading=9.5)
        s.wrapped(x + 9, yy + 31, desc, body_chars, 7.2, "#111", 400, leading=8.5)
        yy += row_h


def bullets(
    s: SVG,
    x: float,
    y: float,
    items: Iterable[str],
    chars: int,
    size: float = 8.5,
    leading: float = 11.5,
    bullet: str = "•",
    fill: str = "#111",
) -> float:
    yy = y
    for item in items:
        yy = s.wrapped(x, yy, item, chars, size, fill, 400, leading=leading, bullet=bullet)
    return yy


def mini_flow(s: SVG, x: float, y: float, w: float, steps: list[tuple[str, str]], color: str) -> None:
    n = len(steps)
    gap = w / n
    for idx, (kind, label) in enumerate(steps):
        cx = x + gap * idx + gap / 2
        mini_icon(s, cx - 18, y, kind, COLORS["gray"], 36)
        s.text_lines(cx, y + 57, label.split("\n"), 7.3, "#111", 400, "middle", 8.4)
        if idx < n - 1:
            s.line(cx + 25, y + 18, x + gap * (idx + 1) + gap / 2 - 28, y + 18, color, 1.6, marker="arrow-gray")


def dashed_link(s: SVG, d: str, color: str = "#344760", marker: str | None = "arrow-gray") -> None:
    s.path(d, color, 1.1, dash="2 4", marker=marker)


def render_01_en() -> None:
    s = begin_svg()
    title(
        s,
        "Harness for AI-Agentic Operator Code Analysis & Programming Model",
        "Architecture: compiler tools, static analysis, and programming-model constraints for agentic operator tuning",
        28,
    )

    panel(s, 17, 84, 294, 315, "1. GOAL AND KEY TASKS", COLORS["blue"], COLORS["soft_blue"])
    mini_icon(s, 30, 132, "target", COLORS["blue"], 36)
    s.text(78, 133, "Goal", 12, COLORS["blue"], 900)
    s.wrapped(78, 151, "Give the AI agent structured knowledge about the operator and target architecture so it can analyze, modify, and optimize code more effectively and reliably.", 39, 9.3, COLORS["ink"], leading=12.4)
    mini_icon(s, 30, 224, "checklist", COLORS["blue"], 35)
    s.text(78, 234, "Key tasks", 12, COLORS["blue"], 900)
    bullets(
        s,
        67,
        254,
        [
            "Extract useful views from compiler and profiler artifacts.",
            "Build an AI-friendly IR and legal transformation set.",
            "Pass knowledge, context, and constraints to the agent.",
            "Let the agent propose code/model changes.",
            "Compile, verify correctness, and measure performance.",
            "Accumulate reusable experience in a skill/motif bank.",
        ],
        43,
        8.3,
        11.5,
        "",
    )

    panel(s, 320, 84, 860, 215, "2. OVERALL HARNESS ARCHITECTURE", COLORS["blue"], "#f7fbff")
    arch = [
        ("doc", "Source artifacts", ["C++/AscendC operator code", "Host-side tiling code", "Operator spec: shape/dtype/layout", "Tests and reference implementation"]),
        ("code", "Compiler pipeline\n(Ascend toolchain)", ["Compile AscendC/C++", "Generate binaries", "IR/dumps, logs, diagnostics"]),
        ("network", "View extractor\n(Static & Program Analysis)", ["Static analysis", "Extract IR and graphs", "Build AI-friendly views"]),
        ("robot", "AI agent\n(analysis and modification)", ["Understand context", "Plan changes", "Generate patches/code/DSL"]),
        ("chart", "Verification and scoring", ["Compile and run", "Check correctness", "Profile", "Score quality of changes"]),
    ]
    for i, (kind, head, items) in enumerate(arch):
        x = 334 + i * 176
        s.text_lines(x + 72, 132, head.split("\n"), 9.2, "#111", 900, "middle", 11)
        mini_icon(s, x + 54, 162, kind, COLORS["gray"], 38)
        bullets(s, x, 222, items, 29, 7.8, 11.4, "•")
        if i < len(arch) - 1:
            s.line(x + 148, 181, x + 176, 181, COLORS["gray"], 2.0, marker="arrow-gray")

    panel(s, 1194, 84, 324, 410, "3. AGENT VIEWS", COLORS["green"], COLORS["soft_green"])
    view_rows = [
        ("doc", "Semantic View", "operator type, shapes, layout, semantics, broadcast, reductions, precision limits"),
        ("checklist", "Tiling View", "axes, tile sizes, core split, tail policy, data volume, local memory"),
        ("gear", "Pipeline View", "CopyIn-Compute-CopyOut stages, queues, events, overlap, double buffering"),
        ("doc", "Memory View", "GM/UB/L1/L0/LOC spaces, buffers, alignment, liveness, bank conflicts"),
        ("network", "Dependence View", "data/control dependence graph, def-use, aliases and effects"),
        ("clock", "Performance View", "time, AI Core utilization, bandwidth, stalls, IPC, bottlenecks, roofline"),
        ("spark", "Transformation Space", "legal transformations, predicates, cost estimates, and risks"),
    ]
    yy = 129
    for kind, name, desc in view_rows:
        mini_icon(s, 1206, yy - 1, kind, COLORS["green"], 28)
        s.text(1240, yy + 10, name, 9.5, COLORS["green"], 900)
        s.wrapped(1240, yy + 24, desc, 45, 7.4, "#111", leading=9.2)
        yy += 52
        s.line(1194, yy - 12, 1518, yy - 12, "#b6dfbd", 0.8)

    panel(s, 17, 423, 294, 303, "4. INDUSTRIAL ANALYSIS TECHNIQUES", COLORS["purple"], COLORS["soft_purple"])
    row_cards(
        s,
        25,
        455,
        278,
        [
            ("Dataflow Analysis", "reaching defs, liveness, const propagation"),
            ("Dependence Analysis (PDG)", "data/control dependencies, dependence graphs"),
            ("Alias & Effect Analysis", "aliases, side effects, memory regions"),
            ("Abstract Interpretation", "ranges, shapes, alignment, safety"),
            ("Polyhedral Analysis", "loops, affine accesses, tiling, interchange"),
            ("Program Slicing & Pattern Mining", "repeated optimization structures"),
            ("E-Graphs & Equality Saturation", "equivalent program forms"),
        ],
        COLORS["purple"],
        "#fbf7ff",
        39,
    )

    s.text(768, 326, "5. AI-AGENT LOOP", 15, COLORS["blue"], 900, "middle")
    s.path("M 538 353 C 640 318, 880 321, 951 357", COLORS["blue"], 1.6, marker="arrow-blue")
    s.path("M 947 533 C 825 570, 624 574, 532 535", COLORS["blue"], 1.6, marker="arrow-blue")
    loop_boxes = [
        (456, 363, 151, 163, "Agent input", ["All views", "Change history", "Previous run results", "Goals and constraints", "API examples/docs"]),
        (650, 373, 191, 163, "Agent actions", ["Change tiling", "Loop reorder", "Enable double buffering", "Adjust queues", "Vectorize/unroll", "Fusion/fission", "Data placement", "Precision changes", "Generate DSL/IR patch", "Refactor code"]),
        (886, 363, 143, 163, "Agent output", ["Code patches/new code", "Run parameters", "Host/tiling changes", "New annotations/directives"]),
    ]
    for bx, by, bw, bh, head, items in loop_boxes:
        fill = "#f2fbf0" if "actions" in head.lower() else "#f8fbff"
        stroke = "#91c59b" if "actions" in head.lower() else COLORS["border"]
        s.rect(bx, by, bw, bh, fill, stroke, 1, 5)
        s.rect(bx, by, bw, 27, "#eef5ff", stroke, 1, 5)
        s.text(bx + bw / 2, by + 19, head, 10, COLORS["blue"], 900, "middle")
        bullets(s, bx + 14, by + 58, items, 32, 7.7, 11.6, "•")
    s.line(615, 437, 642, 437, COLORS["blue2"], 2.4, marker="arrow-blue")
    s.line(879, 437, 851, 437, COLORS["blue2"], 2.4, marker="arrow-blue")

    panel(s, 425, 590, 628, 108, "6. VERIFICATION AND FEEDBACK", COLORS["blue"], "#f8fbff")
    checks = [("gear", "Compile"), ("checklist", "Correctness"), ("clock", "Profiling"), ("chart", "Performance"), ("stars", "Quality")]
    for i, (kind, name) in enumerate(checks):
        bx = 435 + i * 128
        s.rect(bx, 620, 108, 75, "#fbfdff", "#c5d5eb", 1, 4)
        s.text(bx + 54, 641, name, 8.8, "#111", 900, "middle")
        mini_icon(s, bx + 40, 660, kind, COLORS["gray"], 29)
    s.rect(553, 711, 390, 74, "#f8fbff", "#a9c4e8", 1, 6)
    mini_icon(s, 562, 720, "db", COLORS["gray"], 63)
    s.text(645, 728, "Experience / Motif / Skill Bank", 9.6, COLORS["blue"], 900)
    bullets(s, 645, 742, ["Successful optimization patterns", "Anti-patterns and failure causes", "Change -> effect links", "Snippets, annotations, recipes"], 54, 7.6, 10.2, "•")

    panel(s, 1145, 508, 373, 264, "7. PROGRAMMING MODEL AND MODIFICATION", COLORS["orange"], COLORS["soft_orange"])
    s.text(1194, 560, "Make the model AI-friendly", 10.2, "#111", 900)
    bullets(s, 1204, 579, ["Explicit pipeline/memory/sync primitives", "Declarative annotations and contracts", "Constraints and checkable properties", "Metrics and cost model as part of the model", "Structured IR/DSL layer above code"], 52, 8.2, 12, "•")
    s.line(1145, 646, 1518, 646, "#efb56f", 0.9)
    s.text(1194, 677, "What can be modified/extended", 10.2, "#111", 900)
    bullets(s, 1204, 696, ["New DSL/IR layer", "New primitives: copy_async, stage, barrier", "Annotations: buffer, align, reuse", "Lowering rules to AscendC/ISA", "Verifiers and static checks"], 52, 8.2, 12, "•")

    panel(s, 17, 793, 364, 160, "8. TOOLS AND DATA SOURCES", COLORS["teal"], COLORS["soft_teal"])
    tools = [("BiSheng", "compile/build"), ("msProf", "profiling"), ("msobjdump", "ELF/dump analysis"), ("msKPP", "performance modeling"), ("Ascend C API", "runtime/API"), ("Tests & datasets", "shapes, dtypes, workloads")]
    for i, (name, desc) in enumerate(tools):
        ix = 30 + (i % 3) * 120
        iy = 842 + (i // 3) * 60
        mini_icon(s, ix, iy, "doc" if i % 3 != 1 else "code", COLORS["teal"], 27)
        s.text(ix + 35, iy + 9, name, 8.5, "#111", 900)
        s.wrapped(ix + 35, iy + 23, desc, 18, 6.9, "#111", leading=8.4)
    panel(s, 395, 795, 737, 157, "9. SINGLE-OPERATOR FLOW EXAMPLE", COLORS["blue"], "#f9fcff")
    mini_flow(s, 407, 848, 700, [("brain", "Operator\nRMSNorm"), ("checklist", "Source\ncode"), ("gear", "Compile"), ("doc", "Extract\nviews"), ("gear", "Agent\nchanges"), ("code", "New code"), ("db", "Runs"), ("code", "Metrics"), ("checklist", "Better?"), ("spark", "Yes"), ("db", "Save\nexperience")], COLORS["gray"])
    panel(s, 1149, 793, 369, 160, "10. BENEFITS AND EXPECTED EFFECTS", COLORS["green"], COLORS["soft_green"])
    bullets(s, 1187, 833, ["Agent reasons over structure, not only text.", "Smaller search space and fewer mistakes.", "More stable and explainable optimization.", "Reusable patterns accumulate in the skill bank.", "The programming model evolves toward the domain."], 54, 8.7, 13, "☑", COLORS["ink"])

    dashed_link(s, "M 404 301 V 411 H 457", COLORS["purple"])
    dashed_link(s, "M 1086 302 V 411 H 1030")
    dashed_link(s, "M 1028 639 H 1107 V 414 H 1190")
    dashed_link(s, "M 370 640 H 425", COLORS["blue2"], "arrow-blue")
    s.rect(266, 967, 986, 39, "#fffaf0", "#e9b943", 0.9, 5)
    s.text(342, 986, "KEY IDEA:", 10.5, "#111", 900)
    s.text(438, 986, "compiler tools + static analysis + structured views + programming-model constraints", 10, "#111", 700)
    s.text(759, 1000, "help the AI agent optimize operator code with measurable speedups and checkable correctness.", 9.8, "#111", 500, "middle")

    write("01-harness-operator-code-analysis-programming-model.en.svg", s)


def render_02(lang: str) -> None:
    en = lang == "en"
    s = begin_svg()
    title(
        s,
        "Roadmap: Bottom-Up Programming Model Induction with LLMs" if en else "Карта направлений: снизу вверх индукция программных моделей с помощью LLM",
        "How to evolve a programming-model basis when the low-level target is known" if en else "Как автоматически эволюционно формировать базис программной модели, когда нижний уровень (target) известен",
        27,
    )

    panel(s, 29, 73, 286, 347, "1. Library and Abstraction Induction" if en else "1. Индукция библиотек и абстракций\nиз программ", COLORS["green"], COLORS["soft_green"])
    left1 = [
        ("DreamCoder", "extracts and reuses new abstractions in wake-sleep loops" if en else "извлечение и использование новых абстракций в цикле wake-sleep"),
        ("LAPS", "natural language guides library learning and heuristic search" if en else "естественный язык для обучения библиотек и эвристик поиска"),
        ("Stitch", "fast extraction of reusable functions/DSL fragments" if en else "быстрое извлечение переиспользуемых функций/DSL из корпуса программ"),
        ("LILO", "LLM + compression + abstraction documentation" if en else "LLM + сжатие + автодокументация абстракций"),
        ("Babble", "e-graphs and equality saturation for modularity motifs" if en else "e-graphs и equality saturation для поиска общих паттернов модульности"),
        ("AbstractBeam", "adds frequent structures to the DSL, improves syntax search" if en else "добавление часто встречающихся структур в DSL улучшает синтез снизу вверх"),
        ("Leroy", "library learning in imperative languages" if en else "library learning в императивных языках"),
    ]
    row_cards(s, 41, 115, 263, left1, COLORS["green"], "#f7fff8", 42, 24, 49)

    panel(s, 1178, 76, 254, 351, "2. Automatic DSL / Grammar Design" if en else "2. Автоматическое проектирование DSL/грамматик", COLORS["blue"], COLORS["soft_blue"])
    right2 = [
        ("AutoDSL", "syntax-driven DSL design with semantic constraints" if en else "автоматический дизайн DSL с синтаксическими и семантическими ограничениями"),
        ("Grammar Prompting", "BNF grammars guide DSL generation" if en else "использование BNF-грамматик для генерации DSL"),
        ("HYSYNTH", "LLM learns surrogate CFG model for synthesis" if en else "LLM учит суррогатную CFG-модель для синтеза программ"),
        ("Text2DSL", "NL-to-DSL generation constrained by grammar/API" if en else "NL-to-DSL генерация с учётом грамматики и API"),
        ("From Text to DSL", "DSL-model generation and validity/semantic scoring" if en else "генерация DSL-моделей и оценка валидности/семантики"),
        ("HyGenar", "evolution for BNF grammar generation" if en else "LLM + эволюция для генерации BNF-грамматик"),
        ("Metamodel-Grammar Co-Evolution", "joint metamodel and grammar evolution" if en else "совместная эволюция метамодели и грамматики"),
        ("Anka", "DSL designed for reliable LLM generation" if en else "DSL, спроектированный для надёжной генерации LLM"),
    ]
    row_cards(s, 1188, 116, 234, right2, COLORS["blue"], "#f8fbff", 38, 26, 40)

    panel(s, 324, 76, 844, 164, "General Programming-Model Evolution Loop" if en else "Общий цикл эволюции программной модели", COLORS["gray"], "#ffffff")
    steps = [
        ("db", "Program corpus\nprofiles, traces"),
        ("clock", "Analyze and\nextract patterns"),
        ("spark", "Candidate\nabstractions"),
        ("doc", "LLM names,\ndocs, examples"),
        ("code", "Formalize\nIR/DSL"),
        ("clock", "Lower to\ntarget"),
        ("chart", "Compile,\ntest, profile"),
        ("gear", "Accept / reject\nand iterate"),
    ] if en else [
        ("db", "Корпус программ,\nпрофили, трассы"),
        ("clock", "Анализ и\nизвлечение"),
        ("spark", "Кандидаты\nабстракций"),
        ("doc", "LLM: имена,\nописания"),
        ("code", "Формализация\nIR/DSL"),
        ("clock", "Lowering в\ntarget"),
        ("chart", "Компиляция,\nтесты"),
        ("gear", "Принять /\nотклонить"),
    ]
    mini_flow(s, 338, 122, 800, steps, COLORS["gray"])

    cx, cy, cw, ch = 545, 264, 400, 288
    s.rect(cx, cy, cw, ch, "#fffaff", COLORS["purple"], 1.2, 9)
    s.text(cx + cw / 2, cy + 57, "Goal" if en else "Цель", 18, COLORS["purple"], 900, "middle")
    s.text_lines(
        cx + cw / 2,
        cy + 99,
        (
            [
                "Given a known low-level target:",
                "ISA / AscendC / LLVM / MLIR / API / runtime blocks",
                "",
                "Induce and evolve a programming model M:",
                "primitives, combinators, types, contracts,",
                "resource/effect semantics, lowering rules,",
                "verifiers, examples, docs, and cost model.",
                "",
                "M is accepted only when it improves synthesis,",
                "optimization, verification, interpretability,",
                "or productivity over direct target programming.",
            ]
            if en
            else [
                "Дано: известный нижний уровень (target)",
                "ISA / AscendC / LLVM/MLIR / другой язык /",
                "runtime API / набор контроллеров / hardware blocks",
                "",
                "Автоматически индуцировать и эволюционно развивать",
                "программную модель M, включающую:",
                "примитивы, комбинаторы, типы, контракты,",
                "семантику ресурсов/эффектов, правила lowering,",
                "верификаторы, примеры, документацию, cost model.",
                "",
                "M принимается, только если улучшает синтез,",
                "оптимизацию, верификацию, интерпретируемость",
                "или производительность.",
            ]
        ),
        13 if en else 14,
        "#111",
        500,
        "middle",
        19 if en else 18,
    )
    dashed_link(s, "M 420 240 V 290 H 545", COLORS["blue2"], "arrow-blue")
    dashed_link(s, "M 1110 240 V 289 H 945", COLORS["blue2"], "arrow-blue")
    dashed_link(s, "M 315 270 H 374 V 380 H 545", COLORS["blue2"], "arrow-blue")
    dashed_link(s, "M 1178 347 H 1100 V 396 H 945", COLORS["blue2"], "arrow-blue")

    panel(s, 394, 585, 674, 130, "Feedback Sources (Evaluator Signals)" if en else "Источники обратной связи (Evaluator Signals)", COLORS["gray"], "#ffffff")
    feedback = [
        ("checklist", "Correctness"),
        ("clock", "Performance"),
        ("network", "Synthesis\ncomplexity"),
        ("spark", "Interpretability"),
        ("checklist", "Safety"),
        ("db", "Reuse\nfrequency"),
    ] if en else [
        ("checklist", "Корректность"),
        ("clock", "Производительность"),
        ("network", "Сложность\nсинтеза"),
        ("spark", "Интерпретируемость"),
        ("checklist", "Безопасность"),
        ("db", "Повторное\nиспользование"),
    ]
    mini_flow(s, 420, 617, 620, feedback, COLORS["gray"])
    dashed_link(s, "M 632 552 V 585", COLORS["blue2"], "arrow-blue")
    dashed_link(s, "M 739 552 V 585", COLORS["blue2"], "arrow-blue")
    dashed_link(s, "M 843 552 V 585", COLORS["blue2"], "arrow-blue")

    panel(s, 29, 432, 337, 303, "4. Skill Libraries above APIs / Controllers" if en else "4. Библиотеки навыков поверх API/контроллеров", COLORS["orange"], COLORS["soft_orange"])
    skill = [
        ("SayCan", "connects LLM semantics with low-level robot skills"),
        ("Code as Policies", "LLM generates code policies over API primitives"),
        ("ProgPrompt", "structured prompts with available actions"),
        ("Language to Rewards", "LLM maps instructions to reward functions"),
        ("Eureka", "evolutionary reward-program search"),
        ("Voyager", "growing skill library and autocurriculum"),
        ("LRLL / HASP / CODESKILL", "self-evolving libraries over agent and coder skills"),
    ] if en else [
        ("SayCan", "соединение LLM-семантики с низкоуровневыми навыками"),
        ("Code as Policies", "LLM генерирует код-политики поверх API примитивов"),
        ("ProgPrompt", "структурированные промпты с доступными действиями"),
        ("Language to Rewards", "промежуточный интерфейс через reward-функции"),
        ("Eureka", "эволюционный поиск reward-программ для RL-политик"),
        ("Voyager", "непрерывно растущая библиотека навыков"),
        ("LRLL / HASP / CODESKILL", "самоэволюционирующие базы навыков агентов и кодеров"),
    ]
    row_cards(s, 44, 471, 311, skill, COLORS["orange"], "#fffaf1", 37, 28, 49)

    panel(s, 1084, 440, 352, 304, "5. Compiler and IR Platforms\nfor New Models" if en else "5. Компиляторные и IR-платформы\nдля новых моделей", COLORS["purple"], COLORS["soft_purple"])
    comp = [
        ("MLIR", "dialects, multi-level abstractions, progressive lowering"),
        ("Composable MLIR", "modular code generation and structured lowering"),
        ("MimiR", "extensible type-safe IR, typed axioms"),
        ("The Co-Compiler", "relational compilation from raw code to DSL"),
        ("SNN-MLIR", "domain dialect and bridge to bare-metal C"),
        ("AscendCraft", "Ascend-specific DSL semantics and lowering"),
        ("AscendOptimizer", "evolutionary AscendC optimization and motif bank"),
    ] if en else [
        ("MLIR", "диалекты, многоуровневые абстракции, progressive lowering"),
        ("Composable MLIR", "модульная генерация кода и структурированный lowering"),
        ("MimiR", "расширяемый, типобезопасный IR, типизированные аксиомы"),
        ("The Co-Compiler", "lifting низкоуровневого кода в DSL"),
        ("SNN-MLIR", "домен-специфичный диалект и мост к bare-metal C"),
        ("AscendCraft", "DSL для Ascend-специфичной семантики и lowering"),
        ("AscendOptimizer", "эволюционная оптимизация AscendC и банк мотивов"),
    ]
    row_cards(s, 1094, 479, 331, comp, COLORS["purple"], "#fbf7ff", 37, 28, 50)

    panel(s, 32, 744, 491, 168, "3. Evolutionary Program Discovery" if en else "3. Эволюционный поиск программ и алгоритмов с LLM", "#c78a00", "#fff9db")
    evo = [
        ("Evolution through Large Models", "LLM as a genetic-programming operator"),
        ("Evolving Code with LLM", "LLM-based genetic programming"),
        ("FunSearch", "search for programs that generate solutions"),
        ("STOP", "self-taught optimizer optimizing LLM scaffolds"),
        ("LLaMEA / LLM as Evolutionary Optimizer", "LLM generates metaheuristics and algorithms"),
        ("AlphaEvolve / CodeEvolve", "scalable code evolution with evaluator feedback"),
    ] if en else [
        ("Evolution through Large Models", "LLM как оператор мутации в генетическом программировании"),
        ("Evolving Code with LLM", "LLM-based genetic programming для эволюции кода"),
        ("FunSearch", "поиск не решений, а программ, генерирующих решения"),
        ("STOP", "самоулучшающийся scaffolding, вызывающий LLM"),
        ("LLaMEA / LLM as Evolutionary Optimizer", "LLM генерирует новые метаэвристики и алгоритмы"),
        ("AlphaEvolve / CodeEvolve", "масштабируемая эволюция кода с evaluator feedback"),
    ]
    for i, (name, desc) in enumerate(evo):
        col = i % 2
        row = i // 2
        bx = 43 + col * 242
        by = 781 + row * 38
        s.rect(bx, by, 232, 34, "#fffef4", "#e8d172", 0.8, 3)
        s.text(bx + 6, by + 11, name, 7.9, "#111", 900)
        s.wrapped(bx + 6, by + 24, desc, 39, 6.5, "#111", leading=7.5)

    panel(s, 544, 742, 306, 154, "6. Search at ISA / Hardware Level" if en else "6. Поиск на уровне ISA / аппаратуры", "#dd3f3f", "#fff1f1")
    isa = [
        ("STOKE", "stochastic superoptimization of instruction sequences"),
        ("AlphaDev", "discovers new algorithms at assembly/IR level"),
        ("AlphaTensor", "search for matrix multiplication algorithms"),
        ("ARISE", "automatic extension generation for RISC-V"),
        ("EDA-aware LLM", "Verilog/RTL/EDA artifact verification"),
    ] if en else [
        ("STOKE", "стохастическая супероптимизация инструкционных последовательностей"),
        ("AlphaDev", "обнаружение новых алгоритмов на уровне ассемблера / RL-игра"),
        ("AlphaTensor", "поиск новых алгоритмов умножения матриц"),
        ("ARISE", "автоматическая генерация расширений инструкций (RISC-V)"),
        ("EDA-aware LLM", "генерация и верификация RTL/EDA артефактов"),
    ]
    row_cards(s, 557, 779, 279, isa, "#dd3f3f", "#fff8f8", 24, 22, 51)

    panel(s, 893, 744, 356, 151, "7. Agentic System Design\nas Model Evolution" if en else "7. Автоматическое проектирование агентных систем", COLORS["teal"], COLORS["soft_teal"])
    agents = [
        ("ADAS", "search and compose new agents and composition methods"),
        ("GPTSwarm / Agents as Graphs", "optimize graphs of agents and prompts"),
        ("Memento-Skills", "agents design agents; growing skill library"),
        ("MaMa", "safe design of agentic systems"),
    ] if en else [
        ("ADAS", "поиск и создание новых агентов и способов их композиции"),
        ("GPTSwarm / Agents as Graphs", "оптимизация графов агентов и промптов"),
        ("Memento-Skills", "агенты проектируют агентов, растущая библиотека навыков"),
        ("MaMa", "безопасное проектирование агентных систем"),
    ]
    row_cards(s, 907, 781, 326, agents, COLORS["teal"], "#f4ffff", 27, 28, 52)

    s.rect(1289, 724, 220, 175, "#ffffff", "#9ba7b4", 1, 7)
    s.text(1307, 744, "Application to Ascend / AI accelerators" if en else "Приложение к Ascend/AI-ускорителям", 8.6, "#111", 900)
    bullets(
        s,
        1310,
        765,
        [
            "Corpus: AscendC kernels, host tiling, profiles, compilation errors",
            "Extract optimization motifs: double-buffering, pipeline overlap, core split, tiling, UB/L1/L0 reuse",
            "Form DSL/IR constructions for these motifs",
            "Lower to AscendC / GE",
            "Evolve and select by latency, bandwidth, UB usage",
        ]
        if en
        else [
            "Корпус AscendC ядер, host-tiling, профили, ошибки компиляции",
            "Извлечение мотивов оптимизаций: double-buffering, pipeline overlap, tiling, UB/L1 reuse",
            "Формирование DSL/IR конструкций для этих мотивов",
            "Lowering в AscendC / GE",
            "Эволюция и отбор по latency, bandwidth, UB usage",
        ],
        32,
        7.4,
        10,
        "•",
    )

    s.rect(1289, 904, 220, 104, "#ffffff", "#b7c0ca", 1, 6)
    s.text(1310, 923, "Legend" if en else "Условные обозначения", 8.8, "#111", 900)
    legend = [
        ("#eaf2ff", "1,2 - induction / DSL"),
        ("#fff9db", "3 - evolutionary search"),
        ("#fff5e6", "4 - API skills"),
        ("#f6efff", "5 - compilers / IR"),
        ("#fff1f1", "6 - ISA / hardware"),
        ("#eaf9fa", "7 - agent systems"),
    ] if en else [
        ("#eaf2ff", "1,2 - Индукция / DSL"),
        ("#fff9db", "3 - Эволюционный поиск"),
        ("#fff5e6", "4 - Навыки и API"),
        ("#f6efff", "5 - Компиляторы и IR"),
        ("#fff1f1", "6 - ISA/Аппаратура"),
        ("#eaf9fa", "7 - Агентные системы"),
    ]
    yy = 939
    for color, label in legend:
        s.rect(1310, yy - 8, 15, 8, color, "#888", 0.7, 2)
        s.text(1332, yy, label, 7.2, "#111", 400)
        yy += 11

    s.rect(30, 941, 1186, 72, "#ffffff", "#ced6df", 1, 7)
    s.text(624, 958, "Key ideas connecting the directions" if en else "Ключевые идеи, объединяющие направления", 10, "#111", 900, "middle")
    keys = [
        ("db", "Low-level target is known; it is the anchor for induction."),
        ("clock", "Find repeated motifs and patterns in code/traces."),
        ("spark", "Propose abstractions and validate by metrics."),
        ("network", "Map useful abstractions to first-class model primitives."),
        ("checklist", "Provide correct lowering, verification, docs, and tooling."),
        ("gear", "Evolve the model by safety, clarity, productivity, and performance."),
    ] if en else [
        ("db", "Нижний target известен; это якорь для индукции."),
        ("clock", "Ищем повторяющиеся паттерны в коде и трассах."),
        ("spark", "Предлагаем кандидаты абстракций и проверяем по метрикам."),
        ("network", "Превращаем полезные абстракции в first-class элементы модели."),
        ("checklist", "Обеспечиваем корректный lowering, верификацию и инструменты."),
        ("gear", "Эволюционно расширяем модель по безопасности и производительности."),
    ]
    for i, (kind, text) in enumerate(keys):
        ix = 50 + i * 191
        mini_icon(s, ix, 970, kind, COLORS["gray"], 25)
        s.wrapped(ix + 30, 970, text, 26, 7.4, "#111", leading=9)

    write(f"02-bottom-up-programming-model-induction-map.{lang}.svg", s)


def render_03(lang: str) -> None:
    en = lang == "en"
    s = begin_svg()
    title(
        s,
        "Automatic Discovery of an Algebraic Programming Model (CuTe DSL Level) with LLMs" if en else "Автоматическое нахождение алгебраической программной модели (CuTe DSL уровня) с помощью LLM",
        "Goal: from a known low-level target infer domain algebra: objects, operations, laws, normal forms, verifiers, cost semantics, and lowering rules." if en else "Цель: по известному нижнему target (ISA / AscendC / MLIR / контроллеры) автоматически индуцировать предметную алгебру: объекты, операции, законы, нормальные формы, верификаторы, семантику стоимости и правила lowering.",
        25 if en else 27,
    )

    panel(s, 16, 88, 316, 469, "1. Desired CuTe-DSL-Level Result" if en else "1. Что мы хотим получить (результат уровня CuTe DSL)", COLORS["blue"], COLORS["soft_blue"])
    desired = [
        ("cube", "Objects", "Shape, Layout, Tensor, Tile, ThreadLayout, MemorySpace, PipelineStage, Buffer, Event ..."),
        ("gear", "Operations", "compose, product, tile, split_axis, coalesce, inverse, partition, overlap, double_buffer ..."),
        ("spark", "Laws", "associativity, identities, invertibility, coverage, stage independence, resource limits ..."),
        ("doc", "Normal Forms", "canonical representations for layout, pipeline, schedule, expressions"),
        ("checklist", "Verifiers", "tensor coverage, no conflicts, capacity, alignment, dependencies, lifetime, safety"),
        ("clock", "Cost Model", "bytes, cycles, bandwidth, stalls, occupancy, bank conflicts, energy"),
        ("code", "Lowering Rules", "algebraic expression -> target code (AscendC / CUDA / MLIR / ISA / API)"),
    ] if en else [
        ("cube", "Объекты", "Shape, Layout, Tensor, Tile, ThreadLayout, MemorySpace, PipelineStage, Buffer, Event ..."),
        ("gear", "Операции", "compose, product, tile, split_axis, coalesce, inverse, complement, partition, overlap, double_buffer ..."),
        ("spark", "Законы", "ассоциативность, тождества, обратимость, совместимость, сохранение покрытия, независимость стадий ..."),
        ("doc", "Нормальные формы", "канонические представления для layout, pipeline, schedule, выражений"),
        ("checklist", "Верификаторы", "покрытие тензора, отсутствие конфликтов, ёмкость UB, выравнивание, зависимости, безопасность"),
        ("clock", "Cost модель", "байты, циклы, bandwidth, stalls, occupancy, банк-конфликты, энергия"),
        ("code", "Lowering правила", "алгебраическое выражение -> target код (AscendC / CUDA / MLIR / ISA / API ...)"),
    ]
    yy = 130
    for kind, name, desc in desired:
        mini_icon(s, 30, yy - 3, kind, COLORS["gray"], 29)
        s.text(68, yy + 7, name, 9.8, COLORS["blue"], 900)
        s.wrapped(68, yy + 22, desc, 42, 8.0, "#111", leading=10)
        yy += 61
        s.line(16, yy - 14, 332, yy - 14, "#cbdcf2", 0.8)

    panel(s, 344, 88, 883, 313, "2. Pipeline for Automatic Algebraic Model Discovery" if en else "2. Пайплайн автоматического открытия алгебраической модели", COLORS["blue"], "#ffffff")
    pipe = [
        ("db", "Data\ncollection"),
        ("clock", "Semantic\nextraction"),
        ("cube", "Lift and\nrepresent"),
        ("network", "Structure\nsearch"),
        ("spark", "Abstraction\ncandidates"),
        ("spark", "Law\ncandidates"),
        ("checklist", "Check and\nvalidate"),
        ("gear", "Integrate\nmodel"),
    ] if en else [
        ("db", "Сбор\nданных"),
        ("clock", "Извлечение\nсемантики"),
        ("cube", "Lift и\nпредставление"),
        ("network", "Поиск\nструктур"),
        ("spark", "Кандидаты\nабстракций"),
        ("spark", "Кандидаты\nзаконов"),
        ("checklist", "Проверка и\nвалидация"),
        ("gear", "Интеграция\nв модель"),
    ]
    mini_flow(s, 360, 145, 840, pipe, COLORS["gray"])
    stage_bullets = [
        ["program corpus", "tests/specs", "profiles/traces", "compiler logs"],
        ["IR/graph construction", "tensor forms", "indices, memory", "dependencies"],
        ["raw IR lift", "syntactic structure", "intermediate objects"],
        ["recurring motifs", "anti-unification", "clustering"],
        ["objects", "operations", "names", "signatures", "examples"],
        ["candidate laws", "rewrite rules", "preconditions", "constraints"],
        ["property tests", "SMT/Solver", "corpus checks", "profiling feedback"],
        ["new constructs", "rule updates", "canonicalization", "LLM docs"],
    ] if en else [
        ["корпус программ", "тесты и спецификации", "профайлер/трассы", "компиляторные логи"],
        ["построение IR/графов", "тензорные формы", "индексация, layout", "зависимости, ресурсы"],
        ["подъём raw IR", "выделение паттернов", "структуры", "семантика"],
        ["повторяющиеся мотивы", "anti-unification", "кластеризация"],
        ["объекты", "операции", "названия", "сигнатуры", "примеры"],
        ["кандидатные законы", "правила переписывания", "предусловия", "ограничения"],
        ["property-based тесты", "SMT/Solver", "проверка на корпусе", "обратная связь"],
        ["конструкции", "обновление правил", "cost model", "документация"],
    ]
    for i, lines in enumerate(stage_bullets):
        bx = 360 + i * 105
        bullets(s, bx, 216, lines, 20, 6.8, 10, "•")
    s.path("M 422 321 V 346 H 1144 V 321", COLORS["blue"], 1.4, marker="arrow-blue")
    s.text(786, 376, "Evolution loop: new data -> new candidates -> checking -> model improvement" if en else "Эволюционный цикл: новые данные -> новые кандидаты -> проверка -> улучшение модели", 10.5, COLORS["blue"], 900, "middle")

    panel(s, 1240, 88, 280, 423, "3. Roles and Tools" if en else "3. Роли и инструменты", COLORS["green"], COLORS["soft_green"])
    roles = [
        ("robot", "LLM", "suggests entities and operations, laws, examples, docs, lowering templates"),
        ("clock", "Analyzers / solvers", "static analysis, dataflow/dependence, SMT, symbolic execution, property checks"),
        ("network", "e-graph + rewrite engine", "equivalence representation, equality saturation, low-cost forms"),
        ("code", "Compiler / lowering backend", "lowering to AscendC / CUDA / MLIR / ISA / API and checks"),
        ("db", "Experience memory", "accepted constructs and laws, examples, performance effects"),
    ] if en else [
        ("robot", "LLM", "предлагает новые сущности и операции, генерирует законы, примеры, документацию"),
        ("clock", "Анализаторы и решатели", "статический анализ, dataflow, зависимости, SMT, символьное выполнение"),
        ("network", "e-graph + rewrite движок", "представление эквивалентных выражений, equality saturation"),
        ("code", "Компилятор / Lowering бэкенд", "lowering в AscendC / CUDA / MLIR / ISA / API, проверка корректности"),
        ("db", "База опыта", "принятые конструкции и законы, примеры использования, эффекты"),
    ]
    yy = 135
    for kind, name, desc in roles:
        mini_icon(s, 1254, yy - 2, kind, COLORS["gray"], 34)
        s.text(1295, yy + 10, name, 9.8, COLORS["green"], 900)
        s.wrapped(1295, yy + 27, desc, 34, 8.0, "#111", leading=10.5)
        yy += 78
        s.line(1240, yy - 12, 1520, yy - 12, "#b6dfbd", 0.8)

    panel(s, 344, 421, 883, 209, "4. Algebras to Induce Automatically (Ascend Example)" if en else "4. Алгебры, которые мы хотим автоматически индуцировать (пример для Ascend)", COLORS["purple"], COLORS["soft_purple"])
    algebras = [
        ("Layout algebra", ["objects: Shape, Layout, Axis", "operations: compose, product, tile", "laws: associativity, identities"]),
        ("Type / partition algebra", ["objects: Tile, CorePartition", "operations: split, axis, core_split", "laws: coverage, size compatibility"]),
        ("Data movement algebra", ["objects: MemorySpace, Buffer", "operations: promote, copy, tile", "laws: data preservation, capacity"]),
        ("Pipeline algebra", ["objects: Stage, Iteration", "operations: sequence, overlap, buffer", "laws: stage independence"]),
        ("Queue / event algebra", ["objects: Queue, Event, Token", "operations: enqueue, wait, signal", "laws: event ordering, no deadlock"]),
        ("Effect / resource algebra", ["objects: Resource, Effect, LifetimeRegion", "operations: allocate, reuse, release", "laws: lifetime and safety"]),
    ] if en else [
        ("Алгебра layout'ов", ["объекты: Shape, Layout, Axis", "операции: compose, product, tile", "законы: ассоциативность, обратимость"]),
        ("Алгебра типа/разбиения", ["объекты: Tile, CorePartition", "операции: split, axis, core_split", "законы: покрытие, совместимость"]),
        ("Алгебра движения данных", ["объекты: MemorySpace, Buffer", "операции: promote, copy, tile", "законы: сохранение данных, capacity"]),
        ("Алгебра pipeline", ["объекты: Stage, Iteration", "операции: sequence, overlap, buffer", "законы: независимость стадий"]),
        ("Алгебра очередей и событий", ["объекты: Queue, Event, Token", "операции: enqueue, dequeue, wait", "законы: порядок событий"]),
        ("Алгебра эффектов и ресурсов", ["объекты: Resource, Effect", "операции: allocate, reuse, release", "законы: lifetime, безопасность"]),
    ]
    col_w = 147
    for i, (head, items) in enumerate(algebras):
        bx = 346 + i * col_w
        s.rect(bx, 444, col_w, 185, "#fffaff", "#cdb7ec", 0.8, 0)
        s.text(bx + col_w / 2, 462, head, 7.5, "#281071", 900, "middle")
        mini_icon(s, bx + 48, 482, ["doc", "checklist", "network", "code", "gear", "clock"][i], COLORS["blue"], 52)
        bullets(s, bx + 10, 546, items, 28, 6.7, 10, "•")

    panel(s, 16, 640, 387, 230, "5. Law and Equivalence Search" if en else "5. Поиск законов и эквивалентностей", COLORS["orange"], COLORS["soft_orange"])
    s.rect(25, 675, 135, 50, "#fffaf1", COLORS["orange"], 0.8, 5)
    s.text(92, 697, "Law candidate" if en else "Кандидат закона", 8.6, "#111", 900, "middle")
    s.text(92, 714, "compose(id, L) = L", 8, "#111", 700, "middle")
    s.line(92, 729, 92, 759, COLORS["gray"], 2, marker="arrow-gray")
    s.rect(35, 765, 92, 66, "#f8fbff", "#a9c4e8", 0.9, 5)
    s.text(81, 781, "Check" if en else "Проверка", 8, "#111", 900, "middle")
    s.text(66, 812, "✓", 24, COLORS["green"], 900, "middle")
    s.text(105, 812, "×", 22, "#b00020", 900, "middle")
    s.text(253, 684, "Rewrite-rule examples" if en else "Примеры правил переписывания", 8.8, COLORS["blue"], 900, "middle")
    examples = ["compose(A, compose(B, C)) -> compose(compose(A, B), C)", "product(A, product(B, C)) -> product(product(A, B), C)", "coalesce(product(A, B)) -> ...", "inverse(compose(A, B)) -> compose(inverse(B), inverse(A))"]
    bullets(s, 169, 708, examples, 47, 7.2, 12, "•")
    s.rect(31, 840, 361, 22, "#fffdf7", COLORS["orange"], 0.8, 4)
    s.text(211, 855, "E-graph + Equality Saturation -> many equivalent forms" if en else "E-graph (egg) + Equality Saturation -> множество эквивалентных форм", 8, "#111", 700, "middle")

    panel(s, 417, 641, 718, 247, "6. Example: Algebraic Expression -> Lowering to AscendC" if en else "6. Пример: выражение в алгебре -> lowering в AscendC", COLORS["blue"], "#f8fbff")
    s.rect(426, 679, 165, 202, "#ffffff", "#c5d5eb", 0.8, 4)
    s.text(508, 681, "Algebraic expression" if en else "Алгебраическое выражение", 8.1, COLORS["blue"], 900, "middle")
    expr = ["pipeline = double_buffer(", "  sequence(", "    copy(GM[A] -> UB[A_tile]),", "    compute(vector_add,", "      UB[A_tile], UB[B_tile]),", "    copy(UB[C_tile] -> GM[C])", "  )", ")", "", "schedule = core_partition(N, K)", "  ∘ tile(M, T)", "  ∘ guard_tail(pred)"]
    s.text_lines(434, 704, expr, 7.4, "#111", 700, "start", 13)
    s.rect(616, 692, 164, 121, "#ffffff", "#c5d5eb", 0.8, 4)
    s.text(698, 679, "Checks" if en else "Проверки", 8.1, COLORS["blue"], 900, "middle")
    bullets(s, 633, 710, ["types and shapes agree", "tensor covered exactly", "UB capacity satisfied", "alignment OK", "dependencies preserved", "overlap legal", "no resource conflict"] if en else ["типы и формы согласованы", "покрытие тензора полное", "ёмкость UB удовлетворена", "выравнивание OK", "зависимости соблюдены", "overlap допустим", "нет конфликта ресурсов"], 30, 7.4, 12, "☑", COLORS["ink"])
    s.rect(621, 819, 154, 59, "#ffffff", "#c5d5eb", 0.8, 4)
    s.text(698, 837, "Cost model" if en else "Cost модель", 8.4, COLORS["blue"], 900, "middle")
    bullets(s, 643, 854, ["score: bandwidth-bound", "roofline: 78% peak", "bottleneck: CopyIn"] if en else ["оценка: BW-bound", "roofline: 78% от пика", "стадия bottleneck: CopyIn"], 25, 7.2, 10, "•")
    s.rect(792, 692, 334, 187, "#ffffff", "#c5d5eb", 0.8, 4)
    s.text(959, 679, "Generated AscendC fragment" if en else "Сгенерированный AscendC фрагмент", 8.1, COLORS["blue"], 900, "middle")
    code = [
        "for (int core = 0; core < K; ++core) {",
        "  for (int m = 0; m < M; m += T) {",
        "    // double buffering",
        "    int buf = m / T % 2;",
        "    DataCopy(GM, UB_A[buf], A[core, m], tile_MN);",
        "    DataCopy(GM, UB_B[buf], B[core, m], tile_MN);",
        "    VecAdd(UB_C[buf], UB_A[buf], UB_B[buf], tile_MN);",
        "    DataCopy(UB_C[buf], GM, C[core, m], tile_MN);",
        "    PipeBarrier();",
        "  }",
        "}",
        "// TQue/TPipe, events, tail handling ...",
    ]
    s.text_lines(804, 711, code, 7.7, "#111", 700, "start", 12)
    s.line(591, 779, 613, 779, COLORS["blue"], 2, marker="arrow-blue")
    s.line(780, 779, 790, 779, COLORS["blue"], 2, marker="arrow-blue")

    panel(s, 1151, 640, 367, 200, "7. Acceptance Criteria for a New Construct" if en else "7. Критерии принятия новой конструкции", "#c78a00", "#fff9db")
    bullets(s, 1166, 680, ["correctness is preserved", "compiles and passes tests", "improves performance or search quality", "reduces program/search complexity", "has useful laws and normal forms", "is explainable and documented", "has clear lowering rules", "does not violate resources or safety"] if en else ["корректность сохранена", "компилируется и проходит тесты", "улучшает производительность", "снижает сложность программ / поиска", "имеет полезные законы и нормальные формы", "хорошо объяснима и документируется", "имеет ясные правила lowering", "не нарушает ресурсы и безопасность"], 55, 8.5, 15, "☑", COLORS["ink"])

    s.rect(16, 912, 786, 66, "#ffffff", "#cfd7e2", 1, 7)
    s.text(407, 930, "8. Main Model Evolution Loop" if en else "8. Главный цикл эволюции модели", 10, COLORS["blue"], 900, "middle")
    mini_flow(s, 34, 944, 740, [("db", "New programs\nand data"), ("network", "New patterns\nand motifs"), ("cube", "New\nabstractions"), ("spark", "New laws\nand rules"), ("code", "New DSL /\nalgebra"), ("clock", "Better synthesis\nand optimization"), ("gear", "New data\nfeedback loop")] if en else [("db", "Новые программы\nи данные"), ("network", "Новые паттерны\nи мотивы"), ("cube", "Новые\nабстракции"), ("spark", "Новые законы\nи правила"), ("code", "Новый DSL /\nалгебра"), ("clock", "Лучший синтез\nи оптимизация"), ("gear", "Новые данные\nfeedback loop")], COLORS["gray"])

    panel(s, 821, 897, 352, 84, "9. Links to Existing Work" if en else "9. Связь с существующими работами", COLORS["purple"], COLORS["soft_purple"])
    bullets(s, 837, 927, ["CuTe: layout algebra for CUDA", "Categorical / algebraic DSL foundations", "Tiramisu / Halide: algorithm-schedule separation", "LILO / Stitch / Babble: library learning", "e-graphs: equivalence and normal forms", "AscendCraft / AscendOptimizer: Ascend motivation"] if en else ["CuTe: пример зрелой layout-алгебры для CUDA", "Категориальные основы CuTe", "Tiramisu / Halide: разделение алгоритма и расписания", "LILO / Stitch / Babble: обучение абстракций", "e-graphs: равенства, нормализация", "AscendCraft / AscendOptimizer: мотивация для Ascend"], 58, 7.2, 9.5, "•")

    panel(s, 1192, 893, 326, 93, "10. Key Idea" if en else "10. Ключевая идея", COLORS["blue"], COLORS["soft_blue"])
    s.text_lines(
        1355,
        925,
        (
            [
                "We do not ask the LLM to invent a DSL.",
                "We automatically discover an algebraic structure",
                "that better reflects the domain and target,",
                "and make it a tool for synthesis, optimization,",
                "verification, and high-performance code generation.",
            ]
            if en
            else [
                "Мы не просим LLM «придумай DSL».",
                "Мы автоматически открываем алгебраическую структуру,",
                "которая лучше отражает предметную область и target,",
                "и делаем её инструментом для синтеза, оптимизации,",
                "верификации и генерации высокоэффективного кода.",
            ]
        ),
        9.2,
        COLORS["ink"],
        800,
        "middle",
        13,
    )

    write(f"03-algebraic-programming-model-cute-dsl-level.{lang}.svg", s)


def main() -> None:
    render_01_en()
    render_02("ru")
    render_02("en")
    render_03("ru")
    render_03("en")


if __name__ == "__main__":
    main()
