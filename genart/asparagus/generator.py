from itertools import islice
from math import pi

import numpy as np
from genart.asparagus.models import Branch


def generate_asparagus(start: np.array, end: np.array) -> Branch:
    main_branch = Branch(start, end)

    return branch_recursive(main_branch, 300.0)


def branch_recursive(
    branch: Branch, max_length: float, depth: int = 0, max_depth: int = 3
):
    step_size = branch.length() / 10.0

    angle_modifier = 1.0
    length_modifier = 1.0

    # Always skip the first step(s) of walk_along, it's on the parent branch:
    for bud in islice(branch.walk_along(step_size), 2, None):
        child_length = length_modifier * max_length
        child_angle = angle_modifier * (pi / 2)
        child = branch.branch_at(bud, child_length, child_angle)
        branch.children.append(child)
        angle_modifier *= -0.95
        length_modifier *= 0.90

        if depth < max_depth:
            branch_recursive(child, 0.3 * child_length, depth + 1)

    return branch