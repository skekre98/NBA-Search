# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        # TODO
        pass

    # Function to remove node from tree
    def pop(self, name):
        # TODO
        pass

    # Function to export tree as png(Use DotExporter)
    def export(self, file="tree"):
        # TODO
        pass
