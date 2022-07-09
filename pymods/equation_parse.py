import re
from typing import Iterable

class Span:
    def __init__(self, l, r):
        self.l, self.r = l, r
        self.size = r - l
    def __add__(self, v):
        self.l += v
        self.r += v
        return self
    def __repr__(self):
        return '%s %s' % (*self, )
    def __iter__(self):
        return iter((self.l, self.r))
    def as_index(self, data):
        return data[self.l : self.r]

class Closure:
    def __init__(self, name, span=None, *, reference=None, children=None, locked=False, **kwargs):
        self.name = name
        self.span = span
        self.reference = reference
        self.children = children or []
        self.locked = locked
        self.kwargs = kwargs
    def shift(self, v):
        self.span += v
        return self
    def __iter__(self):
        return iter(self.children)
    def __repr__(self):
        return '%s%s' % (self.name, self.print_children() if self.children else '')
    def print_children(self):
        return '[%s]' % ' '.join(map(str, self)) if self.children else ''
    def as_index(self, reference=None):
        if reference is None:
            return self.reference[self.span.l : self.span.r]
        else:
            return reference[self.span.l : self.span.r]
    def flatten_and_seperate_children(self):
        return ''.join(c.name+'_' for c in self.children)
    def get_outer_span(self):
        if isinstance(self, Closure_Pair):
            return self.outer_span
        else:
            return self.span

class Closure_Single(Closure):
    def __init__(self, name, match, **kwargs):
        self.match = match
        super().__init__(name, Span(*match.span()), **kwargs)

class Closure_Pair(Closure):
    def __init__(self, name, match_l, match_r, **kwargs):
        self.match_l = match_l
        self.match_r = match_r
        
        span_l = Span(*match_l.span())
        span_r = Span(*match_r.span())
        
        self.inner_span = Span(span_l.r, span_r.l)
        self.outer_span = Span(span_l.l, span_r.r)
        
        super().__init__(name, self.inner_span, **kwargs)
    def shift(self, v):
        self.inner_span += v
        self.outer_span += v
        return self

class Rule:
    def __init__(self, name, *matches, **kwargs):
        self.name = name
        self.matches = list(map(re.compile, matches))
        self.kwargs = kwargs
    def __repr__(self):
        return f"{self.name}: %s {self.kwargs=}" % (', '.join('"%s"' % m.pattern for m in self.matches))
    def match_iter(self, text) -> Iterable[Closure]:
        if len(self.matches) == 1:
            bound, = self.matches
            for i in bound.finditer(text):
                yield Closure_Single(self.name, i, reference=text, **self.kwargs)
        elif len(self.matches) == 2:
            lb, rb = self.matches
            yield from get_match_balances(text, lb, rb, self.name, **self.kwargs)

class Ruleset:
    def __init__(self, *rules):
        self.rules = rules
    def match_iter(self, text) -> Iterable[Closure]:
        end_pos = 0
        matches = [((rule, i), (match, match.get_outer_span())) for (i, rule) in enumerate(self.rules) for match in rule.match_iter(text)]
        matches.sort(key=lambda x: (x[1][1].l, x[0][1]))
        while len(matches) > 0:
            (rule, _), (match, relevent_span) = matches.pop(0)
            
            if relevent_span.l >= end_pos:
                end_pos = relevent_span.r
                yield rule, match
    def __repr__(self):
        return str(tuple(self.rules))

def get_match_balances(s, o, c, name=None, **kwargs) -> Iterable[Closure_Pair]:
    c_l = [('c', m) for m in c.finditer(s)]
    o_l = [('o', m) for m in o.finditer(s)][:len(c_l)]
    l = sorted(c_l + o_l, key=lambda x: x[1].span()[0])
    
    start, depth = None, 0
    for t, v in l:
        if depth == 0:
            if t == 'o':
                start = v
                depth += 1
        else:
            if t == 'o':
                depth += 1
            elif t == 'c':
                depth -= 1
                if depth == 0:
                    yield Closure_Pair(name, start, v, reference=s, **kwargs)

def tokenize_base_ruleset(text, ruleset, offset=0, reference=None):
    tree = []
    for rule, match in ruleset.match_iter(text):
        if 'r' in rule.kwargs:
            match.children = tokenize_base_ruleset(
                match.span.as_index(text),
                ruleset,
                offset+match.span.l,
                reference)
        
        match.shift(offset)
        tree.append(match)
        if reference:
            match.reference = reference
    return tree

def apply_ruleset(arr, ruleset):
    str_form = ''.join('%s_' % i.name for i in arr)
    # example: PA_LE_JE_
    # token_length would be: 3 (TODO? allow dynamic lengths and map the regex positions)
    token_length = 3
    new = []
    for rule, match in ruleset.match_iter(str_form):
        l = match.span.l // token_length
        r = match.span.r // token_length
        
        new_children = arr[l : r]
        if len(new_children) == 0:
            if l == len(arr):
                new_span = Span(arr[ -1].span.r, arr[ -1].span.r + 1)
            elif l == 0:
                new_span = Span(arr[  0].span.l, arr[  0].span.l + 1)
            else:
                new_span = Span(arr[l-1].span.l, arr[l-1].span.l + 1)
        else:
            new_span = Span(new_children[0].span.l, new_children[-1].span.r + 1)
        match.span = new_span
        
        for c in new_children:
            if c.locked:
                continue
            c.children = apply_ruleset(c.children, ruleset)
        
        match.children = new_children
        
        if 'r' in rule.kwargs:
            match.children = apply_ruleset(match.children, ruleset)
        
        if match.name == '--':
            match, = match.children
        
        new.append(match)
    
    return new

def tokenize_rulematrix(data, rulematrix):
    if isinstance(data, str):
        data = tokenize_base_ruleset(data, rulematrix[0], reference=data)
        if len(rulematrix) == 1:
            return data
        else:
            rulematrix = rulematrix[1:]
    
    for ruleset in rulematrix:
        data = apply_ruleset(data, ruleset)
    
    return data

def ts_toks(tokens):
    if not tokens: return ''
    
    if isinstance(tokens, Closure):
        tokens = [tokens]
    
    r = ""
    for tok in tokens:
        t = tok.name
        o = tok.reference
        c = tok.children
        s = tok.span
        if isinstance(tok, Closure_Pair):
            m = lm, rm = tok.match_l, tok.match_r
        else:
            m = lm = rm = tok.match
        match t:
            case 'PA'|'QB':
                r += ('(%s)' if t == 'PA' else 'abs(%s)') % ts_toks(c)
            case 'BB':
                r += '[%s]' % ts_toks(c)
            case 'NM':
                r += s.as_index(o)
            case 'IM':
                r += '*'.join(map(ts_toks, c))
            case 'VR':
                q = s.as_index(o)
                if len(q) > 1:
                    r += '*'.join(list(q))
                else:
                    r += q
            case 'VM':
                for c in c:
                    match c.name:
                        case 'DT':
                            r += ts_toks(c)
                        case 'VR':
                            r += c.span.as_index(c.reference)
                        case 'CB':
                            r += ts_toks(c)
            case 'FN':
                r += m.group(1)
            case 'NF':
                r += ts_toks(c)
            case 'CM':
                r += ','
            case 'CB':
                r += ts_toks(c)
            case 'RB':
                r += ts_toks(c)
            case 'RG':
                FN = ts_toks(c[0])
                if lm.group(1):
                    IX = ts_toks(c[1])
                    CBs = c[2:]
                else:
                    IX = '2'
                    CBs = c[1:]
                    
                match FN:
                    case "frac":
                        r += '((%s)/(%s))' % (
                            ts_toks(CBs[0]),
                            ts_toks(CBs[1]))
                    case "sqrt":
                        r += '((%s)**(1.0/(%s)))' % (
                            ts_toks(CBs[0]),
                            IX)
            case 'OP':
                r += s.as_index(o)
            case 'DT':
                r += '.'
            case 'PW':
                r += '(%s)' % ts_toks(c[1])
            case 'EX':
                r += '(%s)**(%s)' % (ts_toks(c[0]), '**'.join(map(ts_toks, c[1].children)))
            case 'SB':
                r += ts_toks(c)
            case 'SH':
                r += 'for %s in range(%s)' % (ts_toks(c[2].children[0]), ts_toks(c[4]))
            case 'SR':
                r += '%s((%s) %s)' % (c[0].children[0].match.group(1), ts_toks(c[1]), ts_toks(c[0]))
    return r

def parse_equation(equation):
    return ts_toks(tokenize_rulematrix(equation, [
        Ruleset(
            Rule('CB', r'\{', r'\}', r=True),
            Rule('PA', r'\\left\(', r'\\right\)', r=True),
            Rule('QB', r'\\left\|', r'\\right\|', r=True),
            Rule('BB', r'\\left\[', r'\\right\]', r=True),
            Rule('RB', r'\[', r'\]', r=True),
            Rule('BS', r'_'),
            Rule('PS', r'\^'),
            Rule('OP', r'\-|\+'),
            Rule('CP', r'\=|\<|\>|\\le|\\ge', ),
            Rule('CM', r','),
            Rule('IT', r'\\(sum|prod)'),
            Rule('FN', r'\\([a-zA-Z]{1,})'),
            Rule('NM', r'([0-9]{1,}\.?[0-9]{0,})|([0-9]{0,}\.?[0-9]{1,})'),
            Rule('VR', r'[a-zA-Z]{1,}[a-zA-Z0-9]{0,}'),
            Rule('DT', r'\.')
        ),
        Ruleset(
            Rule('RG', r'FN_((RB_)?)((?:CB_){1,})'),
            Rule('SH', r'IT_BS_CB_PS_CB_', locked=True),
            Rule('VM', r'((VR_((BS_CB_)?)((DT_)?)){1,})(?<!VR_VR_)', locked=True),
            Rule('PW', r'PS_CB_'),
            Rule('NF', r'FN_PA_'),
            Rule('--', r'[A-Z]{2}_'),
        ),
        Ruleset(
            Rule('PC', r'(PW_){1,}'),
            Rule('--', r'[A-Z]{2}_')
        ),
        Ruleset(
            Rule('EX', r'[A-Z]{2}_PC_'),
            Rule('--', r'[A-Z]{2}_')
        ),
        Ruleset(
            Rule('SB', r'(?<=SH_)', '$', r=True),
            Rule('--', r'[A-Z]{2}_')
        ),
        Ruleset(
            Rule('SR', r'SH_SB_', locked=True),
            Rule('--', r'[A-Z]{2}_'),
        ),
        Ruleset(
            Rule('IM', r'(((VM|FN|NF|RG|PA|VR|NM|SR|BB)_){2,})(?<!FN_PA_)'),
            Rule('--', r'[A-Z]{2}_')
        )
    ]))

# o=str(asd)
# q = [[' '] * len(o) for x in range(1+o.count('['))]
# c = 0
# for i, v in enumerate(o):
#     if v == ']':
#         c -= 1
#     q[c][i] = v
#     if v == '[':
#         c += 1
# print('\n'.join(''.join(w) for w in q))
# print(asd)