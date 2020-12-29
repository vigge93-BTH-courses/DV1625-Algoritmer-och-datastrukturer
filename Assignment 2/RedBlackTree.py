from enum import Enum, auto


class RedBlackTree:

    def __init__(self):
        self.root = None

    def inorder_tree_walk(self, x):
        if x is not None:
            self.inorder_tree_walk(x.left)
            print(x.key)
            self.inorder_tree_walk(x.right)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        raise NotImplementedError

    def insert(self, z):
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.color = Color.RED
        self.rb_insert_fixup(z)

    def rb_insert_fixup(self, z):
        while z.parent.color is Color.RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.left
                if y.color is Color.RED:
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                elif z is z.parent.right:
                    z = z.parent
                    self.left_rotate(z)
                z.parent.color = Color.BLACK
                z.parent.parent.color = Color.RED
                self.right_rotate(z.parent.parent)
            else:
                raise NotImplementedError
        self.root.color = Color.BLACK

    def rb_transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.p = u.p

    def remove(self, z):
        y = z
        y_orig_color = y.color
        if z.left is None:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_orig_color is Color.BLACK:
            self.rb_remove_fixup(x)

    def rb_remove_fixup(self, x):
        while x is not self.root and x.color is Color.BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color is Color.RED:
                    w.color = Color.BLACK
                    x.p.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color is Color.BLACK and w.right.color is Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                elif w.right.color is Color.BLACK:
                    w.left.color = Color.BLACK
                    w.color = Color.RED
                    self.right_rotate(w)
                    w = x.parent.right
                w.color = x.parent.Color
                x


class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = None


class Color(Enum):
    RED = auto()
    BLACK = auto()
