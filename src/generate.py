from pathlib import Path
import shutil


def recursive_copy(src: Path, dst: Path) -> None:
    if src.is_file():
        shutil.copy(src=src, dst=dst)

    if src.is_dir():
        for item in src.iterdir():
            if item.is_dir():
                sub_dst_path = dst / item.relative_to(src)
                sub_dst_path.mkdir(parents=True, exist_ok=True)
                recursive_copy(src=item, dst=sub_dst_path)
            else:
                recursive_copy(src=item, dst=dst)
