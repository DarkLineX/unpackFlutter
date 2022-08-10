from enum import Enum


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
