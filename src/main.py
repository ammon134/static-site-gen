from textnode import text_to_textnodes


def main():
    new_nodes = text_to_textnodes(
        "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    )
    print()
    print(new_nodes)


if __name__ == "__main__":
    main()
