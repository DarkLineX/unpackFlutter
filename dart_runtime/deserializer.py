from dart_runtime.datastream import readUnsigned, readCid, read, readInt


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

        for _ in range(self.num_clusters_):
            print("cid", readCid(self.stream))

    def readClusterAlloc(self, isCanonical):
        cid = readCid(self.stream)
        print(cid)
