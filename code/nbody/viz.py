from __future__ import annotations

import math
from pathlib import Path
from datetime import datetime
import json

import matplotlib.pyplot as plt



# Global plotting style 

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})



# Output directory handling

def make_run_dir(
    outputs_dir: str | Path, scene: str, solver: str, integrator: str, n: int,
) -> Path:
    """
    Create a timestamped run directory inside outputs/.
    """
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{timestamp}_{scene}_{solver}_{integrator}_N{n}"

    run_dir = outputs_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir



# Plot: final XY positions

def plot_final_xy(
    bodies,
    filepath: str | Path,
    title: str | None = None,
    clip_quantile: float | None = None,
) -> None:
    """
    Save a 2D XY scatter plot of final body positions.

    If clip_quantile is provided (e.g. 0.98), the axis limits are set using the
    corresponding quantile of the radial distance to reduce the impact of escapers.
    """
    xs = [b.x for b in bodies]
    ys = [b.y for b in bodies]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=8, alpha=0.8)
    plt.gca().set_aspect("equal", adjustable="box")

    # zoom for readability (clip extreme outliers)
    if clip_quantile is not None and len(xs) > 0:
        rs = [math.hypot(x, y) for x, y in zip(xs, ys)]
        rs_sorted = sorted(rs)

        # guard against weird quantiles
        q = min(max(clip_quantile, 0.0), 1.0)
        k = int(q * (len(rs_sorted) - 1))
        r_lim = rs_sorted[k] if rs_sorted else 1.0

        lim = 1.05 * r_lim
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

    plt.xlabel("x")
    plt.ylabel("y")
    if title is not None:
        plt.title(title)

    plt.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close()


# Plot: energy drift over time

def plot_energy_drift(
    energy_drift, filepath: str | Path, title: str | None = None,
) -> None:
    """
    Save a plot of relative energy drift vs simulation step.
    Uses log scale for readability (plots |drift| with epsilon to avoid log(0)).
    """
    steps = list(range(len(energy_drift)))

    eps = 1e-16
    safe = [max(abs(v), eps) for v in energy_drift]

    plt.figure(figsize=(7, 4))
    plt.plot(steps, safe, linewidth=1.5)

    plt.xlabel("step")
    plt.ylabel("|relative energy drift| (log scale)")
    if title is not None:
        plt.title(title)

    plt.grid(True, alpha=0.3)
    plt.yscale("log")

    plt.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close()



# Metadata export

def save_metadata_json(
    metadata: dict, filepath: str | Path,
) -> None:
    """
    Save run metadata to a JSON file.
    """
    filepath = Path(filepath)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)



# Orchestrator (CLI entry point)

def save_stepc_outputs(
    sim,
    run_dir: Path,
    title_prefix: str | None = None,
) -> list[Path]:
    """
    Save all Step C outputs:
    - final XY (full scale)
    - final XY (zoomed, clipped)
    - energy drift (if available)

    Returns a list of file paths that were created.
    """
    saved_files: list[Path] = []

    # --- Final XY (full scale, includes escapers)
    final_full = run_dir / "final_xy_full.png"
    plot_final_xy(
        sim.state.bodies,
        final_full,
        title=f"{title_prefix} — Final XY (full)" if title_prefix else None,
        clip_quantile=None,
    )
    saved_files.append(final_full)

    # --- Final XY (zoomed for readability)
    final_zoom = run_dir / "final_xy_zoom.png"
    plot_final_xy(
        sim.state.bodies,
        final_zoom,
        title=f"{title_prefix} — Final XY (zoom)" if title_prefix else None,
        clip_quantile=0.95, 
    )
    saved_files.append(final_zoom)

    # --- Energy drift plot (if diagnostics exist)
    if hasattr(sim, "energy_drift") and sim.energy_drift is not None:
        energy_path = run_dir / "energy_drift.png"
        plot_energy_drift(
            sim.energy_drift,
            energy_path,
            title=f"{title_prefix} — Energy drift" if title_prefix else None,
        )
        saved_files.append(energy_path)

    return saved_files