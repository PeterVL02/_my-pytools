from src._setup._setup_uv import setup_uv
from src._setup._setup_beartype import init_beartype
from src._maintenance._main_maintenance import main_maintenance

def setup_project() -> None:
    """Initialize the project by setting up UV and beartype."""
    setup_uv()
    init_beartype()
    main_maintenance()