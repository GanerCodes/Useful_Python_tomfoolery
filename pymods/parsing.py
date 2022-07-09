import re

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

def parse(s, matchset):
    for t, v in matchset.items():
        fin = list(s)
        if isinstance(t, tuple):
            l, r = t
            for o, c in get_match_balances(s, l, r)[::-1]:
                fin[o.span()[0] : c.span()[1]] = v(s[o.span()[1] : c.span()[0]], o, c, matchset)
        elif isinstance(t, str):
            t = re.compile(t)
            for m in tuple(t.finditer(s))[::-1]:
                span = m.span()
                fin[span[0] : span[1]] = v(m)
            
        s = ''.join(fin)
    return s