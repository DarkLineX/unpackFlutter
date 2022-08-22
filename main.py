from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from enum import Enum

kVersionSize = int(128 / 4)
kMessageFeaturesSize = int(1024 / 4)

FLAG_precompiled_mode = True


def ReadTokenPosition(stream):
    return ReadInt_32(stream)


def ReadRef(stream):
    return ReadUnsigned(stream)


def ReadInstructions(stream):
    return stream.read(1)


def ReadCid(stream):
    return ReadInt_32(stream)


def ReadVersion(stream):
    return stream.read(kVersionSize).decode('UTF-8')


def ReadFeatures(stream):
    s, i = ReadString(stream)
    return s


def ReadBool(stream):
    b = stream.read(1)
    if b == b'\x00':
        return False
    elif b == b'\x01':
        return True
    else:
        raise Exception(
            'Expected boolean, but received non-boolean value while reading at stream offset: ' + str(stream.tell()))


class FullSnapshotReader:
    def ReadVMSnapshot(self):
        pass

    def ReadProgramSnapshot(self):
        pass


def ReadFromTo(stream, size):
    for _ in range(size):
        p = ReadRef(stream)


# TODO GetCodeByIndex
def GetCodeByIndex(deserializer,code_index, entry_point):
    if code_index == 0:
        return 0
    if FLAG_precompiled_mode:
        return GetCodeAndEntryPointByIndex(deserializer,code_index, entry_point)
    else:
        return 0


def GetCodeAndEntryPointByIndex(deserializer,code_index, entry_point):
    code_index = code_index - 1
    base = deserializer.num_base_objects_
    if code_index < base:
        codePtr = CodePtr(code_index)
    return None

class BitField:
    def __init__(self):
        # BitField<uint8_t, EntryType, 0, 7>;
        pass

    @staticmethod
    def decode(value):
        return value & 0x7f

from enum import Enum


def IsTypedDataViewClassId(index):
    is_byte_data_view = index == kByteDataViewCid
    return is_byte_data_view or (
            IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderView)


def IsTypedDataBaseClassId(index):
    return kTypedDataInt8ArrayCid <= index < kByteDataViewCid


def IsExternalTypedDataClassId(index):
    return IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderExternal


def IsTypedDataClassId(index):
    return IsTypedDataBaseClassId(index) and ((index - kTypedDataInt8ArrayCid) % 3) == kTypedDataCidRemainderInternal


def IsInternalVMdefinedClassId(index):
    return (index < kNumPredefinedCids) and not IsImplicitFieldClassId(index)


def IsImplicitFieldClassId(index):
    return index == kByteBufferCid


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

kLastInternalOnlyCid = kUnwindErrorCid

kTopLevelCidOffset = (1 << 16)


class UnboxedFieldBitmap:
    def __init__(self, n):
        self.bitmap = n

    def Get(self, position):
        if position >= 64:
            return False
        return ((self.bitmap >> position) & 1) != 0


def IsTopLevelCid(class_id):
    return class_id >= kTopLevelCidOffset


kNullabilityBitSize = 2
kNullabilityBitMask = (1 << kNullabilityBitSize) - 1
DART_PRECOMPILED_RUNTIME = True  # AOT
DART_PRECOMPILER = False  # JIT


class DeserializationCluster:
    def __init__(self, cid, is_canonical, deserializer):
        self.cid = cid
        self.is_canonical = is_canonical
        self.deserializer = deserializer
        self.start_index_ = 0
        self.stop_index_ = 0

    def ReadAllocFixedSize(self, class_tag):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.deserializer.AssignRef(class_tag)
        self.stop_index_ = self.deserializer.next_index()


class ClassDeserializationCluster(DeserializationCluster):
    def __init__(self, cid, is_canonical, deserializer):
        super().__init__(cid, is_canonical, deserializer)
        self.predefined_start_index_ = None
        self.predefined_stop_index_ = None

    def ReadAlloc(self):
        self.predefined_start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            class_id = ReadCid(self.deserializer.stream)
            self.deserializer.AssignRef("Class")
        self.predefined_stop_index_ = self.deserializer.next_index()
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.deserializer.AssignRef("Class")
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):
        # 530964 600986
        FLAG_precompiled_mode = True

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.predefined_start_index_, self.predefined_stop_index_):

            classPtr = ClassPtr(refId)
            self._ReadFromTo(classPtr)

            class_id = ReadCid(self.deserializer.stream)
            classPtr.untag.field['id_'] = class_id

            if not DART_PRECOMPILED_RUNTIME:
                if self.deserializer.kind is not Kind.FULL_AOT:
                    classPtr.untag.untag_pointer['kernel_offset_'] = ReadInt_32(self.deserializer.stream)

            if not IsInternalVMdefinedClassId(class_id):

                classPtr.untag.field['host_instance_size_in_words_'] = ReadInt_32(self.deserializer.stream)
                classPtr.untag.field['host_next_field_offset_in_words_'] = ReadInt_32(self.deserializer.stream)

                if DART_PRECOMPILER:
                    pass
            else:
                # skip
                ReadInt_32(self.deserializer.stream)
                ReadInt_32(self.deserializer.stream)

            classPtr.untag.field['host_type_arguments_field_offset_in_words_'] = ReadInt_32(
                self.deserializer.stream)

            if DART_PRECOMPILER:
                classPtr.untag.untag_pointer['target_type_arguments_field_offset_in_words_'] = \
                    classPtr.untag.untag_pointer['host_type_arguments_field_offset_in_words_']

            classPtr.untag.field['num_type_arguments_'] = ReadInt_16(self.deserializer.stream)
            classPtr.untag.field['num_native_fields_'] = ReadInt_16(self.deserializer.stream)

            if not DART_PRECOMPILED_RUNTIME:
                classPtr.untag.field['token_pos_'] = ReadTokenPosition(self.deserializer.stream)
                classPtr.untag.field['end_token_pos_    '] = ReadTokenPosition(self.deserializer.stream)

            classPtr.untag.field['state_bits_'] = ReadInt_32(self.deserializer.stream)

            if self.deserializer.FLAG_precompiled_mode:
                ReadUnsigned64(self.deserializer.stream)  # Skip unboxed fields bitmap.

            self.deserializer.references[refId] = classPtr
            self.deserializer.classes[class_id] = classPtr

        for refId in range(self.start_index_, self.stop_index_):

            classPtr = ClassPtr(refId)
            self._ReadFromTo(classPtr)

            class_id = ReadCid(self.deserializer.stream)

            classPtr.untag.field['id_'] = class_id

            if not DART_PRECOMPILED_RUNTIME:
                if self.deserializer.kind is not Kind.FULL_AOT:
                    classPtr.untag.untag_pointer['kernel_offset_'] = ReadInt_32(self.deserializer.stream)

            classPtr.untag.field['host_instance_size_in_words_'] = ReadInt_32(self.deserializer.stream)
            classPtr.untag.field['host_next_field_offset_in_words_'] = ReadInt_32(self.deserializer.stream)
            classPtr.untag.field['host_type_arguments_field_offset_in_words_'] = ReadInt_32(
                self.deserializer.stream)
            if DART_PRECOMPILER:
                pass
            classPtr.untag.field['num_type_arguments_'] = ReadInt_16(self.deserializer.stream)
            classPtr.untag.field['num_native_fields_'] = ReadInt_16(self.deserializer.stream)

            if not DART_PRECOMPILED_RUNTIME:
                pass

            classPtr.untag.field['state_bits_'] = ReadInt_32(self.deserializer.stream)
            if FLAG_precompiled_mode and (not IsTopLevelCid(class_id)):
                unboxed_fields_map = UnboxedFieldBitmap(ReadUnsigned64(self.deserializer.stream))

            self.deserializer.references[refId] = classPtr
            self.deserializer.classes[class_id] = classPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        # ReadFromTo(self.deserializer.stream, 13)
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class AbstractInstanceDeserializationCluster(DeserializationCluster):
    pass


class InstanceDeserializationCluster(DeserializationCluster):
    def __init__(self, cid, is_canonical, deserializer):
        super().__init__(cid, is_canonical, deserializer)
        self.next_field_offset_in_words_ = None
        self.instance_size_in_words_ = None
        self.instance_size = None

    def ReadAlloc(self):

        self.start_index_ = self.deserializer.next_index()

        count = ReadUnsigned(self.deserializer.stream)

        self.next_field_offset_in_words_ = ReadInt_32(self.deserializer.stream)
        self.instance_size_in_words_ = ReadInt_32(self.deserializer.stream)
        self.instance_size = RoundedAllocationSize(self.instance_size_in_words_ * kCompressedWordSize)
        for i in range(count):
            self.deserializer.AssignRef('Instance')

        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        unboxed_fields_bitmap = UnboxedFieldBitmap(ReadUnsigned64(self.deserializer.stream))
        for refId in range(self.start_index_, self.stop_index_):
            instancePtr = InstancePtr(refId)
            next_field_offset = self.next_field_offset_in_words_ << kCompressedWordSizeLog2
            offset = 8
            instancePtr.untag.field['data'] = []
            while offset < next_field_offset:
                b = unboxed_fields_bitmap.Get(int(offset / kCompressedWordSize))
                if b:
                    p_point = ReadWordWith32BitReads(self.deserializer.stream)
                    instancePtr.untag.field['data'].append(p_point)
                else:
                    p_point = ReadRef(self.deserializer.stream)
                    instancePtr.untag.field['data'].append(p_point)
                offset = offset + kCompressedWordSize
            # TODO
            # while offset < instance_size#

        out_pos = self.deserializer.stream.tell()


class TypedDataViewSerializationCluster:     pass


class ExternalTypedDataSerializationCluster:     pass


class TypedDataSerializationCluster:     pass


class TypedDataViewDeserializationCluster:     pass


class ExternalTypedDataDeserializationCluster:     pass


class TypedDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('TypedData')
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()

        element_size = TypedData.ElementSizeInBytes(self.cid)

        for refId in range(self.start_index_, self.stop_index_):
            typedDataPtr = TypedDataPtr(refId)
            length = ReadUnsigned(self.deserializer.stream)
            length_in_bytes = length * element_size

            typedDataPtr.untag.field['length_'] = length
            typedDataPtr.untag.field['data'] = ReadBytes(self.deserializer.stream, length_in_bytes)
            self.deserializer.references[refId] = typedDataPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class CanonicalSetDeserializationCluster(DeserializationCluster):
    def BuildCanonicalSetFromLayout(self):
        if self.is_canonical:

            table_length = ReadUnsigned(self.deserializer.stream)
            first_element_ = ReadUnsigned(self.deserializer.stream)
            count = self.stop_index_ - (self.start_index_ + first_element_)

            for _ in range(self.start_index_ + first_element_, self.stop_index_):
                ReadUnsigned(self.deserializer.stream)


class TypeParametersDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('TypeParameters')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            typeParametersPtr = TypeParametersPtr(refId)
            self._ReadFromTo(typeParametersPtr)
            self.deserializer.references[refId] = typeParametersPtr
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        # ReadFromTo(self.deserializer.stream, 13)
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class TypeArgumentsDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('TypeArguments')
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            typeArgumentsPtr = TypeArgumentsPtr(refId)
            length = ReadUnsigned(self.deserializer.stream)
            typeArgumentsPtr.untag.field['length_'] = length
            typeArgumentsPtr.untag.field['hash_'] = ReadInt_32(self.deserializer.stream)
            typeArgumentsPtr.untag.field['nullability_'] = ReadUnsigned(self.deserializer.stream)
            typeArgumentsPtr.untag.field['instantiations_'] = ReadUnsigned(self.deserializer.stream)
            typeArgumentsPtr.untag.field['types'] = []
            for _ in range(length):
                typeArgumentsPtr.untag.field['types'].append(ReadUnsigned(self.deserializer.stream))
            self.deserializer.references[refId] = typeArgumentsPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class StringDeserializationCluster(CanonicalSetDeserializationCluster):

    @staticmethod
    def DecodeLengthAndCid(encoded):
        cid = kTwoByteStringCid if (encoded & 0x1) else kOneByteStringCid
        length = encoded >> 1
        return length, cid

    def ReadAlloc(self):

        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)

        for _ in range(count):
            encoded = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('String')

        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            stringPtr = StringPtr(refId)
            encoded = ReadUnsigned(self.deserializer.stream)
            length, cid = self.DecodeLengthAndCid(encoded)
            stringPtr.untag.field['length_'] = length
            stringPtr.untag.field['data'] = []
            if cid == kOneByteStringCid:
                for _ in range(length):
                    code_unit = ReadInt(self.deserializer.stream, 8)
                    stringPtr.untag.field['data'].append(code_unit)
            else:
                for _ in range(length):
                    code_unit = ReadInt(self.deserializer.stream, 8)
                    code_unit_2 = ReadInt(self.deserializer.stream, 8)
                    code_unit = (code_unit | code_unit_2 << 8)
                    stringPtr.untag.field['data'].append(code_unit)
            self.deserializer.references[refId] = stringPtr
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos)


class DoubleDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('double')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            doublePtr = DoublePtr(refId)
            doublePtr.untag.field['value_'] = ReadUnInt_64(self.deserializer.stream)
            self.deserializer.references[refId] = doublePtr
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos)


class TypeParameterDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('TypeParameter')
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            typeParameter = {}
            ReadFromTo(self.deserializer.stream, 3)
            parameterized_class_id_ = ReadInt_32(self.deserializer.stream)
            base_ = ReadInt_8(self.deserializer.stream)
            index_ = ReadInt_8(self.deserializer.stream)
            combined = ReadInt_8(self.deserializer.stream)
            flags_ = combined >> kNullabilityBitSize
            nullability_ = combined & kNullabilityBitMask

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class TypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Type')
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            typePtr = TypePtr(refId)
            self._ReadFromTo(typePtr)
            typePtr.untag.field['type_class_id_'] = ReadUnsigned(self.deserializer.stream)
            combined = ReadInt_8(self.deserializer.stream)
            typePtr.untag.field['type_state_'] = combined >> kNullabilityBitSize
            typePtr.untag.field['nullability_'] = combined & kNullabilityBitMask
            self.deserializer.references[refId] = typePtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        # ReadFromTo(self.deserializer.stream, 13)
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class MintDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('int')

    def ReadFill(self):
        pass


class CodeDeserializationCluster(DeserializationCluster):

    def __init__(self, cid, is_canonical, deserializer):
        super().__init__(cid, is_canonical, deserializer)
        self.deferred_stop_index_ = 0
        self.deferred_start_index_ = 0

    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()

        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.ReadAllocOneCode()

        self.stop_index_ = self.deserializer.next_index()

        self.deferred_start_index_ = self.deserializer.next_index()

        deferred_count = ReadUnsigned(self.deserializer.stream)
        for _ in range(deferred_count):
            self.ReadAllocOneCode()

        self.deferred_stop_index_ = self.deserializer.next_index()

    def ReadAllocOneCode(self):
        state_bits = ReadInt_32(self.deserializer.stream)
        self.deserializer.AssignRef('Code')

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()

        for refId in range(self.start_index_, self.stop_index_):
            self.readFill2(refId, False)

        for refId in range(self.deferred_start_index_, self.deferred_stop_index_):
            self.readFill2(refId, True)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def readFill2(self, refId, deferred):

        in_pos = self.deserializer.stream.tell()

        codePtr = CodePtr(refId)

        ReadInstructions(self.deserializer.stream)

        if self.deserializer.kind is not Kind.FULL_AOT:
            codePtr.untag.field['object_pool_'] = ReadRef(self.deserializer.stream)
        else:
            codePtr.untag.field['object_pool_'] = None
        codePtr.untag.field['owner_'] = ReadRef(self.deserializer.stream)
        codePtr.untag.field['exception_handlers_'] = ReadRef(self.deserializer.stream)
        codePtr.untag.field['pc_descriptors_'] = ReadRef(self.deserializer.stream)
        codePtr.untag.field['catch_entry_'] = ReadRef(self.deserializer.stream)
        if self.deserializer.kind is Kind.FULL_JIT:
            codePtr.untag.field['compressed_stackmaps_'] = ReadRef(self.deserializer.stream)
        elif self.deserializer.kind is Kind.FULL_AOT:
            codePtr.untag.field['compressed_stackmaps_'] = None

        codePtr.untag.field['inlined_id_to_function_'] = ReadRef(self.deserializer.stream)
        codePtr.untag.field['code_source_map_'] = ReadRef(self.deserializer.stream)

        self.deserializer.references[refId] = codePtr

        out_pos = self.deserializer.stream.tell()


class PatchClassDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('PatchClass')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            ptahClassPtr = PatchClassPtr(refId)
            self._ReadFromTo(ptahClassPtr)
            self.deserializer.references[refId] = ptahClassPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        obj.patched_class = ReadRef(self.deserializer.stream)
        obj.origin_class = ReadRef(self.deserializer.stream)
        obj.script = ReadRef(self.deserializer.stream)


class FunctionDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Function')

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()

            func = FunctionPtr(refId)
            in_read_from = self.deserializer.stream.tell()
            self._ReadFromTo(func)
            out_read_from = self.deserializer.stream.tell()

            if self.deserializer.kind == Kind.FULL_AOT:
                code_index = ReadUnsigned(self.deserializer.stream)
                entry_point = 0
                code = GetCodeByIndex(self.deserializer,code_index, entry_point)
                func.untag.field['code_'] = code
                if not entry_point == 0:
                    func.untag.field['entry_point_'] = entry_point
                    func.untag.field['unchecked_entry_point_'] = entry_point

            elif self.deserializer.kind == Kind.FULL_JIT:
                # TODO JIT
                unoptimized_code_ = ReadRef(self.deserializer.stream)
                code_ = ReadRef(self.deserializer.stream)
                ic_data_array_ = ReadRef(self.deserializer.stream)

            func.untag.field['packed_fields_'] = ReadInt_32(self.deserializer.stream)
            func.untag.field['kind_tag_'] = ReadInt_32(self.deserializer.stream)

            self.deserializer.references[refId] = func

            out_for = self.deserializer.stream.tell()

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class FunctionTypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('FunctionType')
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()

            type = {}
            in_read_from = self.deserializer.stream.tell()
            ReadFromTo(self.deserializer.stream, 6)
            out_read_from = self.deserializer.stream.tell()

            combined = ReadInt_8(self.deserializer.stream)
            packed_parameter_counts_ = ReadInt_32(self.deserializer.stream)
            packed_type_parameter_counts_ = ReadInt_16(self.deserializer.stream)

            out_for = self.deserializer.stream.tell()

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class ClosureDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('ClosureData')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            closureDataPtr = ClosureDataPtr(refId)
            if self.deserializer.kind == Kind.FULL_AOT:
                closureDataPtr.untag.field['context_scope_'] = None

            closureDataPtr.untag.field['parent_function_'] = ReadRef(self.deserializer.stream)
            closureDataPtr.untag.field['closure_'] = ReadRef(self.deserializer.stream)
            closureDataPtr.untag.field['default_type_arguments_kind_'] = ReadUnsigned(self.deserializer.stream)
            self.deserializer.references[refId] = closureDataPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class FfiTrampolineDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('FfiTrampolineData')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()

        for refId in range(self.start_index_, self.stop_index_):
            ffiTrampolineDataPtr = FfiTrampolineDataPtr(refId)
            self._ReadFromTo(ffiTrampolineDataPtr)
            ffiTrampolineDataPtr.untag.field['callback_id_'] = ReadUnsigned(self.deserializer.stream)
            self.deserializer.references[refId] = ffiTrampolineDataPtr

        out_pos = self.deserializer.stream.tell()

        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class FieldDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Field')

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):

            fieldPtr = FieldPtr(refId)
            self._ReadFromTo(fieldPtr)

            fieldPtr.untag.field['kind_bits_'] = ReadInt_16(self.deserializer.stream)
            fieldPtr.untag.field['value_or_offset'] = kind_bits_ = ReadRef(self.deserializer.stream)
            if StaticBit.decode(kind_bits_):
                fieldPtr.untag.field['field_id'] = ReadUnsigned(self.deserializer.stream)

            self.deserializer.references[refId] = fieldPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class ScriptDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Script')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            scriptPtr = ScriptPtr(refId)
            self._ReadFromTo(scriptPtr)
            if not DART_PRECOMPILED_RUNTIME:
                scriptPtr.untag.field['flags_and_max_position_'] = ReadInt_32(self.deserializer.stream)
            else:
                scriptPtr.untag.field['kernel_script_index_'] = ReadInt_32(self.deserializer.stream)
                scriptPtr.untag.field['load_timestamp_'] = 0

            self.deserializer.references[refId] = scriptPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class LibraryDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Library')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            libraryPtr = LibraryPtr(refId)
            self._ReadFromTo(libraryPtr)
            libraryPtr.untag.field['index_'] = ReadInt_32(self.deserializer.stream)
            libraryPtr.untag.field['num_imports_'] = ReadInt_16(self.deserializer.stream)
            libraryPtr.untag.field['load_state_'] = ReadInt_8(self.deserializer.stream)
            libraryPtr.untag.field['flags_'] = ReadInt_8(self.deserializer.stream)
            self.deserializer.references[refId] = libraryPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class NamespaceDeserializationCluster:
    pass


class KernelProgramInfoDeserializationCluster:
    pass


class ObjectPoolDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef("ObjectPool")
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            length = ReadUnsigned(self.deserializer.stream)
            objectPoolPtr = ObjectPoolPtr(refId)
            objectPoolPtr.untag.field['length_'] = length
            objectPoolPtr.untag.field['entry_bits'] = []
            objectPoolPtr.untag.field['data'] = []

            for j in range(length):
                entry_bits = ReadUnInt_8(self.deserializer.stream)

                objectPoolPtr.untag.field['entry_bits'].append(entry_bits)
                b = objectPoolPtr.TypeBits.decode(entry_bits)
                entry = {}
                if b == kTaggedObject:
                    entry['raw_obj_'] = ReadRef(self.deserializer.stream)
                elif b == kImmediate:
                    entry['raw_value_'] = ReadInt_64(self.deserializer.stream)
                elif b == kNativeFunction:
                    entry['raw_value_'] = 'native call entry'
                elif b == kSwitchableCallMissEntryPoint:
                    pass
                elif b == kMegamorphicCallEntryPoint:
                    pass
                else:
                    raise Exception('No type associated to decoded type bits')
                objectPoolPtr.untag.field['data'].append(entry)

            self.deserializer.references[refId] = objectPoolPtr

        out_pos = self.deserializer.stream.tell()

        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class PcDescriptorsDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('PcDescriptors')
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()

        for refId in range(self.start_index_, self.stop_index_):
            length = ReadUnsigned(self.deserializer.stream)
            pcDescriptorsPtr = PcDescriptorsPtr(refId)
            pcDescriptorsPtr.untag.field['length_'] = length
            data = ReadBytes(self.deserializer.stream, length)
            pcDescriptorsPtr.untag.field['data'] = data
            # self.deserializer.references[ref_id] = desc
            self.deserializer.references[refId] = pcDescriptorsPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class CodeSourceMapDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('CodeSourceMap')
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            length = ReadUnsigned(self.deserializer.stream)
            ReadBytes(self.deserializer.stream, length)
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class CompressedStackMapsDeserializationCluster:
    pass


class ExceptionHandlersDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('ExceptionHandlers')
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            exceptionHandlersPtr = ExceptionHandlersPtr(refId)
            length = ReadUnsigned(self.deserializer.stream)
            exceptionHandlersPtr.untag.field['num_entries_'] = length
            exceptionHandlersPtr.untag.field['handled_types_data_'] = ReadRef(self.deserializer.stream)
            data = []
            for j in range(length):
                info = {'handler_pc_offset': ReadInt_32(self.deserializer.stream)
                    , 'outer_try_index': ReadInt_16(self.deserializer.stream)
                    , 'needs_stacktrace': ReadInt_8(self.deserializer.stream)
                    , 'has_catch_all': ReadInt_8(self.deserializer.stream)
                    , 'is_generated': ReadInt_8(self.deserializer.stream)}
                data.append(info)

            self.deserializer.references[refId] = exceptionHandlersPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class ContextDeserializationCluster:
    pass


class ContextScopeDeserializationCluster:
    pass


class UnlinkedCallDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('UnlinkedCall')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            unlinkedCallPtr = UnlinkedCallPtr(refId)
            self._ReadFromTo(unlinkedCallPtr)
            unlinkedCallPtr.untag.field['can_patch_to_monomorphic_'] = ReadBool(self.deserializer.stream)
            self.deserializer.references[refId] = unlinkedCallPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class MegamorphicCacheDeserializationCluster:
    pass


class SubtypeTestCacheDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('SubtypeTestCache')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            subtypeTestCachePtr = SubtypeTestCachePtr(refId)
            subtypeTestCachePtr.untag.field['cache_'] = ReadRef(self.deserializer.stream)
            self.deserializer.references[refId] = subtypeTestCachePtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class LoadingUnitDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('LoadingUnit')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            loadingUnitPtr = LoadingUnitPtr(refId)
            loadingUnitPtr.untag.field['parent_'] = ReadRef(self.deserializer.stream)
            loadingUnitPtr.untag.field['base_objects_'] = None
            loadingUnitPtr.untag.field['id_'] = ReadInt_32(self.deserializer.stream)
            loadingUnitPtr.untag.field['loaded_'] = False
            loadingUnitPtr.untag.field['load_outstanding_'] = False
            self.deserializer.references[refId] = loadingUnitPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class UnhandledExceptionDeserializationCluster:
    pass


class LibraryPrefixDeserializationCluster:
    pass


class TypeRefDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('TypeRef')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            typeRefPtr = TypeRefPtr(refId)
            self._ReadFromTo(typeRefPtr)
            self.deserializer.references[refId] = typeRefPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class ClosureDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('Closure')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            closurePtr = ClosurePtr(refId)
            self._ReadFromTo(closurePtr)
            self.deserializer.references[refId] = closurePtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class GrowableObjectArrayDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('GrowableObjectArray')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            growableObjectArrayPtr = GrowableObjectArrayPtr(refId)
            self._ReadFromTo(growableObjectArrayPtr)
            self.deserializer.references[refId] = growableObjectArrayPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

    def _ReadFromTo(self, obj):
        for key in obj.untag.point_field:
            obj.untag.point_field[key] = ReadRef(self.deserializer.stream)


class StackTraceDeserializationCluster:
    pass


class RegExpDeserializationCluster:
    pass


class WeakPropertyDeserializationCluster:
    pass


class LinkedHashMapDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('LinkedHashMap')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()

            map = {}
            in_read_from = self.deserializer.stream.tell()

            ReadFromTo(self.deserializer.stream, 5)
            out_read_from = self.deserializer.stream.tell()

            out_for = self.deserializer.stream.tell()

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class LinkedHashSetDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize('LinkedHashSet')

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()

            map = {}
            in_read_from = self.deserializer.stream.tell()

            ReadFromTo(self.deserializer.stream, 5)
            out_read_from = self.deserializer.stream.tell()

            out_for = self.deserializer.stream.tell()

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class ArrayDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)
            self.deserializer.AssignRef('Array')
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):

        in_pos = self.deserializer.stream.tell()
        for refId in range(self.start_index_, self.stop_index_):
            arrayPtr = ArrayPtr(refId)
            length = ReadUnsigned(self.deserializer.stream)
            arrayPtr.untag.field['type_arguments_'] = ReadRef(self.deserializer.stream)
            arrayPtr.untag.field['length_'] = length
            arrayPtr.untag.field['data'] = []
            for i in range(length):
                arrayPtr.untag.field['data'].append(ReadRef(self.deserializer.stream))
            self.deserializer.references[refId] = arrayPtr

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class NoneCluster(DeserializationCluster):
    def ReadAlloc(self):
        pass


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


AOTSymbolsNameList= [
    '_kDartVmSnapshotData',
    '_kDartVmSnapshotInstructions',
    '_kDartIsolateSnapshotData',
    '_kDartIsolateSnapshotInstructions',
    # '_kDartSnapshotBuildId'
]


# 映射实体的Dart Class
class DartClass:
    def __init__(self, deserializer, clazz):
        self.class_name = 'UnFind'
        self.functions = []
        obj1 = deserializer.references[clazz.untag.point_field['name']]
        if obj1:
            class_name = ''.join(chr(x) for x in obj1.untag.field['data'])
            self.class_name = class_name

        class_functions_id = clazz.untag.point_field['functions']
        references_obj2 = deserializer.references[class_functions_id]
        if references_obj2:
            func_list = references_obj2.untag.field['data']
            for f in func_list:
                dartFunction = DartFunction(deserializer, deserializer.references[f])
                self.functions.append(dartFunction)

    def __str__(self):
        s = 'class ' + self.class_name + "{\n"
        if len(self.functions) > 0:
            for f in self.functions:
                s = s + f.__str__()
        s = s + "}"
        return s


class DartFunction:
    def __init__(self, deserializer, func):
        self.func_name = ''
        self.code_offset = 0xffffffff
        obj1 = deserializer.references[func.untag.point_field['name']]
        if obj1:
            self.func_name = ''.join(chr(x) for x in (obj1.untag.field['data']))

    def __str__(self):
        s = '  ' + self.func_name + "(){}\n"
        return s

kCachedDescriptorCount = 32

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
        return int.from_bytes(stream.read(1), 'big', signed=False)  # No marker
    return Read(stream, kEndUnsignedByteMarker, math.ceil(size / 7))


def ReadUnInt_32(stream):
    return ReadUnsigned(stream, 32)


def ReadUnInt_64(stream):
    return ReadUnsigned(stream, 64)


def ReadUnInt_8(stream):
    return ReadUnsigned(stream, 8)


def ReadUnsigned64(stream):
    return ReadUnsigned(stream, 64)


def ReadInt(stream, size):
    if size == 8:
        return int.from_bytes(stream.read(1), 'big', signed=True)  # No marker
    return Read(stream, kEndByteMarker, math.ceil(size / 7))


def ReadInt_64(stream):
    return ReadInt(stream, 64)


def ReadInt_16(stream):
    return ReadInt(stream, 16)


def ReadInt_32(stream):
    return ReadInt(stream, 32)


def ReadInt_8(stream):
    return ReadInt(stream, 8)


def ReadByte(stream):
    return stream.read(1)


def ReadBytes(stream, size):
    return stream.read(size)


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




kFirstReference = 1


# ReadProgramSnapshot ProgramDeserializationRoots

class ProgramDeserializationRoots:
    def AddBaseObjects(self, deserializer):
        pass

    def ReadRoots(self, deserializer):
        pass


class Deserializer:
    def __init__(self, stream, kind, features):
        self.code = None
        self.symbol_table_ = None
        self.isProduct = None
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
        self.classes = {}
        self.next_ref_index_ = kFirstReference
        # 记录所有的引用 首先是baseObject 1025 个
        self.references = ['illegal']

        self.features = features
        self.kind = kind
        self.FLAG_precompiled_mode = False

        self.setConstants()

    def setConstants(self):
        self.isProduct = 'product' in self.features
        self.FLAG_precompiled_mode = self.kind == Kind.FULL_AOT and 'product' in self.features

    def deserialize(self):
        self.num_base_objects_ = ReadUnsigned(self.stream)
        self.num_objects_ = ReadUnsigned(self.stream)
        self.num_clusters_ = ReadUnsigned(self.stream)
        self.initial_field_table_len = ReadUnsigned(self.stream)
        self.instructions_table_len = ReadUnsigned(self.stream)
        self.instruction_table_data_offset = ReadUnsigned(self.stream)

        print('num_base_objects_ = ', self.num_base_objects_, 'num_objects_ = ', self.num_objects_, self.num_clusters_)
        # print('num_base_objects_ = ', self.num_base_objects_, 'num_objects_ = ', self.num_objects_, self.num_clusters_,
        #       self.initial_field_table_len, self.instructions_table_len, self.instruction_table_data_offset)

        # trace 1025 51549 308 572 7193 16 print(self.num_base_objects_, self.num_objects_, self.num_clusters_,
        # self.initial_field_table_len,self.instructions_table_len, self.instruction_table_data_offset)

        self.AddBaseObjects()

        if self.num_base_objects_ != (self.next_ref_index_ - kFirstReference):
            raise Exception('init baseObject fail')

        for _ in range(self.num_clusters_):
            cluster = self.readCluster
            self.cluster_list.append(cluster)
            cluster.ReadAlloc()

        print(len(self.references), self.num_objects_ + 1)

        if len(self.references) != self.num_objects_ + 1:
            print('error')

        for _ in range(self.num_clusters_):
            cluster = self.cluster_list[_]
            self.cluster_list.append(cluster)
            cluster.ReadFill()

        for clazz in self.classes.values():
            print(DartClass(self, clazz))

    @staticmethod
    def IncludesCode(kind):
        return (kind == Kind.FULL_JIT) or (kind == Kind.FULL_AOT)

    def AssignRef(self, obj=None):
        self.references.append(obj)
        self.next_ref_index_ = self.next_ref_index_ + 1

    def AddBaseObjects(self):
        # ReadProgramSnapshot AddBaseObjects 要从dartvm 第一个区块里面解析出来 暂时忽略
        for read_id in range(self.num_base_objects_):
            self.AddBaseObject(None)

    def AddBaseObject(self, obj):
        self.AssignRef(obj)

    def next_index(self):
        return self.next_ref_index_

    def ReadRoots(self):
        self.symbol_table_ = ReadRef(self.stream)
        for i in range(kNumStubEntries):
            self.code = ReadRef(self.stream)

    @property
    def readCluster(self):
        read_cid_before = self.stream.tell()
        cid_and_canonical = ReadInt_64(self.stream)
        cid = (cid_and_canonical >> 1) & kMaxUint32
        is_canonical = (cid_and_canonical & 0x1) == 0x1

        read_cid_after = self.stream.tell()
        # print('read_cid_before =', read_cid_before, 'read_cid_after =', read_cid_after, 'cid =', cid, 'is_canonical',is_canonical)
        # print("cid_and_canonical", cid_and_canonical, 'cid', cid, 'is_canonical', is_canonical)
        ###
        cluster = ClusterGetter(cid, is_canonical, self).getCluster()
        # print(cluster, cid)
        return cluster

kCompressedWordSizeLog2 = 2 # fix 3
kCompressedWordSize = 4     # fix 8


kObjectAlignment = 16

# 快照类型的枚举类
from enum import Enum


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



kTaggedObject = 0
kImmediate = 1
kNativeFunction = 2
kSwitchableCallMissEntryPoint = 3
kMegamorphicCallEntryPoint = 4

kCachedICDataZeroArgTestedWithoutExactnessTrackingIdx = 0
kCachedICDataMaxArgsTestedWithoutExactnessTracking = 2
kCachedICDataOneArgWithExactnessTrackingIdx = kCachedICDataZeroArgTestedWithoutExactnessTrackingIdx + kCachedICDataMaxArgsTestedWithoutExactnessTracking + 1
kCachedICDataArrayCount = kCachedICDataOneArgWithExactnessTrackingIdx + 1


def RoundedAllocationSize(size):
    return Utils.roundUp(size, kObjectAlignment)


class TypedData:
    @staticmethod
    def ElementSizeInBytes(cid):
        return TypedData.ElementSize(TypedData.ElementType(cid))

    @staticmethod
    def ElementType(cid):
        if cid == kByteDataViewCid:
            return 1
        elif IsTypedDataClassId(cid):
            return (cid - kTypedDataInt8ArrayCid - kTypedDataCidRemainderInternal) / 3
        elif IsTypedDataViewClassId(cid):
            return (cid - kTypedDataInt8ArrayCid - kTypedDataCidRemainderView) / 3
        elif IsExternalTypedDataClassId(cid):
            return (cid - kTypedDataInt8ArrayCid - kTypedDataCidRemainderExternal) / 3

    @staticmethod
    def ElementSize(index):
        return [1, 1, 1, 2, 2, 4, 4, 8, 8, 4, 8, 16, 16, 16][int(index)]


class StaticBit:
    @staticmethod
    def decode(value):
        r = (value >> 1) & 1
        if r == 0:
            return False
        elif r == 1:
            return True
        else:
            raise Exception('Encountered non-boolean expression')


class ClassPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedClass()


class FunctionPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedFunction()


class ObjectPoolPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedObjectPool()
        self.TypeBits = BitField()


class PcDescriptorsPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedPcDescriptors()


class ExceptionHandlersPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedExceptionHandlers()


class UnlinkedCallPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedUnlinkedCall()


class SubtypeTestCachePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedSubtypeTestCache()


class TypeParametersPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedTypeParameters()


class DoublePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedDouble()


class GrowableObjectArrayPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedGrowableObjectArray()


class TypedDataPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedTypedData()


class ArrayPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedArray()


class ClosurePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedClosure()


class TypeRefPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedTypeRef()


class TypePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedType()


class TypeArgumentsPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedTypeArguments()


class InstancePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedInstance()


class LoadingUnitPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedLoadingUnit()


class CodePtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedCode()


class PatchClassPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedClass()


class ClosureDataPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedClosureData()


class FfiTrampolineDataPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedFfiTrampolineData()


class FieldPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedField()


class StringPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedString()


class ScriptPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedScript()


class LibraryPtr:
    def __init__(self, _id):
        self._id = _id
        self.untag = UntaggedLibrary()


class BaseObject:
    def __init__(self, cid, is_base, name):
        self.cid = cid
        self.is_base = is_base
        self.name = name


DART_PRECOMPILED_RUNTIME = True
PRODUCT = True


class UntaggedString:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedClass:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['name'] = 0
        if not PRODUCT:
            self.point_field['user_name'] = 0
        self.point_field['functions'] = 0
        self.point_field['functions_hash_table'] = 0
        self.point_field['fields'] = 0
        self.point_field['offset_in_words_to_field'] = 0
        self.point_field['interfaces'] = 0
        self.point_field['script'] = 0
        self.point_field['library'] = 0
        self.point_field['type_parameters'] = 0
        self.point_field['super_type'] = 0
        self.point_field['constants'] = 0
        self.point_field['declaration_type'] = 0
        self.point_field['invocation_dispatcher_cache'] = 0

        if not PRODUCT or not DART_PRECOMPILED_RUNTIME:
            self.point_field['direct_implementors'] = 0
            self.point_field['direct_subclasses'] = 0

        if not DART_PRECOMPILED_RUNTIME:
            self.point_field['allocation_stub'] = 0
            self.point_field['dependent_code'] = 0


class UntaggedExceptionHandlers:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedPcDescriptors:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedFunction:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['name'] = 0
        self.point_field['owner'] = 0
        self.point_field['signature'] = 0
        self.point_field['data'] = 0
        if DART_PRECOMPILED_RUNTIME:
            pass
        else:
            self.point_field['positional_parameter_names'] = 0
            self.point_field['unoptimized_code'] = 0


class UntaggedObjectPool:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedClosureData:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedFfiTrampolineData:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['signature_type'] = 0
        self.point_field['c_signature'] = 0
        self.point_field['callback_target'] = 0
        self.point_field['callback_exceptional_return'] = 0


class UntaggedCode:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedSubtypeTestCache:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedTypeRef:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['type_test_stub'] = 0
        self.point_field['type'] = 0


class UntaggedDouble:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedArray:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedTypedData:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedGrowableObjectArray:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['type_arguments'] = 0
        self.point_field['length'] = 0
        self.point_field['data'] = 0


class UntaggedClosure:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['instantiator_type_arguments'] = 0
        self.point_field['function_type_arguments'] = 0
        self.point_field['delayed_type_arguments'] = 0
        self.point_field['function'] = 0
        self.point_field['context'] = 0
        self.point_field['hash'] = 0


class UntaggedTypeParameters:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['names'] = 0
        self.point_field['flags'] = 0
        self.point_field['bounds'] = 0
        self.point_field['defaults'] = 0


class UntaggedType:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['type_test_stub'] = 0
        self.point_field['arguments'] = 0
        self.point_field['hash'] = 0


class UntaggedTypeArguments:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedInstance:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedLoadingUnit:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass


class UntaggedUnlinkedCall:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['target_name'] = 0
        self.point_field['args_descriptor'] = 0


class UntaggedField:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['name'] = 0
        self.point_field['owner'] = 0
        self.point_field['type'] = 0
        self.point_field['initializer_function'] = 0


class UntaggedLibrary:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['name'] = 0
        self.point_field['url'] = 0
        self.point_field['private_key'] = 0
        self.point_field['dictionary'] = 0
        self.point_field['metadata'] = 0

        self.point_field['toplevel_class'] = 0
        self.point_field['used_scripts'] = 0
        self.point_field['loading_unit'] = 0
        self.point_field['imports'] = 0
        self.point_field['exports'] = 0


class UntaggedScript:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        self.point_field['url'] = 0


class UntaggedPatchClass:
    def __init__(self):
        self.field = {}
        self.point_field = {}
        self.set_point_field()

    def set_point_field(self):
        pass






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
        magic = self.check_magic()
        le = self.large_length()
        kind = self.kind()
        version = ReadVersion(self.stream)
        features = str(ReadFeatures(self.stream))
        print(magic)
        print(le)
        print(version)
        print(features)
        Deserializer(stream=self.stream, kind=kind, features=features).deserialize()

    def check_magic(self):
        magic = hex(int.from_bytes(self.stream.read(kMagicSize), 'little'))
        return magic

    def large_length(self):
        length_size = int.from_bytes(self.stream.read(kLengthSize), 'little')
        return length_size

    def kind(self):
        kind = Kind(int.from_bytes(self.stream.read(kKindSize), 'little'))
        return kind

kNumStubEntries = 131

class Utils:
    @staticmethod
    def roundUp(n, m):
        return (n - 1) + m - (n - 1) % m


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

    #vm_snapshot_data = Snapshots['_kDartVmSnapshotData']
    # vm roots 加载的是基本类 没必要解析 核心的还是看 isolate
    # vm_snapshot_ = Snapshot(vm_snapshot_data['blob']).SnapshotSetupFromBuffer()

    isolate_snapshot_data = Snapshots['_kDartIsolateSnapshotData']
    isolate_snapshot_ = Snapshot(isolate_snapshot_data['blob']).SnapshotSetupFromBuffer()


if __name__ == '__main__':
    parse_elf_file('libapp.so')
