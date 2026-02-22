# Performance & Scaling Analysis

This document summarizes runtime behavior, scaling trends, and optimization findings
from the Direct and Barnes–Hut solvers.


---

## 1. Solver Complexity

Two force computation strategies are implemented:

### Direct Solver
- Computes all pairwise interactions.
- Time complexity: O(N²)
- Exact (within numerical precision).

### Barnes–Hut Solver
- Approximates distant particle groups using an octree.
- Time complexity: approximately O(N log N)
- Controlled by the θ (theta) parameter.


---

## 2. Empirical Scaling Results

Runtime measurements were collected across increasing particle counts.

Observations:

- For small N, the Direct solver is often faster due to lower overhead.
- As N increases, the O(N²) cost dominates.
- Barnes–Hut becomes faster beyond a moderate N threshold.
- The crossover point depends on:
  - Tree construction overhead
  - θ parameter
  - Hardware performance

These results confirm theoretical expectations in practice.


---

## 3. Theta (θ) Accuracy–Performance Trade-off

The Barnes–Hut solver uses a threshold parameter θ:

- Smaller θ → higher accuracy, slower runtime.
- Larger θ → faster runtime, less accuracy.

Observations:

- Very small θ approximates Direct behavior.
- Moderate θ provides strong speed gains with acceptable accuracy loss.
- Excessively large θ increases energy drift.

This trade-off allows controlled approximation depending on simulation goals.


---

## 4. Energy Conservation Behavior

Energy conservation was evaluated for:

- Euler + Direct
- Leapfrog + Direct
- Leapfrog + Barnes–Hut

Findings:

- Euler exhibits monotonic energy drift.
- Leapfrog maintains bounded oscillatory energy behavior.
- Barnes–Hut introduces additional approximation error.
- Smaller θ reduces long-term drift.

These results confirm the advantage of symplectic integration.


---

## 5. Profiling Results (Phase 6)

Profiling identified the dominant computational costs.

Primary bottlenecks:

- Octree construction
- Tree traversal during force computation

Refactoring focused on:

- Reducing redundant computations
- Minimizing temporary allocations
- Improving structure clarity without altering physics

Optimization decisions were guided strictly by profiling data rather than assumption.


---

## 6. Observed Scaling Pattern

General runtime trend:

- Direct: runtime grows quadratically.
- Barnes–Hut: runtime grows sub-quadratically.
- For sufficiently large N, Barnes–Hut becomes clearly superior.

The implementation validates theoretical complexity behavior within a pure Python environment.


---

## 7. Design Considerations

The implementation prioritizes:

- Correctness over aggressive micro-optimization
- Transparency over premature optimization
- Experimental reproducibility

No external acceleration libraries were used.
All results were obtained using pure Python.


---

## Related Documentation

- `phases.md` – Phase 4, 5, and 6 development details
- `experiments.md` – Selected experimental observations
- `architecture.md` – Solver and tree structure design
- `overview.md` – Project goals and scope