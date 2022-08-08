from enum import Enum


def IsTypedDataViewClassId(cid):
    return False


def IsExternalTypedDataClassId(cid):
    return False


def IsTypedDataClassId(cid):
    return False


kNumPredefinedCids = 158
kInstanceCid = 43


class ClassId(Enum):
    kIllegalCid = 0  # x
    kNativePointer = 1  # x
    kFreeListElement = 2  # x
    kForwardingCorpse = 3  # x
    #  CLASS_LIST(DEFINE_OBJECT_KIND)    5 - 92
    #  CLASS_LIST_FFI(DEFINE_OBJECT_KIND) 93 - 108
    #  CLASS_LIST_TYPED_DATA(DEFINE_OBJECT_KIND) 110 - 123
    kByteDataViewCid = 123
    kByteBufferCid = 124
    kNullCid = 125
    kDynamicCid = 126
    kVoidCid = 127
    kNeverCid = 128
    kNumPredefinedCids = 129


class CLASS_LIST(Enum):
    kObject = 4
    # CLASS_LIST_NO_OBJECT(V) 5 - 92


class CLASS_LIST_NO_OBJECT(Enum):
    pass
    # CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP(V) 5 - 81
    # CLASS_LIST_MAPS(V)  82 - 83
    # CLASS_LIST_SETS(V)  84 - 85
    # CLASS_LIST_ARRAYS(V) 86 - 88
    # CLASS_LIST_STRINGS(V) 89 - 92


class CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP(Enum):
    pass
    # CLASS_LIST_INTERNAL_ONLY(V)        5-42
    # CLASS_LIST_INSTANCE_SINGLETONS(V)  43-81


class CLASS_LIST_INTERNAL_ONLY(Enum):
    kClass = 5
    kPatchClass = 6
    kFunction = 7
    kTypeParameters = 8  # x
    kClosureData = 9 # x
    kFfiTrampolineData = 10
    kField = 11
    kScript = 12
    kLibrary = 13
    kNamespace = 14
    kKernelProgramInfo = 15
    kWeakSerializationReference = 16
    kCode = 17
    kInstructions = 18
    kInstructionsSection = 19
    kInstructionsTable = 20
    kObjectPool = 21  # x
    kPcDescriptors = 22
    kCodeSourceMap = 23
    kCompressedStackMaps = 24
    kLocalVarDescriptors = 25
    kExceptionHandlers = 26
    kContext = 27
    kContextScope = 28
    kSentinel = 29
    kSingleTargetCache = 30
    kUnlinkedCall = 31
    kMonomorphicSmiableCall = 32
    kCallSiteData = 33
    kICData = 34
    kMegamorphicCache = 35
    kSubtypeTestCache = 36
    kLoadingUnit = 37
    kError = 38
    kApiError = 39
    kLanguageError = 40
    kUnhandledException = 41
    kUnwindError = 42


class CLASS_LIST_INSTANCE_SINGLETONS(Enum):
    kInstance = 42
    kLibraryPrefix = 44
    kTypeArguments = 45
    kAbstractType = 46
    kType = 47
    kFinalizerBase = 48
    kFinalizer = 49
    kNativeFinalizer = 50
    kFinalizerEntry = 51
    kFunctionType = 52
    kTypeRef = 53  # x
    kTypeParameter = 54
    kClosure = 55
    kNumber = 56
    kInteger = 57
    kSmi = 58
    kMint = 59
    kDouble = 60
    kBool = 61
    kFloat32x4 = 62
    kInt32x4 = 63
    kFloat64x2 = 64
    kTypedDataBase = 65
    kTypedData = 66
    kExternalTypedData = 67
    kTypedDataView = 68
    kPointer = 69
    kDynamicLibrary = 70
    kCapability = 71
    kReceivePort = 72
    kSendPort = 73
    kStackTrace = 74
    kRegExp = 75
    kWeakProperty = 76
    kWeakReference = 77
    kMirrorReference = 78
    kFutureOr = 79
    kUserTag = 80
    kTransferableTypedData = 81


class CLASS_LIST_MAPS(Enum):
    LinkedHashMap = 82
    ImmutableLinkedHashMap = 83


class CLASS_LIST_SETS(Enum):
    LinkedHashSet = 84
    ImmutableLinkedHashSet = 85


class CLASS_LIST_ARRAYS(Enum):
    # CLASS_LIST_FIXED_LENGTH_ARRAYS(V) 86 - 87
    GrowableObjectArray = 88


class CLASS_LIST_FIXED_LENGTH_ARRAYS(Enum):
    FIXED_Array = 86
    FIXED_ImmutableArray = 87


class CLASS_LIST_STRINGS(Enum):
    String = 89
    OneByteString = 90
    TwoByteString = 91
    ExternalOneByteString = 92
    ExternalTwoByteString = 93


class CLASS_LIST_FFI(Enum):
    FFI_NativeFunction = 93
    # CLASS_LIST_FFI_TYPE_MARKER(V) 94 - 106
    FFI_NativeType = 107
    FFI_Struct = 108


class CLASS_LIST_FFI_TYPE_MARKER(Enum):
    # CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(V) 94 - 103
    FFI_Void = 104
    FFI_Handle = 105
    FFI_Bool = 106


class CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(Enum):
    FFI_Int8 = 94
    FFI_Int16 = 95
    FFI_Int32 = 96
    FFI_Int64 = 97
    FFI_Uint8 = 98
    FFI_Uint16 = 99
    FFI_Uint32 = 100
    FFI_Uint64 = 101
    FFI_Float = 102
    FFI_Double = 103


class CLASS_LIST_TYPED_DATA(Enum):
    TYPE_Int8Array = 110
    TYPE_Uint8Array = 111
    TYPE_Uint8ClampedArray = 112
    TYPE_Int16Array = 113
    TYPE_Uint16Array = 114
    TYPE_Int32Array = 115
    TYPE_Uint32Array = 116
    TYPE_Int64Array = 117
    TYPE_Uint64Array = 118
    TYPE_Float32Array = 119
    TYPE_Float64Array = 120
    TYPE_Float32x4Array = 121
    TYPE_Int32x4Array = 122
    TYPE_Float64x2Array = 123
