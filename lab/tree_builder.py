from anytree import Node as AnyNode, RenderTree
from anytree.exporter import DotExporter

class TreeNode:
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self.left = None
        self.right = None

class TreeBuilder(object):

    def __init__(self, root):
        self.root = root
        self.size = 0

    def push(self, node):
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)
        self.size += 1

    def _insert(self, current, node):
        if node.val < current.val:
            if current.left is None:
                current.left = node
            else:
                self._insert(current.left, node)
        else:
            if current.right is None:
                current.right = node
            else:
                self._insert(current.right, node)

    def pop(self, value):
        self.root = self._remove(self.root, value)

    def _remove(self, current, value):
        if not current:
            return current
        if value < current.val:
            current.left = self._remove(current.left, value)
        elif value > current.val:
            current.right = self._remove(current.right, value)
        else:
            if not current.left:
                return current.right
            elif not current.right:
                return current.left

            temp = self._min_value_node(current.right)
            current.val = temp.val
            current.right = self._remove(current.right, temp.val)
        return current

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def export(self, file="tree"):
        anytree_root = self._convert_to_anytree(self.root)
        DotExporter(anytree_root).to_picture(f"{file}.png")

    def _convert_to_anytree(self, node):
        if not node:
            return None
        anytree_node = AnyNode(node.name)
        children = [self._convert_to_anytree(node.left), self._convert_to_anytree(node.right)]
        anytree_node.children = [child for child in children if child is not None]
        return anytree_node
