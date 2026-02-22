# Development Phases

This project was developed incrementally.  
Each phase introduced a specific technical objective while preserving correctness from previous stages.


---

## Phase 0 – Core Architecture

### Objective
Establish a clean and modular foundation for the simulation engine.

### What Changed
- Defined Body and SystemState structures.
- Separated physics calculations from orchestration.
- Introduced a central engine to manage simulation flow.

### Why It Mattered
A modular structure made it possible to compare integrators and solvers without rewriting the entire system.

### Key Outcome
A flexible foundation that allowed future extensions without architectural collapse.


---

## Phase 1 – Numerical Integrators

### Objective
Implement and compare numerical time integration methods.

### What Changed
- Implemented Euler integrator.
- Implemented Leapfrog integrator (symplectic).
- Added support for consistent stepping interface.

### Why It Mattered
Euler is simple but unstable for long simulations.  
Leapfrog preserves energy better due to its symplectic structure.

### Key Outcome
Clear demonstration of stability differences between integrators.


---

## Phase 2 – Diagnostics & Conservation Tracking

### Objective
Validate physical correctness of the simulation.

### What Changed
- Added total energy calculation.
- Added momentum and angular momentum tracking.
- Added center-of-mass computation.
- Introduced diagnostic logging during simulation.

### Why It Mattered
Without conservation checks, numerical simulations can appear visually correct while being physically inaccurate.

### Key Outcome
Confirmed that Leapfrog conserves energy significantly better than Euler.


---

## Phase 3 – 3D Extension

### Objective
Generalize the engine from 2D to full 3D simulation.

### What Changed
- Extended vectors to 3D.
- Updated force calculations accordingly.
- Extended angular momentum computation.

### Why It Mattered
Many gravitational systems require 3D modeling.  
The extension tested architectural flexibility.

### Key Outcome
The architecture required minimal modification, validating modular design.


---

## Phase 4 – Barnes–Hut Solver

### Objective
Improve scalability for large N systems.

### What Changed
- Implemented octree structure.
- Implemented Barnes–Hut force approximation.
- Added theta parameter for accuracy control.

### Why It Mattered
Direct O(N²) computation becomes impractical for large systems.  
Barnes–Hut reduces complexity to approximately O(N log N).

### Key Outcome
Significant performance improvement for moderate to large N values.


---

## Phase 5 – Scaling Experiments

### Objective
Empirically evaluate solver performance.

### What Changed
- Benchmarked Direct vs Barnes–Hut.
- Measured runtime across increasing N.
- Observed crossover point where Barnes–Hut becomes faster.

### Why It Mattered
Algorithmic complexity must be validated with real measurements.

### Key Outcome
Confirmed theoretical scaling behavior in practice.


---

## Phase 6 – Profiling & Optimization

### Objective
Identify and reduce computational bottlenecks.

### What Changed
- Profiled simulation runtime.
- Identified octree construction as dominant cost.
- Refactored performance-critical sections.

### Why It Mattered
Optimization should be guided by profiling, not assumptions.

### Key Outcome
Reduced overhead in Barnes–Hut implementation while preserving correctness.


---

## Phase 7 – Interface & Visualization Layer

### Objective
Make the project runnable, inspectable, and demonstrable through a CLI, with reproducible scenes and exportable visual outputs.

### What Changed
- Added deterministic predefined scenes:
  - two_body
  - three_body (figure-eight)
  - random_cluster (seeded, optional virialisation)
  - disk (rotating disk distribution)
- Implemented a command-line interface (argparse) supporting:
  - run and list-scenes commands
  - scene selection
  - solver selection (Direct / Barnes–Hut)
  - integrator selection (Euler / Leapfrog)
  - parameter overrides (dt, steps, softening, θ)
  - optional energy diagnostics flag
- Added static plotting utilities:
  - final XY plots (full + zoom)
  - energy drift plot (normalized scaling)
  - outputs saved into timestamped directories
- Added frame sampling support for animation:
  - record_frames flag
  - frame_every interval
  - storage of (x, y, z) frames without full history
- Implemented 2D animation (XY projection) and exposed it via CLI flags.
- Implemented animation export:
  - GIF export (PillowWriter)
  - MP4 export (FFMpegWriter)
  - CLI flags for save-gif, save-mp4, fps, and no-show
- Added visualization aesthetic defaults (“space-style”):
  - black background, static starfield
  - percentile-based camera bounds
  - marker size scaling by N
  - per-scene demo presets for stable outputs
- Added 3D visualization support:
  - 3D animation for small N
  - static 3D snapshots for large N (automatic fallback)
  - CLI flags: animate-3d, max-3d-n, snapshots
- Added an extra benchmark_cluster scene and wired it into CLI scene selection.

### Why It Mattered
Phase 7 turned the project from an internal simulation engine into a usable tool:
reproducible demos, comparable runs, and exportable outputs—without modifying source code.

### Key Outcome
A complete interface + visualization layer: the simulation can be run end-to-end via CLI,
diagnosed, plotted, animated, and exported consistently.

### Limitations
- 3D animation does not include camera rotation.
- Large-N 3D plots can be visually dense.
- Disk scene is visually tuned rather than dynamically exact.
- Implementation remains pure Python.


---

## Phase 8 – Documentation & Refinement

### Objective
Consolidate documentation and prepare for portfolio presentation.

### What Changed
- Structured documentation into organized sections.
- Added retrospective summaries.
- Improved cross-referencing between files.
- Refined README for clarity.

### Why It Mattered
Clear documentation communicates engineering thinking as effectively as code.

### Key Outcome
Project presented as a structured, extensible system rather than a collection of scripts.


---

## Overall Progression

The project evolved from a basic gravitational simulator into:

- A modular physics engine
- A benchmarking platform
- A performance study
- A structured software system

Each phase built upon the previous one without breaking correctness, ensuring that improvements were incremental and controlled.


---

## Related Documentation

- `architecture.md` – System design
- `performance.md` – Runtime analysis
- `experiments.md` – Experimental observations
- `overview.md` – Project summary