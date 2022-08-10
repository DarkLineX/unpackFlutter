from dart_runtime.cid import kNumPredefinedCids, kInstanceCid, IsTypedDataViewClassId, IsExternalTypedDataClassId, \
    IsTypedDataClassId
from dart_runtime.clusters import *
from dart_runtime.datastream import readUnsigned, readInt, kMaxUint32, readInt_64

kFirstReference = 1


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
        self.next_ref_index_ = kFirstReference

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

        for _ in range(self.num_clusters_):
            cluster = self.readCluster
            self.cluster_list.append(cluster)
            cluster.readAlloc()
            if type(cluster) == NoneCluster:
                break

    def addBaseObject(self):
        for _ in range(self.num_base_objects_):
            self.next_ref_index_ = self.next_ref_index_ + 1

    def next_index(self):
        return self.next_ref_index_

    @property
    def readCluster(self):
        read_cid_before = self.stream.tell()
        cid_and_canonical = readInt_64(self.stream)
        cid = (cid_and_canonical >> 1) & kMaxUint32
        is_canonical = (cid_and_canonical & 0x1) == 0x1

        read_cid_after = self.stream.tell()
        print('read_cid_before =',read_cid_before,'read_cid_after =',read_cid_after,'cid =',cid,'is_canonical',is_canonical)
        # print("cid_and_canonical", cid_and_canonical, 'cid', cid, 'is_canonical', is_canonical)
        ###
        cluster = ClusterGetter(cid, is_canonical,self).getCluster()
        print(cluster, cid)
        return cluster
