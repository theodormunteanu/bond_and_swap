# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:33:23 2018

@author: theod
"""


def bond_price(FV, c, T, rate, freq=4, t=0, freq2=0, **opt):
    r"""
    Returns the price of a bond given the zero-rates or a yield
    
    Parameters
    ----------
    `FV` : face value of the bond (float/int).
    
    `c`  : coupon rate (expressed in numbers between 0 and 1) 
    
    `T`  : time to maturity (expressed in years) 
    
    `rate`  : can be a single float number or a tuple containing maturities and  
            zero rates 
    
    `rate` can be of the following types: 
        1. `int` or `float`: a single discounted rate
        2. `tuple` of two elements: the first element is a list of maturities while 
        the second component is a list of interest rates (spot rates)
    
            
    `freq`  : frequency of payments per year. By default it is set to 4, 
              quarterly payments. 
    
    `t`  : time when the bond is evaluated
    
    `freq2`  : compounding frequency (by default is set to 0, which means 
            continuous discounting) \
    `option`  : contains the option of clean price or dirty price: \
              For the clean price it substracts the accrued coupon from the dirty
              price
    Examples
    --------
    1. Compute the price of a 2-year bond with a single yield rate of 6.76%,
    semi-annual coupons with annual coupon rate of 6%. 
    
    Source: John Hull, Options, Futures and Other Derivatives (8th edition), 
            section 4.4: Bond prices --> Bond yield
    
    >>> bond_price(100,0.06,2,0.676,2)
    
       Result: 98.38
    
    2. Compute the price of a 2-year bond with treasury rates 5%, 5.8%, 6.4% 
    and 6.8% corresponding to 6M, 12M, 18M and 24M if the coupon is 6% per year 
    and the payment frequency is twice/year. 
    
    Source: the same but the intro section of Bond pricing instead
    
    >>> bond_price(100,0.06,2,([0.5,1,1.5,2],[0.05,0.058,0.064,0.068]),2)
    
       Result: 98.38
    """
    if isinstance(rate,tuple) and isinstance(rate[0],list) and isinstance(rate[1],list):
       if opt.get("option") in {"dirty price",None}:
          return bond_price2(FV,c,T,rate,freq,t,freq2)
       elif opt.get("option") == "clean price":
          return bond_price2(FV,c,T,rate,freq,t,freq2)-accrued_coupon(FV,c,t,T,freq)
    elif isinstance(rate, (int, float)):
      if opt.get("option") in {"dirty price", None}:
         return bond_price1(FV, c, T, rate, freq, t, freq2)
      elif opt.get("option")=="clean price":
         return bond_price1(FV,c,T,rate, freq, t, freq2)-accrued_coupon(FV,c,t,T,freq)


def bond_price1(FV, c, T, r, freq=4, t=0, freq2=0):
    def times(t,T,freq = 4):
        r"""The above function gives the times of cash-flows posterior to time t"""
        import numpy as np
        if freq*(T-t)==int(freq*(T-t)):
            k = int(freq*(T-t))
            return np.linspace(T-(k-1)/freq,T,k,endpoint = True)
        else:
            k = int(freq*(T-t))+1
            return np.linspace(T-(k-1)/freq,T,k,endpoint = True)
        
    import numpy as np
    if t==T:
        return FV + (c/freq+1)*FV
    elif t>T or t<0:
        raise TypeError('the time when you want to evaluate the bond surpasses\
                        the lifetime of the bond or it is negative')
    else:
        time_points = times(t,T,freq)
        k = len(time_points)
        if freq2==0:
            disc_rates = [np.exp(-r*(time_points[i]-t)) for i in range(k)]
        else:
            disc_rates = [1/(1+r/freq2)**(freq2*(time_points[i]-t)) for i in range(k)]
        cash_flows = [c/freq*FV]*k
        cash_flows[-1]=cash_flows[-1]+FV
        return np.dot(disc_rates,np.array(cash_flows))

def bond_price2(FV,c,T,rates,freq=4,t=0,freq2 = 0):
    import numpy as np
    def times(t,T,freq = 4):
        if freq*(T-t)==int(freq*(T-t)):
            k = freq*(T-t)-1
        else:
            k = int(freq*(T-t))
        return np.linspace(T-k/freq,T,(k+1),endpoint = True)
    if t==T:
        return FV + (c/freq+1)*FV
    elif t>T or t<0:
        raise TypeError('the time when you want to evaluate the bond surpasses\
                        the lifetime of the bond or it is negative')
    else:
        time_points = times(t,T,freq)
        k = len(time_points)
        app_rates = [np.interp(time_points[i],rates[0],rates[1])\
                         for i in range(k)]
        if freq2==0:
            disc_rates = [np.exp(-app_rates[i]*(time_points[i]-t)) for i in range(k)]
        else:
            disc_rates = [1/(1+app_rates[i]/freq2)**(freq2*(time_points[i]-t)) for i in range(k)]
        cash_flows = [c/freq*FV]*k
        cash_flows[-1]=cash_flows[-1]+FV
        return np.dot(disc_rates,np.array(cash_flows))

def accrued_coupon(FV,c,t,T,freq=4):
    def last_time(t,T,freq = 4):
        if freq*(T-t)==int(freq*(T-t)):
            k = freq*(T-t)-1
        else:
            k = int(freq*(T-t))
        return T-(k+1)/freq
    return FV*c/freq * (t-last_time(t,T,freq))