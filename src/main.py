from pathlib import Path
from generate import (
    generate_page_recursive,
    prep_public_folder,
    copy_recursive,
)


def main():
    public = Path("public")
    prep_public_folder(public)
    copy_recursive(Path("static"), public)

    content = Path("content")
    template = Path("template.html")
    generate_page_recursive(content, template, public)


if __name__ == "__main__":
    main()
