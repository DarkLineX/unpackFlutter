import math

kDataBitsPerByte = 7
kByteMask = (1 << kDataBitsPerByte) - 1
kMaxUnsignedDataPerByte = kByteMask
kMinDataPerByte = -(1 << (kDataBitsPerByte - 1))
kMaxDataPerByte = (~kMinDataPerByte & kByteMask)
kEndByteMarker = (255 - kMaxDataPerByte)
kEndUnsignedByteMarker = (255 - kMaxUnsignedDataPerByte)
kMaxUint32 = 0xFFFFFFFF


def read(stream, endByteMarker):
    b = readByte(stream)
    r = 0
    s = 0
    if b > kMaxUnsignedDataPerByte:
        return b - endByteMarker
    while b <= kMaxUnsignedDataPerByte:
        r |= b << s
        s += kDataBitsPerByte
        b = readByte(stream)
    return r | ((b - endByteMarker) << s)


def readUnsigned(stream):
    return read(stream, kEndUnsignedByteMarker)


def readInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return read(stream, kEndByteMarker)


def readInt_64(stream):
    return readInt(stream, 4)


def readInt_32(stream, ):
    return readInt(stream, 4)


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
