from math import sin
from itertools import product
sx, sy = 90, 46

_=[print(chr(10240+int(''.join(map(lambda i:str(1*((lambda x,y:-max(-((.4*(x+5/2))**2+10*(2*y-1.2+(sin(3.2*(x+1)))/4)**2-1),-((x-1.7)**2+(y-2.2-(sin(abs(x-2.3)))/2)**2-1),-min(min(abs(2*y+7+abs(x-5/2))+abs(x-5/2)-1,max(4/5*abs(x-5/2),.15*abs(y+1.5))-.3),min(abs(2*y+8+abs(x-2.9/3))+abs(x-2.9/3)-1,max(.8*abs(x-2.9/3),.15*abs(y+2))-.3),min(abs(2*y+8+abs(x+5/2))+abs(x+5/2)-1,max(.8*abs(x+5/2),.15*abs(y+2))-.3),min(abs(2*y+7+abs(x+(2.9)/3))+abs((x+2.9/3))-1,max(.8*abs(x+2.9/3),.15*abs(y+1.5))-.3)),-.3*x**2-y**4/4+4,-((x-3)**2+(y-.5-x/3)**2-3)*((x-3.6)**2+(y-2.75)**2-.3**2),-.2*(x-5.8)**2-(3*y-x-3-sin(2*x))**2+3/4))((15*2*bx+i%2)/(2*sx)+2,-15*(4*by+(i//2))/(4*sy))<.08)),map(int,'76531420'))),2)),end='\n'*((bx-1-sx//2)%sx==0)) for by,bx in product(range(6-sy//2,sy//2-5),range(1-sx//2,sx//2-4))]

# Slower, less cool looking simi-compressed version: 
#from functools import reduce
#_=[print(chr(10240+int(''.join(map(lambda i:str(1*(eval(reduce(lambda a,b:a.replace(b[0],b[1:]),['(lambda x,y:-]-{.4*(g}>+10*(YI.2V#3.$(x+1})/4BI)_{xI.7BVy-2.2-(#[C2.3})/2BI)_<~Y+7Nh}Nh)I,]4/5KhRZ1.5}XR~Y+8+^)+^I,].8*^,Z2}XR~Y+8Ng}Ng)I,].8KgRZ2}XR~Y+7NxV2.9)/3}N(x+w}I,].8Kx+wRZ1.5}X}_.3*x>-y**4/4+4_{C3BVy-.5-x/3B-3)*{C3.6BVy-2.75BX>)_.$(C5.8B-(3*y-C3-#$x}>+3/4}']+'Cx-;B)>;R),;X-.3;N+[;Z`Ky+;Y$y;K*[;V+(;I-1;~<[;_,-;#sin(;`.15;hx-q;gx+q;$2*;{((;}));q5/2;^[x-w);w2.9/3;<min(;[abs(;>**2;]max('.split(';')))((15*2*bx+i%2)/(2*sx)+2,-15*(4*by+(i//2))/(4*sy))<.08)),map(int,'76531420'))),2)),end='\n'*((bx-1-sx//2)%sx==0)) for by,bx in product(range(6-sy//2,sy//2-5),range(1-sx//2,sx//2-4))]
