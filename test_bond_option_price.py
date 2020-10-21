# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:27:53 2020

@author: Theodor
"""

from bond_option_price import bond_option_price,implied_bop_vol,implied_bop_vol2
#%%    
def test_bop_imp_vol():
    K_opt,rates = 1000,([3/12,9/12,10/12],[0.09,0.095,0.1])
    TTM_opt,fwd_price,mkt_price = 10/12,939.68,9.49
    print(implied_bop_vol(rates,TTM_opt,K_opt,fwd_price,mkt_price,a0 = 0.01,\
                          b0 = 1.0))
test_bop_imp_vol()
#%%
def test_bop_imp_vol2():
    K_opt,rates = 115,0.05
    TTM_opt,TTM_bond,FV,c,freq = 2.25,10,100,0.08,2
    mkt_price = 1.78
    print(implied_bop_vol2(rates,TTM_opt,K_opt,mkt_price,TTM_bond,FV,c,freq,\
                           option = "put",a0 = 0.01))
test_bop_imp_vol2()
#%%
def test_bop():
    import numpy.linalg as la
    import numpy as np
    A = np.array([[1.01,0,0,0,0],[0.02,1.02,0,0,0],[0.025,0.025,1.025,0,0],\
                  [0.028,0.028,0.028,1.028,0],[0.036,0.036,0.036,0.036,1.036]])
    b = np.array([1,1,1,1,1]).T
    discounts = np.dot(la.inv(A),b)
    print(discounts)
    zero_rates = [discounts[i]**(-1/(i+1))-1 for i in range(0,5)]
    print(zero_rates)
    TTM_bond,FV,c,freq,TTM_opt,K_opt,sig_y,rates = 5,100,0.08,1,1,115,0.2,\
               ([1,2,3,4,5],zero_rates)
    rates2 = 0.05
    print(bond_option_price(TTM_bond,FV,c,freq,TTM_opt,K_opt,sig_y,rates,option = "put"))          
    print(bond_option_price(TTM_bond,FV,c,freq,TTM_opt,K_opt,sig_y,rates2,option = "put"))
    print(implied_bop_vol2(rates,TTM_opt,K_opt,27,TTM_bond,100,c,freq,a0=0.01,b0 = 1.0))
    
test_bop()