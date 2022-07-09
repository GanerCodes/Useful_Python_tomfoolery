#!/usr/bin/python 

# +++++++++>>+.>++.<<<[->>>[-<+<+>>]<.[-<+>>+<]<.[->+>+<<]>>.[-<+<+>>]<<<]


# Memory represents an infinite array of integers, who's default values are zero
# The pointer represents a location in memory
# Instructions are executed in order
# '+' add 1 at pointer
# '-' subtract 1 at pointer
# '>' move pointer fowards 1
# '<' move pointer backwards 1
# '[' if value at pointer is 0, jump to 1 past corresponding ']', otherwise move pointer up by 1
# ']' if value at pointer is 0, move pointer up by 1, otherwise jump 1 past corresponding '['
# '.' print number at pointer

ins = """
+++-. This prints 2
><.   This prints 2
[-].  This prints 0
"""

sleep_time = 0.000
show_steps = True
verbose_steps = True
fancy_simple_cursor = True
steps_per_print = 1



from time import sleep

class l(list):
    def check_resize(self, i):
        if i < len(self): return
        self += [0] * (len(self) - i + 1)
    
    def __getitem__(self, i):
        self.check_resize(i)
        return list.__getitem__(self, i)
    
    def __setitem__(self, i, o):
        self.check_resize(i)
        list.__setitem__(self, i, o)

mem = l()
ins = ''.join(filter(".,+-<>[]".__contains__, ins))
jumps = {}

if show_steps and not verbose_steps:
    print("\x1b[?25l", end = '')
    print(ins, end='\n')
    print("\0x9B\0x3F\0x32\0x35\0x6C")

p_m = p_i = step_count = 0
while True:
    if p_i >= len(ins):
        print("Finished!")
        print("Final memory array:", mem)
        exit()
    
    if show_steps and not (step_count % steps_per_print):
        if verbose_steps:
            print("Memory array:", mem)
            print("Instructions:",''.join(ins))
            g = [' '] * len(ins)
            g[p_i] = '^'
            print(' ' * 13, ''.join(g), end = '\n' * 2)
        else:
            q = [' '] * len(ins)
            q[p_i] = "^"
            if fancy_simple_cursor:
                print("\u001B[A\u001B[999D", end="")
                print(''.join(q), " | ", mem, "\033[K")
            else:
                print(mem)
            
    
    i, d = ins[p_i], mem[p_m]
    match i:
        case '+':
            mem[p_m] += 1
        case '-':
            mem[p_m] -= 1
        case '>':
            p_m += 1
        case '<':
            p_m -= 1
        case '[' | ']' as i:
            if (
                d == 0 and i == '[' and (g := (']',  1))
            ) or (
                d != 0 and i == ']' and (g := ('[', -1))
            ):
                if p_i in jumps:
                    p_i = jumps[p_i]
                else:
                    p_loc = p_i
                    e = 1
                    while e > 0:
                        p_i += g[1]
                        if ins[p_i] == i:
                            e += 1
                        elif ins[p_i] == g[0]:
                            e -= 1
                    jumps[p_loc] = p_i
        case '.':
            print(". says", d)
    p_i += 1
    
    if sleep_time > 0:
        sleep(sleep_time)
    
    step_count += 1