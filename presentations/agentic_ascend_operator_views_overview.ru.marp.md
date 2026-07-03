---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Compiler-Derived Operator Views for Agentic AscendC Optimization"
description: "Обзорная презентация по репозиторию: программные модели, анализ и structured views для LLM-агента оптимизации AscendC операторов"
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
  font-size: 0.53em;
  margin: 8px 0;
}

th,
td {
  padding: 7px 9px;
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
  font-size: 1.92em;
  max-width: 1000px;
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
  font-size: 0.61em;
  line-height: 1.34;
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

.map {
  display: grid;
  grid-template-columns: 1.1fr 1.25fr 1.35fr 1.15fr 1.1fr;
  gap: 10px;
  align-items: stretch;
  margin-top: 14px;
}

.map-col {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 10px;
  min-height: 390px;
}

.map-col h3 {
  color: var(--primary);
  font-size: 0.62em;
  margin-bottom: 8px;
}

.map-item {
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent6);
  border-radius: 4px;
  padding: 8px 9px;
  margin-bottom: 8px;
  min-height: 54px;
}

.map-item strong {
  display: block;
  color: var(--text);
  font-size: 0.55em;
  line-height: 1.15;
}

.map-item span {
  color: var(--light-text);
  display: block;
  font-size: 0.46em;
  line-height: 1.22;
  margin-top: 3px;
}

.map-arrow {
  color: var(--accent3);
  font-weight: 700;
}

.compact-list li {
  font-size: 0.64em;
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
</style>

<!-- _class: lead -->

# Compiler-Derived Operator Views for Agentic AscendC Optimization

<p class="subtitle">Как программные модели и инструменты анализа могут дать LLM не только код и логи, а карту решений: семантику оператора, тайлинг, pipeline, память, зависимости, допустимые действия и доказательства производительности.</p>

<div class="metric-row">
  <div class="metric"><strong>AscendC</strong><span>оператор состоит из host-side tiling и device-side kernel</span></div>
  <div class="metric"><strong>LLM</strong><span>плохо видит скрытые ограничения из сырого C++</span></div>
  <div class="metric"><strong>Views</strong><span>структурируют знания для решений агента</span></div>
  <div class="metric"><strong>Loop</strong><span>compile, verify, profile, learn from attempts</span></div>
</div>

---

# Почему сырого кода мало

<div class="two-col">
  <div class="box">
    <h2>AscendC оператор связан</h2>
    <ul>
      <li><strong>Host tiling</strong>: формы, tile sizes, block/core split, хвосты, параметры запуска.</li>
      <li><strong>Device kernel</strong>: CopyIn/Compute/CopyOut, очереди, UB/L1/L0, синхронизация, векторизация.</li>
      <li>Производительность зависит от того, как данные подаются и как kernel их потребляет.</li>
    </ul>
  </div>
  <div class="box">
    <h2>LLM видит слабый интерфейс</h2>
    <ul>
      <li>Compiler errors и profiler logs часто говорят о симптомах, а не о легальном переписывании.</li>
      <li>Публичных AscendC ядер мало, поэтому меньше готовых паттернов в предобучении.</li>
      <li>Без явной модели допустимых действий агент легко делает правку, которая компилируется плохо или ломает семантику.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Гипотеза репозитория:</strong> агенту нужен AI-facing слой между исходниками и действиями, извлеченный из компилятора, анализа программ, профайлера и программной модели.</p>
</div>

<p class="source">Контекст: README.md, docs/problem-statement.md, notes/01-ascend-npu.md.</p>

---

# Центральная идея: не prompt, а представления

<div class="pipeline">
  <div class="step"><strong>1. Operator spec</strong><span>семантика, формы, dtype, layout, tolerance</span></div>
  <div class="step"><strong>2. AscendC / IR</strong><span>host tiling, kernel, memory spaces, pipeline calls</span></div>
  <div class="step"><strong>3. Analysis views</strong><span>tiling, pipeline, liveness, dependence, performance evidence</span></div>
  <div class="step"><strong>4. Action space</strong><span>tile, split, reorder, buffer, vectorize, prefetch, validate</span></div>
  <div class="step"><strong>5. Agent loop</strong><span>LLM proposes legal edits; harness compiles, tests and profiles</span></div>
</div>

<div class="callout">
  <p>Цель не заменить AscendC целиком, а сделать слой, через который LLM понимает, какие решения вообще допустимы и почему они могут ускорить оператор.</p>
</div>

---

# Карта системы: где живут элементы

<div class="map">
  <div class="map-col">
    <h3>Входы</h3>
    <div class="map-item"><strong>Operator spec</strong><span>op, shape, dtype, layout, reference</span></div>
    <div class="map-item"><strong>AscendC source</strong><span>host tiling + device kernel</span></div>
    <div class="map-item"><strong>Compiler IR</strong><span>lowering artifacts, loops, buffers</span></div>
    <div class="map-item"><strong>Profiler traces</strong><span>latency, stalls, component utilization</span></div>
  </div>
  <div class="map-col">
    <h3>Программная модель</h3>
    <div class="map-item"><strong>Semantic layer</strong><span>что вычисляется, численный контракт</span></div>
    <div class="map-item"><strong>Schedule IR</strong><span>как вычисление разложено по плиткам и ядрам</span></div>
    <div class="map-item"><strong>Data movement model</strong><span>GM/UB/L1/L0, CopyIn/Compute/CopyOut</span></div>
    <div class="map-item"><strong>Contracts</strong><span>инварианты, preconditions, legal actions</span></div>
  </div>
  <div class="map-col">
    <h3>Анализ и views</h3>
    <div class="map-item"><strong>Tiling view</strong><span>axis, tile sizes, tail policy, core split</span></div>
    <div class="map-item"><strong>Pipeline view</strong><span>queues, buffers, overlap, double buffering</span></div>
    <div class="map-item"><strong>Memory/liveness</strong><span>live ranges, capacity pressure, reuse</span></div>
    <div class="map-item"><strong>Dependence/legality</strong><span>def-use, alias/effect, reorder constraints</span></div>
    <div class="map-item"><strong>Performance evidence</strong><span>bottleneck class, affected nodes, confidence</span></div>
  </div>
  <div class="map-col">
    <h3>LLM decisions</h3>
    <div class="map-item"><strong>Diagnose</strong><span>выбрать узкое место и affected view nodes</span></div>
    <div class="map-item"><strong>Retrieve</strong><span>похожие эпизоды и motifs</span></div>
    <div class="map-item"><strong>Plan action</strong><span>выбрать легальную трансформацию</span></div>
    <div class="map-item"><strong>Patch</strong><span>редактировать kernel, tiling или schedule</span></div>
  </div>
  <div class="map-col">
    <h3>Контур проверки</h3>
    <div class="map-item"><strong>Compile</strong><span>CANN toolchain, diagnostics</span></div>
    <div class="map-item"><strong>Verify</strong><span>CPU reference, tolerance, invariants</span></div>
    <div class="map-item"><strong>Profile</strong><span>real device feedback</span></div>
    <div class="map-item"><strong>Provenance</strong><span>change, expected benefit, actual result</span></div>
  </div>
</div>

<p class="source">Диаграмма связывает README.md, docs/problem-statement.md и notes/05-ascend-toolchain-views.md.</p>

---

# Программные модели: что сделать видимым

<div class="three-col">
  <div class="box">
    <h2>1. Семантический слой</h2>
    <p>Op type, ranks, shapes, layouts, broadcast/reduction semantics, tolerance.</p>
    <p><span class="tag">StableHLO-like</span><span class="tag">operator contract</span></p>
  </div>
  <div class="box">
    <h2>2. Schedule layer</h2>
    <p>Отделить "что считаем" от "как раскладываем": tile, split, reorder, vectorize, unroll.</p>
    <p><span class="tag">Halide</span><span class="tag">Tiramisu</span><span class="tag">TensorIR</span></p>
  </div>
  <div class="box">
    <h2>3. Data movement layer</h2>
    <p>Сделать first-class объектами GM/UB/L1/L0, CopyIn/Compute/CopyOut и очереди.</p>
    <p><span class="tag">SDFG</span><span class="tag">Ascend pipeline</span></p>
  </div>
</div>

<div class="three-col" style="margin-top: 14px;">
  <div class="box">
    <h2>4. Host tiling as data</h2>
    <p>Не opaque C++ функция, а структурированный набор решений: axis, tile sizes, blockDim, tail policy.</p>
  </div>
  <div class="box">
    <h2>5. Contracts</h2>
    <p>Preconditions, invariants, unsupported regimes, alignment and capacity rules.</p>
  </div>
  <div class="box">
    <h2>6. Action vocabulary</h2>
    <p>LLM выбирает действие из словаря, а не пишет произвольную оптимизацию вслепую.</p>
  </div>
</div>

---

# Инструменты анализа: чем помочь LLM

<table>
  <thead>
    <tr>
      <th>Анализ</th>
      <th>Что дает агенту</th>
      <th>Решения, которые становятся безопаснее</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data-flow</td>
      <td>definitions, uses, constants, ranges</td>
      <td>замена выражений, propagation, проверка параметров тайлинга</td>
    </tr>
    <tr>
      <td>Liveness</td>
      <td>live ranges, peak buffer pressure</td>
      <td>reuse UB, double buffering, memory placement</td>
    </tr>
    <tr>
      <td>Dependence / PDG</td>
      <td>data/control dependencies, alias/effect facts</td>
      <td>reorder, fuse, split, pipeline overlap без нарушения семантики</td>
    </tr>
    <tr>
      <td>Loop / polyhedral</td>
      <td>affine accesses, loop-carried dependencies</td>
      <td>tile, interchange, vectorize, tail handling</td>
    </tr>
    <tr>
      <td>Profiler evidence</td>
      <td>bottleneck class and affected source/view nodes</td>
      <td>выбрать действие по причине, а не по названию счетчика</td>
    </tr>
  </tbody>
</table>

<p class="source">См. notes/04-program-analysis.md и notes/05-ascend-toolchain-views.md.</p>

---

# Техники, которые стоит вынести в систему

<div class="four-col">
  <div class="box">
    <h2>Optimization Rewind</h2>
    <ul>
      <li>взять сильную реализацию;</li>
      <li>контролируемо удалить мотив;</li>
      <li>если стало медленнее, сохранить обратный rewrite как опыт.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Hardware-in-the-loop tiling</h2>
    <ul>
      <li>мутация тайлинга;</li>
      <li>compile + correctness;</li>
      <li>real-device profile;</li>
      <li>survivor update.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Retrieval-guided rewrite</h2>
    <ul>
      <li>diagnose bottleneck;</li>
      <li>найти похожие эпизоды;</li>
      <li>переписать код с учетом applicability и avoid rules.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Constrained action space</h2>
    <ul>
      <li>legal actions из views;</li>
      <li>проверка preconditions;</li>
      <li>объяснение: почему правка допустима.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Главная связка:</strong> техники дают agent loop, а compiler-derived views уменьшают пространство случайных правок и делают каждую попытку объяснимой.</p>
</div>

---

# Как LLM принимает решение с views

<div class="pipeline">
  <div class="step"><strong>Observe</strong><span>operator view + diagnostics + profiling summary</span></div>
  <div class="step"><strong>Localize</strong><span>узкое место привязывается к loop, buffer, stage или tiling node</span></div>
  <div class="step"><strong>Select</strong><span>agent выбирает legal action и проверяет preconditions</span></div>
  <div class="step"><strong>Patch</strong><span>изменяется kernel, tiling template или schedule representation</span></div>
  <div class="step"><strong>Learn</strong><span>результат идет в provenance и experience bank</span></div>
</div>

<div class="two-col" style="margin-top: 16px;">
  <div class="box">
    <h2>Пример вопроса агента</h2>
    <p>"Можно ли увеличить tile size, не переполнив UB и не нарушив tail policy?"</p>
  </div>
  <div class="box">
    <h2>Какие views отвечают</h2>
    <p>Tiling view + memory/liveness + shape/range invariants + profiler evidence.</p>
  </div>
</div>

---

# Что отличает этот подход от AscendOptimizer

<div class="two-col">
  <div class="box">
    <h2>AscendOptimizer как baseline</h2>
    <ul>
      <li>строит банк опыта через Optimization Rewind;</li>
      <li>использует retrieval для kernel rewrite;</li>
      <li>подбирает host-side tiling по обратной связи от железа;</li>
      <li>работает training-free.</li>
    </ul>
  </div>
  <div class="box">
    <h2>Расширение в этом репозитории</h2>
    <ul>
      <li>добавить compiler-derived views до agent action;</li>
      <li>явно представить legality и contracts;</li>
      <li>связать profiling evidence с nodes в IR/views;</li>
      <li>сделать programming model более AI-facing.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>AscendOptimizer показывает ценность эпизодического опыта. Следующий вопрос: насколько сильнее агент станет, если каждый эпизод будет привязан к структурированным представлениям программы.</p>
</div>

---

# Экспериментальная рамка

<table>
  <thead>
    <tr>
      <th>Конфигурация</th>
      <th>Что видит агент</th>
      <th>Что проверяем</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Raw source + logs</td>
      <td>AscendC, compiler errors, test failures, profiler text</td>
      <td>нижняя baseline-точка</td>
    </tr>
    <tr>
      <td>Source + profiling summaries</td>
      <td>структурированные latency and bottleneck summaries</td>
      <td>сколько дает чистая диагностика</td>
    </tr>
    <tr>
      <td>Source + operator views</td>
      <td>semantic, tiling, pipeline, memory, dependence, legal actions</td>
      <td>пользу AI-facing compiler layer</td>
    </tr>
  </tbody>
</table>

<div class="three-col">
  <div class="box"><h2>Correctness</h2><p>compile success, CPU reference, tolerance, regression rate</p></div>
  <div class="box"><h2>Performance</h2><p>speedup, fast_p, iterations, hardware-evaluation budget</p></div>
  <div class="box"><h2>Reasoning</h2><p>legality explanations, motif transfer, provenance quality</p></div>
</div>

---

# Минимальный исследовательский артефакт

<div class="pipeline">
  <div class="step"><strong>Schema</strong><span>JSON views for semantic, tiling, pipeline, memory, dependence, performance</span></div>
  <div class="step"><strong>Extractor</strong><span>парсинг AscendC/IR + статический анализ + profiler ingestion</span></div>
  <div class="step"><strong>Action checker</strong><span>legal/illegal transformations with reasons</span></div>
  <div class="step"><strong>Harness</strong><span>compile, run, compare, profile, archive evidence</span></div>
  <div class="step"><strong>Agent protocol</strong><span>prompt templates, retrieval, provenance, dashboard</span></div>
</div>

<div class="callout">
  <p>Первый полезный slice: один оператор, одна форма, один dtype, 5-7 views, 6-10 legal actions и воспроизводимый compile/verify/profile loop.</p>
</div>

---

# Выводы

<div class="three-col">
  <div class="box">
    <h2>1. LLM нужен интерфейс</h2>
    <p>Сырой AscendC скрывает семантику, ограничения и ресурсные trade-off. Views превращают это в данные.</p>
  </div>
  <div class="box">
    <h2>2. Анализ снижает риск</h2>
    <p>Dependence, liveness, ranges и legality checks уменьшают число бессмысленных или опасных правок.</p>
  </div>
  <div class="box">
    <h2>3. Опыт становится переносимым</h2>
    <p>Optimization Rewind и provenance сильнее, если они привязаны к view nodes, bottleneck classes и action contracts.</p>
  </div>
</div>

<div class="callout">
  <p><strong>Формулировка проекта:</strong> compiler-derived operator knowledge views for agentic AscendC optimization.</p>
</div>

<p class="source">Основные материалы: README.md, docs/problem-statement.md, notes/01-05, publications/translations/ascendoptimizer-2026.md.</p>
