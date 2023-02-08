from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("blender-randomiser")
except PackageNotFoundError:
    # package is not installed
    pass
