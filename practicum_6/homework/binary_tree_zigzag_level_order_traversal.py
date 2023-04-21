from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from collections.abc import Iterable

import yaml


def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
    out = [[root]]
    while out[-1] != [None] * len(out[-1]):

        new = []
        for e in out[-1]:
            if e is None:
                new += [None] * 2
                continue
            new.append(e.left)
            new.append(e.right)
        out.append(new)
    out = list(map(lambda x: list(map(lambda z: z.val, list(filter(lambda y: y is not None, x)))), out))
    out = [out[e][::(-1) ** e] for e in range(len(out) - 1)]
    return out





if __name__ == "__main__":
    # Let's solve Binary Tree Zigzag Level Order Traversal problem from leetcode.com:
    # https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
    # First, implement build_tree() to read a tree from a list format to our class
    # Second, implement BinaryTree.zigzag_traversal() returning the list required by the task
    # Avoid recursive traversal!

    with open(
        "practicum_6/homework/binary_tree_zigzag_level_order_traversal_cases.yaml", "r"
    ) as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        bt = build_tree(c["input"])
        zz_traversal = bt.zigzag_level_order_traversal()
        print(f"Case #{i + 1}: {zz_traversal == c['output']}")
