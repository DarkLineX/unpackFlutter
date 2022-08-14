import math

kDataBitsPerByte = 7
kByteMask = (1 << kDataBitsPerByte) - 1
kMaxUnsignedDataPerByte = kByteMask
kMinDataPerByte = -(1 << (kDataBitsPerByte - 1))
kMaxDataPerByte = (~kMinDataPerByte & kByteMask)
kEndByteMarker = (255 - kMaxDataPerByte)
kEndUnsignedByteMarker = (255 - kMaxUnsignedDataPerByte)
kMaxUint32 = 0xFFFFFFFF
kNumRead32PerWord = 2


def Read(stream, endByteMarker, maxLoops=-1):
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


def ReadUnsigned(stream, size=-7):
    if size == 8:
        return int.from_bytes(stream.Read(1), 'big', signed=False)  # No marker
    return Read(stream, kEndUnsignedByteMarker, math.ceil(size / 7))


def ReadUnsigned64(stream):
    return ReadUnsigned(stream, 64)


def ReadInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return Read(stream, kEndByteMarker, math.ceil(size / 7))


def ReadInt_64(stream):
    return ReadInt(stream, 64)


def ReadInt_16(stream, ):
    return ReadInt(stream, 16)


def ReadInt_32(stream, ):
    return ReadInt(stream, 32)


def ReadInt_8(stream, ):
    return ReadInt(stream, 8)


def ReadByte(stream):
    return int.from_bytes(stream.Read(1), 'big', signed=False)


def ReadWordWith32BitReads(stream):
    value = 0
    for j in range(kNumRead32PerWord):
        partialValue = ReadUnsigned(stream, 32)
        value |= partialValue << (j * 32)
    return value


def ReadString(stream):
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
