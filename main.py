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

    def preorder(self):
        match self:
            case BTree(None, _, _):
                pass
            case BTree(data, left, right):
                yield data
                for l in left.preorder():
                    yield l
                for r in right.preorder():
                    yield r

    def tolist(self):
        return [data for data in self.inorder()]

    def map(self, f):
        # f(x) unary function
        newtree = BTree()
        for node in self.preorder():
            newtree.insert(f(node))
        return newtree

    def fold(self, f, default):
        # f(x, y) associative, commutative binary function
        acc = default
        for node in self.inorder():
            acc = f(acc, node)
        return acc

    def depth(self):
        match self:
            case BTree(None, _, _):
                return 0
            case BTree(_, left, right):
                return 1 + max(left.depth(), right.depth())

    def balance(self):
        match self:
            case BTree(None, _, _):
                return 0
            case BTree(_, left, right):
                return right.depth() - left.depth()

    def validate(self):
        match self:
            case BTree(None, _, _):
                pass
            case BTree(data, left, right):

                try:
                    if left.data >= data:
                        raise ValueError(f"Left side {left.data} is bigger than current node {data}")
                except TypeError:
                    pass

                try:
                    if right.data < data:
                        raise ValueError(f"Right side {right.data} is smaller than current node {data}")
                except TypeError:
                    pass


def main():
    tree_unbalanced = BTree()
    tree_unbalanced.append([0, 1, 2, 3, 4, 5, 6])

    tree_balanced = BTree()
    tree_balanced.append([3, 1, 5, 0, 2, 4, 6])

    tree_unbalanced.validate()
    print(f"Unbalanced tree has depth {tree_unbalanced.depth()}")
    print(f"Unbalanced tree has balance factor {tree_unbalanced.balance()}")

    tree_balanced.validate()
    print(f"Balanced tree has depth {tree_balanced.depth()}")
    print(f"Balanced tree has balance factor {tree_balanced.balance()}")


if __name__ == '__main__':
    main()
