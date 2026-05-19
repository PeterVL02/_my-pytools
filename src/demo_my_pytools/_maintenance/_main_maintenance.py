import pathlib

from demo_my_pytools._maintenance._utils import (
    create_init_file,
    get_root_path,
    get_src_root,
    init_file_path,
    iter_subdirectories,
)

def main_maintenance(root: pathlib.Path | str = pathlib.Path.cwd()) -> None:
    """Ensure every directory under cwd/src has an __init__.py file."""
    root_path = get_root_path(root)
    src_root = get_src_root(root_path)

    for directory in iter_subdirectories(src_root):
        init_path = init_file_path(directory)
        if not init_path.exists():
            create_init_file(directory)