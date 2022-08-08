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
    def __init__(self, cid):
        pass


class TypeParametersDeserializationCluster:
    pass


class TypeArgumentsDeserializationCluster:
    pass


class StringDeserializationCluster:
    pass


class PatchClassDeserializationCluster:
    pass


class FunctionDeserializationCluster:
    pass


class ClosureDataDeserializationCluster:
    pass


class FfiTrampolineDataDeserializationCluster:
    pass


class FieldDeserializationCluster:
    pass


class ScriptDeserializationCluster:
    pass


class LibraryDeserializationCluster:
    pass


class NamespaceDeserializationCluster:
    pass


class KernelProgramInfoDeserializationCluster:
    pass


class CodeDeserializationCluster:
    pass


class ObjectPoolDeserializationCluster:
    pass


class PcDescriptorsDeserializationCluster:
    pass


class CodeSourceMapDeserializationCluster:
    pass


class CompressedStackMapsDeserializationCluster:
    pass


class ExceptionHandlersDeserializationCluster:
    pass


class ContextDeserializationCluster:
    pass


class ContextScopeDeserializationCluster:
    pass


class UnlinkedCallDeserializationCluster:
    pass


class MegamorphicCacheDeserializationCluster:
    pass


class SubtypeTestCacheDeserializationCluster:
    pass


class LoadingUnitDeserializationCluster:
    pass


class UnhandledExceptionDeserializationCluster:
    pass


class LibraryPrefixDeserializationCluster:
    pass


class TypeDeserializationCluster:
    pass


class FunctionTypeDeserializationCluster:
    pass


class TypeRefDeserializationCluster:
    pass


class TypeParameterDeserializationCluster:
    pass


class ClosureDeserializationCluster:
    pass


class MintDeserializationCluster:
    pass


class DoubleDeserializationCluster:
    pass


class GrowableObjectArrayDeserializationCluster:
    pass


class StackTraceDeserializationCluster:
    pass


class RegExpDeserializationCluster:
    pass


class WeakPropertyDeserializationCluster:
    pass


class LinkedHashMapDeserializationCluster:
    pass


class LinkedHashSetDeserializationCluster:
    pass


class ArrayDeserializationCluster:
    pass


class NoneCluster:
    pass


class ClusterGetter:
    def __init__(self, cid):
        self.cid = cid

    def kClassCid(self):
        return ClassDeserializationCluster(self.cid)

    def kTypeParametersCid(self):
        return TypeParametersDeserializationCluster(self.cid)

    def kTypeArgumentsCid(self):
        return TypeArgumentsDeserializationCluster(self.cid)

    def kPatchClassCid(self):
        return PatchClassDeserializationCluster(self.cid)

    def kFunctionCid(self):
        return FunctionDeserializationCluster(self.cid)

    def kClosureDataCid(self):
        return ClosureDataDeserializationCluster(self.cid)

    def kFfiTrampolineDataCid(self):
        return FfiTrampolineDataDeserializationCluster(self.cid)

    def kFieldCid(self):
        return FieldDeserializationCluster(self.cid)

    def kScriptCid(self):
        return ScriptDeserializationCluster(self.cid)

    def kLibraryCid(self):
        return LibraryDeserializationCluster(self.cid)

    def kNamespaceCid(self):
        return NamespaceDeserializationCluster(self.cid)

    def kKernelProgramInfoCid(self):
        return KernelProgramInfoDeserializationCluster(self.cid)

    def kCodeCid(self):
        return CodeDeserializationCluster(self.cid)

    def kObjectPoolCid(self):
        return ObjectPoolDeserializationCluster(self.cid)

    def kPcDescriptorsCid(self):
        return PcDescriptorsDeserializationCluster(self.cid)

    def kCodeSourceMapCid(self):
        return CodeSourceMapDeserializationCluster(self.cid)

    def kCompressedStackMapsCid(self):
        return CompressedStackMapsDeserializationCluster(self.cid)

    def kExceptionHandlersCid(self):
        return ExceptionHandlersDeserializationCluster(self.cid)

    def kContextCid(self):
        return ContextDeserializationCluster(self.cid)

    def kContextScopeCid(self):
        return ContextScopeDeserializationCluster(self.cid)

    def kUnlinkedCallCid(self):
        return UnlinkedCallDeserializationCluster(self.cid)

    def kMegamorphicCacheCid(self):
        return MegamorphicCacheDeserializationCluster(self.cid)

    def kContextScopeCid(self):
        return ContextScopeDeserializationCluster(self.cid)

    def kSubtypeTestCacheCid(self):
        return SubtypeTestCacheDeserializationCluster(self.cid)

    def kLoadingUnitCid(self):
        return LoadingUnitDeserializationCluster(self.cid)

    def kUnhandledExceptionCid(self):
        return UnhandledExceptionDeserializationCluster(self.cid)

    def kLibraryPrefixCid(self):
        return LibraryPrefixDeserializationCluster(self.cid)

    def kTypeCid(self):
        return TypeDeserializationCluster(self.cid)

    def kFunctionTypeCid(self):
        return FunctionTypeDeserializationCluster(self.cid)

    def kTypeRefCid(self):
        return TypeRefDeserializationCluster(self.cid)

    def kTypeParameterCid(self):
        return TypeParameterDeserializationCluster(self.cid)

    def kClosureCid(self):
        return ClosureDeserializationCluster(self.cid)

    def kMintCid(self):
        return MintDeserializationCluster(self.cid)

    def kDoubleCid(self):
        return DoubleDeserializationCluster(self.cid)

    def kGrowableObjectArrayCid(self):
        return GrowableObjectArrayDeserializationCluster(self.cid)

    def kStackTraceCid(self):
        return StackTraceDeserializationCluster(self.cid)

    def kRegExpCid(self):
        return RegExpDeserializationCluster(self.cid)

    def kWeakPropertyCid(self):
        return WeakPropertyDeserializationCluster(self.cid)

    def kLinkedHashMapCid(self):
        return NoneCluster(self.cid)

    def kImmutableLinkedHashMapCid(self):
        return LinkedHashMapDeserializationCluster(self.cid)

    def kLinkedHashSetCid(self):
        return NoneCluster(self.cid)

    def kImmutableLinkedHashSetCid(self):
        return LinkedHashSetDeserializationCluster(self.cid)

    def kArrayCid(self):
        return ArrayDeserializationCluster(self.cid)

    def kImmutableArrayCid(self):
        return ArrayDeserializationCluster(self.cid)

    def kStringCid(self):
        return StringDeserializationCluster(self.cid)
