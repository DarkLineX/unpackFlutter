from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

from dart_runtime.Constants import AOTSymbolsNameList
from dart_runtime.snapshot import Snapshot


def get_AOTSymbols(sections):
    tables = []
    aot_symbols = {}
    # 找到 SymbolTableSection
    for section in sections:
        if isinstance(section, SymbolTableSection):
            tables.append(section)

    # 字典加载 所有 symbols
    for table in tables:
        for sym in table.iter_symbols():
            if sym.name in AOTSymbolsNameList:
                aot_symbols[sym.name] = sym.entry
    return aot_symbols


def parse_elf_file(file_path):
    f = ELFFile(open(file_path, 'rb'))
    sections = list(f.iter_sections())  # 所有section
    aot_symbols = get_AOTSymbols(sections)
    Snapshots = {}
    for AOTSymbolsName in AOTSymbolsNameList:
        # 遍历所有的
        aot_symbol = aot_symbols[AOTSymbolsName]
        # 再次遍历所有 section 比对 section的
        for section in sections:
            # 获取 sh_addr 内存映射起始地址
            # 计算出blob区块的起始位置和大小 这里很简单看代码就行 copy来自Doldrums
            sh_addr = section['sh_addr']
            if 0 <= aot_symbol.st_value - sh_addr < section.data_size:
                snapshot = {}
                blob = section.data()[(aot_symbol.st_value - sh_addr):][:aot_symbol.st_size]
                assert len(blob) == aot_symbol.st_size
                # print(AOTSymbolsName,hex( aot_symbol.st_value), len(blob), hex(aot_symbol.st_value + len(blob)))
                snapshot['blob'] = blob
                snapshot['offsets'] = aot_symbol.st_value
                Snapshots[AOTSymbolsName] = snapshot

    # vm_snapshot_data = Snapshots['_kDartVmSnapshotData']
    # vm roots 加载的是基本类 没必要解析 核心的还是看 isolate
    # vm_snapshot_ = Snapshot(vm_snapshot_data['blob']).SnapshotSetupFromBuffer()

    isolate_snapshot_data = Snapshots['_kDartIsolateSnapshotData']
    isolate_snapshot_ = Snapshot(isolate_snapshot_data['blob']).SnapshotSetupFromBuffer()


if __name__ == '__main__':
    parse_elf_file('res/libapp.so')
