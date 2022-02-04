from functools import reduce

def Γ(x):
    try:
        return x()
    except Exception:
        return None
Δ = lambda a, b = None: a if a else b
δ = lambda x: Δ(x, Γ(type(x))) # x or default value of type of x (if it exists)

class __λ__:
    "Smaller lambda creation"
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
    "Magic functions, consumes many operations into it's chain"
    
    FUNCS = "abs add repr aenter aexit aiter and anext await bool bytes ceil class_getitem cmp coerce complex contains delitem delslice dir div divmod enter eq exit float floor floordiv format fspath ge get getitem getnewargs getslice gt hash hex iadd iand idiv ifloordiv ilshift imatmul imod import imul index init_subclass instancecheck int invert ior ipow irshift isub iter itruediv ixor le len length_hint long lshift lt matmul metaclass missing mod mul ne neg next nonzero oct or pos pow prepare radd rand rcmp rdiv rdivmod reduce reduce_ex reversed rfloordiv rlshift rmatmul rmod rmul ror round rpow rrshift rshift rsub rtruediv rxor set set_name setitem setslice sizeof slots str sub subclasscheck subclasses truediv trunc unicode weakref xor".split()
    RESERVED = "repr str bool".split() # More needs to be added to this 100%
    
    def __init__(self, operations = None):
        self.operations = operations or []
    
    def __call__(self, x):
        for func, val in self.operations:
            x = x.__getattribute__(func)(*val)
        return x
    
    def __getattribute__(self, name):
        return super(__Φ__, self).__getattribute__(name)

# Initalizing overwrites for magic function 
for i in __Φ__.FUNCS:
    func_name = f'__{i}__'
    alias = f'_{i}_' if i in __Φ__.RESERVED else func_name
    setattr(__Φ__, alias,
        lambda *x, f = func_name: (
            __Φ__(x[0].operations.copy() + [(f, x[1:])])
        )
    )

class __Ψ__:
    "Replacement character for χ"
    pass

class __χ__:
    "Method chaining"
    class o:
        def __init__(self, *args):
            self.args = args
            
    def __init__(self, *args, _ = None, **kwargs):
        if not hasattr(self, '_'):
            self._ = Δ(_, [])
        
    def __getattribute__(self, name):
        if name[0] in '_o':
            return super(__χ__, self).__getattribute__(name)
        else:
            return __χ__(_ = self._.copy() + [self.o(eval(name))])
        
    def __call__(self, *args, **kwargs):
        if len(self._) and len(self._[-1].args) == 2:
            stack = [self._[0]]
            for i in range(len(self._))[1:]:
                v = self._[i]
                if len(v.args) == 1 == len(self._[i - 1].args):
                    stack.append(self.o((), {}))
                stack.append(v)
            
            val = None
            while len(stack):
                func, (ia, ika) = stack.pop(0).args[0], stack.pop(0).args
                
                val = func(
                    *[(i, val)[type(i) == __Ψ__] for i in ia],
                    **{k: ((v, val)[type(v) == __Ψ__]) for k, v in ika.items()}
                ) if (ia or ika) else func(val)
            return val
                    
        return __χ__(_ = self._.copy() + [self.o(args, kwargs)])

# Create base instances
Φ = __Φ__()
λ = __λ__()
χ = __χ__()
Ψ = __Ψ__()

print((Φ * 10)(2))
print()
χ.range(10).reversed.map(Φ ** 2, Ψ).list.reduce(λ.x.y("x - y"), Ψ).print()() # prints -123
print()
print(λ.x.y("x**y")(2, 5))
print(λ.a.b.c("str(a) + str(b) + str(c) * 15")(2, 3, 4))
print()
print(list(map(λ.x("x * 10"), range(5))))
print(list(map(Φ * 10, range(5))))
print()
print(list(map( Φ ** 3 + 7 , range(20))))
print(list(map( (Φ ** 2)._str_()[::-1] , range(9))))