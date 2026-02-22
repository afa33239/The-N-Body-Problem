# Experimental Observations

This document summarizes selected observations gathered during development.
The goal of these experiments was to validate physical correctness,
understand numerical behavior, and evaluate approximation effects.


---

## 1. Integrator Stability Comparison

### Setup
- Two-body orbital system
- Fixed timestep
- Direct solver

### Observations

**Euler Integrator**
- Energy drift increases steadily.
- Orbit gradually expands or decays.
- Momentum conservation degrades over long simulations.

**Leapfrog Integrator**
- Energy oscillates but remains bounded.
- Orbital structure remains stable.
- Long-term behavior significantly improved.

### Conclusion

The Leapfrog method demonstrates the expected advantages of symplectic integration,
preserving long-term qualitative behavior.


---

## 2. Energy Conservation Trends

Energy tracking revealed three important behaviors:

1. Euler produces monotonic drift.
2. Leapfrog produces bounded oscillatory error.
3. Barnes–Hut introduces additional approximation error.

Energy drift is sensitive to:
- Timestep size (dt)
- Softening parameter
- θ value (for Barnes–Hut)

Smaller timesteps consistently improve stability.


---

## 3. Barnes–Hut Accuracy Behavior

### Varying θ

- Small θ → results closely match Direct solver.
- Moderate θ → noticeable speed gains with minor deviations.
- Large θ → visible energy drift and orbital distortion.

The relationship between θ and accuracy is smooth and predictable.


---

## 4. Scaling Behavior

As particle count increases:

- Direct solver runtime increases rapidly.
- Barnes–Hut runtime increases more slowly.
- For large N systems, Barnes–Hut enables simulations that would otherwise be impractical.

The crossover point where Barnes–Hut becomes faster depends on N and θ.


---

## 5. 3D Extension Validation

After extending to 3D:

- Conservation laws remained consistent.
- Energy behavior matched 2D trends.
- Angular momentum calculation required full 3D cross product.

The architecture required minimal structural modification,
indicating successful modular design.


---

## 6. Disk and Cluster Behavior

Random clusters:
- Naturally form gravitational contraction patterns.
- Demonstrate chaotic behavior over long simulations.

Disk systems:
- Show rotational coherence.
- Useful for visualization and animation testing.

These scenes are primarily demonstrative rather than astrophysically precise.


---

## 7. General Observations

Throughout experimentation:

- Symplectic integration is critical for stability.
- Approximation methods require careful parameter tuning.
- Profiling often reveals unexpected bottlenecks.
- Clean architecture simplifies controlled experimentation.

The combination of diagnostics, interchangeable components,
and reproducible scenes enabled reliable comparative analysis.


---

## Related Documentation

- `performance.md` – Runtime scaling and profiling
- `phases.md` – Development progression
- `architecture.md` – System design
- `overview.md` – Project goals