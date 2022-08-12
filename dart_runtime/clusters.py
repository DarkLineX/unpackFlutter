from dart_runtime.app_snapshot import ReadFromTo
from dart_runtime.cid import *
from dart_runtime.datastream import readUnsigned, readInt, readInt_64, readInt_32, readInt_8

kNullabilityBitSize = 2
kNullabilityBitMask = (1 << kNullabilityBitSize) - 1


class DeserializationCluster:
    def __init__(self, cid, is_canonical, deserializer):
        self.cid = cid
        self.is_canonical = is_canonical
        self.deserializer = deserializer
        self.start_index_ = 0
        self.stop_index_ = 0

    def ReadAllocFixedSize(self):
        self.start_index_ = self.deserializer.next_index()
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        self.stop_index_ = self.deserializer.next_index()


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
        self.ReadAllocFixedSize()


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
        # readFill in pos =  62560
        # readFill out pos =  247023
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            encoded = readUnsigned(self.deserializer.stream)
            length, cid = self.DecodeLengthAndCid(encoded)
            if cid == kOneByteStringCid:
                for _ in range(length):
                    code_unit = readInt(self.deserializer.stream, 8)
            else:
                for _ in range(length):
                    code_unit = readInt(self.deserializer.stream, 8)
                    code_unit_2 = readInt(self.deserializer.stream, 8)
                    code_unit = (code_unit | code_unit_2 << 8)
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'readFill in pos = ', in_pos, 'out pos =', out_pos)


class DoubleDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()

    def readFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            encoded = readUnsigned(self.deserializer.stream)
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'readFill in pos = ', in_pos, 'out pos =', out_pos)


class TypeParameterDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()
        self.BuildCanonicalSetFromLayout()

    def readFill(self):
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            # 在 num_objects_ 里面取一个出来
            typeParameter = {}
            ReadFromTo(self.deserializer)
            parameterized_class_id_ = readInt_32(self.deserializer.stream)
            base_ = readInt_8(self.deserializer.stream)
            index_ = readInt_8(self.deserializer.stream)
            combined = readInt_8(self.deserializer.stream)
            flags_ = combined >> kNullabilityBitSize
            nullability_ = combined & kNullabilityBitMask

        # ReadFromTo(self.deserializer)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'readFill in pos = ', in_pos, 'out pos =', out_pos,self.start_index_, self.stop_index_)


class TypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()


class MintDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readUnsigned(self.deserializer.stream)

    def readFill(self):
        pass


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
        self.ReadAllocFixedSize()


class FunctionDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class FunctionTypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()


class ClosureDataDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class FfiTrampolineDataDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class FieldDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class ScriptDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class LibraryDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


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
        self.ReadAllocFixedSize()


class MegamorphicCacheDeserializationCluster:
    pass


class SubtypeTestCacheDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class LoadingUnitDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class UnhandledExceptionDeserializationCluster:
    pass


class LibraryPrefixDeserializationCluster:
    pass


class TypeRefDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class ClosureDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class GrowableObjectArrayDeserializationCluster(DeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class StackTraceDeserializationCluster:
    pass


class RegExpDeserializationCluster:
    pass


class WeakPropertyDeserializationCluster:
    pass


class LinkedHashMapDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


class LinkedHashSetDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self):
        self.ReadAllocFixedSize()


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
