from enum import Enum
import re

from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_u_list = "unordered_list"
    block_type_o_list = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    if len(lines) == 1 and re.match(r"#{1,6} ", lines[0]):
        return BlockType.block_type_heading

    matches = re.findall(r"([*|\-|>]) ", block, re.MULTILINE)
    if matches:
        symbol = matches[0]
        for line in lines:
            if not line.strip().startswith(symbol):
                return BlockType.block_type_paragraph
        if symbol == ">":
            return BlockType.block_type_quote
        if symbol == "*" or symbol == "-":
            return BlockType.block_type_u_list

    if re.match(r"`{3}.*`{3}", block, re.DOTALL):
        return BlockType.block_type_code

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
            return BlockType.block_type_o_list

    return BlockType.block_type_paragraph


def markdown_to_block(markdown: str) -> list[str]:
    output: list[str] = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip(" \n")
        if block != "":
            output.append(block)

    return output


def block_to_htmlnode(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.block_type_heading:
        return heading_to_htmlnode(block)
    if block_type == BlockType.block_type_code:
        return code_to_htmlnode(block)
    if block_type == BlockType.block_type_quote:
        return quote_to_htmlnode(block)
    if block_type == BlockType.block_type_u_list:
        return unordered_list_to_htmlnode(block)
    if block_type == BlockType.block_type_o_list:
        return ordered_list_to_htmlnode(block)

    return paragraph_to_htmlnode(block)


def paragraph_to_htmlnode(text: str) -> HTMLNode:
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))

    return ParentNode("p", children_nodes)


def heading_to_htmlnode(text: str) -> HTMLNode:
    match = re.match(r"(#{1,6}) ", text)
    if not match:
        raise Exception("invalid syntax - heading")

    text = text.lstrip(match.group(1) + " ")
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))

    level = str.count(match.group(1), "#")

    return ParentNode(f"h{level}", children_nodes, None)


def code_to_htmlnode(text: str) -> HTMLNode:
    lines = text.splitlines()
    if len(lines) < 2:
        raise Exception("invalid syntax - code")

    lines = lines[1:-1]
    text_lines = []
    for line in lines:
        text_lines.append(line.strip())

    text_nodes = text_to_textnodes("\n".join(text_lines))
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))

    return ParentNode("pre", [ParentNode("code", children_nodes, None)], None)


def quote_to_htmlnode(text: str) -> HTMLNode:
    lines = text.splitlines()
    text_lines = []
    for line in lines:
        text_lines.append(line.strip("> "))

    text_nodes = text_to_textnodes("\n".join(text_lines))
    children_nodes = []
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))

    return ParentNode("blockquote", children_nodes, None)


def unordered_list_to_htmlnode(text: str) -> HTMLNode:
    lines = text.splitlines()

    ul_children_nodes = []
    for line in lines:
        line = line.strip("*- ")
        text_nodes = text_to_textnodes(line)

        li_children_nodes = []
        for node in text_nodes:
            li_children_nodes.append(text_node_to_html_node(node))

        ul_children_nodes.append(ParentNode("li", li_children_nodes))

    return ParentNode("ul", ul_children_nodes, None)


def ordered_list_to_htmlnode(text: str) -> HTMLNode:
    lines = text.splitlines()

    ul_children_nodes = []
    for line in lines:
        line = line.strip()
        splits = re.split(r"^\d\. ", line, 1)
        line = splits[-1]
        text_nodes = text_to_textnodes(line)

        li_children_nodes = []
        for node in text_nodes:
            li_children_nodes.append(text_node_to_html_node(node))

        ul_children_nodes.append(ParentNode("li", li_children_nodes))

    return ParentNode("ol", ul_children_nodes, None)
