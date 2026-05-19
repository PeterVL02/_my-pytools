from functools import wraps

from demo_my_pytools._func_main._helpers_main import (
    assert_main_name, 
    assert_main_has_no_arguments, 
    assert_main_returns_none, 
    get_source_file, 
    run_mypy_on_source,
    MainFunc
    )

def main_check(func: MainFunc) -> MainFunc:
    assert_main_name(func)
    assert_main_returns_none(func)
    assert_main_has_no_arguments(func)

    @wraps(func)
    def wrapper() -> None:
        source_file = get_source_file(func)
        if run_mypy_on_source(source_file):
            func()

    return wrapper