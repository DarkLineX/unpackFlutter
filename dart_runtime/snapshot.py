from enum import Enum
from io import BytesIO

from dart_runtime.app_snapshot import  ReadVersion, ReadFeatures

kMagicOffset = 0
kMagicSize = 4
kLengthOffset = kMagicOffset + kMagicSize
kLengthSize = 8
kKindOffset = kLengthOffset + kLengthSize
kKindSize = 8
kHeaderSize = kKindOffset + kKindSize


# 快照类型的枚举类
class Kind(Enum):
    FULL = 0  # Full snapshot of an application.
    FULL_CORE = 1
    FULL_JIT = 2  # Full + JIT code
    FULL_AOT = 3  # Full + AOT code
    MESSAGE = 4  # A partial snapshot used only for isolate messaging.
    NONE = 5  # gen_snapshot
    INVALID = 6

    def __str__(self):
        if self.value == 0:
            name = "Full (full snapshot of an application)"
        elif self.value == 1:
            name = "Full core"
        elif self.value == 2:
            name = "Full JIT (full + JIT code)"
        elif self.value == 3:
            name = "Full AOT (full + AOT code)"
        elif self.value == 4:
            name = "Message (a partial snapshot used only for isolate messaging)"
        elif self.value == 5:
            name = "None (gen_snapshot)"
        elif self.value == 6:
            name = "Invalid"
        else:
            name = "Unknown"

        return name


class Snapshot:

    def __init__(self, snapshot_data):
        self.snapshot_data = snapshot_data
        self.stream = BytesIO(self.snapshot_data)

    def SnapshotSetupFromBuffer(self):
        print(self.check_magic())
        print(self.large_length())
        print(self.kind())
        print(ReadVersion(self.stream))
        print(ReadFeatures(self.stream))

        # snapshotHash = self.stream.read(32).decode('UTF-8')
        # print(snapshotHash)

    def check_magic(self):
        magic = hex(int.from_bytes(self.stream.read(kMagicSize), 'little'))
        return magic

    def large_length(self):
        length_size = int.from_bytes(self.stream.read(kLengthSize), 'little')
        return length_size

    def kind(self):
        kind = Kind(int.from_bytes(self.stream.read(kKindSize), 'little'))
        return kind
