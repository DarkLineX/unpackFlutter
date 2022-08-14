from dart_runtime.app_snapshot import ReadFromTo, ReadInstructions, ReadRef
from dart_runtime.cid import *
from dart_runtime.class_table import UnboxedFieldBitmap
from dart_runtime.datastream import *
from dart_runtime.globals import kCompressedWordSizeLog2, kCompressedWordSize
from dart_runtime.kind import Kind
from dart_runtime.object import RoundedAllocationSize

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
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        self.stop_index_ = self.deserializer.next_index()


class ClassDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadInt_32(self.deserializer.stream)
        count = ReadUnsigned(self.deserializer.stream)


class AbstractInstanceDeserializationCluster(DeserializationCluster):
    pass


class InstanceDeserializationCluster(ClassDeserializationCluster):
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
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1

        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):
        # 478413 478414
        in_pos = self.deserializer.stream.tell()

        unboxed_fields_bitmap = UnboxedFieldBitmap(ReadUnsigned64(self.deserializer.stream))
        for _ in range(self.start_index_, self.stop_index_):
            next_field_offset = self.next_field_offset_in_words_ << kCompressedWordSizeLog2
            offset = 8  # ARM64 8 ARM32 4
            while offset < next_field_offset:
                if unboxed_fields_bitmap.Get(int(offset / kCompressedWordSize)):
                    ReadWordWith32BitReads(self.deserializer.stream)
                else:
                    ReadRef(self.deserializer.stream)
                offset += kCompressedWordSize

            while offset < self.instance_size:
                offset += kCompressedWordSize

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class TypedDataViewSerializationCluster:     pass


class ExternalTypedDataSerializationCluster:     pass


class TypedDataSerializationCluster:     pass


class TypedDataViewDeserializationCluster:     pass


class ExternalTypedDataDeserializationCluster:     pass


class TypedDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)


class CanonicalSetDeserializationCluster(DeserializationCluster):
    def BuildCanonicalSetFromLayout(self):
        if self.is_canonical:
            # count = 8569 stop_index_ = 9595 start_index_ = 1026 first_element_ = 0
            table_length = ReadUnsigned(self.deserializer.stream)
            first_element_ = ReadUnsigned(self.deserializer.stream)
            count = self.stop_index_ - (self.start_index_ + first_element_)
            # print(count, self.stop_index_, self.start_index_, first_element_, table_length)
            for _ in range(self.start_index_ + first_element_, self.stop_index_):
                ReadUnsigned(self.deserializer.stream)


class TypeParametersDeserializationCluster(ClassDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class TypeArgumentsDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        # 229
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        # 231
        # 8569
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        # 8974
        self.stop_index_ = self.deserializer.next_index()

        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        # TypeParameterPtr 参数类型
        # 266965
        # 272828
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            # 在 num_objects_ 里面取一个出来
            typeParameter = {}
            length = ReadUnsigned(self.deserializer.stream)
            hash_ = ReadInt_32(self.deserializer.stream)
            nullability_ = ReadUnsigned(self.deserializer.stream)
            instantiations_ = ReadUnsigned(self.deserializer.stream)
            types = []
            for _ in range(length):
                types.append(ReadUnsigned(self.deserializer.stream))

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
        # 229
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        # 231
        # 8569
        for _ in range(count):
            encoded = ReadUnsigned(self.deserializer.stream)
            self.deserializer.next_ref_index_ = self.deserializer.next_ref_index_ + 1
        # 8974
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        # ReadFill in pos =  62560
        # ReadFill out pos =  247023
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            encoded = ReadUnsigned(self.deserializer.stream)
            length, cid = self.DecodeLengthAndCid(encoded)
            if cid == kOneByteStringCid:
                for _ in range(length):
                    code_unit = ReadInt(self.deserializer.stream, 8)
            else:
                for _ in range(length):
                    code_unit = ReadInt(self.deserializer.stream, 8)
                    code_unit_2 = ReadInt(self.deserializer.stream, 8)
                    code_unit = (code_unit | code_unit_2 << 8)
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos)


class DoubleDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            encoded = ReadUnsigned(self.deserializer.stream)
        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos)


class TypeParameterDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            # 在 num_objects_ 里面取一个出来
            typeParameter = {}
            ReadFromTo(self.deserializer, 3)
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
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            # 在 num_objects_ 里面取一个出来
            typePtr = {}
            ReadFromTo(self.deserializer, 3)
            type_class_id_ = ReadUnsigned(self.deserializer.stream)
            combined = ReadInt_8(self.deserializer.stream)
            type_state_ = combined >> kNullabilityBitSize
            nullability_ = combined & kNullabilityBitMask

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class MintDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)

    def ReadFill(self):
        pass


class CodeDeserializationCluster(ClassDeserializationCluster):

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
        self.deserializer.AssignRef()

    def ReadFill(self):
        # TypeParameterPtr 参数类型
        # 272828
        # 364690
        in_pos = self.deserializer.stream.tell()

        for _ in range(self.start_index_, self.stop_index_):
            self.readFill2(_, False)

        for _ in range(self.deferred_start_index_, self.deferred_stop_index_):
            self.readFill2(_, True)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)

        # 16927 24120
        # 12.7
        # print(self.stop_index_ - self.start_index_)

    def readFill2(self, int_id, deferred):

        in_pos = self.deserializer.stream.tell()

        ReadInstructions(self.deserializer)

        if self.deserializer.kind is not Kind.FULL_AOT:
            object_pool_ = ReadRef(self.deserializer.stream)
        else:
            object_pool_ = None
        owner_ = ReadRef(self.deserializer.stream)
        exception_handlers_ = ReadRef(self.deserializer.stream)
        pc_descriptors_ = ReadRef(self.deserializer.stream)
        catch_entry_ = ReadRef(self.deserializer.stream)
        if self.deserializer.kind is Kind.FULL_JIT:
            compressed_stackmaps_ = ReadRef(self.deserializer.stream)
        elif self.deserializer.kind is Kind.FULL_AOT:
            compressed_stackmaps_ = None

        inlined_id_to_function_ = ReadRef(self.deserializer.stream)
        code_source_map_ = ReadRef(self.deserializer.stream)

        out_pos = self.deserializer.stream.tell()

        # print(in_pos, out_pos, out_pos - in_pos)


class PatchClassDeserializationCluster(ClassDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class FunctionDeserializationCluster(ClassDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()

    def ReadFill(self):
        # 364690 477989
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            func = {}
            in_read_from = self.deserializer.stream.tell()
            ReadFromTo(self.deserializer, 4)
            out_read_from = self.deserializer.stream.tell()

            if self.deserializer.kind == Kind.FULL_AOT:
                code_index = ReadUnsigned(self.deserializer.stream)
                code = None
            elif self.deserializer.kind == Kind.FULL_JIT:
                unoptimized_code_ = ReadRef(self.deserializer.stream)
                code_ = ReadRef(self.deserializer.stream)
                ic_data_array_ = ReadRef(self.deserializer.stream)
            packed_fields_ = ReadInt_32(self.deserializer.stream)
            kind_tag_ = ReadInt_32(self.deserializer.stream)

            out_for = self.deserializer.stream.tell()
            # print(in_for, out_for, out_for - in_for, in_read_from, out_read_from, out_read_from - in_read_from)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class FunctionTypeDeserializationCluster(CanonicalSetDeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        self.ReadAllocFixedSize()
        self.stop_index_ = self.deserializer.next_index()
        self.BuildCanonicalSetFromLayout()

    def ReadFill(self):
        # 478414 490686
        # FunctionTypePtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            type = {}
            in_read_from = self.deserializer.stream.tell()
            ReadFromTo(self.deserializer, 6)
            out_read_from = self.deserializer.stream.tell()

            combined = ReadInt_8(self.deserializer.stream)
            packed_parameter_counts_ = ReadInt_32(self.deserializer.stream)
            packed_type_parameter_counts_ = ReadInt_16(self.deserializer.stream)

            out_for = self.deserializer.stream.tell()
            # print(in_for, out_for, out_for - in_for, in_read_from, out_read_from, out_read_from - in_read_from)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class ClosureDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class FfiTrampolineDataDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class FieldDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class ScriptDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class LibraryDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class NamespaceDeserializationCluster:
    pass


class KernelProgramInfoDeserializationCluster:
    pass


class ObjectPoolDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)


class PcDescriptorsDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)


class CodeSourceMapDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)


class CompressedStackMapsDeserializationCluster:
    pass


class ExceptionHandlersDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            length = ReadUnsigned(self.deserializer.stream)


class ContextDeserializationCluster:
    pass


class ContextScopeDeserializationCluster:
    pass


class UnlinkedCallDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class MegamorphicCacheDeserializationCluster:
    pass


class SubtypeTestCacheDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class LoadingUnitDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class UnhandledExceptionDeserializationCluster:
    pass


class LibraryPrefixDeserializationCluster:
    pass


class TypeRefDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class ClosureDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()

    def ReadFill(self):
        # 477989 478413
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            closure = {}
            in_read_from = self.deserializer.stream.tell()
            ReadFromTo(self.deserializer, 6)

            out_for = self.deserializer.stream.tell()
            # print(in_for, out_for, out_for - in_for, in_read_from, out_read_from, out_read_from - in_read_from)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class GrowableObjectArrayDeserializationCluster(DeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()


class StackTraceDeserializationCluster:
    pass


class RegExpDeserializationCluster:
    pass


class WeakPropertyDeserializationCluster:
    pass


class LinkedHashMapDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()

    def ReadFill(self):
        # 490686 491250
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            map = {}
            in_read_from = self.deserializer.stream.tell()
            # untag_to_snapshot - untag_from

            ReadFromTo(self.deserializer, 5)
            out_read_from = self.deserializer.stream.tell()

            out_for = self.deserializer.stream.tell()
            # print(in_for, out_for, out_for - in_for, in_read_from, out_read_from, out_read_from - in_read_from)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class LinkedHashSetDeserializationCluster(AbstractInstanceDeserializationCluster):
    def ReadAlloc(self):
        self.ReadAllocFixedSize()

    def ReadFill(self):
        # 491250 491262
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            map = {}
            in_read_from = self.deserializer.stream.tell()
            # untag_to_snapshot - untag_from

            ReadFromTo(self.deserializer, 5)
            out_read_from = self.deserializer.stream.tell()

            out_for = self.deserializer.stream.tell()
            # print(in_for, out_for, out_for - in_for, in_read_from, out_read_from, out_read_from - in_read_from)

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class ArrayDeserializationCluster(ClassDeserializationCluster):
    def ReadAlloc(self):
        self.start_index_ = self.deserializer.next_index()
        count = ReadUnsigned(self.deserializer.stream)
        for _ in range(count):
            ReadUnsigned(self.deserializer.stream)
        self.stop_index_ = self.deserializer.next_index()

    def ReadFill(self):
        # 491262 514072
        # TypeParameterPtr 参数类型
        in_pos = self.deserializer.stream.tell()
        for _ in range(self.start_index_, self.stop_index_):
            in_for = self.deserializer.stream.tell()
            # 在 num_objects_ 里面取一个出来
            array = {}
            length = ReadUnsigned(self.deserializer.stream)
            type_arguments_ = ReadRef(self.deserializer.stream)
            for i in range(length):
                data = ReadRef(self.deserializer.stream)
            out_for = self.deserializer.stream.tell()

        out_pos = self.deserializer.stream.tell()
        print(self.__class__.__name__, 'ReadFill in pos = ', in_pos, 'out pos =', out_pos, self.start_index_,
              self.stop_index_)


class NoneCluster(ClassDeserializationCluster):
    def ReadAlloc(self):
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
