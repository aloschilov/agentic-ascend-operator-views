# Candidate Ascend toolchain-to-agent views

This file defines a candidate schema for the compiler-to-AI information pipeline.

## 1. Operator semantic view

Purpose: tell the agent what the operator computes.

Fields:

- op name and family;
- input/output shapes;
- dtypes;
- layouts/formats;
- broadcasting/reduction axes;
- numerical tolerance contract;
- reference implementation;
- dynamic-shape constraints.

## 2. Host tiling view

Purpose: expose the host-side tiling program as data rather than opaque C++.

Fields:

- tiling axes;
- tile sizes;
- block/core split;
- tail policy;
- per-core workload;
- buffer footprint estimate;
- constraints from UB/L1/L0 capacity;
- candidate legal tiling actions.

## 3. Device pipeline view

Purpose: expose CopyIn/Compute/CopyOut and concurrency structure.

Fields:

- pipeline stages;
- stage resources;
- queues;
- buffer count;
- event/wait dependencies;
- stage overlap potential;
- double-buffering legality;
- observed bubbles/stalls if available.

## 4. Memory-space and liveness view

Purpose: expose memory movement and resource pressure.

Fields:

- GM/UB/L1/L0/L0C allocation summary;
- buffer live ranges;
- peak live bytes;
- alignment status;
- reuse opportunities;
- data movement edges;
- possible bank/conflict hints.

## 5. Dependence and legality view

Purpose: prevent invalid agent edits.

Fields:

- def-use/use-def chains;
- data/control dependencies;
- alias/effect annotations;
- loop-carried dependencies;
- synchronization constraints;
- legal/illegal transformations with reasons.

## 6. Performance evidence view

Purpose: convert profiler/compiler output into actionable evidence.

Fields:

- total latency;
- component utilization;
- bandwidth / MTE pressure;
- compute utilization;
- pipeline parallelism score;
- bottleneck class;
- source locations / view nodes affected;
- candidate actions ranked by confidence.

## 7. Transformation provenance view

Purpose: support learning from attempts.

Fields:

- action applied;
- affected view node;
- expected benefit;
- correctness result;
- performance result;
- regression status;
- notes for reusable motif extraction.

## Example JSON sketch

```json
{
  "operator": {
    "name": "rms_norm",
    "dtype": "float16",
    "shape": [32, 4096],
    "reference": "aclnnRmsNorm"
  },
  "tiling": {
    "axis": 1,
    "tile_size": 1024,
    "core_split": 32,
    "tail_policy": "none"
  },
  "pipeline": {
    "stages": ["CopyIn", "Compute", "CopyOut"],
    "double_buffer": true,
    "queue_depth": 2
  },
  "performance": {
    "latency_us": null,
    "bottleneck": "unknown",
    "evidence": []
  },
  "legal_actions": [
    "change_tile_size",
    "toggle_double_buffer",
    "adjust_core_split",
    "modify_tail_policy"
  ]
}
```
