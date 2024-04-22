from enum import Enum
import re

from htmlnode import LeafNode


class TextType(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"


class DelimiterType(Enum):
    delimiter_type_bold = "**"
    delimiter_type_italic = "*"
    delimiter_type_code = "`"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag: str | None = None
    value: str | None = text_node.text
    props: dict[str, str] | None = None
    match text_node.text_type:
        case TextType.text_type_bold.value:
            tag = "b"
        case TextType.text_type_italic.value:
            tag = "i"
        case TextType.text_type_code.value:
            tag = "code"
        case TextType.text_type_link.value:
            if not text_node.url:
                raise Exception("link url missing")
            tag = "a"
            props = {"href": text_node.url}
        case TextType.text_type_image.value:
            if not text_node.url:
                raise Exception("image url missing")
            tag = "img"
            props = {"src": text_node.url, "alt": text_node.text}
        case _:
            raise Exception("text_type of text_node is not valid")
    return LeafNode(tag=tag, value=value, props=props)


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.text_type_text.value)]
    nodes = split_nodes_delimiter(
        nodes, DelimiterType.delimiter_type_bold.value, TextType.text_type_bold.value
    )
    nodes = split_nodes_delimiter(
        nodes,
        DelimiterType.delimiter_type_italic.value,
        TextType.text_type_italic.value,
    )
    nodes = split_nodes_delimiter(
        nodes, DelimiterType.delimiter_type_code.value, TextType.text_type_code.value
    )
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    if delimiter not in DelimiterType:
        raise Exception("invalid markdown syntax")

    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.text_type_text.value:
            new_nodes.append(node)
            continue

        temp = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 != 1:
            raise Exception("invalid markdown syntax")

        for i, split in enumerate(splits):
            if i % 2 != 0:
                temp.append(TextNode(split, text_type))
            else:
                temp.append(TextNode(split, TextType.text_type_text.value))

        new_nodes.extend(temp)

    return new_nodes


def split_nodes_images(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.text_type_text.value:
            new_nodes.append(node)
            continue

        image_tuples = extract_markdown_images(node.text)
        if len(image_tuples) == 0:
            new_nodes.append(node)
            continue

        temp = []
        node_text = node.text
        for tuple in image_tuples:
            delimiter = f"![{tuple[0]}]({tuple[1]})"
            splits = node_text.split(delimiter, 1)

            if splits[0] != "":
                temp.append(TextNode(splits[0], TextType.text_type_text.value))

            temp.append(TextNode(tuple[0], TextType.text_type_image.value, tuple[1]))
            node_text = splits[1]

        if node_text != "":
            temp.append(TextNode(node_text, TextType.text_type_text.value))

        new_nodes.extend(temp)

    return new_nodes


def split_nodes_links(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.text_type_text.value:
            new_nodes.append(node)
            continue

        link_tuples = extract_markdown_links(node.text)
        if len(link_tuples) == 0:
            new_nodes.append(node)
            continue

        temp = []
        node_text = node.text
        for tuple in link_tuples:
            delimiter = f"[{tuple[0]}]({tuple[1]})"
            splits = node_text.split(delimiter, 1)

            if splits[0] != "":
                temp.append(TextNode(splits[0], TextType.text_type_text.value))

            temp.append(TextNode(tuple[0], TextType.text_type_link.value, tuple[1]))
            node_text = splits[1]

        if node_text != "":
            temp.append(TextNode(node_text, TextType.text_type_text.value))

        new_nodes.extend(temp)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
