from textnode import TextNode, TextType, split_nodes_delimiter
from htmlnode import LeafNode, ParentNode


def main():
    # txt = TextNode("text node", "bold", "boot.dev")
    # print(txt)
    # txt2 = TextNode("text node", "bold")
    # print(txt2)

    # props = {"href": "https://www.google.com", "target": "_blank"}
    # children = [
    #     LeafNode("b", "bold text"),
    #     LeafNode(None, "normal text"),
    #     LeafNode("i", "italic text"),
    # ]
    # node = ParentNode(tag="a", children=children, props=props)
    # outer_children = [
    #     LeafNode("b", "bold texd"),
    #     node,
    # ]
    # outer_node = ParentNode(tag="p", children=outer_children, props=None)
    # html = outer_node.to_html()
    # print(html)

    node = TextNode(
        "This is text with a `code block` with a few words",
        TextType.text_type_text.value,
    )
    node_image = TextNode(
        "This is an image", TextType.text_type_image.value, "https://google.com"
    )
    new_nodes = split_nodes_delimiter(
        [node, node_image], "`", TextType.text_type_code.value
    )
    print(f"{node = }")
    print(f"{new_nodes = }")


if __name__ == "__main__":
    main()
