# CLASS_LIST
#   Object                                                                    = 0
#   CLASS_LIST_NO_OBJECT(V
#     CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP(V
#       CLASS_LIST_INTERNAL_ONLY(V
#       CLASS_LIST_INSTANCE_SINGLETONS(V
#     CLASS_LIST_MAPS(V                                                           = 0
#     CLASS_LIST_SETS(V                                                           = 0
#     CLASS_LIST_ARRAYS(V                                                         = 0
#     CLASS_LIST_STRINGS(V

# CLASS_LIST_FFI

# CLASS_LIST_TYPED_DATA


kIllegalCid = 0
kNativePointer = 1
kFreeListElement = 2
kForwardingCorpse = 3

# CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP -> CLASS_LIST_INTERNAL_ONLY
Object = 4
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

# CLASS_LIST_NO_OBJECT_NOR_STRING_NOR_ARRAY_NOR_MAP -> CLASS_LIST_INSTANCE_SINGLETONS
Instance = 43
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

# CLASS_LIST_MAPS(V
LinkedHashMap = 82
ImmutableLinkedHashMap = 83
# CLASS_LIST_SETS(V
LinkedHashSet = 84
ImmutableLinkedHashSet = 85

#  CLASS_LIST_ARRAYS(V -> CLASS_LIST_FIXED_LENGTH_ARRAYS(V
Array = 86
ImmutableArray = 87
#  CLASS_LIST_ARRAYS(V
GrowableObjectArray = 88

# CLASS_LIST_STRINGS(V
String = 89
OneByteString = 90
TwoByteString = 91
ExternalOneByteString = 92
ExternalTwoByteString = 93

# START CLASS_LIST_FFI(V)
NativeFunction = 94
# START CLASS_LIST_FFI(V) -> CLASS_LIST_FFI_TYPE_MARKER(V)
# START CLASS_LIST_FFI(V) -> CLASS_LIST_FFI_TYPE_MARKER(V) -> CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(V)
Int8 = 95
Int16 = 95
Int32 = 95
Int64 = 95
Uint8 = 95
Uint16 = 95
Uint32 = 95
Uint64 = 95
Float = 95
Double = 95
# END CLASS_LIST_FFI(V) -> CLASS_LIST_FFI_TYPE_MARKER(V) -> CLASS_LIST_FFI_NUMERIC_FIXED_SIZE(V)
Void = 96
Handle = 97
Bool = 98
# END CLASS_LIST_FFI(V) -> CLASS_LIST_FFI_TYPE_MARKER(V)
NativeType = 0
Struct = 0
# END CLASS_LIST_FFI(V)

kByteDataViewCid = 100

kByteBufferCid = 101

kNullCid = 102
kDynamicCid = 102
kVoidCid = 103
kNeverCid = 104

kNumPredefinedCids = 105
