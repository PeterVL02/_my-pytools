import subprocess
import pathlib
import logging

logging.basicConfig(level=logging.INFO)

def add_dependency(dependency: str) -> None:
    try:
        logging.info(f"Adding {dependency} to uv dependencies.")
        subprocess.run(['uv', 'add', dependency], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to add {dependency} to uv") from e
    
def get_current_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent