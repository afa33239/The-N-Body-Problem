# Technical Notes

This document contains mathematical and implementation notes that support
design decisions made throughout the project.


---

## 1. Gravitational Model

The simulation implements Newtonian gravity.

Force between two bodies:

F = G * (m1 * m2) / r²

Vector form:

a_i = G * Σ (m_j * (r_j - r_i) / |r_j - r_i|³)

Where:
- r_i is the position vector of body i
- G is the gravitational constant
- Softening is applied to prevent singularities at small distances

A softening term ε is added:

|r|³ → (|r|² + ε²)^(3/2)

This stabilizes close interactions and prevents numerical blow-up.


---

## 2. Numerical Integration

### Euler Method

Update rule:

x(t + dt) = x(t) + v(t) dt  
v(t + dt) = v(t) + a(t) dt  

Properties:
- First-order accurate
- Non-symplectic
- Energy drift accumulates


### Leapfrog Method

Velocity-Verlet style scheme:

v(t + dt/2) = v(t) + a(t) dt/2  
x(t + dt) = x(t) + v(t + dt/2) dt  
v(t + dt) = v(t + dt/2) + a(t + dt) dt/2  

Properties:
- Second-order accurate
- Symplectic
- Bounded long-term energy error

Leapfrog requires velocity synchronization when computing diagnostics.


---

## 3. Energy Calculations

Total energy:

E_total = K + U

Kinetic energy:

K = 1/2 Σ m_i |v_i|²

Potential energy:

U = -G Σ (m_i m_j / r_ij), i < j

Energy drift is used as a primary stability indicator.


---

## 4. Momentum & Angular Momentum

Linear momentum:

P = Σ m_i v_i

Angular momentum (3D):

L = Σ (r_i × m_i v_i)

Conservation of these quantities provides validation
that force symmetry is correctly implemented.


---

## 5. Barnes–Hut Approximation

The Barnes–Hut algorithm uses an octree.

Key idea:
- If a cluster of particles is sufficiently far away,
  it can be approximated by its center of mass.

Acceptance criterion:

s / d < θ

Where:
- s = size of node
- d = distance from particle to node center
- θ = accuracy parameter

Smaller θ increases accuracy but reduces performance.


---

## 6. Time Step Considerations

Simulation stability depends strongly on dt.

- Large dt → unstable orbits, energy explosion
- Small dt → stable but computationally expensive

There is no adaptive timestep in this implementation.
dt is fixed for controlled comparison between methods.


---

## 7. Design Decisions

### Pure Python Implementation
Chosen for:
- Clarity
- Educational transparency
- Simplicity of distribution

Not optimized for maximum performance.


### Explicit State Handling
SystemState is explicitly passed between components.
This avoids hidden mutation and improves traceability.


### Separation of Concerns
Physics, integration, solving, and orchestration
are kept strictly separate to enable experimentation.


---

## 8. Known Limitations

- No adaptive timestep.
- No GPU acceleration.
- No collision handling or merging.
- No relativistic corrections.
- Large-N simulations are limited by Python performance.

These limitations are intentional for clarity and scope control.


---

## 9. Possible Extensions

Future improvements could include:

- Adaptive timestep integration.
- Parallelized force computation.
- GPU acceleration.
- Higher-order symplectic integrators.
- Collision detection and merging.
- Visualization camera controls for 3D.

The architecture is designed to allow these additions
without major structural changes.