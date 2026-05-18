import pathlib
import logging

from src._my_pytools._setup._setup_uv import setup_uv
from src._my_pytools._setup._utils import get_current_dir

logging.basicConfig(level=logging.INFO)

def _resolve_beartype_package_dir(current_dir: pathlib.Path) -> pathlib.Path:
    if current_dir.name == 'src':
        return current_dir.parent
    package_dir = current_dir / 'src'
    package_dir.mkdir(parents=True, exist_ok=True)
    return package_dir

def _write_beartype_init(package_dir: pathlib.Path) -> None:
    init_path = package_dir.joinpath('__init__.py')
    init_contents = 'from beartype.claw import beartype_this_package\nbeartype_this_package()\n'
    init_path.write_text(init_contents)

def init_beartype() -> None:
    logging.info("Initializing beartype in the package.")
    setup_uv()
    current_dir = get_current_dir()
    package_dir = _resolve_beartype_package_dir(current_dir)
    _write_beartype_init(package_dir)