from __future__ import annotations

"""
Visualization helpers for the N-body project.

This file handles:
- creating output run folders
- saving plots (final positions, energy drift)
- saving animations (2D + 3D)
- a simple "space" style (black background + star field)
"""

import math
import json
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Small global style tweaks so plots look consistent
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Space-style defaults (used in 2D animation)
BODY_COLOR = "#FFFFFF"
STAR_COUNT = 450
STAR_ALPHA = 0.6
STAR_SIZE = 1
STAR_SEED = 123


def make_run_dir(outputs_dir: str | Path, scene: str, solver: str, integrator: str, n: int) -> Path:
    """
    Creates a unique output directory inside outputs_dir for this run.

    Folder name includes timestamp + scene + solver + integrator + N.
    """
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{timestamp}_{scene}_{solver}_{integrator}_N{n}"

    run_dir = outputs_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def save_metadata_json(metadata: dict, filepath: str | Path) -> None:
    """
    Saves a metadata dict as a JSON file.
    Useful for recording run config info.
    """
    filepath = Path(filepath)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def apply_space_style(ax, lim: float, *, hide_axes: bool = True) -> None:
    """
    Applies a black "space" theme to a 2D axis and draws a background star field.

    lim controls where stars are placed (random uniform in [-lim, lim]).
    """
    ax.figure.set_facecolor("black")
    ax.set_facecolor("black")

    # Star field is deterministic (seeded) so animations look consistent per run
    rng = np.random.default_rng(STAR_SEED)
    sx = rng.uniform(-lim, lim, size=STAR_COUNT)
    sy = rng.uniform(-lim, lim, size=STAR_COUNT)
    ax.scatter(
        sx, sy,
        s=STAR_SIZE,
        c="white",
        alpha=STAR_ALPHA,
        linewidths=0,
        zorder=0,
    )

    # Usually for the space style we hide ticks/spines
    if hide_axes:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)


def _robust_lim_from_frames(xy: np.ndarray, *, percentile: float = 99.0, padding: float = 2.0) -> float:
    """
    Computes a stable plot limit from animation frames.

    We use a percentile instead of max() so one extreme body doesn't ruin the scale.
    padding just gives extra breathing room.
    """
    x_all = xy[..., 0].ravel()
    y_all = xy[..., 1].ravel()

    # Remove NaN/inf values (can happen in unstable runs)
    mask = np.isfinite(x_all) & np.isfinite(y_all)
    x_all = x_all[mask]
    y_all = y_all[mask]

    if x_all.size == 0 or y_all.size == 0:
        return 1.0

    r = np.maximum(np.abs(x_all), np.abs(y_all))
    lim = float(np.percentile(r, percentile)) * padding

    if not np.isfinite(lim) or lim <= 0:
        lim = 1.0

    return lim


def plot_final_xy(bodies, filepath: str | Path, title: str | None = None, clip_quantile: float | None = None) -> None:
    """
    Saves a simple XY scatter plot of the final body positions.

    If clip_quantile is provided, we zoom by limiting the axis range to a radius
    percentile (useful when there are outliers).
    """
    xs = [b.x for b in bodies]
    ys = [b.y for b in bodies]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=8, alpha=0.8)
    plt.gca().set_aspect("equal", adjustable="box")

    # Optional zoom: compute radii and clip using a quantile
    if clip_quantile is not None and xs:
        rs = [math.hypot(x, y) for x, y in zip(xs, ys)]
        rs_sorted = sorted(rs)

        q = min(max(clip_quantile, 0.0), 1.0)
        k = int(q * (len(rs_sorted) - 1))
        r_lim = rs_sorted[k] if rs_sorted else 1.0

        lim = 1.05 * r_lim
        plt.xlim(-lim, lim)
        plt.ylim(-lim, lim)

    plt.xlabel("x")
    plt.ylabel("y")
    if title:
        plt.title(title)

    plt.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close()


def plot_energy_drift(energy_drift, filepath: str | Path, title: str | None = None) -> None:
    """
    Saves a plot of energy drift over time on a log scale.

    We clamp values to eps so log scale doesn't crash at zeros.
    """
    steps = list(range(len(energy_drift)))

    eps = 1e-16
    safe = [max(abs(v), eps) for v in energy_drift]

    plt.figure(figsize=(7, 4))
    plt.plot(steps, safe, linewidth=1.5)
    plt.xlabel("step")
    plt.ylabel("|relative energy drift| (log)")
    if title:
        plt.title(title)

    plt.grid(True, alpha=0.3)
    plt.yscale("log")
    plt.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close()


def save_stepc_outputs(sim, run_dir: Path, title_prefix: str | None = None) -> list[Path]:
    """
    Saves the default output plots used in the project:
    - final XY full view
    - final XY zoomed view
    - energy drift (if available)
    """
    saved: list[Path] = []

    final_full = run_dir / "final_xy_full.png"
    plot_final_xy(
        sim.state.bodies,
        final_full,
        title=f"{title_prefix} — Final XY (full)" if title_prefix else None,
    )
    saved.append(final_full)

    final_zoom = run_dir / "final_xy_zoom.png"
    plot_final_xy(
        sim.state.bodies,
        final_zoom,
        title=f"{title_prefix} — Final XY (zoom)" if title_prefix else None,
        clip_quantile=0.95,
    )
    saved.append(final_zoom)

    # Only save energy drift if sim computed it
    if getattr(sim, "energy_drift", None) is not None:
        energy_path = run_dir / "energy_drift.png"
        plot_energy_drift(
            sim.energy_drift,
            energy_path,
            title=f"{title_prefix} — Energy drift" if title_prefix else None,
        )
        saved.append(energy_path)

    return saved


def save_animation(anim, out_path: str | Path, fps: int = 30):
    """
    Saves a matplotlib animation to .gif or .mp4 based on file extension.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ext = out_path.suffix.lower()

    if ext == ".gif":
        anim.save(str(out_path), writer=PillowWriter(fps=fps))
        return out_path

    if ext == ".mp4":
        # ffmpeg must be installed for this to work
        from matplotlib.animation import FFMpegWriter
        anim.save(str(out_path), writer=FFMpegWriter(fps=fps))
        return out_path

    raise ValueError(f"Unsupported extension '{ext}'. Use .gif or .mp4")


def animate_xy(
    frames,
    out_path: str | Path | None = None,
    interval: int = 20,
    title: str | None = None,
    show: bool = True,
    fps: int = 30,
) -> Path | None:
    """
    Creates a 2D XY animation from recorded frames.

    frames is expected to be:
      frames[t][i] = (x, y, z)

    Only x and y are used here.
    """
    if not frames:
        raise ValueError("No frames recorded (try --animate and check frame_every).")

    # Convert frames into a NumPy array for easy indexing
    # Shape becomes (T, N, 2)
    xy = np.array([[(p[0], p[1]) for p in frame] for frame in frames], dtype=float)
    T, N, _ = xy.shape

    # Pick a scatter point size based on number of bodies
    if N <= 5:
        body_size = 250
    elif N <= 50:
        body_size = 100
    elif N <= 200:
        body_size = 25
    else:
        body_size = 10

    # Compute axis limits using percentiles so outliers don't ruin the scale
    lim = _robust_lim_from_frames(xy, percentile=99.0, padding=2.0)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    if title:
        ax.set_title(title)

    # Space-style (black background + stars)
    apply_space_style(ax, lim, hide_axes=True)
    if title:
        ax.title.set_color("white")

    # Initial scatter plot (frame 0)
    sc = ax.scatter(
        xy[0, :, 0],
        xy[0, :, 1],
        s=body_size,
        c=BODY_COLOR,
        alpha=1.0,
        linewidths=0,
        zorder=3,
    )

    # Update function called by matplotlib each frame
    def update(i: int):
        sc.set_offsets(xy[i])
        return (sc,)

    anim = FuncAnimation(fig, update, frames=T, interval=interval, blit=True, repeat=False)

    # Save if user requested an output path
    saved = None
    if out_path is not None:
        saved = save_animation(anim, out_path=out_path, fps=fps)

    # Either show interactively or close to avoid memory leaks
    if show:
        plt.show()
    else:
        plt.close(fig)

    return saved


def plot_frame_xyz(frame, filepath: str | Path, title: str | None = None) -> None:
    """
    Saves a single 3D scatter snapshot for one frame.
    """
    xs = [p[0] for p in frame]
    ys = [p[1] for p in frame]
    zs = [p[2] for p in frame]

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.scatter(xs, ys, zs, s=8, c="white", alpha=0.8, linewidths=0)

    # Choose a stable axis range using percentiles (similar to 2D approach)
    all_vals = xs + ys + zs
    finite_vals = [v for v in all_vals if np.isfinite(v)]
    if finite_vals:
        r = np.percentile(np.abs(finite_vals), 99.0)
        r = r if r > 0 else 1.0
    else:
        r = 1.0

    r *= 2.0
    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_zlim(-r, r)

    # Try to keep equal scaling on all axes (older matplotlib may not support this)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    if title:
        ax.set_title(title, color="white")

    plt.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_snapshots_xyz(sim, run_dir: Path, title_prefix: str | None = None) -> list[Path]:
    """
    Saves two 3D snapshots (initial and final frame).
    Used as a fallback when 3D animation is disabled for large N.
    """
    saved: list[Path] = []
    if not sim.frames:
        return saved

    # initial snapshot
    p0 = run_dir / "initial_xyz.png"
    plot_frame_xyz(sim.frames[0], p0, title=f"{title_prefix} — Initial XYZ" if title_prefix else None)
    saved.append(p0)

    # final snapshot
    p1 = run_dir / "final_xyz.png"
    plot_frame_xyz(sim.frames[-1], p1, title=f"{title_prefix} — Final XYZ" if title_prefix else None)
    saved.append(p1)

    return saved


def animate_xyz(
    frames,
    out_path: str | Path | None = None,
    interval: int = 30,
    title: str | None = None,
    show: bool = True,
    fps: int = 30,
):
    """
    Creates a 3D XYZ animation from recorded frames.

    Note: This does not use the star background (it's heavier in 3D).
    """
    if not frames:
        raise ValueError("No frames recorded (try --animate / record_frames).")

    # Shape becomes (T, N, 3)
    xyz = np.array(frames, dtype=float)
    T, N, _ = xyz.shape

    # Flatten all coordinates so we can choose stable axis limits
    x_all = xyz[..., 0].ravel()
    y_all = xyz[..., 1].ravel()
    z_all = xyz[..., 2].ravel()

    def lims(v):
        # Use percentiles so a single extreme point doesn't destroy the scale
        finite = v[np.isfinite(v)]
        if finite.size == 0:
            r = 1.0
        else:
            r = np.percentile(np.abs(finite), 99.0)
            r = float(r) if np.isfinite(r) and r > 0 else 1.0
        r *= 2.0
        return -r, r

    xlim = lims(x_all)
    ylim = lims(y_all)
    zlim = lims(z_all)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)

    # Try to keep equal scaling (depends on matplotlib version)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass

    # Hide axes to keep the "space" look clean
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            axis.line.set_color((1, 1, 1, 0))
        except Exception:
            pass

    if title:
        ax.set_title(title, color="white")

    # Choose marker size based on N
    size = 30 if N <= 5 else 12

    # Initial scatter (frame 0)
    sc = ax.scatter(
        xyz[0, :, 0],
        xyz[0, :, 1],
        xyz[0, :, 2],
        s=size,
        c="white",
        alpha=1.0,
        linewidths=0,
    )

    def update(i):
        # Matplotlib 3D scatter uses a private attribute for updating points
        sc._offsets3d = (xyz[i, :, 0], xyz[i, :, 1], xyz[i, :, 2])
        return (sc,)

    anim = FuncAnimation(fig, update, frames=T, interval=interval, blit=False, repeat=False)

    saved = None
    if out_path is not None:
        saved = save_animation(anim, out_path=out_path, fps=fps)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return saved