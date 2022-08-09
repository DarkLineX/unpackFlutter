from dart_runtime.cid import kNumPredefinedCids, kInstanceCid, IsTypedDataViewClassId, IsExternalTypedDataClassId, \
    IsTypedDataClassId
from dart_runtime.clusters import Clusters, InstanceDeserializationCluster, TypedDataViewDeserializationCluster, \
    ClassDeserializationCluster, TypedDataDeserializationCluster, ClusterGetter
from dart_runtime.datastream import readUnsigned, readInt, kMaxUint32, readInt_64


class Deserializer:
    def __init__(self, stream):
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
        self.next_ref_index_ = 1

    def deserialize(self):
        self.num_base_objects_ = readUnsigned(self.stream)
        self.num_objects_ = readUnsigned(self.stream)
        self.num_clusters_ = readUnsigned(self.stream)
        self.initial_field_table_len = readUnsigned(self.stream)
        self.instructions_table_len = readUnsigned(self.stream)
        self.instruction_table_data_offset = readUnsigned(self.stream)

        # trace 1025 51549 308 572 7193 16
        print(self.num_base_objects_, self.num_objects_, self.num_clusters_,
              self.initial_field_table_len,
              self.instructions_table_len, self.instruction_table_data_offset)

        self.addBaseObject()

        cluster = self.readCluster()
        self.cluster_list.append(cluster)
        cluster.readAlloc(False)

        # 17549
        cluster = self.readCluster()
        self.cluster_list.append(cluster)
        cluster.readAlloc(False)

    def addBaseObject(self):
        for _ in range(self.num_base_objects_):
            self.next_ref_index_ = self.next_ref_index_ + 1

    def next_index(self):
        return self.next_ref_index_

    def readCluster(self):
        print(self.stream.tell())
        cid_and_canonical = readInt_64(self.stream)
        cid = (cid_and_canonical >> 1) & kMaxUint32
        print(self.stream.tell(), cid)
        is_canonical = (cid_and_canonical & 0x1) == 0x1
        # print("cid_and_canonical", cid_and_canonical, 'cid', cid, 'is_canonical', is_canonical)
        # 判断cid
        if cid >= kNumPredefinedCids and cid == kInstanceCid:
            return InstanceDeserializationCluster(cid, is_canonical)
        if IsTypedDataViewClassId(cid):
            return TypedDataViewDeserializationCluster(cid)
        if IsExternalTypedDataClassId(cid):
            return ClassDeserializationCluster(cid)
        if IsTypedDataClassId(cid):
            return TypedDataDeserializationCluster(cid)
        ###
        cluster = ClusterGetter(cid, self).getCluster()
        print(cluster, cid)
        return cluster