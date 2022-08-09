import math

kDataBitsPerByte = 7
kByteMask = (1 << kDataBitsPerByte) - 1
kMaxUnsignedDataPerByte = kByteMask
kMinDataPerByte = -(1 << (kDataBitsPerByte - 1))
kMaxDataPerByte = (~kMinDataPerByte & kByteMask)
kEndByteMarker = (255 - kMaxDataPerByte)
kEndUnsignedByteMarker = (255 - kMaxUnsignedDataPerByte)
kMaxUint32 = 0xFFFFFFFF


def read(stream, endByteMarker, maxLoops=-1):
    b = int.from_bytes(stream.read(1), 'big', signed=False)
    r = 0
    s = 0
    while b <= kMaxUnsignedDataPerByte:
        r |= b << s
        s += kDataBitsPerByte
        x = stream.read(1)
        b = int.from_bytes(x, 'big', signed=False)
        maxLoops -= 1
    return r | ((b - endByteMarker) << s)


def readUnsigned(stream, size=-7):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=False)  # No marker
    return read(stream, kEndUnsignedByteMarker, math.ceil(size / 7))


def readInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return read(stream, kEndByteMarker, math.ceil(size / 7))


def readInt_64(stream):
    return readInt(stream, 64)


def readInt_32(stream, ):
    return readInt(stream, 32)


def readByte(stream):
    return int.from_bytes(stream.read(1), 'big', signed=False)


def readString(stream):
    res = b''
    i = 1
    b = stream.read(1)
    while b != b'\x00':
        res += b
        b = stream.read(1)
        i = i + 1
    return res, i


if __name__ == '__main__':
    # 179 89
    cid_and_canonical = 179
    cid = (cid_and_canonical >> 1) & kMaxUint32
    print(cid)
