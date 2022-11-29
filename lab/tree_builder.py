from anytree import Node
from anytree.exporter import DotExporter

class TreeNode(Node):

    def __init__(self, name, val):
        super().__init__(name)
        self.val = val
        self.left = None
        self.right = None


class TreeBuilder(object):

    def __init__(self, root):
        # root will be type TreeNode
        self.root = root
        self.size = 0

     # Function to push to tree 
    def push(self, node):
        self.root = pushHelper(self, self.root, node)
        return self.root

    def pushHelper(self, root, node):
        if root == None:
            root = node
        else:
            if root.val == node.val:
                return root
            elif root.val < node.val:
                root.right = pushHelper(self, root.right, node)
            else:
                root.left = pushHelper(self, root.left, node)
        return root

    # Function to remove node from tree 
    def pop(self, name):
        # TODO
        pass

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):
        # TODO 
        pass