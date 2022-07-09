#!/usr/bin/python 
import re
from parsing import *
from equation_parse import parse_equation

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

def pair_ternary(s, l, r, matchset):
    q = s.split('!')
    if len(q) % 2 == 0:
        q.insert(-2, q[-2])
    while len(q) > 2:
        c, v1, v2 = q[-3:]
        q[-3:] = [f"({v1}) if ({c}) else ({v2})"]
    return f"({q[-1]})"

euqation_match_funcs = "min max abs sin cos tan atan atan2 prod sum".split(' ')
def pair_equation(s, l, r, matchset):
    return parse_equation(s)

def pair_quick_lambda(s, l, r, matchset):
    s = parse(s, matchset)
    return f'''make_chain_func({','.join(f"(lambda *args: ({i.strip()}))" for i in s.split('🠒'))})'''

def pair_inline_var(s, l, r, matchset):
    return f"(set_then_return(globals(), '{l.groups()[0]}', {parse(s, matchset)}))"

def simple_arg_chain(s):
    t = int(''.join(str('₀₁₂₃₄₅₆₇₈₉'.index(i)) for i in s.groups()[0] or '₀'))
    return f"args[{t}]"

def extra_repls(s):
    return re.sub(r'𝔽 {0,}\(', r'__get_index_of_first__(', s)

def final_parse(s):
    return extra_repls(parse(s, {
        ('«', '»'): pair_quick_lambda,
        (r'\?', '¿'): pair_ternary,
        ('ƒ([₀₁₂₃₄₅₆₇₈₉]{0,})'): simple_arg_chain,
        ('([a-zA-Z_][a-zA-Z0-9_]*)⟨', '⟩'): pair_inline_var,
        ('∈', '∋'): pair_equation
    }))

if __name__ != '__main__':
    from xonsh.built_ins import XSH
    XSH.execer.parser.custom_pre_tree_process = final_parse
else:
    xd = "«x⟨ƒ⟩+2🠒ƒ*?x>2!ƒ**2!-1¿🠒print(ƒ₂)🠒ƒ₁»(5)"
    print(xd)
    print(xd := final_parse(xd))
    print(eval(xd))