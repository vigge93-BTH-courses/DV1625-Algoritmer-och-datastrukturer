"""Red and black balanced binary tree module."""
from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional, Union


class RedBlackTree:
    """Red and black binary tree."""

    def __init__(self) -> None:
        """Create empty red and black binary tree."""
        self.nil = Node(None)
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.color = Color.BLACK
        self.root = self.nil

    def _inorder_tree_walk(self, x: Node) -> List[List[Union[float, str]]]:
        res = []
        left = []
        right = []
        if x is not self.nil:
            left = self._inorder_tree_walk(x.left)
            res.append([x.key, x.color.name, x.left.key, x.right.key])
            right = self._inorder_tree_walk(x.right)
        return left + res + right

    def _left_rotate(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x: Node) -> None:
        y = x.left
        x.left = y.right
        if y.right is not self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, k: float) -> None:
        """Insert value into tree."""
        if self._search_node(k) is not self.nil:
            return
        z = Node(k, self.nil)
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.color = Color.RED
        self._insert_fixup(z)

    def _insert_fixup(self, z: Node) -> None:
        while z.parent.color is Color.RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color is Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color is Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._left_rotate(z.parent.parent)
        self.root.color = Color.BLACK

    def _transplant(self, u: Node, v: Node) -> None:
        if u.parent is self.nil:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def remove(self, k: float) -> None:
        """Remove value from tree."""
        z = self._search_node(k)
        y = z
        y_orig_color = y.color
        if z.left is self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._tree_minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_orig_color is Color.BLACK:
            self._remove_fixup(x)

    def _tree_minimum(self, x: Node) -> Node:
        """Find the minimum value for the descendant of a node."""
        while x.left is not self.nil:
            x = x.left
        return x

    def _remove_fixup(self, x: Node) -> None:
        while x is not self.root and x.color is Color.BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if (w.left.color is Color.BLACK
                        and w.right.color is Color.BLACK):
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color is Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if (w.right.color is Color.BLACK
                        and w.left.color is Color.BLACK):
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color is Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def search(self, k: float) -> bool:
        """Check if tree contains value."""
        x = self.root
        while x is not self.nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x is not self.nil

    def _search_node(self, k: float) -> Node:
        x = self.root
        while x is not self.nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def path(self, k: float) -> List[float]:
        """Return the path through the tree to the value."""
        x = self.root
        if x is self.nil:
            return []
        path = [x.key]
        while x is not self.nil and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
            path.append(x.key)
        return path

    def min(self) -> Optional[float]:
        """Find the minimum value in the tree."""
        x = self.root
        k = None
        while x is not self.nil:
            k = x.key
            x = x.left
        return k

    def max(self) -> Optional[float]:
        """Find the maximum value in the tree."""
        x = self.root
        k = None
        while x is not self.nil:
            k = x.key
            x = x.right
        return k

    def bfs(self) -> List[List[Union[float, str]]]:
        """Walk through the tree and print each node in order."""
        x = self.root
        return self._inorder_tree_walk(x)


class Node:
    """Red and black tree node."""

    def __init__(self, key: float, nil: Node = None):
        """Create a red and black tree node with optional nil sentinel."""
        self.key = key
        self.left = nil
        self.right = nil
        self.parent = nil
        self.color = None


class Color(Enum):
    """Color enum."""

    RED = auto()
    BLACK = auto()
