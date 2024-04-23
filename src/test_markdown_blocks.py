import unittest

from htmlnode import LeafNode, ParentNode
from markdown_blocks import BlockType, block_to_block_type, block_to_htmlnode
from textnode import text_node_to_html_node, text_to_textnodes


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        block = """## Heading 2"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_heading
        self.assertIs(block_type, target_block_type)

    def test_multiple_headings(self):
        block = """## Heading 2
        ### Heading 3"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_heading
        self.assertIsNot(block_type, target_block_type)

    def test_code(self):
        block = """```sh
        Code block
        ### Heading 3
        ```"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_code
        self.assertIs(block_type, target_block_type)

    def test_unbalanced_code_symbols(self):
        block = """```sh
            Code block
            ### Heading 3
            `"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_code
        self.assertIsNot(block_type, target_block_type)

    def test_quote(self):
        block = """> sh
        > Code block
        > ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_quote
        self.assertIs(block_type, target_block_type)

        block = """* sh
        * Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_u_list
        self.assertIs(block_type, target_block_type)

        block = """- sh
        - Code block
        - ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_u_list
        self.assertIs(block_type, target_block_type)

    def test_mixed_symbols(self):
        block = """- sh
        > Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_u_list
        self.assertIsNot(block_type, target_block_type)

        block = """- sh
        - Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_u_list
        self.assertIsNot(block_type, target_block_type)

        block = """> sh
        > Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_quote
        self.assertIsNot(block_type, target_block_type)

    def test_ordered_list(self):
        block = """1. sh
        2. Code block
        3. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_o_list
        self.assertIs(block_type, target_block_type)

    def test_ordered_list_increments(self):
        block = """1. sh
        2. Code block
        4. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_o_list
        self.assertIsNot(block_type, target_block_type)

        block = """2. sh
        3. Code block
        4. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_o_list
        self.assertIsNot(block_type, target_block_type)


class TestBlockToHTML(unittest.TestCase):
    def test_success(self):
        markdown = """This is some simple text 
        On another line

        # Heading 1

        ## Heading 2

        ```sh
        A code block
        ```
        > Some quote
        > Second line quote

        * Unordered item 1
        * Unordered item 2

        - Unordered item 3
        - Unordered item 4"""
        pass

    def test_paragraph(self):
        value = """This is some text
            On **another** line"""
        html_node = block_to_htmlnode(value)

        target_text_nodes = text_to_textnodes(value)
        target_children_nodes = []
        for node in target_text_nodes:
            target_children_nodes.append(text_node_to_html_node(node))
        target_html_node = ParentNode("p", target_children_nodes)

        self.assertEqual(html_node, target_html_node)

    def test_heading_block(self):
        value = """# Heading 1"""
        value2 = """## Heading 2"""
        html_node = block_to_htmlnode(value)
        html_node2 = block_to_htmlnode(value2)

        target_value = "Heading 1"
        target_value2 = "Heading 2"
        target_text_nodes = text_to_textnodes(target_value)
        target_text_nodes2 = text_to_textnodes(target_value2)

        target_children_nodes = []
        target_children_nodes2 = []
        for node in target_text_nodes:
            target_children_nodes.append(text_node_to_html_node(node))
        for node in target_text_nodes2:
            target_children_nodes2.append(text_node_to_html_node(node))
        target_html_node = ParentNode("h1", target_children_nodes)
        target_html_node2 = ParentNode("h2", target_children_nodes2)

        self.assertEqual(html_node, target_html_node)
        self.assertEqual(html_node2, target_html_node2)

    def test_code_block(self):
        value = """```sh
        A code block
        Second line
        ```"""
        html_node = block_to_htmlnode(value)

        target_value = "A code block\nSecond line"
        target_text_nodes = text_to_textnodes(target_value)

        target_children_nodes = []
        for node in target_text_nodes:
            target_children_nodes.append(text_node_to_html_node(node))
        target_html_node = ParentNode(
            "pre", [ParentNode("code", target_children_nodes)]
        )

        self.assertEqual(html_node, target_html_node)

    def test_quote_block(self):
        value = """> Some quote
        > Second line quote """
        html_node = block_to_htmlnode(value)

        target_value = "Some quote\nSecond line quote"
        target_text_nodes = text_to_textnodes(target_value)

        target_children_nodes = []
        for node in target_text_nodes:
            target_children_nodes.append(text_node_to_html_node(node))
        target_html_node = ParentNode("blockquote", target_children_nodes)

        self.assertEqual(html_node, target_html_node)

    def test_unordered_list_block(self):
        value = """- List item 1
        - Second list item """
        value2 = """* List item 1
        * Second *list* item """

        html_node = block_to_htmlnode(value)
        html_node2 = block_to_htmlnode(value2)

        target_children_nodes = [
            ParentNode("li", [LeafNode(None, "List item 1", None)]),
            ParentNode("li", [LeafNode(None, "Second list item", None)]),
        ]
        target_children_nodes2 = [
            ParentNode("li", [LeafNode(None, "List item 1", None)]),
            ParentNode(
                "li",
                [
                    LeafNode(None, "Second ", None),
                    LeafNode("i", "list", None),
                    LeafNode(None, " item", None),
                ],
            ),
        ]

        target_html_node = ParentNode("ul", target_children_nodes)
        target_html_node2 = ParentNode("ul", target_children_nodes2)

        self.assertEqual(html_node, target_html_node)
        self.assertEqual(html_node2, target_html_node2)

    def test_ordered_list_block(self):
        value = """1. List item 1
        2. Second list item 
        3. Third list item """

        html_node = block_to_htmlnode(value)

        target_children_nodes = [
            ParentNode("li", [LeafNode(None, "List item 1", None)]),
            ParentNode("li", [LeafNode(None, "Second list item", None)]),
            ParentNode("li", [LeafNode(None, "Third list item", None)]),
        ]

        target_html_node = ParentNode("ol", target_children_nodes)

        self.assertEqual(html_node, target_html_node)
