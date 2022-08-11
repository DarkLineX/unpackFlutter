from dart_runtime.datastream import readString, readUnsigned

kVersionSize = int(128 / 4)
kMessageFeaturesSize = int(1024 / 4)


def ReadAllocFixedSize(deserializer):
    start_index_ = deserializer.next_index()
    count = readUnsigned(deserializer.stream)
    for _ in range(count):
        deserializer.next_ref_index_ = deserializer.next_ref_index_+1


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
