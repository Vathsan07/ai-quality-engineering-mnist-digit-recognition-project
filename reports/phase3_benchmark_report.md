# Phase 3: Performance Benchmarking and Quantization

Generated (UTC): 2026-11-02T18:26:33.487023+00:00

## Results

| Model | Accuracy | State-dict size (MB) | P50 (ms) | P95 (ms) | P99 (ms) |
|---|---:|---:|---:|---:|---:|
| FP32 | 97.76% | 0.4205 | 0.1262 | 0.2666 | 1.1005 |
| INT8 dynamic | 97.83% | 0.1102 | 0.6558 | 1.1600 | 2.1441 |

## Interpretation

- State-dict size change: 73.80% reduction.
- P50 latency improvement: -419.61%.
- Accuracy change: 0.070 percentage points.

## Limitations
- Results are local CPU microbenchmarks.
- They exclude API, networking, and deployment overhead.
- Performance can vary with system load and hardware.
- Quantization benefits must be verified empirically.