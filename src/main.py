from pathlib import Path
from generate import generate_page, prep_public_folder, recursive_copy


def main():
    public = Path("public")
    prep_public_folder(public)
    recursive_copy(Path("static"), public)

    content = Path("content/index.md")
    generate_page(content, Path("template.html"), public / "index.html")


if __name__ == "__main__":
    main()
