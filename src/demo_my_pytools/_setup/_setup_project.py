from demo_my_pytools._setup._setup_uv import setup_uv
from demo_my_pytools._setup._setup_self import add_self_dependency
from demo_my_pytools._setup._setup_beartype import init_beartype
from demo_my_pytools._maintenance._main_maintenance import main_maintenance

def setup_project() -> None:
    """Initialize the project by setting up UV and beartype."""
    setup_uv()
    add_self_dependency()
    init_beartype()
    main_maintenance()