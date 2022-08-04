from dart_runtime.StreamUtil import readString

kVersionSize = int(128 / 4)
kMessageFeaturesSize = int(1024 / 4)


def ReadVersion(stream):
    return stream.read(kVersionSize).decode('UTF-8')


def ReadFeatures(stream):
    return readString(stream)
