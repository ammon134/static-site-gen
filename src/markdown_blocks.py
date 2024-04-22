from enum import Enum
import re


class BlockType(Enum):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_unordered_list = "unordered_list"
    block_type_ordered_list = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()
    if len(lines) == 1 and re.match(r"#{1,6} ", lines[0]):
        return BlockType.block_type_heading

    if re.match(r"`{3}.*`{3}", block, re.DOTALL):
        return BlockType.block_type_code

    matches = re.findall(r"([*|\-|>]) ", block, re.MULTILINE)
    if matches:
        symbol = matches[0]
        for match in matches:
            if match != symbol:
                return BlockType.block_type_paragraph
        if symbol == ">":
            return BlockType.block_type_quote
        if symbol == "*" or symbol == "-":
            return BlockType.block_type_unordered_list

    matches = re.findall(r"(\d+)\. ", block, re.MULTILINE)
    if matches:
        expected_num = 1
        is_ordered = True
        for match in matches:
            if int(match) != expected_num:
                is_ordered = False
                break
            expected_num += 1
        if is_ordered:
            return BlockType.block_type_ordered_list

    return BlockType.block_type_paragraph


def markdown_to_block(markdown: str) -> list[str]:
    output: list[str] = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip(" \n")
        if block != "":
            output.append(block)

    return output
