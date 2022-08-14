from dart_runtime.datastream import readString, readUnsigned, readInt_32

kVersionSize = int(128 / 4)
kMessageFeaturesSize = int(1024 / 4)


def ReadRef(stream):
    return readUnsigned(stream)


def ReadInstructions(deserializer):
    image_reader_ = readInt_32(deserializer.stream)
    unchecked_offset = readUnsigned(deserializer.stream)




def ReadVersion(stream):
    return stream.read(kVersionSize).decode('UTF-8')


def ReadFeatures(stream):
    s, i = readString(stream)
    return s


class FullSnapshotReader:
    def ReadVMSnapshot(self):
        pass

    def ReadProgramSnapshot(self):
        pass


def ReadFromTo(deserializer):
    for _ in range(3):
        p = readUnsigned(deserializer.stream)
