# _my-pytools

A small personal toolbox for Python projects. Spin up a new project and have the boring stuff handled for you so you can go directly to the sweaty coding phase.

It also ships a `@main_check` decorator that runs `mypy` on your file before your `main()` is allowed to execute. Annoying? A little. Useful? Maybe in the long run?

This decorator is heavily inspired by Indently: [Did I just ruin Python with Enforced Static Typing?](https://www.youtube.com/watch?v=LRGKtGnsufM)

More decorators and utilities coming as I need them.

Note: Until I come up with a better name, the package is actually called `demo_my-pytools` (can't start a package name with `_`).

## Install the CLI tools

```bash
uv tool install git+https://github.com/PeterVL02/_my-pytools.git
```

This gives you two commands (so far) globally: `_my-setup` and `_my-maintain`.

## Starting a new project

Run:

```bash
_my-setup
```

This will:
- Set up `uv` and `pyproject.toml` if not already there
- Sync with potentially existing `pyproject.toml`
- Add `beartype` and `mypy` as dependencies
- Add `demo_my-pytools` as a dependency so you can import from it
- Enable runtime type checking across your whole `src/` package via `beartype`
- Move `main.py` into `src/` and wire up `@main_check` on your `main()` function. If `main.py` didn't already exist, it is created as a `uv` project is initialized.
- Make sure every directory under `src/` has an `__init__.py`

## Usage

```python
from demo_my_pytools.tools import main_check

@main_check
def main() -> None:
    print("hello")

if __name__ == "__main__":
    main()
```

`@main_check` enforces that your entry point is named `main`, takes no arguments, and returns `None`. At runtime it runs `mypy` on the file. If there are type errors, `main()` won't execute. Sweaty. Probably shouldn't use this for queued jobs on servers. Unless you are very confident in your annotation skills or just use `typing.Any` everywhere. Probably also slowing you down.

I am just having fun with it.
