# Перевод и комментарий к исходной постановке

## Перевод

### Harness для анализа и генерации кода операторов с помощью AI-агентов и программной модели

Как использовать компиляторные инструменты, чтобы улучшить работу ML-оптимизации.

- Представления кода, удобные для AI-тюнинга:
  - представления зависимостей в pipeline оператора;
  - представления dataflow;
  - другие структурные представления кода.
- Модификация программной модели для большей пригодности к AI:
  - pipeline передачи информации от компилятора к AI.
- Повторное использование индустриальных техник статического анализа:
  - dataflow analysis;
  - dependency analysis;
  - и другие техники анализа программ.

### Технические вызовы

- Существующие фреймворки работают напрямую с исходным кодом и не имеют структурных представлений, специфичных для Ascend-домена. Из-за этого агентам трудно понимать семантику на уровне операторов.
- Как восстановить необходимые представления кода из практик оптимизации производительности под Ascend, например из double-buffering pipeline concurrency?

### Основной фокус

- Какие промежуточные представления и результаты анализа может предоставлять компилятор, например Ascend compilation toolchain, и как передавать их AI-системам тюнинга.
- Какие индустриальные техники статического анализа и анализа программ можно напрямую переиспользовать для построения нужных представлений.
- Какие изменения нужны на уровне программной модели, чтобы код изначально был более понятным для AI благодаря явной семантической структуре.

## Комментарий

Исходная постановка содержит правильные интуиции, но выглядит как набор brainstorming keywords, а не как зрелое problem statement. В одном месте смешаны разные уровни:

- harness;
- compiler toolchain;
- programming model;
- static analysis;
- LLM-agent feedback loop;
- AscendC performance practices;
- IR design.

Главная проблема: **harness**, **programming model** и **code analysis** — это разные сущности. Их можно связать, но надо явно сформулировать связку:

> We build a harness that extracts compiler-derived structured views from AscendC/IR and passes them to an AI agent for constrained operator optimization.

Фраза “existing frameworks work directly on source code” слишком грубая. TVM, MLIR, Triton, Halide, XLA, DaCe и Tiramisu как раз вводят IR, schedule representation, dataflow graphs, loop-nest views и tensor IR. Более точная версия:

> Existing LLM/agentic coding frameworks often expose raw source code and logs to the agent, but do not expose Ascend-specific structured views: tiling, CopyIn/Compute/CopyOut pipeline, TQue/TPipe, memory spaces, synchronization, buffer liveness, and profiler bottlenecks.

Фраза “AI-tuning-friendly code knowledge views” перспективная, но её надо расшифровать через конкретные views: semantic operator view, tiling view, pipeline DAG, memory-space/liveness view, dependence graph, legal transformation/action-space view, profile bottleneck view.

Фраза “programming model modification for AI-friendliness” тоже пока слишком широкая. Практичнее говорить не о полной замене AscendC, а об AI-facing structured layer: annotations/contracts + schedule IR + compiler-extracted views.

## More precise formulation

**Compiler-Derived Operator Knowledge Views for Agentic AscendC Optimization**

We propose a harness for AI-assisted AscendC operator optimization that does not expose only raw source code to an LLM agent. Instead, the harness extracts structured, compiler-derived operator knowledge views: semantic operator information, tiling parameters, CopyIn/Compute/CopyOut pipeline structure, memory-space and buffer-liveness information, dependence graphs, legal transformation actions, and profiling-based bottleneck evidence.

The goal is to make Ascend operator optimization more understandable and controllable for AI agents. Rather than asking an agent to edit arbitrary AscendC code, the system provides domain-specific views and a constrained action space, allowing the agent to reason about tiling, data movement, double buffering, synchronization, and pipeline overlap while preserving correctness.
