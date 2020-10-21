# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 11:47:19 2019

@author: Theodor
"""

from bond_prices import bond_price
from bond_duration import bond_yield,bond_duration
#%%
print(bond_price(100,0.08,3,([1,2,3],[0.08,0.09,0.1]),1,freq2=1))
print(bond_price(100,0.07,3,([1,2,3],[0.08,0.09,0.1]),1,freq2=1))
print(bond_price(100,0.06,3,([1,2,3],[0.08,0.09,0.1]),1,0.5,freq2=1,option = "clean price" ))
print(bond_price(100,0.06,3,([1,2,3],[0.08,0.09,0.1]),1,0.5,freq2=1,option = "dirty price" ))
print(bond_yield(100,0.06,3,([1,2,3],[0.08,0.09,0.1]),1,freq2=1,y0=0.0))
#%%
print(bond_yield(100,0.05,3,freq=1,freq2 = 1,mkt_price=100.65))
print(bond_yield(100,0.02,3,freq=1,freq2=1,mkt_price = 100.25))
#%%
print(bond_yield(100,0.08,10,freq=1,freq2 = 1,mkt_price = 85.5030))
print(bond_price(100,0.08,9,0.1040,freq = 1,freq2 = 1))
#%%
PV1 = 5/1.0305+5/1.0305**2+105/1.0305**3
PV2 = 5/1.0295+5/1.0295**2+105/1.0295**3
app_mod_dur = (PV2-PV1)/(2 * 0.0005*105.657223)
print(app_mod_dur)
#%%
x=1/(1+0.02)
price = 2.5*(x+x**2+x**3+x**4+x**4)+100*x**5
full_price = price * (1+0.02)**(66/180)
print(full_price)
#%%
#print((2.5*7.5+102.5*3)/bond_price(100,0.05,3,0.03,2))
print(bond_duration(100,0.05,3,freq = 2,rate = 0.03))
print(bond_duration(100,0.06,4,freq = 1,rate = 0.04))
print(bond_price(100,0.05,3,0.03,2),bond_price(200,0.06,4,0.04,1))
#%%
def test():
    f = lambda y: 104/(1+y)**2+4/(1+y)-99.52
    f2 = lambda y: 108/(1+y)**3+8/(1+y)**2+8/(1+y)-94.05
    f3 = lambda y: 105/(1+y)**2 + 8/(1+y) - 94.05
    import scipy.optimize as opt
    print(opt.newton(f,0.0))
    print(opt.newton(f2,0.0),opt.newton(f3,0.0))
test()
#%%
print(bond_duration(100,0.12,19.66,freq=1,freq2 = 1,rate = 0.088))