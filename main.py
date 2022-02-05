# https://github.com/GanerCodes/Useful_Python_tomfoolery/blob/master/main.py

lazy_load = lambda i, s: exec(f"""def {s}(*args, **kwargs):
    from {i} import {s}
    return {s}(*args, **kwargs)""", globals())

lazy_load("numpy", "arange")
lazy_load("functools", "reduce")

def __Γ__(x):
    try:
        return x()
    except Exception:
        return None

def __Σ__(f, a = 0, b = 1, samples = 1000):
    return (s := 1 / samples) and sum(map(λ.x("s*f(x)", f=f, s=s), 𝛢(a, b, s * abs(b - a))
))

class __λ__:
    "Smaller lambda creation"
    def __init__(self, _ = (), code = None, kwargs = None):
        self._ = δ(_)
        self.code = Δ(code)
        self.kwargs = Δ(kwargs, {})
    def __getattr__(self, name):
        return __λ__(self._ + (name, ))
    def __call__(self, *args, **kwargs):
        if self.code:
            return eval(self.code, globals() | kwargs | self.kwargs | {
                self._[i]: v for i, v in enumerate(args)
            }, locals())
        else:
            return __λ__(self._, args[0], kwargs)

class __Φ__:
    "Magic functions, can consume many operations into it's chain"
    
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
    def __init__(self, func = None):
        self.func = func
    def __call__(self, func = None):
        return __Ψ__(func)

class __χ__:
    "Method chaining"
    class o:
        def __init__(self, *args):
            self.args = args
    
    def Ψ_run(Ψ, val):
        return Ψ.func(val) if Ψ.func else val
    
    def __init__(self, *args, _ = None, **kwargs):
        if not hasattr(self, '_'):
            self._ = Δ(_, [])
        
    def __getattribute__(self, name):
        if name[0] in '_o':
            return super(__χ__, self).__getattribute__(name)
        elif name[0] == 'ƒ':
            return __χ__(_ = self._.copy() + [self.o()])
        else:
            return __χ__(_ = self._.copy() + [self.o(eval(name))])
     
    def __call__(self, *args, **kwargs):
        if len(self._):
            if len(self._[-1].args) == 0:
                return __χ__(_ = self._[:-1].copy() + [self.o(args[0])])
                
            if len(self._[-1].args) == 2:
                stack = [self._[0]]
                for i in range(len(self._))[1:]:
                    v = self._[i]
                    if len(v.args) == 1 == len(self._[i - 1].args):
                        stack.append(self.o((), {}))
                    stack.append(v)
                
                final = None
                while len(stack):
                    func, (ia, ika) = stack.pop(0).args[0], stack.pop(0).args
                    
                    final = func(
                        *[(__χ__.Ψ_run(i, final) if type(i) == __Ψ__ else i) for i in ia],
                        **{k: (__χ__.Ψ_run(i, final) if type(v) == __Ψ__ else v) for k, v in ika.items()}
                    ) if (ia or ika) else func(final)
                
                return final
        else:
            return __χ__(_ = [self.o(lambda x: x), self.o(args, kwargs)])
                    
        return __χ__(_ = self._.copy() + [self.o(args, kwargs)])

Δ = lambda a, b = None: a if a else b
δ = lambda x: Δ(x, __Γ__(type(x))) # x or default value of type of x (if it exists)
𝛢 = lambda a = 0, b = 10, step = 1: arange(a, b + step, step)
Γ = __Γ__
Φ = __Φ__()
λ = __λ__()
χ = __χ__()
Ψ = __Ψ__()
β = λ.x
ζ = λ.x.y
Σ = __Σ__

print(list(( map(λ.x('χ(x).ƒ(Φ ** 3 + 7).str()()'), range(5)) )))

χ.range(5).map((Φ ** 3 + 7)._str_(), Ψ(β('x[::-1]'))).ƒ(''.join).print()()

print(χ.Σ(Φ * 2, -5, 5)())

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