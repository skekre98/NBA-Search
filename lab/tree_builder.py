from anytree import Node
from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter
from anytree.search import find_by_attr

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
        cur_node = self.root
        while True:
            # If the node exists, we return False
            if cur_node.name == node.name:
                return False
            if node.val < cur_node.val:
                if cur_node.left:
                    cur_node = cur_node.left
                else:
                    cur_node.left = node
                    node.parent = cur_node
                    self.size += 1
                    break
            else:
                if cur_node.right:
                    cur_node = cur_node.right
                else:   
                    cur_node.right = node
                    node.parent = cur_node
                    self.size += 1
                    break
        return True

    # Function to remove node from tree 
    def pop(self, name):
        node = find_by_attr(self.root, name)
        # if the node doesn't exist, we return false
        if node is None:
            return False
        node.parent = None
        # if the node exists, we return True
        return True

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):
        RenderTreeGraph(self.root).to_picture(file + ".png")

