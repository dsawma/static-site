import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is the third node", TextType.CODE)
        self.assertNotEqual(node2, node3)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()