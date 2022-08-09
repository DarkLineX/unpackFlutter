from dart_runtime.app_snapshot import ReadAllocFixedSize
from dart_runtime.cid import *
from dart_runtime.datastream import readUnsigned, readInt, readInt_64


class Clusters:
    def __init__(self, cid):
        pass

    def readAlloc(self, isCanonical):
        pass


#  -----------------------------------------


class ClassDeserializationCluster:
    def __init__(self, cid, deserializer):
        self.cid = cid
        self.deserializer = deserializer


class AbstractInstanceDeserializationCluster(ClassDeserializationCluster):
    pass


class InstanceDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self, is_canonical):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readUnsigned(self.deserializer.stream)


class TypedDataViewDeserializationCluster(ClassDeserializationCluster):
    pass


class ExternalTypedDataDeserializationCluster(ClassDeserializationCluster):
    pass


class TypedDataDeserializationCluster(ClassDeserializationCluster):
    pass


class CanonicalSetDeserializationCluster(ClassDeserializationCluster):
    def BuildCanonicalSetFromLayout(self, start_index_, stop_index_):
        # count = 8569 stop_index_ = 9595 start_index_ = 1026 first_element_ = 0
        table_length = readUnsigned(self.deserializer.stream)
        first_element_ = readUnsigned(self.deserializer.stream)
        count = stop_index_ - (start_index_ + first_element_)
        print(count, stop_index_, start_index_, first_element_, table_length)
        for _ in range(start_index_ + first_element_, stop_index_):
            readUnsigned(self.deserializer.stream)


class TypeParametersDeserializationCluster(ClassDeserializationCluster):
    pass


class TypeArgumentsDeserializationCluster(ClassDeserializationCluster):
    pass


class StringDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self, is_canonical):
        # 229
        start_index_ = self.deserializer.next_index()
        count = readUnsigned(self.deserializer.stream)
        # 231
        # 8569
        for _ in range(count):
            readUnsigned(self.deserializer.stream)
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        # 8974
        stop_index_ = self.deserializer.next_index()

        self.BuildCanonicalSetFromLayout(start_index_, stop_index_)


class MintDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self, is_canonical):
        count = readUnsigned(self.deserializer.stream)
        for _ in range(count):
            readUnsigned(self.deserializer.stream)


class DoubleDeserializationCluster(AbstractInstanceDeserializationCluster):
    def readAlloc(self, is_canonical):
        ReadAllocFixedSize(self.deserializer)


class TypeParameterDeserializationCluster(CanonicalSetDeserializationCluster):
    def readAlloc(self, is_canonical):
        start_index_ = self.deserializer.next_index()
        ReadAllocFixedSize(self.deserializer)
        stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout(start_index_, stop_index_);


class PatchClassDeserializationCluster(ClassDeserializationCluster):
    pass


class FunctionDeserializationCluster(ClassDeserializationCluster):
    pass


class ClosureDataDeserializationCluster(ClassDeserializationCluster):
    pass


class FfiTrampolineDataDeserializationCluster(ClassDeserializationCluster):
    pass


class FieldDeserializationCluster(ClassDeserializationCluster):
    pass


class ScriptDeserializationCluster(ClassDeserializationCluster):
    pass


class LibraryDeserializationCluster(ClassDeserializationCluster):
    pass


class NamespaceDeserializationCluster(ClassDeserializationCluster):
    pass


class KernelProgramInfoDeserializationCluster(ClassDeserializationCluster):
    pass


class CodeDeserializationCluster(ClassDeserializationCluster):
    pass


class ObjectPoolDeserializationCluster(ClassDeserializationCluster):
    pass


class PcDescriptorsDeserializationCluster(ClassDeserializationCluster):
    pass


class CodeSourceMapDeserializationCluster(ClassDeserializationCluster):
    pass


class CompressedStackMapsDeserializationCluster(ClassDeserializationCluster):
    pass


class ExceptionHandlersDeserializationCluster(ClassDeserializationCluster):
    pass


class ContextDeserializationCluster(ClassDeserializationCluster):
    pass


class ContextScopeDeserializationCluster(ClassDeserializationCluster):
    pass


class UnlinkedCallDeserializationCluster(ClassDeserializationCluster):
    pass


class MegamorphicCacheDeserializationCluster(ClassDeserializationCluster):
    pass


class SubtypeTestCacheDeserializationCluster(ClassDeserializationCluster):
    pass


class LoadingUnitDeserializationCluster(ClassDeserializationCluster):
    pass


class UnhandledExceptionDeserializationCluster(ClassDeserializationCluster):
    pass


class LibraryPrefixDeserializationCluster(ClassDeserializationCluster):
    pass


class TypeDeserializationCluster(ClassDeserializationCluster):
    pass


class FunctionTypeDeserializationCluster(ClassDeserializationCluster):
    pass


class TypeRefDeserializationCluster(ClassDeserializationCluster):
    pass


class ClosureDeserializationCluster(ClassDeserializationCluster):
    pass


class GrowableObjectArrayDeserializationCluster(ClassDeserializationCluster):
    pass


class StackTraceDeserializationCluster(ClassDeserializationCluster):
    pass


class RegExpDeserializationCluster(ClassDeserializationCluster):
    pass


class WeakPropertyDeserializationCluster(ClassDeserializationCluster):
    pass


class LinkedHashMapDeserializationCluster(ClassDeserializationCluster):
    pass


class LinkedHashSetDeserializationCluster(ClassDeserializationCluster):
    pass


class ArrayDeserializationCluster(ClassDeserializationCluster):
    pass


class NoneCluster(ClassDeserializationCluster):
    def readAlloc(self, is_canonical):
        pass


# kStringCid = 89
# kClassCid = 5
# kTypeParametersCid = 8
# kTypeArgumentsCid = 45


class ClusterGetter:

    def __init__(self, cid, deserializer):
        self.cid = cid
        self.deserializer = deserializer

    def getCluster(self):
        if self.cid == kClassCid:
            return ClassDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kTypeParametersCid:
            return TypeParametersDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kTypeArgumentsCid:
            return TypeArgumentsDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kPatchClassCid:
            return PatchClassDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kFunctionCid:
            return FunctionDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kClosureDataCid:
            return ClosureDataDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kFfiTrampolineDataCid:
            return FfiTrampolineDataDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kFieldCid:
            return FieldDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kScriptCid:
            return ScriptDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kLibraryCid:
            return LibraryDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kNamespaceCid:
            return NamespaceDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kKernelProgramInfoCid:
            return KernelProgramInfoDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kCodeCid:
            return CodeDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kObjectPoolCid:
            return ObjectPoolDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kPcDescriptorsCid:
            return PcDescriptorsDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kCodeSourceMapCid:
            return CodeSourceMapDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kCompressedStackMapsCid:
            return CompressedStackMapsDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kExceptionHandlersCid:
            return ExceptionHandlersDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kContextCid:
            return ContextDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kUnlinkedCallCid:
            return UnlinkedCallDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kMegamorphicCacheCid:
            return MegamorphicCacheDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kSubtypeTestCacheCid:
            return SubtypeTestCacheDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kLoadingUnitCid:
            return LoadingUnitDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kUnhandledExceptionCid:
            return UnhandledExceptionDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kLibraryPrefixCid:
            return LibraryPrefixDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kTypeCid:
            return TypeDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kFunctionTypeCid:
            return FunctionTypeDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kTypeRefCid:
            return TypeRefDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kTypeParameterCid:
            return TypeParameterDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kClosureCid:
            return ClosureDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kMintCid:
            return MintDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kDoubleCid:
            return DoubleDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kGrowableObjectArrayCid:
            return GrowableObjectArrayDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kStackTraceCid:
            return StackTraceDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kRegExpCid:
            return RegExpDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kWeakPropertyCid:
            return WeakPropertyDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kLinkedHashMapCid:
            return NoneCluster(self.cid, self.deserializer)

        if self.cid == kImmutableLinkedHashMapCid:
            return LinkedHashMapDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kLinkedHashSetCid:
            return NoneCluster(self.cid, self.deserializer)

        if self.cid == kImmutableLinkedHashSetCid:
            return LinkedHashSetDeserializationCluster(self.cid, self.deserializer)

        if self.cid == FIXED_kArrayCid:
            return ArrayDeserializationCluster(self.cid, self.deserializer)

        if self.cid == FIXED_kImmutableArrayCid:
            return ArrayDeserializationCluster(self.cid, self.deserializer)

        if self.cid == kStringCid:
            return StringDeserializationCluster(self.cid, self.deserializer)

        else:
            return NoneCluster(self.cid, self.deserializer)
