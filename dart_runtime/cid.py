from enum import Enum


class ClassId(Enum):
    kIllegalCid = 0
    kNativePointer = 1
    kFreeListElement = 2
    kForwardingCorpse = 3
    #  CLASS_LIST(DEFINE_OBJECT_KIND)    5 - 92
    #  CLASS_LIST_FFI(DEFINE_OBJECT_KIND) 93 - 108
    #  CLASS_LIST_TYPED_DATA(DEFINE_OBJECT_KIND) 109 - 122
    kByteDataViewCid = 123
    kByteBufferCid = 124
    kNullCid = 125
    kDynamicCid = 126
    kVoidCid = 127
    kNeverCid = 128
    kNumPredefinedCids = 129


class CLASS_LIST(Enum):
    Object = 4
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
    Class = 5
    PatchClass = 6
    Function = 7
    TypeParameters = 8
    ClosureData = 9
    FfiTrampolineData = 10
    Field = 11
    Script = 12
    Library = 13
    Namespace = 14
    KernelProgramInfo = 15
    WeakSerializationReference = 16
    Code = 17
    Instructions = 18
    InstructionsSection = 19
    InstructionsTable = 20
    ObjectPool = 21
    PcDescriptors = 22
    CodeSourceMap = 23
    CompressedStackMaps = 24
    LocalVarDescriptors = 25
    ExceptionHandlers = 26
    Context = 27
    ContextScope = 28
    Sentinel = 29
    SingleTargetCache = 30
    UnlinkedCall = 31
    MonomorphicSmiableCall = 32
    CallSiteData = 33
    ICData = 34
    MegamorphicCache = 35
    SubtypeTestCache = 36
    LoadingUnit = 37
    Error = 38
    ApiError = 39
    LanguageError = 40
    UnhandledException = 41
    UnwindError = 42


class CLASS_LIST_INSTANCE_SINGLETONS(Enum):
    Instance = 42
    LibraryPrefix = 44
    TypeArguments = 45
    AbstractType = 46
    Type = 47
    FinalizerBase = 48
    Finalizer = 49
    NativeFinalizer = 50
    FinalizerEntry = 51
    FunctionType = 52
    TypeRef = 53
    TypeParameter = 54
    Closure = 55
    Number = 56
    Integer = 57
    Smi = 58
    Mint = 59
    Double = 60
    Bool = 61
    Float32x4 = 62
    Int32x4 = 63
    Float64x2 = 64
    TypedDataBase = 65
    TypedData = 66
    ExternalTypedData = 67
    TypedDataView = 68
    Pointer = 69
    DynamicLibrary = 70
    Capability = 71
    ReceivePort = 72
    SendPort = 73
    StackTrace = 74
    RegExp = 75
    WeakProperty = 76
    WeakReference = 77
    MirrorReference = 78
    FutureOr = 79
    UserTag = 80
    TransferableTypedData = 81


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
    String = 88
    OneByteString = 89
    TwoByteString = 90
    ExternalOneByteString = 91
    ExternalTwoByteString = 92


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
    TYPE_Int8Array = 109
    TYPE_Uint8Array = 110
    TYPE_Uint8ClampedArray = 111
    TYPE_Int16Array = 112
    TYPE_Uint16Array = 113
    TYPE_Int32Array = 114
    TYPE_Uint32Array = 115
    TYPE_Int64Array = 116
    TYPE_Uint64Array = 117
    TYPE_Float32Array = 118
    TYPE_Float64Array = 119
    TYPE_Float32x4Array = 120
    TYPE_Int32x4Array = 121
    TYPE_Float64x2Array = 122
