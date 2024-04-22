import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "boot.dev")
        self.assertNotEqual(node, node2)


class TestSplitInlineMarkdown(unittest.TestCase):
    def test_success(self):
        node = TextNode(
            "This is text with a `code block` with a few words",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.text_type_code.value)
        target_nodes = [
            TextNode("This is text with a ", TextType.text_type_text.value, None),
            TextNode("code block", TextType.text_type_code.value, None),
            TextNode(" with a few words", TextType.text_type_text.value, None),
        ]
        self.assertEqual(new_nodes, target_nodes)

        node = TextNode(
            "This is text with a `code block` with **a few** words",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.text_type_bold.value)
        target_nodes = [
            TextNode(
                "This is text with a `code block` with ",
                TextType.text_type_text.value,
                None,
            ),
            TextNode("a few", TextType.text_type_bold.value, None),
            TextNode(" words", TextType.text_type_text.value, None),
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_valid_delimiter(self):
        node = TextNode(
            "This is text with a `code block` with a few words",
            TextType.text_type_text.value,
        )
        self.assertRaises(
            (Exception),
            split_nodes_delimiter,
            [node],
            "'",
            TextType.text_type_code.value,
        )

    def test_closing_delimiter(self):
        node = TextNode(
            "This is **text with a `code block` with **a few** words",
            TextType.text_type_text.value,
        )
        self.assertRaises(
            (Exception),
            split_nodes_delimiter,
            [node],
            "**",
            TextType.text_type_bold.value,
        )

    def test_node_not_text(self):
        node = TextNode(
            "This is text with a `code block` with **a few** words",
            TextType.text_type_text.value,
        )
        node_image = TextNode(
            "This is an image", TextType.text_type_image.value, "https://google.com"
        )
        new_nodes = split_nodes_delimiter(
            [node, node_image], "**", TextType.text_type_bold.value
        )
        target_nodes = [
            TextNode(
                "This is text with a `code block` with ",
                TextType.text_type_text.value,
                None,
            ),
            TextNode("a few", TextType.text_type_bold.value, None),
            TextNode(" words", TextType.text_type_text.value, None),
            node_image,
        ]
        self.assertEqual(new_nodes, target_nodes)


if __name__ == "__main__":
    unittest.main()
