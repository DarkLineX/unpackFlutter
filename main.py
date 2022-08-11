import math
from enum import Enum
from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


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


AOTSymbolsNameList= [
    '_kDartVmSnapshotData',
    '_kDartVmSnapshotInstructions',
    '_kDartIsolateSnapshotData',
    '_kDartIsolateSnapshotInstructions',
    # '_kDartSnapshotBuildId'
]

class DartClass:
    def __init__(self):
        self.class_name = ''
        self.functions = ''

    def __str__(self):
        pass


class DartFunction:
    def __init__(self):
        self.func_name = 'getInfo'
        self.code_offset = '0x000000ff'

kFirstReference = 1


class Deserializer:
    def __init__(self, stream):
        self.clusters = None
        self.num_base_objects_ = None
        self.num_objects_ = None
        self.num_clusters_ = None
        self.initial_field_table_len = None
        self.instructions_table_len = None
        self.instruction_table_data_offset = None
        self.unit_program_hash = None
        self.stream = stream
        self.cluster_list = []
        self.next_ref_index_ = kFirstReference

    def deserialize(self):
        self.num_base_objects_ = readUnsigned(self.stream)
        self.num_objects_ = readUnsigned(self.stream)
        self.num_clusters_ = readUnsigned(self.stream)
        self.initial_field_table_len = readUnsigned(self.stream)
        self.instructions_table_len = readUnsigned(self.stream)
        self.instruction_table_data_offset = readUnsigned(self.stream)

        # trace 1025 51549 308 572 7193 16
        print(self.num_base_objects_, self.num_objects_, self.num_clusters_,
              self.initial_field_table_len,
              self.instructions_table_len, self.instruction_table_data_offset)

        self.addBaseObject()

        for _ in range(self.num_clusters_):
            cluster = self.readCluster
            self.cluster_list.append(cluster)
            cluster.readAlloc()

        # for _ in range(self.num_clusters_):
        #     cluster = self.cluster_list[_]
        #     self.cluster_list.append(cluster)
        #     cluster.readFill()

    def addBaseObject(self):
        for _ in range(self.num_base_objects_):
            self.next_ref_index_ = self.next_ref_index_ + 1

    def next_index(self):
        return self.next_ref_index_

    @property
    def readCluster(self):
        read_cid_before = self.stream.tell()
        cid_and_canonical = readInt_64(self.stream)
        cid = (cid_and_canonical >> 1) & kMaxUint32
        is_canonical = (cid_and_canonical & 0x1) == 0x1

        read_cid_after = self.stream.tell()
        print('read_cid_before =', read_cid_before, 'read_cid_after =', read_cid_after, 'cid =', cid, 'is_canonical',
              is_canonical)
        # print("cid_and_canonical", cid_and_canonical, 'cid', cid, 'is_canonical', is_canonical)
        ###
        cluster = ClusterGetter(cid, is_canonical, self).getCluster()
        print(cluster, cid)
        return cluster


def IsTypedDataViewClassId(index):
    is_byte_data_view = index == kByteDataViewCid
    return is_byte_data_view or (IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderView)


def IsTypedDataBaseClassId(index):
    return kTypedDataInt8ArrayCid <= index < kByteDataViewCid


def IsExternalTypedDataClassId(index):
    return IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderExternal


def IsTypedDataClassId(index):
    return IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderInternal


kTypedDataCidRemainderInternal = 0
kTypedDataCidRemainderView = 1
kTypedDataCidRemainderExternal = 2

# ClassId(Enum):
kIllegalCid = 0  # x
kNativePointerCid = 1  # x
kFreeListElementCid = 2  # x
kForwardingCorpseCid = 3  # x
#  CLASS_LIST(DEFINE_OBJECT_KIND)    5 - 92
#  CLASS_LIST_FFI(DEFINE_OBJECT_KIND) 93 - 108
#  CLASS_LIST_TYPED_DATA(DEFINE_OBJECT_KIND) 110 - 123
kByteDataViewCid = 152
kByteBufferCid = 153
kNullCid = 154
kDynamicCid = 155
kVoidCid = 156
kNeverCid = 157
kNumPredefinedCids = 158

# CLASS_LIST(Enum):
kObjectCid = 4
# CLASS_LIST_NO_OBJECT(V) 5 - 92


# CLASS_LIST_NO_OBJECT(Enum):
# CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP(V) 5 - 81
# CLASS_LIST_MAPS(V)  82 - 83
# CLASS_LIST_SETS(V)  84 - 85
# CLASS_LIST_ARRAYS(V) 86 - 88
# CLASS_LIST_STRINGS(V) 89 - 92


# CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP(Enum)
# CLASS_LIST_INTERNAL_ONLY(V)        5-42
# CLASS_LIST_INSTANCE_SINGLETONS(V)  43-81


# CLASS_LIST_INTERNAL_ONLY(Enum)

kClassCid = 5
kPatchClassCid = 6
kFunctionCid = 7
kTypeParametersCid = 8  # x
kClosureDataCid = 9  # x
kFfiTrampolineDataCid = 10
kFieldCid = 11
kScriptCid = 12
kLibraryCid = 13
kNamespaceCid = 14
kKernelProgramInfoCid = 15
kWeakSerializationReferenceCid = 16
kCodeCid = 17
kInstructionsCid = 18
kInstructionsSectionCid = 19
kInstructionsTableCid = 20
kObjectPoolCid = 21  # x
kPcDescriptorsCid = 22
kCodeSourceMapCid = 23
kCompressedStackMapsCid = 24
kLocalVarDescriptorsCid = 25
kExceptionHandlersCid = 26
kContextCid = 27
kContextScopeCid = 28
kSentinelCid = 29
kSingleTargetCacheCid = 30
kUnlinkedCallCid = 31
kMonomorphicSmiableCallCid = 32
kCallSiteDataCid = 33
kICDataCid = 34
kMegamorphicCacheCid = 35
kSubtypeTestCacheCid = 36
kLoadingUnitCid = 37
kErrorCid = 38
kApiErrorCid = 39
kLanguageErrorCid = 40
kUnhandledExceptionCid = 41
kUnwindErrorCid = 42

# CLASS_LIST_INSTANCE_SINGLETONS(Enum)
kInstanceCid = 43
kLibraryPrefixCid = 44
kTypeArgumentsCid = 45
kAbstractTypeCid = 46
kTypeCid = 47
kFinalizerBaseCid = 48
kFinalizerCid = 49
kNativeFinalizerCid = 50
kFinalizerEntryCid = 51
kFunctionTypeCid = 52
kTypeRefCid = 53  # x
kTypeParameterCid = 54
kClosureCid = 55
kNumberCid = 56
kIntegerCid = 57
kSmiCid = 58
kMintCid = 59
kDoubleCid = 60
kBoolCid = 61
kFloat32x4Cid = 62
kInt32x4Cid = 63
kFloat64x2Cid = 64
kTypedDataBaseCid = 65
kTypedDataCid = 66
kExternalTypedDataCid = 67
kTypedDataViewCid = 68
kPointerCid = 69
kDynamicLibraryCid = 70
kCapabilityCid = 71
kReceivePortCid = 72
kSendPortCid = 73
kStackTraceCid = 74
kRegExpCid = 75
kWeakPropertyCid = 76
kWeakReferenceCid = 77
kMirrorReferenceCid = 78
kFutureOrCid = 79
kUserTagCid = 80
kTransferableTypedDataCid = 81

# CLASS_LIST_MAPS(Enum):
kLinkedHashMapCid = 82
kImmutableLinkedHashMapCid = 83

# CLASS_LIST_SETS(Enum):
kLinkedHashSetCid = 84
kImmutableLinkedHashSetCid = 85

# CLASS_LIST_ARRAYS(Enum):
# CLASS_LIST_FIXED_LENGTH_ARRAYS(V) 86 - 87
kGrowableObjectArrayCid = 88

# CLASS_LIST_FIXED_LENGTH_ARRAYS(Enum):
FIXED_kArrayCid = 86
FIXED_kImmutableArrayCid = 87

# CLASS_LIST_STRINGS(Enum):
kStringCid = 89
kOneByteStringCid = 90
kTwoByteStringCid = 91
kExternalOneByteStringCid = 92
kExternalTwoByteStringCid = 93

# CLASS_LIST_FFI(Enum):
kFfiNativeFunctionCid = 93
# CLASS_LIST_FFI_TYPE_MARKER(V) 94 - 106
kFfiNativeTypeCid = 107
kFfiStructCid = 108

# CLASS_LIST_FFI_TYPE_MARKER(Enum):
# CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(V) 94 - 103
kFfiVoidCid = 104
kFfiHandleCid = 105
kFfiBoolCid = 106

# CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(Enum):
kFfiInt8Cid = 94
kFfiInt16Cid = 95
kFfiInt32Cid = 96
kFfiInt64Cid = 97
kFfiUint8Cid = 98
kFfiUint16Cid = 99
kFfiUint32Cid = 100
kFfiUint64Cid = 101
kFfiFloatCid = 102
kFfiDoubleCid = 103

# CLASS_LIST_TYPED_DATA(Enum):
kTypedDataInt8ArrayCid = 110
kTypedDataUint8ArrayCid = 111
kTypedDataUint8ClampedArrayCid = 112
kTypedDataInt16ArrayCid = 113
kTypedDataUint16ArrayCid = 114
kTypedDataInt32ArrayCid = 115
kTypedDataUint32ArrayCid = 116
kTypedDataInt64ArrayCid = 117
kTypedDataUint64ArrayCid = 118
kTypedDataFloat32ArrayCid = 119
kTypedDataFloat64ArrayCid = 120
kTypedDataFloat32x4ArrayCid = 121
kTypedDataInt32x4ArrayCid = 122
kTypedDataFloat64x2ArrayCid = 123


kDataBitsPerByte = 7
kByteMask = (1 << kDataBitsPerByte) - 1
kMaxUnsignedDataPerByte = kByteMask
kMinDataPerByte = -(1 << (kDataBitsPerByte - 1))
kMaxDataPerByte = (~kMinDataPerByte & kByteMask)
kEndByteMarker = (255 - kMaxDataPerByte)
kEndUnsignedByteMarker = (255 - kMaxUnsignedDataPerByte)
kMaxUint32 = 0xFFFFFFFF


def read(stream, endByteMarker, maxLoops=-1):
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


def readUnsigned(stream, size=-7):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=False)  # No marker
    return read(stream, kEndUnsignedByteMarker, math.ceil(size / 7))


def readInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return read(stream, kEndByteMarker, math.ceil(size / 7))


def readInt_64(stream):
    return readInt(stream, 64)


def readInt_32(stream, ):
    return readInt(stream, 32)


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


class DeserializationCluster:
    def __init__(self, cid, is_canonical, deserializer):
        self.cid = cid
        self.is_canonical = is_canonical
        self.deserializer = deserializer
        self.start_index_ = 0
        self.stop_index_ = 0


class ClassDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readInt_32(self.deserializer.stream)
        count = readUnsigned(self.deserializer.stream)


class AbstractInstanceDeserializationCluster(DeserializationCluster):
    pass


class InstanceDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        next_field_offset_in_words_ = readUnsigned(self.deserializer.stream)
        instance_size_in_words_ = readUnsigned(self.deserializer.stream)


class TypedDataViewSerializationCluster:     pass


class ExternalTypedDataSerializationCluster:     pass


class TypedDataSerializationCluster:     pass


class TypedDataViewDeserializationCluster:     pass


class ExternalTypedDataDeserializationCluster:     pass


class TypedDataDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = readUnsigned(self.deserializer.stream)


class CanonicalSetDeserializationCluster(DeserializationCluster):
    def BuildCanonicalSetFromLayout(self):
        if self.is_canonical:
            # count = 8569 stop_index_ = 9595 start_index_ = 1026 first_element_ = 0
            table_length = readUnsigned(self.deserializer.stream)
            first_element_ = readUnsigned(self.deserializer.stream)
            count = self.stop_index_ - (self.start_index_ + first_element_)
            print(count, self.stop_index_, self.start_index_, first_element_, table_length)
            for _ in range(self.start_index_ + first_element_, self.stop_index_):
                readUnsigned(self.deserializer.stream)


class TypeParametersDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class TypeArgumentsDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        # 229
        self.start_index_ = self.deserializer.next_index()
        count = readUnsigned(self.deserializer.stream)
        # 231
        # 8569
        for _ in range(count):
            readUnsigned(self.deserializer.stream)
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        # 8974
        self.stop_index_ = self.deserializer.next_index()

        self.BuildCanonicalSetFromLayout()


class StringDeserializationCluster(CanonicalSetDeserializationCluster):

    @staticmethod
    def DecodeLengthAndCid(encoded):
        cid = kTwoByteStringCid if (encoded & 0x1) else kOneByteStringCid
        length = encoded >> 1
        return length, cid

    def readAlloc(self):
        # 229
        self.start_index_ = self.deserializer.next_index()
        count = readUnsigned(self.deserializer.stream)
        # 231
        # 8569
        for _ in range(count):
            encoded = readUnsigned(self.deserializer.stream)
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        # 8974
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def readFill(self):
        for _ in range(self.start_index_, self.stop_index_):
            encoded = readUnsigned(self.deserializer.stream)
            length, cid = self.DecodeLengthAndCid(encoded)
            if cid == kOneByteStringCid:
                for _ in range(length):
                    code_unit = readInt(self.deserializer.stream,8)
            else:
                for _ in range(length):
                    code_unit = readInt(self.deserializer.stream,8)
                    code_unit_2 = readInt(self.deserializer.stream,8)
                    code_unit = (code_unit | code_unit_2 << 8)


class DoubleDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class TypeParameterDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        ReadAllocFixedSize(self.deserializer)
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()


class TypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        ReadAllocFixedSize(self.deserializer)
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()


class MintDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readUnsigned(self.deserializer.stream)


class CodeDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.ReadAllocOneCode()
        deferred_count = readUnsigned(self.deserializer.stream)
        for _ in range(deferred_count):
            self.ReadAllocOneCode()

    def ReadAllocOneCode(self):
        state_bits = readInt_32(self.deserializer.stream)


class PatchClassDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class FunctionDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class FunctionTypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        ReadAllocFixedSize(self.deserializer)
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()


class ClosureDataDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class FfiTrampolineDataDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class FieldDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class ScriptDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class LibraryDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class NamespaceDeserializationCluster:
    pass


class KernelProgramInfoDeserializationCluster:
    pass


class ObjectPoolDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = readUnsigned(self.deserializer.stream)


class PcDescriptorsDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = readUnsigned(self.deserializer.stream)


class CodeSourceMapDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = readUnsigned(self.deserializer.stream)


class CompressedStackMapsDeserializationCluster:
    pass


class ExceptionHandlersDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = readUnsigned(self.deserializer.stream)


class ContextDeserializationCluster:
    pass


class ContextScopeDeserializationCluster:
    pass


class UnlinkedCallDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class MegamorphicCacheDeserializationCluster:
    pass


class SubtypeTestCacheDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class LoadingUnitDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class UnhandledExceptionDeserializationCluster:
    pass


class LibraryPrefixDeserializationCluster:
    pass


class TypeRefDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class ClosureDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class GrowableObjectArrayDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class StackTraceDeserializationCluster:
    pass


class RegExpDeserializationCluster:
    pass


class WeakPropertyDeserializationCluster:
    pass


class LinkedHashMapDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class LinkedHashSetDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        ReadAllocFixedSize(self.deserializer)


class ArrayDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readUnsigned(self.deserializer.stream)


class NoneCluster(ClassDeserializationCluster):
    def readAlloc(self):
        pass


# kStringCid = 89
# kClassCid = 5
# kTypeParametersCid = 8
# kTypeArgumentsCid = 45


class ClusterGetter:

    def __init__(self, cid, is_canonical, deserializer):
        self.cid = cid
        self.deserializer = deserializer
        self.is_canonical = is_canonical

    def getCluster(self):

        if self.cid > 10000:
            return NoneCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid > kNumPredefinedCids or self.cid == kInstanceCid:
            return InstanceDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if IsTypedDataViewClassId(self.cid):
            return TypedDataViewDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if IsExternalTypedDataClassId(self.cid):
            return ExternalTypedDataDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if IsTypedDataClassId(self.cid):
            return TypedDataDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kClassCid:
            return ClassDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kTypeParametersCid:
            return TypeParametersDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kTypeArgumentsCid:
            return TypeArgumentsDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kPatchClassCid:
            return PatchClassDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kFunctionCid:
            return FunctionDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kClosureDataCid:
            return ClosureDataDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kFfiTrampolineDataCid:
            return FfiTrampolineDataDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kFieldCid:
            return FieldDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kScriptCid:
            return ScriptDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kLibraryCid:
            return LibraryDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kNamespaceCid:
            return NamespaceDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kKernelProgramInfoCid:
            return KernelProgramInfoDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kCodeCid:
            return CodeDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kObjectPoolCid:
            return ObjectPoolDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kPcDescriptorsCid:
            return PcDescriptorsDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kCodeSourceMapCid:
            return CodeSourceMapDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kCompressedStackMapsCid:
            return CompressedStackMapsDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kExceptionHandlersCid:
            return ExceptionHandlersDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kContextCid:
            return ContextDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kUnlinkedCallCid:
            return UnlinkedCallDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kMegamorphicCacheCid:
            return MegamorphicCacheDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kSubtypeTestCacheCid:
            return SubtypeTestCacheDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kLoadingUnitCid:
            return LoadingUnitDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kUnhandledExceptionCid:
            return UnhandledExceptionDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kLibraryPrefixCid:
            return LibraryPrefixDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kTypeCid:
            return TypeDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kFunctionTypeCid:
            return FunctionTypeDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kTypeRefCid:
            return TypeRefDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kTypeParameterCid:
            return TypeParameterDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kClosureCid:
            return ClosureDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kMintCid:
            return MintDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kDoubleCid:
            return DoubleDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kGrowableObjectArrayCid:
            return GrowableObjectArrayDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kStackTraceCid:
            return StackTraceDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kRegExpCid:
            return RegExpDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kWeakPropertyCid:
            return WeakPropertyDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kLinkedHashMapCid:
            return NoneCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kImmutableLinkedHashMapCid:
            return LinkedHashMapDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kLinkedHashSetCid:
            return NoneCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kImmutableLinkedHashSetCid:
            return LinkedHashSetDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == FIXED_kArrayCid:
            return ArrayDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == FIXED_kImmutableArrayCid:
            return ArrayDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid == kStringCid:
            return StringDeserializationCluster(self.cid, self.is_canonical, self.deserializer)

        if self.cid >= 94 and self <= 108:
            return InstanceDeserializationCluster(self.cid, self.is_canonical, self.deserializer)
        else:
            return NoneCluster(self.cid, self.is_canonical, self.deserializer)


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
        Deserializer(stream=self.stream).deserialize()

    def check_magic(self):
        magic = hex(int.from_bytes(self.stream.read(kMagicSize), 'little'))
        return magic

    def large_length(self):
        length_size = int.from_bytes(self.stream.read(kLengthSize), 'little')
        return length_size

    def kind(self):
        kind = Kind(int.from_bytes(self.stream.read(kKindSize), 'little'))
        return kind

def get_AOTSymbols(sections):
    tables = []
    aot_symbols = {}
    # 找到 SymbolTableSection
    for section in sections:
        if isinstance(section, SymbolTableSection):
            tables.append(section)

    # 字典加载 所有 symbols
    for table in tables:
        for sym in table.iter_symbols():
            if sym.name in AOTSymbolsNameList:
                aot_symbols[sym.name] = sym.entry
    return aot_symbols


def parse_elf_file(file_path):
    f = ELFFile(open(file_path, 'rb'))
    sections = list(f.iter_sections())  # 所有section
    aot_symbols = get_AOTSymbols(sections)
    Snapshots = {}
    for AOTSymbolsName in AOTSymbolsNameList:
        # 遍历所有的
        aot_symbol = aot_symbols[AOTSymbolsName]
        # 再次遍历所有 section 比对 section的
        for section in sections:
            # 获取 sh_addr 内存映射起始地址
            # 计算出blob区块的起始位置和大小 这里很简单看代码就行 copy来自Doldrums
            sh_addr = section['sh_addr']
            if 0 <= aot_symbol.st_value - sh_addr < section.data_size:
                snapshot = {}
                blob = section.data()[(aot_symbol.st_value - sh_addr):][:aot_symbol.st_size]
                assert len(blob) == aot_symbol.st_size
                # print(AOTSymbolsName,hex( aot_symbol.st_value), len(blob), hex(aot_symbol.st_value + len(blob)))
                snapshot['blob'] = blob
                snapshot['offsets'] = aot_symbol.st_value
                Snapshots[AOTSymbolsName] = snapshot

    # vm_snapshot_data = Snapshots['_kDartVmSnapshotData']
    # vm roots 加载的是基本类 没必要解析 核心的还是看 isolate
    # vm_snapshot_ = Snapshot(vm_snapshot_data['blob']).SnapshotSetupFromBuffer()

    isolate_snapshot_data = Snapshots['_kDartIsolateSnapshotData']
    isolate_snapshot_ = Snapshot(isolate_snapshot_data['blob']).SnapshotSetupFromBuffer()


if __name__ == '__main__':
    parse_elf_file('res/libapp.so')
