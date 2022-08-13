import pkg_resources  # part of setup tools


def say_hello():
    print("hello world!")


def version() -> str:
    ver = pkg_resources.require("atmesh")[0].version
    print("autotwin mesh module version:")
    return ver
