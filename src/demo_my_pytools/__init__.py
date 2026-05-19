import pathlib
from beartype.claw import beartype_this_package

beartype_this_package() 

__package_name__ = pathlib.Path(__file__).parent.name