---
marp: true
theme: chapter-theme
paginate: true
html: true
math: mathjax
title: "Babble для PyAsc: применимость к обучению DSL-абстракций"
description: "Обзорная презентация о применимости идей babble-2022 к pyasc-fork: e-graphs, anti-unification, AscIR и LLM-помощники"
---

<style>
section {
  padding: 42px 48px;
  font-size: 26px;
}

h1 {
  font-size: 1.52em;
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
  font-size: 0.7em;
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
  line-height: 1.22;
}

.lead {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lead h1 {
  font-size: 1.86em;
  max-width: 1000px;
}

.subtitle {
  color: var(--light-text);
  font-size: 0.92em;
  line-height: 1.35;
  margin: 0 0 24px 0;
  max-width: 1040px;
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
  border-radius: 4px;
  min-height: 118px;
  padding: 12px 12px;
  position: relative;
}

.step::after {
  content: ">";
  position: absolute;
  right: -9px;
  top: 43%;
  color: var(--accent3);
  font-weight: 700;
}

.step:last-child::after {
  content: "";
}

.step strong {
  color: var(--primary);
  display: block;
  font-size: 0.74em;
  line-height: 1.18;
  margin-bottom: 7px;
}

.step span {
  color: var(--light-text);
  display: block;
  font-size: 0.52em;
  line-height: 1.26;
}

.fit-table td:first-child {
  width: 27%;
  font-weight: 700;
}

.fit-table td:nth-child(2) {
  width: 18%;
  color: var(--primary);
  font-weight: 700;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 9px;
}

.tag {
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--light-text);
  font-size: 0.5em;
  line-height: 1;
  padding: 7px 9px;
  white-space: nowrap;
}

.map {
  display: grid;
  grid-template-columns: 1.05fr 1.3fr 1fr;
  gap: 14px;
  align-items: stretch;
  margin-top: 10px;
}

.lane {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px;
  min-height: 455px;
}

.lane h3 {
  color: var(--primary);
  margin-bottom: 10px;
}

.node {
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent3);
  border-radius: 4px;
  margin-bottom: 9px;
  padding: 9px 10px;
}

.node strong {
  display: block;
  font-size: 0.58em;
  line-height: 1.18;
  margin-bottom: 4px;
}

.node span {
  color: var(--light-text);
  display: block;
  font-size: 0.49em;
  line-height: 1.25;
}

.bridge {
  background: rgba(0, 146, 158, 0.08);
  border-color: rgba(0, 146, 158, 0.38);
}

.danger {
  border-left-color: var(--accent2);
}

.code-sample {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 10px;
}

.caption {
  color: var(--light-text);
  font-size: 0.5em;
  line-height: 1.26;
  margin-top: 7px;
}
</style>

<!-- _class: lead -->
# Babble для PyAsc

<p class="subtitle">Где идеи library learning modulo theory могут помочь PyAsc: от корпуса Python/AscIR программ до подсказок для LLM, новых DSL-комбинаторов и проверяемых compiler rewrites.</p>

<div class="tag-row">
  <span class="tag">babble-2022</span>
  <span class="tag">e-graphs</span>
  <span class="tag">anti-unification</span>
  <span class="tag">PyAsc / AscIR</span>
  <span class="tag">LLM-assisted optimization</span>
</div>

<div class="source">Основа: <code>publications/files/babble-2022.pdf</code>, <code>publications/translations/babble-2022.md</code>, <code>/Users/aloschilov/articles-workspace/pyasc-fork</code>.</div>

---

# Короткий вывод

<div class="callout">
  <p><strong>Babble стоит применять к PyAsc не как автономный оптимизатор latency, а как слой извлечения переиспользуемых программных абстракций.</strong></p>
</div>

<div class="three-col" style="margin-top: 18px;">
  <div class="box">
    <h3>Что хорошо ложится</h3>
    <ul>
      <li>повторяющиеся tile-скелеты;</li>
      <li>эквивалентные формы индексации;</li>
      <li>канонизация AscTile / AscVF фрагментов;</li>
      <li>подбор примеров для LLM.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Что надо ограничить</h3>
    <ul>
      <li>side effects: память, синхронизация, очереди;</li>
      <li>типы, shape и memory location;</li>
      <li>эквивалентности только там, где есть verifier.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Что не заменяет</h3>
    <ul>
      <li>профилирование на Ascend NPU;</li>
      <li>стоимостную модель производительности;</li>
      <li>ручные инварианты CANN / Ascend C.</li>
    </ul>
  </div>
</div>

<div class="source">Babble оптимизирует сжатие корпуса через библиотеки; для performance-приоритизации PyAsc нужен внешний compile/run/profiler loop.</div>

---

# Что делает Babble

<p class="subtitle">Babble решает задачу <em>library learning modulo theory</em>: находит общие подпрограммы не только по синтаксическому совпадению, но и с учётом эквивалентных переписываний.</p>

<div class="pipeline">
  <div class="step">
    <strong>Корпус программ</strong>
    <span>много похожих реализаций, но разная запись одних и тех же идей</span>
  </div>
  <div class="step">
    <strong>Equational theory</strong>
    <span>доменные правила: ассоциативность, коммутативность, identities, rearrangements</span>
  </div>
  <div class="step">
    <strong>E-graph</strong>
    <span>компактное пространство эквивалентных программных форм</span>
  </div>
  <div class="step">
    <strong>Anti-unification</strong>
    <span>общий шаблон над несколькими выражениями, с параметрами вместо различий</span>
  </div>
  <div class="step">
    <strong>Extraction</strong>
    <span>выбор abstractions, которые лучше всего сжимают корпус</span>
  </div>
</div>

<div class="source">Babble: “Learning Better Abstractions with E-Graphs and Anti-Unification”, arXiv:2212.04596.</div>

---

# Что есть в PyAsc

<div class="two-col">
  <div class="box">
    <h3>Программная модель</h3>
    <ul>
      <li><code>asc2</code>: tile-based Python API, ближе к NumPy-стилю.</li>
      <li><code>asc</code>: низкоуровневое 1:1 отображение на Ascend C API.</li>
      <li><code>@asc2.jit</code> и <code>@asc.jit</code>: вход в JIT-компиляцию.</li>
      <li><code>GlobalTensor</code>, <code>LocalTensor</code>, <code>TensorLocation</code>: явная модель памяти.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Compiler substrate</h3>
    <ul>
      <li>Python AST → AscIR / MLIR.</li>
      <li>Диалекты: <code>Asc</code>, <code>AscTile</code>, <code>AscVF</code>, <code>EmitAsc</code>.</li>
      <li>Трансформации: lowering, sync, memory allocation, vector/cube rewrites.</li>
      <li>Codegen в Ascend C, затем Bisheng / CANN toolchain.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Это почти идеальная среда для Babble-подхода: есть корпус программ, типизированный IR, локальные переписывания и compile-time verifier.</p>
</div>

<div class="source">См. <code>/Users/aloschilov/articles-workspace/pyasc-fork/README.md</code>, <code>AGENTS.md</code>, <code>docs/architecture_introduction.md</code>.</div>

---

# Где Babble встраивается

<div class="map">
  <div class="lane">
    <h3>PyAsc corpus</h3>
    <div class="node">
      <strong>Python kernels</strong>
      <span><code>python/tutorials/asc2</code>, tests, docs examples</span>
    </div>
    <div class="node">
      <strong>Dumped AscIR</strong>
      <span>IR до и после ключевых passes</span>
    </div>
    <div class="node">
      <strong>Generated Ascend C</strong>
      <span>опционально как downstream evidence</span>
    </div>
    <div class="node danger">
      <strong>Runtime traces</strong>
      <span>compile success, profiling, memory pressure</span>
    </div>
  </div>
  <div class="lane">
    <h3>Babble-style learner</h3>
    <div class="node bridge">
      <strong>Typed normalization</strong>
      <span>MLIR canonicalization + PyAsc-specific laws</span>
    </div>
    <div class="node bridge">
      <strong>E-graph saturation</strong>
      <span>эквивалентные формы tile algebra, affine offsets, casts</span>
    </div>
    <div class="node bridge">
      <strong>E-graph anti-unification</strong>
      <span>поиск общих шаблонов между неидентичными kernels</span>
    </div>
    <div class="node bridge">
      <strong>Costed extraction</strong>
      <span>compression + typed validity + compile/profiler score</span>
    </div>
  </div>
  <div class="lane">
    <h3>Outputs</h3>
    <div class="node">
      <strong><code>asc2</code> helpers</strong>
      <span>DSL-комбинаторы для повторяемых tile patterns</span>
    </div>
    <div class="node">
      <strong>AscIR rewrites</strong>
      <span>canonicalization и optimization pass candidates</span>
    </div>
    <div class="node">
      <strong>LLM memory</strong>
      <span>retrieval-база verified examples and counterexamples</span>
    </div>
    <div class="node danger">
      <strong>Review queue</strong>
      <span>человек принимает только проверенные абстракции</span>
    </div>
  </div>
</div>

---

# Применимость по слоям PyAsc

<table class="fit-table">
  <thead>
    <tr>
      <th>Слой</th>
      <th>Оценка</th>
      <th>Почему</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>asc2</code> tile API</td>
      <td>Высокая</td>
      <td>Много чистых выражений над tile-значениями; повторяются load/compute/store, map, reduce, matmul skeletons.</td>
    </tr>
    <tr>
      <td><code>AscTile</code> / <code>AscVF</code></td>
      <td>Высокая</td>
      <td>Типизированный MLIR-уровень удобен для e-graphs, canonicalization и проверки shape/location constraints.</td>
    </tr>
    <tr>
      <td><code>asc</code> low-level API</td>
      <td>Средняя</td>
      <td>Есть полезные паттерны, но память, синхронизация и очереди требуют effect-aware теории.</td>
    </tr>
    <tr>
      <td>Ascend C codegen</td>
      <td>Средняя</td>
      <td>Хорош как validation target; как основной уровень обучения шумнее из-за boilerplate.</td>
    </tr>
    <tr>
      <td>Latency tuning</td>
      <td>Низкая без профайлера</td>
      <td>Babble выбирает компактные библиотеки, а не гарантированно быстрые kernels.</td>
    </tr>
  </tbody>
</table>

---

# Какую теорию эквивалентностей задать

<div class="two-col">
  <div class="box">
    <h3>Безопасная стартовая зона</h3>
    <ul>
      <li>арифметика индексов и offsets;</li>
      <li>ассоциативность и коммутативность для разрешённых ops;</li>
      <li>identity rewrites: <code>x + 0</code>, <code>x * 1</code>;</li>
      <li>shape-preserving casts и broadcasts;</li>
      <li>эквивалентные формы tile slicing.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Только с guards</h3>
    <ul>
      <li><code>copy_in</code> / <code>copy_out</code>: memory location и layout;</li>
      <li>sync elimination / movement;</li>
      <li>buffer reuse и allocation movement;</li>
      <li>matmul decomposition через L1/L0A/L0B;</li>
      <li>любые правила с order-sensitive side effects.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p>Практический критерий: правило попадает в Babble theory только если его можно проверить через MLIR verifier, type/shape constraints и compile-only тест.</p>
</div>

---

# Какие абстракции можно выучить

<div class="three-col">
  <div class="box">
    <h3>Python DSL helpers</h3>
    <ul>
      <li><code>block_tiles(size, cores)</code></li>
      <li><code>load_tile(gm, offset, shape)</code></li>
      <li><code>store_tile(tile, gm, offset)</code></li>
      <li><code>vector_map(fn, *tiles)</code></li>
      <li><code>tile_reduce(fn, tile)</code></li>
    </ul>
  </div>
  <div class="box">
    <h3>IR patterns</h3>
    <ul>
      <li>redundant cast/fold;</li>
      <li>common mask elimination;</li>
      <li>copy-in split через L1;</li>
      <li>load/compute/store fusion;</li>
      <li>canonical offsets.</li>
    </ul>
  </div>
  <div class="box">
    <h3>LLM examples</h3>
    <ul>
      <li>типовые skeletons;</li>
      <li>контрпримеры unsafe rewrites;</li>
      <li>проверенные lowering traces;</li>
      <li>performance annotations;</li>
      <li>review checklists.</li>
    </ul>
  </div>
</div>

<div class="source">Идея: не просить LLM “угадать” idiom, а давать ей mined, verified, domain-grounded abstractions.</div>

---

# Пример: от похожих kernels к helper

<div class="code-sample">
  <div>

```python
@asc2.jit
def vadd(x_ptr, y_ptr, out_ptr, size, tile_size):
    x_gm = asc2.global_tensor(x_ptr, [size])
    y_gm = asc2.global_tensor(y_ptr, [size])
    out_gm = asc2.global_tensor(out_ptr, [size])

    for i in range(size // tile_size):
        off = i * tile_size
        x = asc2.copy_in(x_gm, [off], [tile_size])
        y = asc2.copy_in(y_gm, [off], [tile_size])
        out = x + y
        asc2.copy_out(out, out_gm, [off])
```

  <div class="caption">Исходный повторяемый скелет: tile loop + load + compute + store.</div>
  </div>
  <div>

```python
def elementwise_tile_loop(ins, out, size, tile_size, fn):
    for off in tile_offsets(size, tile_size):
        tiles = [load_tile(t, off, tile_size) for t in ins]
        result = fn(*tiles)
        store_tile(result, out, off)

@asc2.jit
def vadd(...):
    elementwise_tile_loop([x_gm, y_gm], out_gm,
                          size, tile_size,
                          lambda x, y: x + y)
```

  <div class="caption">Babble-like output: candidate abstraction, затем compile/test/profiler validation.</div>
  </div>
</div>

---

# MVP-пайплайн для pyasc-fork

<div class="pipeline">
  <div class="step">
    <strong>1. Corpus</strong>
    <span>собрать <code>asc2</code> tutorials, tests, docs examples и dumped MLIR snapshots</span>
  </div>
  <div class="step">
    <strong>2. Normalize</strong>
    <span>AST/MLIR normalization: names, constants, offsets, canonical ops</span>
  </div>
  <div class="step">
    <strong>3. Learn</strong>
    <span>e-graph saturation + anti-unification для pure-ish fragments</span>
  </div>
  <div class="step">
    <strong>4. Validate</strong>
    <span>type/shape verifier, compile-only tests, optional runtime checks</span>
  </div>
  <div class="step">
    <strong>5. Feed LLM</strong>
    <span>retrieval cards: abstraction, examples, guards, failed rewrites</span>
  </div>
</div>

<div class="callout">
  <p>Первая цель должна быть не “ускорить всё”, а “собрать маленькую библиотеку verified PyAsc idioms, которую LLM может применять и объяснять”.</p>
</div>

---

# Где нужны инструменты анализа

<div class="four-col">
  <div class="box">
    <h3>Static shape/type</h3>
    <p>Проверка, что learned abstraction сохраняет dtype, rank, shape, tensor location и const-expression constraints.</p>
  </div>
  <div class="box">
    <h3>Effect model</h3>
    <p>Разделение pure tile expressions и order-sensitive operations: memory copies, flags, queues, barriers.</p>
  </div>
  <div class="box">
    <h3>IR diffing</h3>
    <p>Сравнение до/после: какие AscIR операции исчезли, какие появились, меняется ли lowering path.</p>
  </div>
  <div class="box">
    <h3>Profiler score</h3>
    <p>Компрессия библиотеки ранжируется вместе с compile success, latency, memory footprint и generated code size.</p>
  </div>
</div>

<div class="tag-row">
  <span class="tag">MLIR verifier</span>
  <span class="tag">pass snapshots</span>
  <span class="tag">CANN compile</span>
  <span class="tag">msprof / runtime profiling</span>
  <span class="tag">LLM retrieval</span>
</div>

---

# Риски

<div class="three-col">
  <div class="box">
    <h3>Unsound rewrites</h3>
    <p>Эквивалентность в арифметике не означает эквивалентность в присутствии памяти, sync и layout constraints.</p>
  </div>
  <div class="box">
    <h3>E-graph blowup</h3>
    <p>AscIR и tile expressions могут быстро разрастаться; начинать лучше с одного семейства kernels.</p>
  </div>
  <div class="box">
    <h3>Wrong objective</h3>
    <p>Сжатие корпуса может ухудшить читаемость или latency; cost model должен учитывать реальные проверки.</p>
  </div>
</div>

<div class="callout">
  <p>Guardrail: Babble предлагает кандидатов; PyAsc compiler, тесты и профилировщик решают, можно ли превращать кандидата в DSL/API/pass.</p>
</div>

---

# Рекомендация

<div class="two-col">
  <div class="box">
    <h3>Делать сейчас</h3>
    <ul>
      <li>начать с <code>asc2</code> vector/tile kernels;</li>
      <li>учить common skeletons на Python AST и AscTile IR;</li>
      <li>строить retrieval cards для LLM;</li>
      <li>проверять каждую абстракцию через compile-only pipeline.</li>
    </ul>
  </div>
  <div class="box">
    <h3>Отложить</h3>
    <ul>
      <li>переписывания sync/memory scheduling без effect model;</li>
      <li>автоматическое изменение low-level <code>asc</code> kernels;</li>
      <li>performance claims без запуска на железе;</li>
      <li>широкую теорию правил сразу для всех dialects.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Лучший первый результат:</strong> mined library из 10-20 PyAsc idioms с примерами, guards и ссылками на passing compile/runtime evidence.</p>
</div>

<div class="source">Следующий практический артефакт: прототип extractor для <code>python/tutorials/asc2</code> + карточки “pattern / guard / rewrite / validation”.</div>
