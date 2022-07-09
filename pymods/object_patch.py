from ctypes import c_char

# Made by W man chilaxan

BYTES_HEADER = bytes.__basicsize__ - 1
Py_TPFLAGS_IMMUTABLETYPE = 1 << 8

def sizeof(obj):
    return type(obj).__sizeof__(obj)

def getmem(obj_or_addr, size=None, fmt='P'):
    if size is None:
        size = sizeof(obj_or_addr)
        addr = id(obj_or_addr)
    else:
        addr = obj_or_addr
    return memoryview((c_char*size).from_address(addr)).cast('c').cast(fmt)

def alloc(size, _storage=[]):
    _storage.append(bytes(size))
    return id(_storage[-1]) + BYTES_HEADER

def get_structs(htc=type('',(),{'__slots__':()})):
    htc_mem = getmem(htc)
    last = None
    for ptr, idx in sorted([(ptr, idx) for idx, ptr in enumerate(htc_mem)
            if id(htc) < ptr < id(htc) + sizeof(htc)]):
        if last:
            offset, lp = last
            yield offset, ptr - lp
        last = idx, ptr

def allocate_structs(cls):
    cls_mem = getmem(cls)
    for subcls in type(cls).__subclasses__(cls):
        allocate_structs(subcls)
    for offset, size in get_structs():
        cls_mem[offset] = cls_mem[offset] or alloc(size)
    return cls_mem

def unlock(cls):
    cls_mem = allocate_structs(cls)
    flags = cls.__flags__
    flag_offset = [*cls_mem].index(flags)
    cls_mem[flag_offset] &= ~Py_TPFLAGS_IMMUTABLETYPE

def lock(cls):
    cls_mem = getmem(cls)
    flags = cls.__flags__
    flag_offset = [*cls_mem].index(flags)
    cls_mem[flag_offset] |= Py_TPFLAGS_IMMUTABLETYPE

def patch_object():
    # adds extra *fake* object class to inheritance chain so that object can be modified
    int_mem = getmem(int)
    tp_base_offset = [*int_mem].index(id(int.__base__))
    tp_basicsize_offset = [*int_mem].index(int.__basicsize__)
    fake_addr = alloc(sizeof(object))
    fake_mem = getmem(fake_addr, sizeof(object))
    fake_mem[0] = 1
    fake_mem[1] = id(type)
    fake_mem[3] = alloc(0)
    fake_mem[tp_basicsize_offset] = object.__basicsize__
    getmem(object)[tp_base_offset] = fake_addr

patch_object()

class objmod:
    def __init__(self, *types):
        self.types = set(types)
    def __enter__(self):
        for t in self.types:
            unlock(t)
        return set(self.types)
    def __exit__(self, type=None, value=None, traceback=None):
        for t in self.types:
            lock(t)
    def __iter__(self):
        self.__enter__()
        yield from self.types
        self.__exit__()