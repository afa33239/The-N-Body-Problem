# Project Overview

## Introduction

The N-Body Problem Expansion is a modular gravitational simulation engine written in Python.  
It models the motion of interacting bodies under Newtonian gravity and explores both physical accuracy and computational performance.

The project evolved from a basic numerical simulation into a structured, extensible engine supporting:

- Multiple numerical integrators
- Multiple force solvers (Direct and Barnes–Hut)
- 2D and 3D simulation
- Energy and momentum diagnostics
- Performance benchmarking
- Visualization and animation
- Reproducible predefined simulation scenes


---

## Project Goals

The primary goals of this project were:

1. Implement physically correct gravitational simulation.
2. Compare numerical integration methods.
3. Investigate performance scaling for large N systems.
4. Implement the Barnes–Hut algorithm for approximate O(N log N) scaling.
5. Design a clean and extensible architecture.
6. Produce reproducible experiments and visual outputs.


---

## What This Project Demonstrates

This project demonstrates:

- Understanding of classical mechanics and conservation laws.
- Implementation of symplectic vs non-symplectic integrators.
- Algorithmic complexity trade-offs (O(N²) vs O(N log N)).
- Use of spatial tree structures (octree).
- Profiling and performance optimization.
- Clean modular software design.
- Reproducible scientific experimentation.


---

## System Overview

At a high level, the simulation engine operates as follows:

1. Initial bodies are generated (manually or via predefined scenes).
2. A solver computes gravitational accelerations.
3. An integrator advances the system state in time.
4. Diagnostics track conserved quantities.
5. Optional visualization renders results.

The solver and integrator are interchangeable components, allowing direct comparison between methods without modifying the core engine.


---

## Evolution of the Project

The project was developed in phases:

- Phase 0 – Core architecture foundation
- Phase 1 – Numerical integrators (Euler, Leapfrog)
- Phase 2 – Diagnostics and conservation tracking
- Phase 3 – 3D extension
- Phase 4 – Barnes–Hut implementation
- Phase 5 – Performance scaling experiments
- Phase 6 – Profiling and optimization
- Phase 7 – Predefined scenes and CLI interface
- Phase 8/9 – Documentation and structure refinement

Each phase introduced a specific technical objective while preserving the correctness of previous results.


---

## Scope and Limitations

This project focuses on:

- Newtonian gravity only
- Classical mechanics (no relativistic corrections)
- CPU-based implementation (no GPU acceleration)
- Educational and experimental purposes

It is not designed as a production astrophysics engine, but as a structured exploration of physics simulation and algorithm design.


---

## Related Documentation

For deeper technical details, see:

- `architecture.md` – system design and module breakdown
- `phases.md` – development progression
- `performance.md` – scaling and optimization results
- `experiments.md` – selected experiment observations
- `notes.md` – mathematical and implementation notes