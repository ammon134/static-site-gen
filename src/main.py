from pathlib import Path
import shutil
from generate import recursive_copy


def main():
    public = Path("public")
    shutil.rmtree(public, ignore_errors=True)
    public.mkdir()
    recursive_copy(Path("static"), public)


if __name__ == "__main__":
    main()
