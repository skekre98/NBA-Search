
from anytree import Node
from anytree.exporter import DotExporter
from anytree.search import find_by_attr
from anytree import RenderTree

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
        self.all = []
        self.size = 0

    # Function to push to tree 
    def push(self, node):
        def insert(current_node, node):
            if node.value < current_node.val:
                if current_node.left != None:  # Left child
                    insert(current_node.left, node)
                else:
                    current_node.left = node
                    self.size += 1
            elif node.value > current_node.val:
                if current_node.right != None:  # Right child
                    insert(current_node.right, node)
                else:
                    current_node.right = node
                    self.size += 1
            else:
                # Value already exists in the tree, do nothing
                pass

        insert(self.root, node)
        self.all.append(node.name)

    # Function to remove node from tree 
    def pop(self, name):
        def delete(nodeDel):
            node = find_by_attr(self.root, name)
            node.parent = None
            return

        # Find the node to delete
        nodeDel = name in self.all
        if nodeDel:
            delete(name)

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):
        file_path = f"{file}.png"
        DotExporter(self.root).to_picture(file_path)
        print(f"Tree exported to {file_path}")

    