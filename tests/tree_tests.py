import unittest
import os
from lab.tree_builder import TreeBuilder, TreeNode

class TestTreeBuilder(unittest.TestCase):

    def test_push(self):
        root = TreeNode("root", 10)
        tree = TreeBuilder(root)
        tree.push(TreeNode("left", 5))
        tree.push(TreeNode("right", 15))
        self.assertEqual(tree.root.left.val, 5)
        self.assertEqual(tree.root.right.val, 15)

    def test_pop(self):
        root = TreeNode("root", 10)
        tree = TreeBuilder(root)
        tree.push(TreeNode("left", 5))
        tree.push(TreeNode("right", 15))
        tree.pop(5)
        self.assertIsNone(tree.root.left)
        tree.pop(10)
        self.assertEqual(tree.root.val, 15)

    def test_export(self):
        root = TreeNode("root", 10)
        tree = TreeBuilder(root)
        tree.push(TreeNode("left", 5))
        tree.push(TreeNode("right", 15))
        tree.export("test_tree")
        self.assertTrue(os.path.exists("test_tree.png"))
        os.remove("test_tree.png")

if __name__ == '__main__':
    unittest.main()
