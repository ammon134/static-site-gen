import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("a", "google.com", None, props)
        html = node.props_to_html()
        target_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html, target_html)


class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode("a", "google.com", props)
        html = node.to_html()
        target_html = '<a href="https://www.google.com" target="_blank">google.com</a>'
        self.assertEqual(html, target_html)

    def test_no_tag(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode(value="google.com", props=props, tag=None)
        html = node.to_html()
        target_html = "google.com"
        self.assertEqual(html, target_html)

    def test_no_props(self):
        node = LeafNode(value="This is a paragraph", props=None, tag="p")
        html = node.to_html()
        target_html = "<p>This is a paragraph</p>"
        self.assertEqual(html, target_html)


class TestParentNode(unittest.TestCase):
    def test(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        children = [
            LeafNode("b", "bold text"),
            LeafNode(None, "normal text"),
            LeafNode("i", "italic text"),
        ]
        node = ParentNode(tag="a", children=children, props=props)
        html = node.to_html()
        target_html = '<a href="https://www.google.com" target="_blank"><b>bold text</b>normal text<i>italic text</i></a>'
        self.assertEqual(html, target_html)

        outer_children = [
            LeafNode("b", "bold text"),
            node,
        ]
        outer_node = ParentNode(tag="p", children=outer_children, props=None)
        outer_html = outer_node.to_html()
        target_outer_html = "<p><b>bold text</b>" + target_html + "</p>"
        self.assertEqual(outer_html, target_outer_html)


if __name__ == "__main__":
    unittest.main()
