# Architecture

## Design Philosophy

The simulation engine is designed around clear separation of concerns.  
Each module has a single responsibility, allowing components to be modified or replaced without affecting the rest of the system.

The core design principle is modularity:
- Data is separated from physics logic.
- Physics logic is separated from numerical integration.
- Integration is separated from orchestration.
- Visualization is separated from simulation.

This makes the system extensible and suitable for experimentation.


---

## High-Level Structure

The project is organized into the following conceptual layers:

### 1. Data Layer

**bodies.py**

- Defines the Body class.
- Defines SystemState (positions, velocities, masses).
- Contains no physics logic.

This layer only stores structured data.


---

### 2. Physics Layer

**physics.py**

- Computes gravitational accelerations.
- Computes potential and kinetic energy.
- Computes total energy.
- Computes momentum and angular momentum.
- Computes center of mass.

This layer contains only physical equations and is independent of the integration scheme.


---

### 3. Solver Layer

**solvers/**
- direct.py
- barneshut.py
- octree.py

The solver is responsible for computing accelerations given the current system state.

Two implementations exist:

- **Direct solver** — O(N²) pairwise force computation.
- **Barnes–Hut solver** — O(N log N) approximation using an octree.

The integrator interacts only with the solver interface, allowing both methods to be swapped without code changes elsewhere.


---

### 4. Integrator Layer

**integrators/**
- euler.py
- leapfrog.py

The integrator advances the system forward in time.

Implemented methods:

- Euler (explicit, first-order, non-symplectic)
- Leapfrog (symplectic, second-order)

Leapfrog uses half-step velocity updates and includes a synchronization mechanism for accurate diagnostics.


---

### 5. Engine Layer

**engine.py**

The engine coordinates:

- Integrator stepping
- Solver acceleration calls
- Diagnostics collection
- Frame recording (optional)

It does not implement physics or numerical methods directly — it only orchestrates components.


---

### 6. Interface & Visualization Layer

**viz.py**
- Static plotting
- 2D and 3D animation
- Diagnostic plots

**cli.py**
- Command-line argument parsing
- Scene selection
- Configuration handling
- Output management

This layer is fully separated from simulation logic.


---

## Data Flow

The simulation loop follows this structure:

1. Initial SystemState is created.
2. Solver computes accelerations.
3. Integrator updates positions and velocities.
4. Engine optionally records diagnostics.
5. Loop repeats for the specified number of steps.

Conceptually:

SystemState → Solver → Integrator → Updated SystemState → Diagnostics


---

## Interchangeability

The architecture allows:

- Switching integrators without touching physics.
- Switching solvers without touching integrators.
- Adding new solvers or integrators with minimal changes.
- Running simulations without visualization.
- Running visualization without modifying core simulation code.

This separation enables controlled experimentation and fair performance comparison.


---

## Architectural Evolution

The architecture was not designed in a single step.  
It evolved through refactoring during development.

Earlier versions mixed physics, integration, and orchestration logic.  
Through refactoring, responsibilities were separated into distinct modules.

This restructuring improved:

- Maintainability
- Testability
- Extensibility
- Clarity of data flow


---

## Design Trade-offs

- Pure Python implementation for clarity over raw speed.
- Explicit state management rather than implicit mutation.
- Readability prioritized over micro-optimizations.
- No external physics libraries used.

These choices keep the project educational and transparent.


---

## Related Documentation

For development progression, see:
- `phases.md`

For performance analysis:
- `performance.md`

For experimental results:
- `experiments.md`