def Γ(x):
    try:
        return x()
    except Exception:
        return None
Δ = lambda a, b = None: a if a else b
δ = lambda x: Δ(x, Γ(type(x))) # x or default value of type of x (if it exists)

class __λ__(object):
    def __init__(self, _ = ()):
        self._ = δ(_)
        self.code = None
    def __getattr__(self, name):
        return __λ__(self._ + (name, ))
    def __call__(self, *args):
        if self.code:
            return eval(self.code, globals(), locals() | {
                self._[i]: v for i, v in enumerate(args)
            })
        else:
            self.code = args[0]
        return self

class __Φ__:
    FUNCS = "abs add repr aenter aexit aiter and anext await bool bytes ceil class_getitem cmp coerce complex contains delitem delslice dir div divmod enter eq exit float floor floordiv format fspath ge get getitem getnewargs getslice gt hash hex iadd iand idiv ifloordiv ilshift imatmul imod import imul index init_subclass instancecheck int invert ior ipow irshift isub iter itruediv ixor le len length_hint long lshift lt matmul metaclass missing mod mul ne neg next nonzero oct or pos pow prepare radd rand rcmp rdiv rdivmod reduce reduce_ex reversed rfloordiv rlshift rmatmul rmod rmul ror round rpow rrshift rshift rsub rtruediv rxor set set_name setitem setslice sizeof slots str sub subclasscheck subclasses truediv trunc unicode weakref xor".split()
    RESERVED = "repr str bool".split() # More needs to be added to this 100%
    
    def __init__(self, operations = None):
        self.operations = operations or []
        for i in self.FUNCS:
            func_name = f'__{i}__'
            alias = f'_{i}_' if i in self.RESERVED else func_name
            setattr(__Φ__, alias, lambda *x, __i__ = func_name: self.operate(__i__, x))
    
    def operate(self, name, values):
        t = (name, values[1:])
        if len(self.operations):
            self.operations.append(t)
            return self
        else:
            return __Φ__([t])
    
    def __call__(self, x):
        for func, val in self.operations:
            x = getattr(x, func)(*val)
        return x
    
    def __getattribute__(self, name):
        return super(__Φ__, self).__getattribute__(name)

Φ = __Φ__()
λ = __λ__()



print(λ.x.y("x**y")(2,5))
print(λ.a.b.c("str(a) + str(b) + str(c) * 15")(2, 3, 4))
print()
print(list(map(λ.x("x * 10"), range(5))))
print(list(map(Φ * 10, range(5))))
print()
print(list(map( Φ ** 3 + 7 , range(20))))
print(list(map( (Φ ** 2)._str_()[::-1] , range(20))))