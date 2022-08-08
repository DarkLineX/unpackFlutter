from dart_runtime.cid import *
from dart_runtime.datastream import readUnsigned, readInt, readInt_64


class Clusters:
    def __init__(self, cid):
        pass

    def readAlloc(self, isCanonical):
        pass


class InstanceDeserializationCluster:
    def __init__(self, cid):
        pass


class TypedDataViewDeserializationCluster:
    def __init__(self, cid):
        pass


class ExternalTypedDataDeserializationCluster:
    def __init__(self, cid):
        pass


class TypedDataDeserializationCluster:
    def __init__(self, cid, is_canonical):
        pass


#  -----------------------------------------


class ClassDeserializationCluster:
    def __init__(self, cid, stream):
        self.cid = cid
        self.stream = stream


class TypeParametersDeserializationCluster(ClassDeserializationCluster):
    pass


class TypeArgumentsDeserializationCluster(ClassDeserializationCluster):
    pass


class StringDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self, is_canonical):
        count = readUnsigned(self.stream)
        for _ in range(count):
            readUnsigned(self.stream)


class MintDeserializationCluster(ClassDeserializationCluster):
    def readAlloc(self, is_canonical):
        count = readUnsigned(self.stream)
        for _ in range(count):
            readInt_64(self.stream)


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


class TypeParameterDeserializationCluster(ClassDeserializationCluster):
    pass


class ClosureDeserializationCluster(ClassDeserializationCluster):
    pass


class DoubleDeserializationCluster(ClassDeserializationCluster):
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
    pass


# kStringCid = 89
# kClassCid = 5
# kTypeParametersCid = 8
# kTypeArgumentsCid = 45


class ClusterGetter:

    def __init__(self, cid, stream):
        self.cid = cid
        self.stream = stream

    def getCluster(self):
        if self.cid == kClassCid:
            return ClassDeserializationCluster(self.cid, self.stream)

        if self.cid == kTypeParametersCid:
            return TypeParametersDeserializationCluster(self.cid, self.stream)

        if self.cid == kTypeArgumentsCid:
            return TypeArgumentsDeserializationCluster(self.cid, self.stream)

        if self.cid == kPatchClassCid:
            return PatchClassDeserializationCluster(self.cid, self.stream)

        if self.cid == kFunctionCid:
            return FunctionDeserializationCluster(self.cid, self.stream)

        if self.cid == kClosureDataCid:
            return ClosureDataDeserializationCluster(self.cid, self.stream)

        if self.cid == kFfiTrampolineDataCid:
            return FfiTrampolineDataDeserializationCluster(self.cid, self.stream)

        if self.cid == kFieldCid:
            return FieldDeserializationCluster(self.cid, self.stream)

        if self.cid == kScriptCid:
            return ScriptDeserializationCluster(self.cid, self.stream)

        if self.cid == kLibraryCid:
            return LibraryDeserializationCluster(self.cid, self.stream)

        if self.cid == kNamespaceCid:
            return NamespaceDeserializationCluster(self.cid, self.stream)

        if self.cid == kKernelProgramInfoCid:
            return KernelProgramInfoDeserializationCluster(self.cid, self.stream)

        if self.cid == kCodeCid:
            return CodeDeserializationCluster(self.cid, self.stream)

        if self.cid == kObjectPoolCid:
            return ObjectPoolDeserializationCluster(self.cid, self.stream)

        if self.cid == kPcDescriptorsCid:
            return PcDescriptorsDeserializationCluster(self.cid, self.stream)

        if self.cid == kCodeSourceMapCid:
            return CodeSourceMapDeserializationCluster(self.cid, self.stream)

        if self.cid == kCompressedStackMapsCid:
            return CompressedStackMapsDeserializationCluster(self.cid, self.stream)

        if self.cid == kExceptionHandlersCid:
            return ExceptionHandlersDeserializationCluster(self.cid, self.stream)

        if self.cid == kContextCid:
            return ContextDeserializationCluster(self.cid, self.stream)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.stream)

        if self.cid == kUnlinkedCallCid:
            return UnlinkedCallDeserializationCluster(self.cid, self.stream)

        if self.cid == kMegamorphicCacheCid:
            return MegamorphicCacheDeserializationCluster(self.cid, self.stream)

        if self.cid == kContextScopeCid:
            return ContextScopeDeserializationCluster(self.cid, self.stream)

        if self.cid == kSubtypeTestCacheCid:
            return SubtypeTestCacheDeserializationCluster(self.cid, self.stream)

        if self.cid == kLoadingUnitCid:
            return LoadingUnitDeserializationCluster(self.cid, self.stream)

        if self.cid == kUnhandledExceptionCid:
            return UnhandledExceptionDeserializationCluster(self.cid, self.stream)

        if self.cid == kLibraryPrefixCid:
            return LibraryPrefixDeserializationCluster(self.cid, self.stream)

        if self.cid == kTypeCid:
            return TypeDeserializationCluster(self.cid, self.stream)

        if self.cid == kFunctionTypeCid:
            return FunctionTypeDeserializationCluster(self.cid, self.stream)

        if self.cid == kTypeRefCid:
            return TypeRefDeserializationCluster(self.cid, self.stream)

        if self.cid == kTypeParameterCid:
            return TypeParameterDeserializationCluster(self.cid, self.stream)

        if self.cid == kClosureCid:
            return ClosureDeserializationCluster(self.cid, self.stream)

        if self.cid == kMintCid:
            return MintDeserializationCluster(self.cid, self.stream)

        if self.cid == kDoubleCid:
            return DoubleDeserializationCluster(self.cid, self.stream)

        if self.cid == kGrowableObjectArrayCid:
            return GrowableObjectArrayDeserializationCluster(self.cid, self.stream)

        if self.cid == kStackTraceCid:
            return StackTraceDeserializationCluster(self.cid, self.stream)

        if self.cid == kRegExpCid:
            return RegExpDeserializationCluster(self.cid, self.stream)

        if self.cid == kWeakPropertyCid:
            return WeakPropertyDeserializationCluster(self.cid, self.stream)

        if self.cid == kLinkedHashMapCid:
            return NoneCluster(self.cid, self.stream)

        if self.cid == kImmutableLinkedHashMapCid:
            return LinkedHashMapDeserializationCluster(self.cid, self.stream)

        if self.cid == kLinkedHashSetCid:
            return NoneCluster(self.cid, self.stream)

        if self.cid == kImmutableLinkedHashSetCid:
            return LinkedHashSetDeserializationCluster(self.cid, self.stream)

        if self.cid == FIXED_kArrayCid:
            return ArrayDeserializationCluster(self.cid, self.stream)

        if self.cid == FIXED_kImmutableArrayCid:
            return ArrayDeserializationCluster(self.cid, self.stream)

        if self.cid == kStringCid:
            return StringDeserializationCluster(self.cid, self.stream)
