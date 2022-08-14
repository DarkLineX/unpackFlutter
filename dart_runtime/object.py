from dart_runtime.globals import kObjectAlignment
from dart_runtime.util import Utils


def RoundedAllocationSize(size):
    return Utils.roundUp(size,kObjectAlignment)
