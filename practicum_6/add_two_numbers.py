from __future__ import annotations
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import yaml


@dataclass
class Element:
    key: Any
    data: Any = None
    next: Element = None
    prev: Element = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Element = None

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        x = self.head
        node_keys = []
        while x is not None:
            node_keys.append(str(x.key))
            x = x.next
        return " <-> ".join(node_keys)

    def empty(self):
        return self.head is None

    def search(self, k: Element) -> Optional[Element]:
        x = self.head
        while (x is not None) and (x.key != k.key):
            x = x.next
        return x

    def insert(self, x: Element) -> None:
        x.next = self.head
        if self.head is not None:
            self.head.prev = x
        self.head = x
        x.prev = None

    def remove(self, x: Element) -> None:
        if x.prev is not None:
            x.prev.next = x.next
        else:
            self.head = x.next

        if x.next is not None:
            x.next.prev = x.prev

    @staticmethod
    def is_tail(x):
        return x.next is None


def add_two_numbers(l1: DoublyLinkedList, l2: DoublyLinkedList) -> DoublyLinkedList:
    e1 = l1.head
    e2 = l2.head
    out = DoublyLinkedList
    ost = 0

    while e1 is not None and e2 is not None:
        out.insert((ost + e1.data + e2.data) % 10)
        ost = (ost + e1.data + e2.data) // 10
        e1 = e1.next
        e2 = e2.next

    if e1 is None and e2 is None and ost == 0:
        return out

    last_el = 0
    if e1 is not None:
        la

if __name__ == "__main__":
    # Let's solve Add Two Numbers problem from leetcode.com:
    # https://leetcode.com/problems/add-two-numbers/description/

    # l = DoublyLinkedList()
    # l.insert(Element(key=1))
    # l.insert(Element(key=2))
    # l.insert(Element(key=3))
    # l.insert(Element(key=4))
    # e = l.search(Element(key=3))
    # l.remove(e)

    with open("practicum_6/add_two_numbers_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    for c in cases:
        l1 = read_from_str(c["input"]["a"])
        l2 = read_from_str(c["input"]["b"])
        l_sum_true = read_from_str(c["output"])
        l_sum = add_two_numbers(l1, l2)
        print(
            f"Input: a = {c['input']['a']}, b = {c['input']['b']}. "
            f"Output: {l_sum}. "
            f"Expected output: {l_sum_true}"
        )
