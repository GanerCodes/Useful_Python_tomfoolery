del __builtins__['copyright'], __builtins__['credits']

import threading
from warnings import filterwarnings
filterwarnings("ignore",category=DeprecationWarning)
del filterwarnings

from sys import setrecursionlimit
setrecursionlimit(10_000)

def load_heavy_libs():
	from sympy.parsing.latex import parse_latex as __tmp__
	__tmp__('0')
	import numpy as __np__
	globals()['parse_latex'] = __tmp__
	globals()['np'] = __np__
(big_load_thread := threading.Thread(target=load_heavy_libs)).start()

import itertools, functools
from types import FunctionType
from time import time, sleep

permute = itertools.permutations
groupby = itertools.groupby
reduce = functools.reduce

source ~/Scripts/xonsh_scripts/pymods/tools.xsh
source ~/Scripts/xonsh_scripts/pymods/transform.xsh
import_filepath("~/Scripts/xonsh_scripts/pymods/object_patch.xsh")

Δ = lambda a, b = None: a if a else b
δ = lambda x: Δ(x, __Γ__(type(x)))
X = lambda *args, r=None: list(itertools.product(*args, **({'repeat': r} if r else {})))
χ = lambda *args, r=None: list(zip(*itertools.product(*args, **({'repeat': r} if r else {}))))
K = lambda *args: reduce(args[1], args[0], *args[2:])
KK = lambda o, f, r=None, exins=False: list(itertools.accumulate(itertools.accumulate(o if r is None else [r] + list(o), f)))[bool(exins):]
lmap  = lambda *args, **kwargs: list(map(*args, **kwargs))
jmap  = lambda *args, **kwargs: ''.join(map(str, map(*args, **kwargs)))
pjmap = lambda *args, **kwargs: print(jmap(*args, **kwargs))
group = lambda d, f=lambda x: x: {k: list(v) for k, v in groupby(sorted(d, key=f), f)}

def ᐄ(a, *k):
	m = k[0] if k else a
	return m if a else Γ(type(m))

def ᐂ(a, *k):
	return a if a else (k[0] if k else Γ(type(a)))

def __Γ__(x, alt=None):
    try:
        return x()
    except Exception:
        return alt

class __Δ__:
    def __getitem__(self, i):
        return range(i) if type(i) == int else range(
             0  if i.start is None else i.start,
             10 if i.stop is None else i.stop,
             1  if i.step is None else i.step)

Γ = __Γ__
Δ = __Δ__()

def __get_index_of_first__(*l):
	c = 0
	for i in l:
		if i:
			return c
		c += 1

def set_nested_values(obj, keys, v):
	for i in keys[:-1]:
		obj = obj[i]
	obj[keys[-1]]=v
	return v

big_load_thread.join()
source ~/Scripts/xonsh_scripts/pymods/inline_stuff.py

# Modify types
indexable = {range, set, list, dict, tuple, frozenset, bytes, bytearray}
def patch_types():
	with object_patch.objmod(FunctionType, object, int, str):
		FunctionType.__or__  = lambda s, m: Chained_Lambda(Chained_Lambda.N, s) | m
		FunctionType.__mul__ = lambda s, m: Chained_Lambda(Chained_Lambda.N, s) * m
		FunctionType.map     = lambda x, d: list(map(x, d))
		int.rep = lambda x, c: [x] * c
		int.__iter__ = lambda s: iter(range(s))
		int.__len__  = lambda s: s
		str.__add__ = lambda a, b: a + str(b)
		object.apply = lambda x, f, *args, **kwargs: f(x, *args, **kwargs)
		object.iapply = lambda x, f, *args, **kwargs: [f(i, *args, **kwargs) for i in x]
		object.str = lambda x: str(x)
		object.τ = lambda x: print(dir(x))
		object.π = lambda x: print(x) or x
		object.Π = lambda x: print(x, end='') or x
		object.ℝ = lambda x, *args: x[args[0]] if len(args)==1 else x[args[0]].ℝ(*args[1:])
		object.ℚ = lambda x, *args: set_nested_values(x,args[:-1],args[-1])
		object.__invert__ = lambda x: print(x) or x
		
		# should prob make the keyword default have None as valid arg
		object.vals = lambda x, *vals, alt=None: [getattr(x, i) for i in vals if hasattr(x, i)] if alt is None else [
			getattr(x, i) if hasattr(x, i) else alt for i in vals]
patch_types()

def int_patch(b=True):
	with object_patch.objmod(int):
		if b:
			int.__iter__ = lambda s: iter(range(s))
			int.__len__  = lambda s: s
		else:
			del int.__iter__
			del int.__len__

for t in object_patch.objmod(*indexable):
	t.vals = lambda x, *vals, alt=None: [x[i] for i in vals if i in x] if alt is None else [
		i if i in x else alt for i in vals]

for t in object_patch.objmod(int, map, zip, filter,
	*itertools.vals('product', 'accumulate', 'group'), *indexable):
	
	t.filter = lambda x, key=None: list(filter(key, x))
	t.sorted = lambda x, key=None: list(sorted(x, key=key))
	t.group  = lambda x, key: group(x, key)
	t.list   = lambda s: list(s)
	t.map    = lambda x, f: list(map(f, x))
	t.cat    = lambda s, d='': str(d).join(map(str, s))
	t.len    = lambda s: s.__len__()
	t.KK     = lambda x, *args: KK(x, *args)
	t.K      = lambda x, *args:  K(x, *args)