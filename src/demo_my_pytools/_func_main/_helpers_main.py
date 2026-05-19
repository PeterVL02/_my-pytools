from inspect import getsourcefile
from typing import Callable
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

type MainFunc = Callable[[], None]

def assert_main_name(func: MainFunc) -> None:
    if func.__name__ != 'main':
        raise AssertionError("The @main_check decorator can only be applied to a function named 'main'")

def assert_main_returns_none(func: MainFunc) -> None:
    if not func.__annotations__ or func.__annotations__.get('return') is not None:
        raise AssertionError("The main function must have a return type of None")

def assert_main_has_no_arguments(func: MainFunc) -> None:
    if func.__code__.co_argcount != 0 or func.__code__.co_kwonlyargcount != 0:
        raise AssertionError("The main function must not have any arguments")

def get_source_file(func: MainFunc) -> str:
    return getsourcefile(func) or func.__code__.co_filename

def run_mypy_on_source(source_file: str) -> bool:
    try:
        subprocess.run(['mypy', source_file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

