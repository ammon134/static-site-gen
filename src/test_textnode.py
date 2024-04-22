import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)


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


class TestSplitImages(unittest.TestCase):
    def test_success(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) and some more text",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_images([node])
        target_nodes = [
            TextNode("This is text with an ", TextType.text_type_text.value, None),
            TextNode(
                "image",
                TextType.text_type_image.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and ", TextType.text_type_text.value, None),
            TextNode(
                "another",
                TextType.text_type_image.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
            TextNode(" and some more text", TextType.text_type_text.value, None),
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_duplicate_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and some more text",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_images([node])
        target_nodes = [
            TextNode("This is text with an ", TextType.text_type_text.value, None),
            TextNode(
                "image",
                TextType.text_type_image.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextType.text_type_text.value, None),
            TextNode(
                "image",
                TextType.text_type_image.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and some more text", TextType.text_type_text.value, None),
        ]
        self.assertEqual(new_nodes, target_nodes)


class TestSplitLinks(unittest.TestCase):
    def test_success(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_links([node])
        target_nodes = [
            TextNode("This is text with a ", TextType.text_type_text.value, None),
            TextNode(
                "link",
                TextType.text_type_link.value,
                "https://www.example.com",
            ),
            TextNode(" and ", TextType.text_type_text.value, None),
            TextNode(
                "another",
                TextType.text_type_link.value,
                "https://www.example.com/another",
            ),
        ]
        self.assertEqual(new_nodes, target_nodes)

    def test_duplicate_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [link](https://www.example.com)",
            TextType.text_type_text.value,
        )
        new_nodes = split_nodes_links([node])
        target_nodes = [
            TextNode("This is text with a ", TextType.text_type_text.value, None),
            TextNode(
                "link",
                TextType.text_type_link.value,
                "https://www.example.com",
            ),
            TextNode(" and another ", TextType.text_type_text.value, None),
            TextNode(
                "link",
                TextType.text_type_link.value,
                "https://www.example.com",
            ),
        ]
        self.assertEqual(new_nodes, target_nodes)


class TestTextToTextNode(unittest.TestCase):
    def test_success(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        target_nodes = [
            TextNode("This is ", TextType.text_type_text.value),
            TextNode("text", TextType.text_type_bold.value),
            TextNode(" with an ", TextType.text_type_text.value),
            TextNode("italic", TextType.text_type_italic.value),
            TextNode(" word and a ", TextType.text_type_text.value),
            TextNode("code block", TextType.text_type_code.value),
            TextNode(" and an ", TextType.text_type_text.value),
            TextNode(
                "image",
                TextType.text_type_image.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.text_type_text.value),
            TextNode("link", TextType.text_type_link.value, "https://boot.dev"),
        ]

        self.assertEqual(new_nodes, target_nodes)


if __name__ == "__main__":
    unittest.main()
