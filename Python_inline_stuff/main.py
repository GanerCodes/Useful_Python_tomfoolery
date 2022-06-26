#!/usr/bin/python 

import re

def set_then_return(a, b, c):
    a[b] = c
    return c

def make_chain_func(*func_list):
    def func(*args, func_list=func_list):
        args = list(args)
        for i in func_list:
            out = i(*args)
            args = [out] + args
        return args[0]
    return func

def get_match_balances(s, o, c):
    if isinstance(o, str): o = re.compile(o)
    if isinstance(c, str): c = re.compile(c)
    
    l = sorted(
        [('o', i) for i in o.finditer(s)] + [('c', i) for i in c.finditer(s)],
        key=lambda x: x[1].span()[0])
    
    pairs = []
    start, depth = None, 0
    for t, v in l:
        if depth == 0:
            if t == 'o':
                start = v
                depth += 1
            continue
        else:
            if t == 'o':
                depth += 1
            elif t == 'c':
                depth -= 1
                if depth == 0:
                    pairs.append((start, v))
    
    return pairs

def pair_quick_lambda(s, l, r):
    s = parse(s)
    return f'''make_chain_func({','.join(f"(lambda *args: ({i.strip()}))" for i in s.split('🠒'))})'''

def pair_inline_var(s, l, r):
    return f"(set_then_return(globals(), '{l.groups()[0]}', {s}))"

def simple_arg_chain(s):
    t = int(''.join(str('₀₁₂₃₄₅₆₇₈₉'.index(i)) for i in s.groups()[0] or '₀'))
    return f"args[{t}]"

def parse(s):
    for t, v in matchset.items():
        fin = list(s)
        if isinstance(t, tuple):
            l, r = t
            for o, c in get_match_balances(s, l, r)[::-1]:
                fin[o.span()[0] : c.span()[1]] = v(s[o.span()[1] : c.span()[0]], o, c)
        elif isinstance(t, str):
            t = re.compile(t)
            for m in tuple(t.finditer(s))[::-1]:
                span = m.span()
                fin[span[0] : span[1]] = v(m)
            
        s = ''.join(fin)
    return s

matchset = {
    ('«', '»'): pair_quick_lambda,
    ('([a-zA-Z_][a-zA-Z0-9_]*)⟨', '⟩'): pair_inline_var,
    ('ƒ([₀₁₂₃₄₅₆₇₈₉]{0,})'): simple_arg_chain
}
    
xd = "«x⟨ƒ + 2⟩ 🠒 (x ** 2, ƒ)»(5)"
print(xd)
print(xd := parse(xd))
print(eval(xd))