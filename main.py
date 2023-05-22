from dataclasses import dataclass
from typing import Any, Optional, Self


@dataclass
class BTree:
    data: Any = None
    left: Optional[Self] = None
    right: Optional[Self] = None

    def insert(self, a):
        match self:
            case BTree(None, _, _):
                self.data = a
                self.left = BTree()
                self.right = BTree()
            case BTree(data, left, right):
                if a < data:
                    left.insert(a)
                else:
                    right.insert(a)

    def append(self, data):
        for a in data:
            self.insert(a)

    def inorder(self):
        match self:
            case BTree(None, _, _):
                pass
            case BTree(data, left, right):
                for l in left.inorder():
                    yield l
                yield data
                for r in right.inorder():
                    yield r

    def tolist(self):
        return [data for data in self.inorder()]

    def reorder(self):
        newroot = BTree()
        newroot.append(self.inorder())
        self.data = newroot.data
        self.left = newroot.left
        self.right = newroot.right

    def map(self, f):
        # f(x) unary function
        newtree = BTree()
        for node in self.inorder():
            newtree.insert(f(node))
        return newtree

    def fold(self, f, default):
        # f(x, y) associative, commutative binary function
        acc = default
        for node in self.inorder():
            acc = f(acc, node)
        return acc


def main():
    tree = BTree()
    tree.insert(5)
    tree.insert(1)
    tree.insert(10)
    tree.insert(-2)

    square_tree = tree.map(lambda x: x**2)
    print(tree.tolist())

    print(square_tree.tolist())

    print(f"Sum of values is {tree.fold(lambda x,y: x+y, 0)}")
    print(f"Largest value is {tree.fold(lambda x,y: max(x, y), -10000)}")
    print(f"Sum of squared values is {square_tree.fold(lambda x,y:x+y, 0)}")


if __name__ == '__main__':
    main()
