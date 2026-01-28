import math
import random
from typing import List

from code.nbody.bodies import Body


def two_body(separation: float = 1.0, mass: float = 1.0, v: float = 0.5) -> List[Body]:
    """
    Simple two-body setup (rough orbit-like motion).
    Bodies are placed at +/- separation/2 on x-axis with opposite y-velocities.
    """
    x = separation / 2.0
    b1 = Body(mass, -x, 0.0, 0.0, 0.0, -v, 0.0)
    b2 = Body(mass,  x, 0.0, 0.0, 0.0,  v, 0.0)
    return [b1, b2]


def three_body(scale: float = 1.0, mass: float = 1.0) -> List[Body]:
    """
    Simple three-body setup designed to show interesting/chaotic behaviour.
    """
    b1 = Body(mass, -1.0 * scale, 0.0, 0.0, 0.0, -0.2, 0.0)
    b2 = Body(mass,  1.0 * scale, 0.0, 0.0, 0.0,  0.2, 0.0)
    b3 = Body(mass,  0.0,  1.0 * scale, 0.0, 0.2, 0.0, 0.0)
    return [b1, b2, b3]


def random_cluster(n: int, seed: int = 0, radius: float = 1.0, mass_min: float = 0.5, mass_max: float = 2.0, v_scale: float = 0.05) -> List[Body]:
    """
    Random cluster of n bodies (seeded for reproducibility).
    Positions are uniform in a cube [-radius, radius].
    Velocities are small random values so the system does not instantly explode.
    """
    rng = random.Random(seed)

    bodies: List[Body] = []
    for _ in range(n):
        x = rng.uniform(-radius, radius)
        y = rng.uniform(-radius, radius)
        z = rng.uniform(-radius, radius)

        vx = rng.uniform(-v_scale, v_scale)
        vy = rng.uniform(-v_scale, v_scale)
        vz = rng.uniform(-v_scale, v_scale)

        m = rng.uniform(mass_min, mass_max)
        bodies.append(Body(m, x, y, z, vx, vy, vz))

    return bodies


def disk(n: int, seed: int = 0, radius: float = 5.0, mass: float = 1.0, v_scale: float = 0.4, thickness: float = 0.05 ) -> list[Body]:
    """
    Rotating disk-like system (useful for animation demos).

    Bodies are distributed in a flat disk (mostly XY plane) with
    velocities perpendicular to their radius, producing rotation.

    This is a visual/demo setup, not a physically exact galaxy model.
    """
    rng = random.Random(seed)
    bodies = []

    for _ in range(n):
        # radius sampled so density is higher near centre
        r = radius * math.sqrt(rng.random())
        theta = rng.uniform(0.0, 2.0 * math.pi)

        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = rng.uniform(-thickness, thickness)

        # perpendicular velocity (rotation)
        speed = v_scale / math.sqrt(r + 0.1)
        vx = -speed * math.sin(theta)
        vy =  speed * math.cos(theta)
        vz = 0.0

        bodies.append(Body(mass, x, y, z, vx, vy, vz))

    return bodies


def list_scenes() -> List[str]:
    return ["two_body", "three_body", "cluster", "disk"]


def get_scene(name: str, **kwargs) -> List[Body]:
    name = name.lower().strip()

    if name in ("two_body", "two-body", "two"):
        return two_body(**kwargs)

    if name in ("three_body", "three-body", "three"):
        return three_body(**kwargs)

    if name in ("cluster", "random_cluster", "random"):
        return random_cluster(**kwargs)

    if name in ("disk", "rotating_disk"):
        return disk(**kwargs)

    raise ValueError(f"Unknown scene '{name}'. Available: {', '.join(list_scenes())}")