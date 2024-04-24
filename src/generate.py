from pathlib import Path
import re
import shutil

from markdown_blocks import markdown_to_html


def prep_public_folder(path: Path) -> None:
    print(f"Cleaning '{path}' folder...")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(exist_ok=True, parents=True)


def copy_recursive(src: Path, dst: Path) -> None:
    if src.is_file():
        shutil.copy(src=src, dst=dst)

    if src.is_dir():
        for item in src.iterdir():
            if item.is_dir():
                sub_dst_path = dst / item.relative_to(src)
                sub_dst_path.mkdir(parents=True, exist_ok=True)
                print(f"Copying content of '{item}' to '{sub_dst_path}' ...")
                copy_recursive(src=item, dst=sub_dst_path)
            else:
                print(f"Copying '{item}' into '{dst}' ...")
                copy_recursive(src=item, dst=dst)


def extract_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No title found")


def generate_page(src_path: Path, template_path: Path, dst_path: Path) -> None:
    print(
        f"Generating page from '{src_path}' to '{dst_path}' using '{template_path}'..."
    )

    with open(src_path) as f:
        src = f.read()
    with open(template_path) as f:
        output_html = f.read()

    # Replace title
    title = extract_title(src)
    output_html = re.sub(r"{{ *Title *}}", title, output_html)

    # Replace body
    body = markdown_to_html(src)
    output_html = re.sub(r"{{ *Content *}}", body, output_html)

    # Write output to file
    if dst_path.suffix != ".html":
        raise Exception("invalid file path for generated page")

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_path, "w") as f:
        f.write(output_html)


def generate_page_recursive(
    src_path: Path, template_path: Path, dst_path: Path
) -> None:
    if not src_path.is_dir():
        raise Exception("source path is not a directory")

    for item in src_path.iterdir():
        if item.is_dir():
            sub_dst_path = dst_path / item.relative_to(src_path)
            sub_dst_path.mkdir(parents=True, exist_ok=True)
            generate_page_recursive(item, template_path, sub_dst_path)
        else:
            generate_page(item, template_path, dst_path / (item.stem + ".html"))
