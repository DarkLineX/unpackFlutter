def readString(stream):
    res = b''
    i = 1
    b = stream.read(1)
    while b != b'\x00':
        res += b
        b = stream.read(1)
        i = i + 1
    return res, i
