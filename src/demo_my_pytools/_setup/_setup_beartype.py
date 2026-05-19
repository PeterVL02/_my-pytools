import pathlib
import logging

logging.basicConfig(level=logging.INFO)

def _write_beartype_init(src_dir: pathlib.Path) -> None:
    init_path = src_dir / '__init__.py'
    init_contents = 'from beartype.claw import beartype_this_package\nbeartype_this_package()\n'
    init_path.write_text(init_contents)

def init_beartype(root: pathlib.Path | str = pathlib.Path.cwd()) -> None:
    logging.info("Initializing beartype in the package.")
    src_dir = pathlib.Path(root).expanduser().resolve() / 'src'
    src_dir.mkdir(parents=True, exist_ok=True)
    _write_beartype_init(src_dir)