import math


def read(stream, endByteMarker, maxLoops=-1):
    b = int.from_bytes(stream.read(1), 'big', signed=False)
    r = 0
    s = 0
    while b <= ReadStream.kMaxUnsignedDataPerByte:
        r |= b << s
        s += ReadStream.kDataBitsPerByte
        x = stream.read(1)
        b = int.from_bytes(x, 'big', signed=False)
        maxLoops -= 1
    return r | ((b - endByteMarker) << s)


kDataBitsPerByte = 7
kByteMask = (1 << kDataBitsPerByte) - 1
kMaxUnsignedDataPerByte = kByteMask
kMinDataPerByte = -(1 << (kDataBitsPerByte - 1))
kMaxDataPerByte = (~kMinDataPerByte & kByteMask)
kEndByteMarker = (255 - kMaxDataPerByte)
kEndUnsignedByteMarker = (255 - kMaxUnsignedDataPerByte)


# 每7byte为一个bit
def readUnsigned(stream, size=-7):
    # 计算循环次数 math.ceil(size / 7)
    return read(stream, ReadStream.kEndUnsignedByteMarker, math.ceil(size / 7))


def readCid(stream):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return self.readInt(stream, 32)


def readInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return read(stream, ReadStream.kEndByteMarker, math.ceil(size / 7))
