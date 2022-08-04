

class Deserializer:
    def __init__(self, stream):
        self.clusters = None
        self.num_base_objects_ = None
        self.num_objects_ = None
        self.num_clusters_ = None
        self.initial_field_table_len = None
        self.instructions_table_len = None
        self.instruction_table_data_offset = None
        self.stream = stream

    def deserialize(self):
        self.num_base_objects_ = ReadStream().readUnsigned(self.stream)
        self.num_objects_ = ReadStream().readUnsigned(self.stream)
        self.num_clusters_ = ReadStream().readUnsigned(self.stream)
        self.initial_field_table_len = ReadStream().readUnsigned(self.stream)
        self.instructions_table_len = ReadStream().readUnsigned(self.stream)
        self.instruction_table_data_offset = ReadStream().readUnsigned(self.stream)
        print(self.num_base_objects_, self.num_objects_, self.num_clusters_, self.initial_field_table_len,
              self.instructions_table_len, self.instruction_table_data_offset)

        # Alloc stage        

        self.clusters = [self.readClusterAlloc(False) for _ in range(self.num_clusters_)]

    def readClusterAlloc(self, isCanonical):
        cid = ReadStream().readCid(self.stream)
        print(cid)
