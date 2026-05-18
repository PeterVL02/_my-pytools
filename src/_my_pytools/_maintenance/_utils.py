from __future__ import annotations

from pathlib import Path
from typing import Generator


def get_root_path(root: Path | str = Path.cwd()) -> Path:
    """Return the absolute path for the maintenance root directory."""
    return Path(root).expanduser().resolve()


def get_src_root(root_path: Path) -> Path:
    """Return the src directory under the given root, creating it if necessary."""
    src_path = root_path / 'src'
    src_path.mkdir(parents=True, exist_ok=True)
    return src_path


def iter_subdirectories(root_path: Path) -> Generator[Path, None, None]:
    """Recursively yield all subdirectories beneath the given root path."""
    yield root_path
    for child in sorted(root_path.iterdir()):
        if child.is_dir():
            yield from iter_subdirectories(child)


def init_file_path(directory: Path) -> Path:
    """Return the __init__.py file path for a specific directory."""
    return directory / '__init__.py'


def create_init_file(directory: Path) -> Path:
    """Create __init__.py in the directory if it does not already exist."""
    init_path = init_file_path(directory)
    if not init_path.exists():
        init_path.write_text('# Package initializer\n')
    return init_path



