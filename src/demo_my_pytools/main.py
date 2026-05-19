from demo_my_pytools.tools import main_check

def foo(x: int, y: str) -> str:
    """Good function that should pass type checking."""
    return f"{x} {y}"

@main_check
def main() -> None:
    result = foo(5, y="hello")
    print(result, '<-- should be "5 hello"')

if __name__ == '__main__':
    main()