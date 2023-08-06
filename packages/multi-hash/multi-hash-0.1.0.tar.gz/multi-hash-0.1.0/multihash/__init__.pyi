from typing import NamedTuple

class MultiHash(NamedTuple):
    function: int
    length: int
    digest: bytes

class LengthMismatchError(Exception):
    expected: int
    actual: int
    def __init__(self, expected: int, actual: int) -> None: ...

def decode(multihash: bytes) -> MultiHash: ...
