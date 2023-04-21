from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import ctypes

import yaml


@dataclass
class Element:
    key: Any
    data: Any = None
    np: int = None

    def next(self, prev_np) -> Element:
        a = ctypes.cast(self.np ^ prev_np, ctypes.py_object).value
        return ctypes.cast(self.np ^ prev_np, ctypes.py_object).value

    def prev(self, next_np) -> Element:
        return ctypes.cast(self.np ^ next_np, ctypes.py_object).value


def id_to_el(id: int) -> Any:
    return ctypes.cast(id, ctypes.py_object).value


class XorDoublyLinkedList:
    def __init__(self) -> None:
        self.head: Element = None
        self.tail: Element = None
        self.ids = list()  # Нужно, чтобы нам не мешал сборщик  мусора
        pass

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        node_keys = []
        cur_el = self.head
        prev_id = 0
        if cur_el is None:
            return ""
        while id(cur_el.next(prev_id)) != prev_id:
            node_keys.append(cur_el.key)
            i = id(cur_el)
            cur_el = cur_el.next(prev_id)
            prev_id = i
        return " <-> ".join(node_keys)

    def to_pylist(self) -> list[Any]:
        py_list = []
        next_el: Element = self.head()
        while next_el is not None:
            py_list.append(next_el.key)
            next_el = next_el.next()
        return py_list

    def empty(self):
        return self.head is None

    def search(self, k: Any) -> Element:
        """Complexity: O(n)"""
        print(self)
        cur_id = 0
        next_el: Element = self.head
        while next_el != self.tail:
            if next_el.key == k:
                break
            next_el, cur_id = next_el.next(cur_id), id(next_el)
        return next_el

    def insert(self, x: Element) -> None:
        """Insert to the front of the list (i.e., it is 'prepend')
        Complexity: O(1)
        """
        x = Element(key=x)
        self.ids.append(id(x))

        if self.head is None:
            self.head = self.tail = x
            return

        if self.head.np is not None:
            self.head.np = self.head.np ^ id(x)
        else:
            self.head.np = id(x)
        x.np = id(self.head)
        self.head = x

    def remove(self, x: Any) -> None:
        """Remove x from the list
        Complexity: O(1)
        """
        if x is None:
            return

        if self.tail is None:
            raise NameError

        self.ids.remove(id(self.search(x)))

        # Code from "search"

        cur_id = 0
        next_el: Element = self.head
        while next_el != self.tail:
            if next_el.key == x:
                break
            next_el, cur_id = next_el.next(cur_id), id(next_el)

        # renaming variables to ...
        cur_el = next_el
        prev_id = cur_id
        next_el = cur_el.next(prev_id)

        next_el.np = prev_id ^ id(next_el.next(id(cur_el)))
        id_to_el(prev_id).np = id(id_to_el(prev_id).prev(id(cur_el))) ^ id(next_el)

    def reverse(self) -> XorDoublyLinkedList:
        """Returns the same list but in the reserved order
        Complexity: O(1)
        """
        ret = self
        ret.head, ret.tail = ret.tail, ret.head
        return ret


if __name__ == "__main__":
    # You need to implement a doubly linked list using only one pointer
    # self.np per element. In python, by pointer, we understand id(object).
    # Any object can be accessed via its id, e.g.
    # >>> import ctypes
    # >>> a = ...
    # >>> ctypes.cast(id(a), ctypes.py_object).value
    # Hint: assuming that self.next and self.prev store pointers
    # define self.np as self.np = self.next XOR self.prev

    with open("practicum_6/homework/xor_list_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    for i, c in enumerate(cases):
        l = XorDoublyLinkedList()
        for el in reversed(c["input"]["list"]):
            l.insert(el)
        for op_info in c["input"]["ops"]:
            if op_info["op"] == "insert":
                l.insert(op_info["key"])
            elif op_info["op"] == "remove":
                l.remove(op_info["key"])
            elif op_info["op"] == "reverse":
                l = l.reverse()
        py_list = l.to_pylist()
        print(f"Case #{i + 1}: {py_list == c['output']}")
