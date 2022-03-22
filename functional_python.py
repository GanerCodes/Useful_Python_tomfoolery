lazy_load = lambda i, s: exec(f"""def {s}(*args, **kwargs):
    from {i} import {s}
    return {s}(*args, **kwargs)""", globals())

lazy_load("numpy", "arange")
lazy_load("functools", "reduce")

def __Γ__(x, alt = None):
    try:
        return x()
    except Exception:
        return alt

def __Σ__(f, a = 0, b = 1, samples = 1000):
    return (s := 1 / samples) and sum(map(λ.x("s*f(x)", f=f, s=s), iarange(a, b, s * abs(b - a))
))

class __λ__:
    def __init__(self, _ = (), code = None, kwargs = None):
        self._ = δ(_)
        self.__code__ = Δ(code)
        self.kwargs = Δ(kwargs, {})
    def __getattr__(self, name):
        if name in ('xonsh_display', '__signature__', '__wrapped__'):
            raise AttributeError()
        return __λ__(self._ + (name, ))
    def __call__(self, *args, **kwargs):
        if self.__code__:
            return eval(self.__code__, globals() | kwargs | self.kwargs | {
                self._[i]: v for i, v in enumerate(args)
            }, locals())
        else:
             return __λ__(self._, args[0], kwargs)

class __Φ__:
    FUNCS = "abs add repr aenter aexit aiter and anext await bool bytes ceil class_getitem cmp coerce complex contains delitem delslice dir div divmod enter eq exit float floor floordiv format fspath ge get getitem getnewargs getslice gt hash hex iadd iand idiv ifloordiv ilshift imatmul imod import imul index init_subclass instancecheck int invert ior ipow irshift isub iter itruediv ixor le len length_hint long lshift lt matmul metaclass missing mod mul ne neg next nonzero oct or pos pow prepare radd rand rcmp rdiv rdivmod reduce reduce_ex reversed rfloordiv rlshift rmatmul rmod rmul ror round rpow rrshift rshift rsub rtruediv rxor set set_name setitem setslice sizeof slots str sub subclasscheck subclasses truediv trunc unicode weakref xor".split()
    RESERVED = "repr str bool".split() # More needs to be added to this 100%
    
    def once_init():
        for i in __Φ__.FUNCS:
            func_name = f'__{i}__'
            alias = f'_{i}_' if i in __Φ__.RESERVED else func_name
            setattr(__Φ__, alias,
                lambda *x, f = func_name: (
                    __Φ__(x[0].operations.copy() + [(f, x[1:])])
                )
            )
    
    def __init__(self, operations = None):
        self.operations = operations or []
    
    def __call__(self, x):
        for func, val in self.operations:
            x = x.__getattribute__(func)(*val)
        return x
    
    def __getattribute__(self, name):
        return super(__Φ__, self).__getattribute__(name)

# Initalizing overwrites for magic function 
__Φ__.once_init()

class __Ψ__:
    def __init__(self, func = None):
        self.__function__ = func
    def __proc_func__(self, func):
        return β(func) if type(func) == str else func
    def __call__(self, func = None):
        return self.__class__(func = self.__proc_func__(func))

class __ρ__(__Ψ__):
    def __init__(self, key = None, func = None):
        self.__key__ = key
        self.__function__ = func
    def __getitem__(self, key):
        return self.__class__(key = key, func = self.__function__)
    def __call__(self, func = None):
        return self.__class__(key = self.__key__, func = self.__proc_func__(func))
    def __add__(self, key):
        return self.__getitem__(key)
    def __sub__(self, key):
        return self.__getitem__(-key)
    def __getattr__(self, name):
        return self.__getitem__(name)

class __φ__(__ρ__):
    pass

class __χ__:
    class o:
        def __init__(self, *args):
            self.args = args
    
    def run_callable(Ψ, final):
        return Ψ.__function__(final) if Ψ.__function__ is not None else final
    
    def Ψ_run(Ψ, final, args, kwargs):
        match type(Ψ).__name__:
            case "__Ψ__":
                return Ψ.__function__(final) if Ψ.__function__ else final
            case ("__ρ__" | "__φ__") as t:
                ctx = args if t == "__ρ__" else kwargs
                return __χ__.run_callable(Ψ, ctx[Ψ.__key__]) if Ψ.__key__ is not None else ctx
            case _:
                return Ψ
    
    def __init__(self, *args, _ = None, **kwargs):
        if not hasattr(self, '_'):
            self._ = Δ(_, [])
        
    def __getattribute__(self, name):
        if name == 'xonsh_display':
            raise AttributeError()
        if name[0] in '_o':
            return super(__χ__, self).__getattribute__(name)
        elif name[0] == 'ƒ':
            return __χ__(_ = self._.copy() + [self.o()])
        else:
            return __χ__(_ = self._.copy() + [self.o(eval(name))])
     
    def __call__(self, *args, **kwargs):
        if len(self._):
            if len(self._[-1].args) == 0:
                return __χ__(_ = self._[:-1].copy() + [
                    self.o(ζ(args[0]) if type(args[0]) == str else args[0])
                ])
                
            if len(self._[-1].args) == 2:
                stack = [next(itter := enumerate(self._))[1]]
                for i, v in itter:
                    if len(v.args) == 1 == len(self._[i - 1].args):
                        stack.append(self.o((), {}))
                    stack.append(v)
                
                final = args[0] if args else None
                while len(stack):
                    func, (ia, ika) = stack.pop(0).args[0], stack.pop(0).args
                    
                    dat = (
                        [   __χ__.Ψ_run(i, final, args, kwargs) for i in ia],
                        {k: __χ__.Ψ_run(i, final, args, kwargs) for k, i in ika.items()}
                    ) if ia or ika else ([final], {})
                    
                    final = eval("func(*dat[0], **dat[1])", globals(), locals())
                
                return final
        else:
            return __χ__(_ = [self.o(lambda x: x), self.o(args, kwargs)])
        return __χ__(_ = self._.copy() + [self.o(args, kwargs)])

lmap  = lambda *args, **kwargs: list(map(*args, **kwargs))
jmap  = lambda *args, **kwargs: ''.join(map(str, map(*args, **kwargs)))
pjmap = lambda *args, **kwargs: print(jmap(*args, **kwargs))
# These are just just for convenient

iarange = lambda a = 0, b = 10, step = 1: arange(a, b + step, step)
# Same as arange but includes final step

Σ = __Σ__
# Usage: Σ(func, a = start, b = stop, samples = amount)
# Integral approximator
# χ.Σ(Φ * 2, -5, 5)() # ~zero

Δ = lambda a, b = None: a if a else b
# Δ(0) # None
# Δ(0, "hi") # "hi"
# Δ(1, "hi") # 1

Γ = __Γ__
# Γ(error producing function) # None
# Γ(error producing function, "hi") # "hi"
# Γ(lambda: 5) # 5

δ = lambda x: Δ(x, __Γ__(type(x)))
# (mostly applicable for arbitrary types that may have false boolean states that you want the "default" state of)
# (Returns None if default constructor results in error)
# δ(1) # 1
# δ([]) # []

Φ = __Φ__()
# Magic variable, inspired by magic ƒ
# Basically, most opperations performed on it returns a new instance with that operation in the chain
# When called, it chains past operations onto a variable
# Because TypeErrors, some operations need to be called using the magic method with 1 _ removed from each end
# Φ + 5 # lambda x: x + 5
# (Φ ** 5) + 2 # lambda x: (x ** 5) + 2
# Φ.str() # lambda x: x.__str__() # str

λ = __λ__()
# Magic lambda, allows shorter lambda creation
# Keyword arguments are treated as variables when evaluated
# Missing arguments default to None
# λ.x("x + 2") # lambda x: x + 2
# λ.a.b("a ** b + 5") # lambda a, b: a ** b + 5
# λ.a("a + f", f = 5) # lambda a: eval("a + f", {'f': 5})

β = λ.x
# Shortcut for λ.x
 
ζ = λ.x.y.z.w
# Shortcut for λ with up to 4 arguments, x y z & w

χ = __χ__()
# Used to create composite methods in a more linear fashion
# If arguments are not provided after a function it provides blank ones
# Note: using ƒ allows you to pass in a function rather than naming it
# Note: if ƒ receives a string it is automatically passed into ζ
# χ.range(5) # lambda: range(5)
# χ.range(5).list.print() # lambda: print(list(range(5)))
# χ.range(5).ƒ(sum).print() # lambda: print(list(range(5)))

Ψ = __Ψ__()
# Serves as a replacement argument for χ, and can hold a transformation of the previous output
# χ.range(5).map(str, Ψ) # lambda: map(str, range(5))
# χ.range(5).map(str, Ψ('x[::2]')).ƒ(''.join).print() # lambda: print(''.join(map(str, range(5)[::2])))
# χ.range(5).map(str, Ψ(β('x[::-1]'))).ƒ(''.join).print()() # prints "43210"

ρ = __ρ__()
φ = __φ__()
# Similar to Ψ but to access final call arguments for χ, can hold a transformation of the previous output
# ρ for args and φ for kwargs
# The add, sub, and attribute methods on ρ and φ are overloaded for simpler argument access
# χ.range(φ['k'])(k = 3) = range(3)
# χ.range(ρ[0]('x - 3'))(5) = range(2)
# χ.print(φ.k)(k = "hello") # prints "hello"
# χ.print(ρ+0)("hello") # prints "hello"
__all__ = list("λζχΣΔΓδΦβΨρφ") + ["iarange"]

if __name__ == '__main__':
    # Random examples I've thrown together, try and guess what they will do before running to practice
    print('e' * χ.range(φ['k']('x * 10')).len()(k = 3))
    print((Φ * 10)(2))
    print(ζ("x**y + v")(2, 5, v = 5))
    print(λ.a.b.c("str(a) + str(b) + str(c) + x * 15")(2, 3, 4, x = "xd"))
    pjmap(χ(ρ[0]).ƒ(Φ ** 3 + 7).str(), range(5))
    pjmap(Φ * 10, range(5))
    pjmap(Φ ** 3 + 7, range(20))
    pjmap(λ.x("x * 10"), range(5))
    pjmap((Φ ** 2)._str_()[::-1], range(9))
    χ.range(10).reversed.map(Φ ** 2, Ψ).list.reduce(ζ("x - y"), Ψ).print()()
    χ(5).ƒ('(x+y+z(hello)) // 2')(Ψ, ρ+0, φ.e, hello = φ.hi(Φ - 2)).range(Ψ('x+2')).\
        map((Φ ** 3 + 7)._str_(), Ψ('x[::-1]')).ƒ(''.join).print()(3, e = Φ + 2, hi = 5)
