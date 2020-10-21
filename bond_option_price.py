# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:29:41 2020

@author: Theodor
"""
from bond_prices import bond_price
from bond_duration import bond_duration
#%%
def bond_option_price(TTM_bond,FV,c,freq,TTM_opt,K_opt,sig_y,rates,option = "call"):
    import numpy as np
    cash_price = bond_price(FV,c,TTM_bond,rates,freq)
    k = int(TTM_opt * freq)
    cash_flows = [c*FV/freq]*k
    times = np.linspace(1/freq,k/freq,k)
    bp = bond_price(FV,c,TTM_bond,rates,freq,t = TTM_opt)
    duration = bond_duration(FV,c,TTM_bond,mkt_price = bp,freq = freq,t=TTM_opt )
    if isinstance(rates,(int,float)):
        disc_rates = [np.exp(-times[i]*rates) for i in range(k)]
        sig_bond = sig_y * duration * rates
        PV_interest = np.dot(cash_flows,[disc_rates[i] for i in range(k)])
        fwd_price_bond = (cash_price - PV_interest)*np.exp(TTM_opt * rates)
    elif isinstance(rates,tuple) and [isinstance(rates[i],list) for i in range(len(rates))]:
        rate = lambda x:np.interp(x,rates[0],rates[1])
        disc_rates = [np.exp(-times[i]*rate(times[i])) for i in range(k)]
        sig_bond = sig_y * duration * rates[0][0]
        PV_interest = np.dot(cash_flows,[disc_rates[i] for i in range(k)])
        fwd_price_bond = (cash_price - PV_interest)*np.exp(TTM_opt * rate(TTM_opt))
    return bop_black(rates,TTM_opt,K_opt,fwd_price_bond,sig_bond,option)

def bop_black(rates,TTM_opt,K_opt,fwd_price,sig_B,option = "call"):
    r"""
    
    bond option price under black model
    """
    import numpy as np
    if isinstance(rates,(int,float)):
        disc_rate = np.exp(-TTM_opt*rates)
    elif isinstance(rates,tuple) and [isinstance(rates[i],list) for i in range(len(rates))]:   
        rate = lambda x:np.interp(x,rates[0],rates[1])
        disc_rate = np.exp(-TTM_opt*rate(TTM_opt))
    import scipy.stats as stats
    d1 = (np.log(fwd_price/K_opt)+sig_B**2 * TTM_opt/2)/(sig_B*np.sqrt(TTM_opt))
    d2 = d1 - sig_B * np.sqrt(TTM_opt)
    if option == "call":
        return disc_rate * (fwd_price * stats.norm.cdf(d1)-K_opt * stats.norm.cdf(d2))
    elif option in ["Put","put"]:
        return disc_rate * (K_opt * stats.norm.cdf(-d2) - fwd_price * stats.norm.cdf(-d1))
#%%
def falsi_method(f,a0,b0,tol,niter = 30):
    err = abs(a0-b0)
    iters = 0
    while abs(err)>tol and iters<niter:
        c = (a0*f(b0)-b0*f(a0))/(f(b0)-f(a0))
        if f(a0)*f(c)>0:
            a0 = c
        elif f(a0)*f(c)<0:
            b0 = c
        else:
            return c
        iters = iters+1
        err = f(c)
    return c,err,iters

def implied_bop_vol(rates,TTM_opt,K_opt,fwd_price,mkt_price,option = "call",\
                        a0 = 0.0,b0 = 1.0,niters = 30,tol = 0.0001):
    f = lambda sig:bop_black(rates,TTM_opt,K_opt,fwd_price,sig,option) - mkt_price
    return falsi_method(f,a0,b0,tol = tol,niter = niters)

def implied_bop_vol2(rates,TTM_opt,K_opt,mkt_price,TTM_bond,FV,c,freq,option = "call",\
                     a0 = 0.0,b0 = 1.0,niters = 30,tol = 0.0001):
    import numpy as np
    bp = bond_price(FV,c,TTM_bond,rates,freq,t = TTM_opt)
    duration = bond_duration(FV,c,TTM_bond,mkt_price = bp,freq = freq,t=TTM_opt )
    cash_price = bond_price(FV,c,TTM_bond,rates,freq)
    k = int(TTM_opt * freq)
    cash_flows = [c*FV/freq]*k
    times = np.linspace(1/freq,k/freq,k)
    if isinstance(rates,(int,float)):
        y0 = rates
        disc_rates = [np.exp(-times[i]*rates) for i in range(k)]
        PV_interest = np.dot(cash_flows,[disc_rates[i] for i in range(k)])
        fwd_price_bond = (cash_price - PV_interest)*np.exp(TTM_opt * rates)
    elif isinstance(rates,tuple) and [isinstance(rates[i],list) for i in range(len(rates))]:
        y0 = rates[0][0]
        rate = lambda x:np.interp(x,rates[0],rates[1])
        disc_rates = [np.exp(-times[i]*rate(times[i])) for i in range(k)]
        PV_interest = np.dot(cash_flows,[disc_rates[i] for i in range(k)])
        fwd_price_bond = (cash_price - PV_interest)*np.exp(TTM_opt * rate(TTM_opt))
    sig_B = implied_bop_vol(rates,TTM_opt,K_opt,fwd_price_bond,mkt_price,\
                            option = option,a0 = a0,b0 = b0,niters = niters,tol = tol)[0]
    return sig_B/(duration * y0)

