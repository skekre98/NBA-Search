from anytree import Node
from anytree.exporter import DotExporter
from graphviz import Source, render


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
        # pointer for the current node
        currNode = self.root
        while True:
            # if value of node to be added is greater, go right
            if node.val > currNode.val:
                # if right child exists, go right
                if currNode.right != None:
                    currNode = currNode.right
                # if no right child, add node as right child
                else:
                    currNode.right = node
                    node.parent = currNode
                    break
            # else, go left
            else:
                # if left child exists, go left
                if currNode.left != None:
                    currNode = currNode.left
                # if no left child, add node as left child and break
                else:
                    currNode.left = node
                    node.parent = currNode
                    break

        return

    # Function to remove node from tree
    def pop(self, name):
        # TODO
        pass

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):

        # export to dot file
        DotExporter(self.root).to_dotfile(file+".dot")
        Source.from_file(file+'.dot')
        # render as png
        render('dot', 'png', file+'.dot')
        return
