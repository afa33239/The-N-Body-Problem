import math
from code.nbody.bodies import Body, G


class OctreeNode:
    """
    Octree node used by the Barnes–Hut solver.

    Each node stores:
    - total mass + center of mass (for approximation)
    - either one body (leaf) or 8 children (internal)
    """

    def __init__(self, center, half_size):
        """
        center: (cx, cy, cz) center of this cube
        half_size: half the side length of the cube
        """
        self.center = center
        self.half_size = half_size

        self.total_mass = 0.0
        self.center_of_mass = (0.0, 0.0, 0.0)

        self.body = None
        self.children = None

    def insert(self, body_to_insert: Body):
        """
        Inserts a body into the octree and updates mass/center of mass.
        """
        # empty leaf
        if self.body is None and self.children is None:
            self.body = body_to_insert

        # leaf already has a body -> subdivide and re-insert both
        elif self.children is None and self.body is not None:
            self.subdivide()
            old = self.body
            self.body = None
            self._insert_into_child(old)
            self._insert_into_child(body_to_insert)

        # internal node -> insert into correct child
        else:
            idx = self.cube_to_insert(body_to_insert)
            self.children[idx].insert(body_to_insert)

        # update mass/center of mass on the way back up
        self._update_mass_and_com(body_to_insert)

    def subdivide(self):
        """
        Splits this node into 8 children.
        """
        # note: this can break if two bodies have exactly the same position
        quarter = self.half_size / 2.0
        offsets = [
            (-quarter, -quarter, -quarter),
            ( quarter, -quarter, -quarter),
            (-quarter,  quarter, -quarter),
            ( quarter,  quarter, -quarter),
            (-quarter, -quarter,  quarter),
            ( quarter, -quarter,  quarter),
            (-quarter,  quarter,  quarter),
            ( quarter,  quarter,  quarter),
        ]

        self.children = []
        cx, cy, cz = self.center
        for dx, dy, dz in offsets:
            new_center = (cx + dx, cy + dy, cz + dz)
            self.children.append(OctreeNode(new_center, quarter))

    def cube_to_insert(self, body: Body) -> int:
        """
        Returns which child cube the body belongs in (0..7).
        """
        idx = 0
        cx, cy, cz = self.center
        if body.x >= cx:
            idx |= 1
        if body.y >= cy:
            idx |= 2
        if body.z >= cz:
            idx |= 4
        return idx

    def _insert_into_child(self, body: Body):
        """
        Helper used after subdividing: inserts a body into the correct child.
        """
        idx = self.cube_to_insert(body)
        self.children[idx].insert(body)

    def _update_mass_and_com(self, body: Body):
        """
        Updates this node's total mass and center of mass after inserting a body.
        """
        m = body.m
        x, y, z = body.x, body.y, body.z

        M = self.total_mass
        if M == 0.0:
            self.total_mass = m
            self.center_of_mass = (x, y, z)
            return

        new_M = M + m
        cx, cy, cz = self.center_of_mass
        self.center_of_mass = (
            (cx * M + x * m) / new_M,
            (cy * M + y * m) / new_M,
            (cz * M + z * m) / new_M,
        )
        self.total_mass = new_M

    def compute_accelerations(self, body: Body, theta: float, softening: float):
        """
        Computes acceleration contribution from this node on a target body.

        Uses Barnes–Hut rule:
        - if (s / d) < theta, treat node as one mass at center of mass
        - otherwise recurse into children
        """
        total_mass = self.total_mass
        children = self.children

        # empty node, or leaf node containing the same body
        if total_mass == 0.0 or (self.body is body and children is None):
            return (0.0, 0.0, 0.0)

        bx, by, bz = body.x, body.y, body.z
        cx, cy, cz = self.center_of_mass

        dx = cx - bx
        dy = cy - by
        dz = cz - bz

        soft2 = softening * softening
        dist2 = dx * dx + dy * dy + dz * dz + soft2
        if dist2 == 0.0:
            return (0.0, 0.0, 0.0)

        dist = math.sqrt(dist2)
        s = self.half_size * 2.0  # node width

        # approximation condition
        if children is None or (s / dist) < theta:
            inv_dist = 1.0 / dist
            inv_dist3 = inv_dist / dist2
            factor = G * total_mass * inv_dist3
            return (factor * dx, factor * dy, factor * dz)

        # otherwise recurse into children
        ax = ay = az = 0.0
        for child in children:
            if child.total_mass > 0.0:
                cax, cay, caz = child.compute_accelerations(body, theta, softening)
                ax += cax
                ay += cay
                az += caz

        return (ax, ay, az)