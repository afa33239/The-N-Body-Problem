#allows interchangeable solver implementations

class Solver:
    def accelerations(self, bodies, cfg):
        raise NotImplementedError()