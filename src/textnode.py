from enum import Enum

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


def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    if delimiter not in DelimiterType:
        raise Exception("invalid markdown syntax")

    new_nodes = []
    for i, node in enumerate(nodes):
        if node.text_type is not TextType.text_type_text.value:
            new_nodes.append(node)
            continue

        temp = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 != 1:
            raise Exception("invalid markdown syntax")

        for i, split in enumerate(splits):
            if i % 2 == 0:
                temp.append(TextNode(split, TextType.text_type_text.value))
            else:
                temp.append(TextNode(split, text_type))

        new_nodes.extend(temp)

    return new_nodes
