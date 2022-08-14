from enum import Enum
from io import BytesIO

from dart_runtime.app_snapshot import ReadVersion, ReadFeatures
from dart_runtime.deserializer import Deserializer
from dart_runtime.kind import Kind

kMagicOffset = 0
kMagicSize = 4
kLengthOffset = kMagicOffset + kMagicSize
kLengthSize = 8
kKindOffset = kLengthOffset + kLengthSize
kKindSize = 8
kHeaderSize = kKindOffset + kKindSize





class Snapshot:

    def __init__(self, snapshot_data):
        self.snapshot_data = snapshot_data
        self.stream = BytesIO(self.snapshot_data)

    def SnapshotSetupFromBuffer(self):
        print(self.check_magic())
        print(self.large_length())
        kind = self.kind()
        print(ReadVersion(self.stream))
        print(ReadFeatures(self.stream))
        Deserializer(stream=self.stream, kind = kind).deserialize()

    def check_magic(self):
        magic = hex(int.from_bytes(self.stream.read(kMagicSize), 'little'))
        return magic

    def large_length(self):
        length_size = int.from_bytes(self.stream.read(kLengthSize), 'little')
        return length_size

    def kind(self):
        kind = Kind(int.from_bytes(self.stream.read(kKindSize), 'little'))
        return kind
