import unittest

from markdown_blocks import BlockType, block_to_block_type


class TestHeadings(unittest.TestCase):
    def test_success(self):
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


class TestCode(unittest.TestCase):
    def test_success(self):
        block = """```sh
        Code block
        ### Heading 3
        ```"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_code
        self.assertIs(block_type, target_block_type)

    def test_unbalanced_quote_symbols(self):
        block = """```sh
            Code block
            ### Heading 3
            `"""
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_code
        self.assertIsNot(block_type, target_block_type)


class TestQuoteUnorderedList(unittest.TestCase):
    def test_success(self):
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
        target_block_type = BlockType.block_type_unordered_list
        self.assertIs(block_type, target_block_type)

        block = """- sh
        - Code block
        - ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_unordered_list
        self.assertIs(block_type, target_block_type)

    def test_mixed_symbols(self):
        block = """- sh
        > Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_unordered_list
        self.assertIsNot(block_type, target_block_type)

        block = """- sh
        - Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_unordered_list
        self.assertIsNot(block_type, target_block_type)

        block = """> sh
        > Code block
        * ### Heading 3 """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_quote
        self.assertIsNot(block_type, target_block_type)


class TestOrderedList(unittest.TestCase):
    def test_success(self):
        block = """1. sh
        2. Code block
        3. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_ordered_list
        self.assertIs(block_type, target_block_type)

    def test_list_increments(self):
        block = """1. sh
        2. Code block
        4. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_ordered_list
        self.assertIsNot(block_type, target_block_type)

        block = """2. sh
        3. Code block
        4. ### Heading 3
        """
        block_type = block_to_block_type(block)
        target_block_type = BlockType.block_type_ordered_list
        self.assertIsNot(block_type, target_block_type)
