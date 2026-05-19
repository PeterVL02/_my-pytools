from pathlib import Path
import subprocess
import platform
import logging

from demo_my_pytools._setup._utils import add_dependency

logging.basicConfig(level=logging.INFO)

def _get_project_root(root: Path | str = Path.cwd()) -> Path:
    return Path(root).expanduser().resolve()


def _get_src_directory(root: Path | str = Path.cwd()) -> Path:
    src_dir = _get_project_root(root) / 'src'
    src_dir.mkdir(parents=True, exist_ok=True)
    return src_dir


def _get_main_file_path(root: Path | str = Path.cwd()) -> Path:
    return Path(root).expanduser().resolve() / 'main.py'


def _get_src_main_path(root: Path | str = Path.cwd()) -> Path:
    return _get_src_directory(root) / 'main.py'


def _move_main_py_to_src(root: Path | str = Path.cwd()) -> Path | None:
    main_py_path = _get_main_file_path(root)
    if not main_py_path.exists():
        logging.info("No main.py found in the root directory. Skipping move.")
        return None

    target_path = _get_src_main_path(root)
    if target_path.exists():
        logging.info("src/main.py already exists. Skipping move.")
        return target_path

    logging.info("Moving main.py to src/ directory.")
    main_py_path.rename(target_path)
    return target_path


def _read_file_lines(path: Path) -> list[str]:
    return path.read_text().splitlines(keepends=True)


def _write_file_lines(path: Path, lines: list[str]) -> None:
    path.write_text(''.join(lines))


def _has_main_check_import(lines: list[str]) -> bool:
    return any(line.strip() == 'from _my_pytools.tools import main_check' for line in lines)


def _insert_main_check_import(lines: list[str]) -> list[str]:
    if _has_main_check_import(lines):
        return lines

    if lines and lines[0].startswith('#!'):
        return [lines[0], 'from _my_pytools.tools import main_check\n'] + lines[1:]

    return ['from _my_pytools.tools import main_check\n'] + lines


def _decorate_main_function(lines: list[str]) -> list[str]:
    decorated_lines: list[str] = []
    for line in lines:
        if line.startswith('def main('):
            decorated_lines.append('@main_check\n')
        decorated_lines.append(line)
    return decorated_lines


def _update_main_py_with_main_check(root: Path | str = Path.cwd()) -> None:
    main_py_path = _get_src_main_path(root)
    if not main_py_path.exists():
        logging.info("No main.py found in src/ directory. Skipping edit.")
        return

    logging.info("Editing main.py to import main_check and decorate main with @main_check.")
    lines = _read_file_lines(main_py_path)
    lines = _decorate_main_function(lines)
    lines = _insert_main_check_import(lines)
    _write_file_lines(main_py_path, lines)


def _get_operating_system() -> str:
    return platform.system()


def _run_uv_install_command(os_name: str) -> None:
    if os_name == 'Windows':
        logging.info("Detected Windows OS. Installing uv using PowerShell.")
        subprocess.run(
            ['powershell', '-ExecutionPolicy', 'ByPass', '-c', 'irm https://astral.sh/uv/install.ps1 | iex'],
            check=True,
        )
    elif os_name in ['Linux', 'MacOS']:
        logging.info(f"Detected {os_name} OS. Installing uv using curl.")
        subprocess.run(['curl', '-LsSf', 'https://astral.sh/uv/install.sh | sh'], check=True)
    else:
        logging.error(f"Unsupported OS: {os_name}")
        raise RuntimeError(f"Unsupported OS: {os_name}")


def _install_uv() -> None:
    os_name = _get_operating_system()
    try:
        _run_uv_install_command(os_name)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to install uv") from e
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError("An unexpected error occurred during uv installation") from e


def _is_uv_installed() -> bool:
    try:
        subprocess.run(['uv', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def _sync_uv() -> None:
    logging.info("Synchronizing uv venv.")
    subprocess.run(['uv', 'sync'])


def _project_has_pyproject(root: Path | str = Path.cwd()) -> bool:
    return _get_project_root(root).joinpath('pyproject.toml').exists()


def _initialize_uv_project(root: Path | str = Path.cwd()) -> None:
    logging.info("Initializing uv project because pyproject.toml is missing.")
    subprocess.run(['uv', 'init', '.'], check=True, cwd=_get_project_root(root))


def setup_uv() -> None:
    logging.info("Setting up uv.")
    if _is_uv_installed():
        logging.info("uv is already installed.")
    else:
        logging.info("uv is not installed. Attempting to install uv.")
        _install_uv()

    if not _project_has_pyproject():
        _initialize_uv_project()

    _sync_uv()
    add_dependency('beartype')
    add_dependency('mypy')

    main_py_path = _move_main_py_to_src()
    if main_py_path is not None:
        _update_main_py_with_main_check()



