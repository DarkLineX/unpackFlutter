from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

from dart.Constants import AOTSymbolsNameList
from dart.Snapshot import Snapshot


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


def parse_elf_file():
    f = ELFFile(open('res/libapp.so', 'rb'))
    sections = list(f.iter_sections())  # 所有section
    aot_symbols = get_AOTSymbols(sections)
    blobs, offsets = [], []
    for AOTSymbolsName in AOTSymbolsNameList:
        # 遍历所有的
        aot_symbol = aot_symbols[AOTSymbolsName]
         # 再次遍历所有 section 比对 section的
        for section in sections:
            # 获取 sh_addr 内存映射起始地址
            # 计算出blob区块的起始位置和大小 这里很简单看代码就行 copy来自Doldrums
            sh_addr = section['sh_addr']
            if 0 <= aot_symbol.st_value - sh_addr < section.data_size:
                print(sh_addr, aot_symbol.st_value, section.data_size, aot_symbol.st_value - sh_addr)
                blob = section.data()[(aot_symbol.st_value - sh_addr):][:aot_symbol.st_size]
                assert len(blob) == aot_symbol.st_size
                blobs.append(blob)
                offsets.append(aot_symbol.st_value)


if __name__ == '__main__':
    parse_elf_file()
