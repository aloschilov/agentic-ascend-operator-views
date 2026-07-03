---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Инструменты компилятора и анализ программ для AI-агентной оптимизации операторов AscendC: обзор"
description: "Обзорная презентация по библиографии репозитория: работы по Ascend/NPU, агентная оптимизация ядер, compiler IR и autotuning, основы анализа программ, сведенные к compiler-derived operator views."
---

<style>
section {
  padding: 42px 48px;
  font-size: 26px;
}

h1 {
  font-size: 1.58em;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
}

h2 {
  font-size: 1.02em;
  margin: 0 0 11px 0;
}

h3 {
  font-size: 0.78em;
  margin: 0 0 8px 0;
}

p,
li {
  font-size: 0.72em;
  line-height: 1.34;
}

table {
  width: 100%;
  font-size: 0.5em;
  margin: 8px 0;
}

th,
td {
  padding: 6px 8px;
}

code {
  font-size: 0.88em;
}

pre {
  font-size: 0.54em;
  line-height: 1.24;
}

.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lead h1 {
  font-size: 1.7em;
  max-width: 1040px;
}

.subtitle {
  color: var(--light-text);
  font-size: 0.92em;
  line-height: 1.35;
  margin: 0 0 24px 0;
  max-width: 1020px;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.metric {
  border: 1px solid var(--border);
  border-radius: 4px;
  min-height: 104px;
  padding: 14px 14px 12px 14px;
}

.metric strong {
  color: var(--primary);
  display: block;
  font-size: 1.24em;
  line-height: 1.05;
  margin-bottom: 8px;
}

.metric span {
  color: var(--light-text);
  display: block;
  font-size: 0.56em;
  line-height: 1.28;
}

.two-col {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.three-col {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 13px;
}

.four-col {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 11px;
}

.box {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 13px 15px;
  overflow: hidden;
}

.box h3 {
  line-height: 1.18;
}

.box p,
.box li {
  font-size: 0.6em;
  line-height: 1.32;
}

.box ul {
  margin: 0;
  padding-left: 18px;
}

.callout {
  border-left: 5px solid var(--accent3);
  background: rgba(237, 109, 0, 0.08);
  padding: 12px 16px;
  margin-top: 12px;
}

.callout p {
  margin: 0;
}

.source {
  position: absolute;
  left: 48px;
  bottom: 24px;
  right: 150px;
  color: var(--light-text);
  font-size: 0.46em;
  line-height: 1.35;
}

.small {
  color: var(--light-text);
  font-size: 0.56em;
  line-height: 1.28;
}

.pipeline {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
  align-items: stretch;
  margin-top: 18px;
}

.step {
  border: 1px solid var(--border);
  border-top: 5px solid var(--accent6);
  border-radius: 4px;
  min-height: 126px;
  padding: 12px;
}

.step strong {
  color: var(--primary);
  display: block;
  font-size: 0.75em;
  margin-bottom: 8px;
}

.step span {
  color: var(--light-text);
  display: block;
  font-size: 0.55em;
  line-height: 1.28;
}

.tag {
  display: inline-block;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--light-text);
  font-size: 0.46em;
  padding: 3px 6px;
  margin-right: 4px;
  margin-bottom: 5px;
}

.refs {
  columns: 2;
  column-gap: 28px;
}

.refs p {
  font-size: 0.5em;
  line-height: 1.3;
  margin: 0 0 6px 0;
  break-inside: avoid;
}
</style>

<!-- _class: lead -->

# Инструменты компилятора и анализ программ для AI-агентной оптимизации операторов AscendC

<p class="subtitle">Обзор по четырем кластерам литературы: работы по Ascend/NPU, агентная оптимизация ядер, compiler IR / scheduling / autotuning и основы анализа программ - со сведением к compiler-derived operator knowledge views.</p>

<div class="metric-row">
  <div class="metric"><strong>4 кластера</strong><span>Ascend, агенты, compiler IR, анализ</span></div>
  <div class="metric"><strong>~30 работ</strong><span>из библиографии репозитория и смежных ссылок</span></div>
  <div class="metric"><strong>1 вопрос</strong><span>как артефакты компилятора делают агентную настройку рабочей?</span></div>
  <div class="metric"><strong>1 разрыв</strong><span>нет единого AI-facing слоя views для AscendC</span></div>
</div>

---

# Охват и метод обзора

<div class="two-col">
  <div class="box">
    <h2>Ведущий вопрос</h2>
    <p>Как инструменты компилятора и артефакты анализа программ могут сделать AI-агентную оптимизацию ML-операторов эффективнее, особенно для операторов AscendC на Ascend NPU?</p>
    <p>Каждую работу читаем как ответ на вопрос: <em>что видит оптимизатор и как он принимает решение?</em></p>
  </div>
  <div class="box">
    <h2>Как организованы работы</h2>
    <ul>
      <li><strong>Кластер A - Ascend/NPU:</strong> целевой домен и его baselines.</li>
      <li><strong>Кластер B - агентная оптимизация:</strong> бенчмарки, агенты, RL-интернализация.</li>
      <li><strong>Кластер C - compiler IR / autotuning:</strong> представления и поиск.</li>
      <li><strong>Кластер D - анализ программ:</strong> классические основы для переиспользования.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Сквозные оси через весь обзор: <strong>какая обратная связь открыта</strong> (код / ошибки / профилирование / structured views), <strong>как приобретается знание</strong> (pretraining, поиск, RL, эпизодический опыт) и <strong>как гарантируется корректность</strong>.</p>
</div>

<p class="source">Источники: README.md, docs/problem-statement.md, bibliography/reading-list.md, notes/01-05.</p>

---

# Таксономия области

<div class="pipeline">
  <div class="step"><strong>Семантика</strong><span>StableHLO, MLIR: что вычисляет оператор, dtype/layout/tolerance</span></div>
  <div class="step"><strong>Schedule / IR</strong><span>Halide, TVM, TensorIR, Tiramisu, Exo, Triton, SDFG: как раскладывается</span></div>
  <div class="step"><strong>Анализ</strong><span>data-flow, dependence/PDG, abstract interpretation, ProGraML</span></div>
  <div class="step"><strong>Agent loop</strong><span>KernelBench, Geak, CompilerGPT, AscendOptimizer: диагностика, правка, проверка</span></div>
  <div class="step"><strong>Обратная связь железа</strong><span>roofline, NPUMeter, profiler-in-the-loop поиск</span></div>
</div>

<div class="callout">
  <p>Каждая рассмотренная система стоит где-то на этом стеке. Повторяющаяся слабость: слои изучаются изолированно, а для AscendC агент по-прежнему потребляет в основном сырой код плюс логи.</p>
</div>

---

# Мотивирующее свидетельство: разрыв в знаниях AscendC

<div class="two-col">
  <div class="box">
    <h2>Одношаговая генерация проваливается на AscendC</h2>
    <table>
      <thead><tr><th>Модель</th><th>CUDA Pass@1</th><th>AscendC Pass@1</th></tr></thead>
      <tbody>
        <tr><td>DeepSeek-R1</td><td>52.6%</td><td>1.4%</td></tr>
        <tr><td>Claude-Sonnet-4</td><td>47.0%</td><td>2.1%</td></tr>
        <tr><td>Qwen3-235B (think)</td><td>44.2%</td><td>0.7%</td></tr>
      </tbody>
    </table>
    <p>MultiKernelBench Pass@1: модели, сильные на CUDA, почти проваливаются на AscendC.</p>
  </div>
  <div class="box">
    <h2>Две структурные причины</h2>
    <ul>
      <li><strong>Дефицит данных:</strong> мало открытых ядер/идиом AscendC против зрелой экосистемы CUDA/Triton.</li>
      <li><strong>Связанный артефакт:</strong> host tiling program + device kernel program, с явной иерархией UB/L1/L0.</li>
      <li>Обратная связь компилятора/профайлера показывает симптомы, а не легальное структурное переписывание.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Именно этот разрыв - причина существования обзора: pretraining reuse, движок CUDA-агентов, почти не переносится, поэтому нужны другие источники знаний.</p>
</div>

<p class="source">MultiKernelBench (arXiv:2507.17773); числа по AscendOptimizer (arXiv:2603.23566), таблица 1.</p>

---

# Кластер A - работы по Ascend / NPU

<table>
  <thead>
    <tr><th>Работа</th><th>Роль</th><th>Ключевой вклад для темы</th></tr>
  </thead>
  <tbody>
    <tr><td>AscendOptimizer (2026)</td><td>ближайший baseline</td><td>агент с эпизодическим опытом; Optimization Rewind; two-stage host/kernel; training-free</td></tr>
    <tr><td>AscendCraft (2026)</td><td>программная модель</td><td>DSL-guided транскомпиляция в AscendC; делает execution semantics явными</td></tr>
    <tr><td>AscendKernelGen (2026)</td><td>диагностика</td><td>систематическое исследование: общие LLM слабы на NPU-ядрах без доменной адаптации</td></tr>
    <tr><td>MultiKernelBench (2025)</td><td>бенчмарк</td><td>мультиплатформенный (GPU/NPU/TPU) бенчмарк генерации; измеряет разрыв</td></tr>
    <tr><td>Squeezing Operator Perf., ASPLOS'25</td><td>модель производительности</td><td>component-based roofline и классификация узких мест для операторов Ascend</td></tr>
    <tr><td>NPUMeter (2026)</td><td>модель производительности</td><td>аналитические модели производительности для автоматической оптимизации на Ascend</td></tr>
  </tbody>
</table>

<div class="callout">
  <p>Вместе они показывают домен с трех сторон: <strong>генерация</strong> (Craft, KernelGen), <strong>оптимизация</strong> (AscendOptimizer) и <strong>измерение/моделирование</strong> (roofline, NPUMeter, MultiKernelBench).</p>
</div>

<p class="source">arXiv:2603.23566, 2601.22760, 2601.07160, 2507.17773; DOI 10.1145/3676641.3716243, 10.1145/3820380. См. notes/01-ascend-npu.md.</p>

---

# Детальный разбор - AscendOptimizer, ближайший baseline

<div class="two-col">
  <div class="box">
    <h2>Механизм</h2>
    <ul>
      <li><strong>Optimization Rewind:</strong> контролируемо деоптимизировать сильные ядра; оставить мотивы, чье удаление измеримо замедляет железо, как переиспользуемый опыт.</li>
      <li><strong>Стадия I:</strong> retrieval-guided переписывание ядра из общего банка опыта.</li>
      <li><strong>Стадия II:</strong> эволюционный поиск тайлинга с железом в контуре.</li>
      <li>Training-free; опыт живет вне весов модели.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Результаты (101 реальный оператор AscendC)</h2>
    <ul>
      <li>1.21x геомеан над baseline cann-ops; 53.47% обогнали эталон.</li>
      <li>Level-3 GM 1.89 против 1.38 BoN / 1.45 OpenEvolve.</li>
      <li>Абляция: опыт поднимает GM с 1.09 до 1.16; только tiling лишь 1.02.</li>
      <li>Ascend 910B2, CANN 8.3, 230 аппаратных оценок на оператор.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Вывод для обзора: эпизодический опыт работает, но хранится как свободные записи. Он <em>еще не</em> привязан к compiler-derived структурным views - именно на это нацелен этот репозиторий.</p>
</div>

<p class="source">AscendOptimizer (arXiv:2603.23566), таблицы 1-3, рисунки 1, 3, 6.</p>

---

# Кластер B - агентная оптимизация ядер (1/2)

<div class="two-col">
  <div class="box">
    <h2>Бенчмарки и метрики</h2>
    <ul>
      <li><strong>KernelBench:</strong> "могут ли LLM писать быстрые GPU-ядра?"; вводит семейство метрик fast_p.</li>
      <li><strong>TritonBench:</strong> генерация операторов Triton; даже дружелюбный DSL труден, когда важна производительность.</li>
      <li><strong>MultiKernelBench:</strong> кросс-платформенный охват GPU/NPU/TPU.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Агенты и мосты от компилятора</h2>
    <ul>
      <li><strong>Geak:</strong> агентный feedback loop для AMD Triton ядер.</li>
      <li><strong>CompilerGPT:</strong> подает compiler optimization reports в LLM - ближайший аналог compiler-to-AI views.</li>
      <li><strong>Обзор Code Optimization:</strong> широкая рамка вызовов LLM-for-code-optimization.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Общий паттерн: итерации с обратной связью выполнения бьют one-shot prompting. Общий предел: интерфейс - это по-прежнему код + ошибки + текст профайлера, а не структурированный legal-action space.</p>
</div>

<p class="source">arXiv:2502.10517, 2502.14752, 2507.23194, 2506.06227, 2501.01277. См. notes/02-agentic-kernel-optimization.md.</p>

---

# Кластер B - агентная оптимизация ядер (2/2)

<div class="three-col">
  <div class="box">
    <h2>Мультиагентные и profiling-guided</h2>
    <ul>
      <li>Astra - мультиагентная перф GPU-ядер</li>
      <li>PRAGMA - profiling-reasoned агенты</li>
      <li>CudaForge - агент с обратной связью железа</li>
      <li>TritonForge - profiling-guided Triton</li>
      <li>GPU Kernel Scientist; StitchCUDA</li>
    </ul>
  </div>
  <div class="box">
    <h2>Эволюционный поиск</h2>
    <ul>
      <li>KernelEvolve - агентные ядра в масштабе Meta</li>
      <li>EvoEngineer - эволюция CUDA-кода</li>
      <li>OpenEvolve - открытый эволюционный агент (baseline)</li>
    </ul>
  </div>
  <div class="box">
    <h2>RL / SFT интернализация</h2>
    <ul>
      <li>Kevin - multi-turn RL для CUDA</li>
      <li>CUDA-L1 / CUDA-L2 - контрастивный RL</li>
      <li>AutoTriton, TritonRL - RL для Triton</li>
      <li>Seed-Coder - self-curation данных</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Две философии приобретения: <strong>интернализовать в веса</strong> (RL/SFT, нужно много пар код-производительность) против <strong>вынести как опыт/поиск</strong> (training-free). NPU с дефицитом знаний тянут ко второму.</p>
</div>

<p class="source">Смежные ссылки из related work AscendOptimizer (arXiv:2509.07506, 2511.06345, 2511.01884, 2512.09196, 2506.20807, 2603.02637, 2512.23236, 2510.03760, 2507.11948, 2507.14111, 2512.02551, 2507.05687, 2510.17891, 2506.03524).</p>

---

# Кластер C - compiler IR, scheduling, autotuning

<div class="three-col">
  <div class="box">
    <h2>Разделение algorithm / schedule</h2>
    <ul>
      <li>Halide - отделить алгоритм от schedule</li>
      <li>Tiramisu - полиэдральный, слои + коммуникации</li>
      <li>Exo - user-schedulable ускорители</li>
      <li>Triton / TileLang - tile-centric модели</li>
    </ul>
  </div>
  <div class="box">
    <h2>Тензорные программы и поиск</h2>
    <ul>
      <li>TVM - сквозной оптимизирующий компилятор</li>
      <li>AutoTVM - обученные модели стоимости</li>
      <li>Ansor - иерархическое пространство поиска</li>
      <li>MetaSchedule - вероятностные программы</li>
      <li>TensorIR - IR тензоризованных программ</li>
    </ul>
  </div>
  <div class="box">
    <h2>Инфраструктура и data-centric IR</h2>
    <ul>
      <li>MLIR - multi-level dialect инфраструктура</li>
      <li>StableHLO - переносимая семантика операторов</li>
      <li>DaCe / SDFG - перемещение данных и double buffering как трансформации</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Они дают словарь для AI-facing views: <strong>schedule actions</strong> (tile, split, reorder, vectorize, double-buffer), <strong>семантический верхний слой</strong> и <strong>data-centric</strong> графы перемещения данных.</p>
</div>

<p class="source">arXiv:2002.11054, 1802.04799, 1805.08166, 2006.06762, 2205.13603, 2207.04296, 1902.10345, 1804.10694; Halide (PLDI'13), Triton (MAPL'19), Exo (PLDI'22), спецификация StableHLO. См. notes/03-compiler-ir-autotuning.md.</p>

---

# Сравнение систем IR и scheduling

<table>
  <thead>
    <tr><th>Система</th><th>Ключевая абстракция</th><th>Поиск / настройка</th><th>Что берет этот репозиторий</th></tr>
  </thead>
  <tbody>
    <tr><td>Halide / Tiramisu</td><td>algorithm vs schedule</td><td>ручной / autoscheduler / полиэдральный</td><td>отделить семантику от schedule</td></tr>
    <tr><td>TVM / Ansor / MetaSchedule</td><td>тензорная программа + schedule</td><td>обученная cost model, эволюция, вероятностный</td><td>schedule actions как структурированные выборы</td></tr>
    <tr><td>TensorIR</td><td>IR тензоризованных loop-nest</td><td>schedule primitives + tuning</td><td>легальные трансформы уровня block/loop</td></tr>
    <tr><td>Triton / TileLang / Exo</td><td>tile-centric / user-schedulable</td><td>компилятор + подсказки пользователя</td><td>tile как first-class объект</td></tr>
    <tr><td>MLIR / StableHLO</td><td>multi-level IR / семантика</td><td>n/a (инфраструктура)</td><td>диалекты для views; семантический контракт</td></tr>
    <tr><td>DaCe / SDFG</td><td>data-centric dataflow граф</td><td>граф-трансформации</td><td>перемещение данных и liveness как first-class</td></tr>
  </tbody>
</table>

<p class="source">Синтез Кластера C; отображен на кандидатную схему views в notes/05-ascend-toolchain-views.md.</p>

---

# Кластер D - основы анализа программ

<table>
  <thead>
    <tr><th>Основа</th><th>Год</th><th>Дает</th><th>Отображается на view</th></tr>
  </thead>
  <tbody>
    <tr><td>Килдалл - unified data-flow</td><td>1973</td><td>reaching defs, константы, диапазоны</td><td>view параметров тайлинга / семантики</td></tr>
    <tr><td>Кузо - abstract interpretation</td><td>1977</td><td>корректные инварианты, диапазоны, выравнивание</td><td>контракты UB-capacity / tail-correctness</td></tr>
    <tr><td>Ферранте и др. - PDG</td><td>1987</td><td>data/control dependence</td><td>view зависимостей / легальности</td></tr>
    <tr><td>ProGraML - graph ML над кодом</td><td>2020</td><td>атрибутированные графы программ</td><td>граф знаний оператора</td></tr>
  </tbody>
</table>

<div class="callout">
  <p>Ключевой инсайт обзора: liveness, dependence, ranges и legality - это <em>решенные задачи</em> в компиляторах. Для AscendC их можно переупаковать как agent-facing views, а не изобретать заново.</p>
</div>

<p class="source">DOI 10.1145/512927.512945, POPL'77, DOI 10.1145/24039.24041, arXiv:2003.10536. См. notes/04-program-analysis.md.</p>

---

# Сквозная ось 1 - что видит оптимизатор

<div class="pipeline">
  <div class="step"><strong>Сырой код</strong><span>большинство LLM-prompting baselines</span></div>
  <div class="step"><strong>+ ошибки компилятора</strong><span>итеративные агенты (Geak, CudaForge)</span></div>
  <div class="step"><strong>+ текст профайлера</strong><span>PRAGMA, TritonForge, AscendOptimizer</span></div>
  <div class="step"><strong>+ compiler reports</strong><span>CompilerGPT</span></div>
  <div class="step"><strong>+ structured views</strong><span>цель этого репозитория</span></div>
</div>

<div class="callout">
  <p>Область движется слева направо, но не доходит до полного структурированного, legality-aware слоя views. AscendOptimizer достигает "текст профайлера + эпизодический опыт"; работы roofline и NPUMeter дают недостающую часть модели производительности.</p>
</div>

---

# Сквозная ось 2 - методология оценки

<div class="two-col">
  <div class="box">
    <h2>Общий язык метрик</h2>
    <ul>
      <li><strong>Pass@1 / compile success</strong> - может ли вообще сгенерировать валидный код (MultiKernelBench, KernelBench).</li>
      <li><strong>speedup vs reference</strong> - отношение к базовой реализации.</li>
      <li><strong>fast_p</strong> - доля операторов выше порога ускорения p (KernelBench, AscendOptimizer).</li>
      <li><strong>evaluation budget</strong> - аппаратные оценки как wall-clock стоимость.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Дисциплина корректности</h2>
    <ul>
      <li>CPU-эталон + абсолютный/относительный tolerance (политики CANN).</li>
      <li>compile / correctness / profile как одна аппаратная оценка.</li>
      <li>regression rate и стабильность baseline-задержки.</li>
      <li>трансдуктивный autotuning, а не zero-shot predictive заявления.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Сходящаяся методология между кластерами делает предлагаемую систему на views напрямую сравнимой: переиспользовать fast_p, speedup и фиксированный бюджет оценок.</p>
</div>

<p class="source">KernelBench (arXiv:2502.10517), AscendOptimizer (arXiv:2603.23566) разд. 4; docs/problem-statement.md evaluation sketch.</p>

---

# Сквозная ось 3 - как приобретается знание

<div class="four-col">
  <div class="box">
    <h2>Pretraining reuse</h2>
    <p>Работает для CUDA/Triton; проваливается на AscendC (таблица 1).</p>
  </div>
  <div class="box">
    <h2>Поиск / эволюция</h2>
    <p>Ansor, MetaSchedule, OpenEvolve, HITL tiling; сильно, но требует бюджета.</p>
  </div>
  <div class="box">
    <h2>RL / SFT</h2>
    <p>Kevin, CUDA-L1/L2, AutoTriton; нужно много пар код-производительность.</p>
  </div>
  <div class="box">
    <h2>Эпизодический опыт</h2>
    <p>Rewind-банк AscendOptimizer; training-free, переносимые мотивы.</p>
  </div>
</div>

<div class="callout">
  <p>Недостающий пятый источник: <strong>compiler-derived структурное знание</strong> - liveness, dependence, tiling и legality, извлеченные статически и переданные агенту, дополняют четыре выше.</p>
</div>

---

# Разрыв синтеза

<div class="two-col">
  <div class="box">
    <h2>Что литература уже дает</h2>
    <ul>
      <li>schedule/семантические абстракции (Кластер C);</li>
      <li>переиспользуемые статические анализы (Кластер D);</li>
      <li>agent loops с обратной связью выполнения (Кластер B);</li>
      <li>Ascend baselines, бенчмарки, модели производительности (Кластер A).</li>
    </ul>
  </div>
  <div class="box">
    <h2>Чего не хватает</h2>
    <ul>
      <li>единого AI-facing слоя, который сливает их для AscendC;</li>
      <li>легальности/контрактов, явно открытых агенту;</li>
      <li>profiling evidence, привязанного к узлам IR/view;</li>
      <li>опыта, привязанного к структурированным views, а не к свободному тексту.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Тезис обзора:</strong> части существуют в четырех сообществах; возможность вклада - их интеграция в compiler-derived operator knowledge views.</p>
</div>

---

# Предлагаемый синтез - compiler-derived operator views

<div class="three-col">
  <div class="box"><h3>1. Семантический view</h3><p>op family, формы, dtype, layout, broadcast/reduction, tolerance.</p></div>
  <div class="box"><h3>2. Tiling view</h3><p>оси, tile sizes, core split, tail policy, buffer footprint, legal actions.</p></div>
  <div class="box"><h3>3. Pipeline view</h3><p>CopyIn/Compute/CopyOut, очереди, overlap, легальность double-buffer, stalls.</p></div>
</div>

<div class="three-col" style="margin-top: 12px;">
  <div class="box"><h3>4. Memory / liveness</h3><p>GM/UB/L1/L0, live ranges, пик байт, выравнивание, reuse, конфликты.</p></div>
  <div class="box"><h3>5. Dependence / legality</h3><p>def-use, data/control deps, alias/effect, легальное vs нелегальное с причинами.</p></div>
  <div class="box"><h3>6. Performance evidence</h3><p>bottleneck class, component utilization, affected nodes, ранжированные actions.</p></div>
</div>

<div class="callout">
  <p>Плюс <strong>7. provenance view</strong>: action, ожидаемая польза, корректность, производительность, regression - чтобы эпизодический опыт стал привязан к узлам views и контрактам.</p>
</div>

<p class="source">Кандидатная схема из notes/05-ascend-toolchain-views.md и docs/problem-statement.md.</p>

---

# Исследовательская повестка и открытые проблемы

<div class="two-col">
  <div class="box">
    <h2>Открытые исследовательские вопросы</h2>
    <ul>
      <li>Какие артефакты IR/tooling реально может открыть пайплайн Ascend?</li>
      <li>Какие классические анализы переносятся напрямую, а какие нужно адаптировать?</li>
      <li>Какие дополнения к программной модели делают AscendC изначально более понятным для AI?</li>
      <li>Бьют ли views сырой код по success, корректности, скорости и качеству объяснений?</li>
    </ul>
  </div>
  <div class="box">
    <h2>Минимальный первый артефакт</h2>
    <ul>
      <li>один оператор, одна форма, один dtype;</li>
      <li>5-7 views + 6-10 legal actions;</li>
      <li>schema, extractor, action checker, harness, agent protocol;</li>
      <li>трехсторонняя абляция: raw / +profiling / +views.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Оценка переиспользует собственные мерки области: compile success, speedup, fast_p, итерации, regression rate, переносимость мотивов.</p>
</div>

<p class="source">docs/problem-statement.md (research questions и evaluation sketch); roadmap.md.</p>

---

# Выводы

<div class="three-col">
  <div class="box">
    <h2>1. Разрыв реален</h2>
    <p>AscendC ломает рецепт pretraining-reuse, питающий CUDA-агентов; нужны другие источники знаний.</p>
  </div>
  <div class="box">
    <h2>2. Части существуют</h2>
    <p>Schedules, анализы, agent loops и модели производительности Ascend зрелы - но разрознены по четырем сообществам.</p>
  </div>
  <div class="box">
    <h2>3. Интеграция - это возможность</h2>
    <p>Compiler-derived operator views могут слить их в один AI-facing интерфейс с легальностью и provenance.</p>
  </div>
</div>

<div class="callout">
  <p><strong>Одной строкой:</strong> обзор отображает четыре литературы на одну цель - compiler-derived operator knowledge views for agentic AscendC optimization.</p>
</div>

---

# Ссылки (1/2)

<div class="refs">
  <p><strong>Ascend / NPU.</strong> AscendOptimizer, arXiv:2603.23566. AscendCraft, arXiv:2601.22760. AscendKernelGen, arXiv:2601.07160. MultiKernelBench, arXiv:2507.17773. Squeezing Operator Performance (ASPLOS'25), DOI 10.1145/3676641.3716243. NPUMeter, DOI 10.1145/3820380.</p>
  <p><strong>Агентная оптимизация.</strong> KernelBench, arXiv:2502.10517. TritonBench, arXiv:2502.14752. Geak, arXiv:2507.23194. CompilerGPT, arXiv:2506.06227. Обзор Code Optimization, arXiv:2501.01277.</p>
  <p><strong>Смежные агенты.</strong> Astra 2509.07506; PRAGMA 2511.06345; CudaForge 2511.01884; TritonForge 2512.09196; GPU Kernel Scientist 2506.20807; StitchCUDA 2603.02637; KernelEvolve 2512.23236; EvoEngineer 2510.03760.</p>
  <p><strong>RL / SFT.</strong> Kevin 2507.11948; CUDA-L1 2507.14111; CUDA-L2 2512.02551; AutoTriton 2507.05687; TritonRL 2510.17891; Seed-Coder 2506.03524. OpenEvolve (github: algorithmicsuperintelligence/openevolve).</p>
</div>

---

# Ссылки (2/2)

<div class="refs">
  <p><strong>Compiler IR / scheduling / autotuning.</strong> MLIR, arXiv:2002.11054. StableHLO spec (openxla.org/stablehlo). TVM, arXiv:1802.04799. Learning to Optimize Tensor Programs (AutoTVM), arXiv:1805.08166. Ansor, arXiv:2006.06762. MetaSchedule, arXiv:2205.13603. TensorIR, arXiv:2207.04296. Triton (MAPL'19). Halide (PLDI'13 / CACM). Exo (PLDI'22). DaCe/SDFG, arXiv:1902.10345. Tiramisu, arXiv:1804.10694. TileLang, arXiv:2504.17577.</p>
  <p><strong>Анализ программ.</strong> Kildall, A Unified Approach to Global Program Optimization, DOI 10.1145/512927.512945 (1973). Cousot &amp; Cousot, Abstract Interpretation, POPL'77. Ferrante et al., The Program Dependence Graph and Its Use in Optimization, DOI 10.1145/24039.24041 (1987). ProGraML, arXiv:2003.10536.</p>
  <p><strong>Материалы репозитория.</strong> README.md; docs/problem-statement.md; notes/01-05; bibliography/reading-list.md; bibliography/articles.yaml; publications/translations/ascendoptimizer-2026.md.</p>
</div>
