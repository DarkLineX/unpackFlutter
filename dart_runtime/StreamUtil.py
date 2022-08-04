def readString(stream):
    res = b''
    b = stream.read(1)
    while b != b'\x00':
        res += b
        b = stream.read(1)
    return res
