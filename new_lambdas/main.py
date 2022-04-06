#!/usr/bin/python 

import ast
from ast import *
from collections import OrderedDict

v = {
    'Constant': ((None, ), {
        'ctx': Load()
    }),
    'Attribute': ((), {
        'ctx': Load()
    }),
    'Name': ((), {
        'ctx': Load()
    }),
    'arguments': ((), {
        'posonlyargs': [],
        'kwonlyargs': [],
        'kw_defaults': [],
        'args': [],
        'defaults': []
    }),
    'Call': ((), {
        'args': [],
        'keywords': []
    })
}
for k, v in v.items():
    globals()[k] = lambda *a, v=v, f=getattr(ast, k), **args: f(
        *(dict(enumerate(v[0])) | dict(enumerate(a))).values(),
        **(v[1] | args)
    )

class λ_template:
    stack = []
    modes = {
        'λ' : 'n',
        'λt': 't',
        'tλ': 't',
        'λf': 'f',
        'fλ': 'f',
        'λs': 's',
        'sλ': 's'
    }
    
    class __ω:
        def __init__(self, ω):
            self.ω = ω
        def __call__(self, *args, **kwargs):
            return self.ω(*args, **kwargs)
        def __getitem__(self, n):
            return λ_template.stack[-1-n]
    
    def __new__(cls, *args, convert_to_chain=True, **kwargs):
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        if convert_to_chain:
            return λ_chain(obj)
        else:
            return obj
            
    def __init__(self, λ, *i_args, mode='n', barg=None, **i_kwargs):
        self.λ = λ
        self.mode = mode
        self.barg = barg
        self.i_args = i_args
        self.i_kwargs = {i: None for i in 'xyzw'} | i_kwargs
        
    def __call__(self, *args, **kwargs):
        t = OrderedDict(self.i_kwargs | kwargs)
        for v, a in zip([i for i in t if i not in kwargs], args):
            t[v] = a
        
        t['ω'] = λ_template.__ω(self)
        t['δ'] = t
        t['stack'] = globals()['λ_template'].stack
        
        return self.λ(**t)
    
    def __str__(self):
        return f"λ[{self.barg}]<{self.mode}, {id(self)}>"

def set_or_add(l, i, v):
    if i < len(l):
        l[i] = v
    else:
        l.append(v)

class λ_chain:
    def __init__(self, *λs: 'λ_template|λ_chain'):
        self.λs = λs
    
    def __or__(self, l: 'λ_chain|λ_template'):
        if isinstance(l, λ_chain):
            return λ_chain(*self.λs, *l.λs)
        else:
            return λ_chain(*self.λs, l)
    
    def __mul__(self, l: 'λ_chain|λ_template|int'):
        if isinstance(l, λ_chain):
            return λ_chain(l, self)
        elif isinstance(l, λ_template):
            return λ_chain(λ_template, λ_chain(*self.λs))
        else:
            return λ_chain(*[λ_chain(self.λs)] * l)
    
    def __iter__(self):
        return iter(self.λs)
    
    def __len__(self):
        return len(self.λs)
    
    def __call__(self, *args: any, **kwargs: any):
        args, inital_arg_length = list(args), len(args)
        λ_template.stack.append(self)
        try:
            for λ in self:
                if isinstance(λ, λ_chain):
                    args = λ(*args, **kwargs)
                elif isinstance(λ, λ_template):
                    mode, barg, i_args, i_kwargs = λ.mode, λ.barg, λ.i_args, λ.i_kwargs
                    match mode:
                        case 'n':
                            set_or_add(args, 0, λ(*args, **kwargs))
                        case 't':
                            set_or_add(args, 0, [λ(*i, **kwargs) for i in zip(*args)])
                        case 'f':
                            set_or_add(args, 0, list(zip(*[i for i in zip(*args) if λ(*i, **kwargs)]))[barg or 0])
                        case 's':
                            z = zip(*args)
                            q = list(zip(*sorted(z, key=lambda x: λ(*x, **kwargs))))
                            set_or_add(args, 0, q[barg or 0])
            
            return args[0]
        finally:
            λ_template.stack.pop()
    
    def __str__(self):
        return f"λ Chain of length {len(self)} ({' > '.join(map(lambda x: 'C' if isinstance(x, λ_chain) else x.mode, self))}):\n\t" + ('\n\t'.join('\n'.join(map(str, self)).split('\n')))

class Macro_transformer(NodeTransformer):
    def __init__(self):
        pass
    
    def visit_Call(self, node):
        super().generic_visit(node)
        
        if isinstance(node, ast.Call) and hasattr(node, 'func'):
            func = node.func
            
            if type(func) == ast.Subscript:
                if func.value.id not in λ_template.modes:
                    return node
                mode = λ_template.modes[func.value.id]
                barg = func.slice
                node.func = Name(id="λ_template")
            elif type(func) == ast.Name:
                if func.id not in λ_template.modes:
                    return node
                mode = λ_template.modes[func.id]
                barg = Constant(None)
                func.id = "λ_template"
            else:
                return node
            
            keyargs = OrderedDict({i: Constant(None) for i in "xyzw"} | {i.arg: i.value for i in node.keywords})
            node.args[0] = Lambda(
                body = node.args[0],
                args = arguments(
                    args        = [arg(arg=a) for a in keyargs.keys()],
                    vararg      = arg(arg="args"),
                    kwarg       = arg(arg="kwargs"),
                    defaults    = [Constant(None)] * len(keyargs),
                    kwonlyargs  = (k := [arg(arg='ω'), arg(arg='δ'), arg(arg='stack')]),
                    kw_defaults = [Constant(None)] * len(k)
                )
            )
            
            node.keywords += [
                keyword(arg="mode", value=Constant(mode)),
                keyword(arg="barg", value=barg) 
            ]
            
            return node

q = Expression(parse('''λt(x + y)''', mode='eval').body)
Macro_transformer().visit(q)
q = eval(compile(fix_missing_locations(q), '<bruh>', 'eval'))

print(q(range(5), range(5)))