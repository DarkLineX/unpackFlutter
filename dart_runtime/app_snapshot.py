from dart_runtime.datastream import ReadString, ReadUnsigned,ReadInt_32

kVersionSize = int(128 / 4)
kMessageFeaturesSize = int(1024 / 4)


def ReadRef(stream):
    return ReadUnsigned(stream)


def ReadInstructions(deserializer):
    deserializer.stream.read(1)




def ReadVersion(stream):
    return stream.read(kVersionSize).decode('UTF-8')


def ReadFeatures(stream):
    s, i = ReadString(stream)
    return s


class FullSnapshotReader:
    def ReadVMSnapshot(self):
        pass

    def ReadProgramSnapshot(self):
        pass


def ReadFromTo(deserializer,size):
    for _ in range(size):
        p = ReadUnsigned(deserializer.stream)
