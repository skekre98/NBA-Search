from anytree import Node
from anytree.search import find_by_attr
from anytree.dotexport import RenderTreeGraph

class TreeNode(Node):

    def __init__(self, name, val):
        super().__init__(name)
        self.val = val
        self.left = None
        self.right = None


class TreeBuilder(object):

    def __init__(self, root):
        self.root = root
        self.size = 0

    # Function to push to tree 
    def push(self, node):
        currentNode = self.root
        while True:
            if node.val < currentNode.val:
                if currentNode.left:
                    currentNode = currentNode.left
                else:
                    currentNode.left = node
                    node.parent = currentNode
                    self.size += 1
                    break
            else:
                if currentNode.right:
                    currentNode = currentNode.right
                else: 
                    currentNode.right = node
                    node.parent = currentNode
                    self.size += 1
                    break

    # Function to remove node from tree 
    def pop(self, name):
        node = find_by_attr(self.root, name)
        node.parent = None

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):
        RenderTreeGraph(self.root).to_picture(file+".png")
