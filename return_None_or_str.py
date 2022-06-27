from types import UnionType


def my_func(a:int) -> UnionType[None, str]:
    if a>10:
        return "big"
    else:
        return None
