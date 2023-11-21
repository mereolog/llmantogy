from enum import Enum


class ProverResult(Enum):
    CONSISTENT = 1
    INCONSISTENT = 2
    UNDECIDED = 3
    THEOREM = 4
    COUNTERSATISFIABLE = 5