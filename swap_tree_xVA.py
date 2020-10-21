# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:31:38 2020

@author: Theodor
"""

def swap_tree(par_rates,maturities,sig,FV,c,R1,R2,PD1,PD2):
    r"""
    We compute the value of a swap at each node of a binomial tree given a par curve.
    
    The input maturities is a list of integers usually. 
    
    par_rates = a list of coupons for which the bonds sell at par 
    
    sig = the implied forward yield volatility (from either bond option prices, \
          caps/floors)
    
    R1,R2 = recovery rates of entity 1 and 2. 
    
    The probabilities of default are PD1,PD2. \\
    """
    import numpy as np
    import numpy.linalg as la
    def create_lower_diag():
        mat = [[1+par_rates[i] if j==i else par_rates[i] for j in range(len(par_rates))]\
                for i in range(len(par_rates))]
        return np.tril(np.array(mat))
    A = create_lower_diag()
    b = np.ones(len(par_rates))
    discounts = np.dot(la.inv(A),b)
    forwards = [1/discounts[0]-1 if i==0 else discounts[i-1]/discounts[i]-1 \
                for i in range(0,len(par_rates))]
    forwards_down = [2**i * forwards[i]/(np.exp(2*sig)+1)**i for i in range(1,len(par_rates))]
    fwd_tree = [[forwards_down[i]*np.exp(j*2*sig) for j in range(0,i+2)] \
                 for i in range(0,len(forwards)-1)]
    fwd_tree.insert(0,[forwards[0]])
    swap_values = []
    for i in range(0,len(par_rates)):
        if i==0:
            swap_values.append([(c-fwd_tree[-1][j])*FV/(1+fwd_tree[-1][j]) \
                                for j in range(0,len(par_rates))])
        else:
            swap_values.append([(1/2*(swap_values[-1][j]+swap_values[-1][j+1])+\
                         (c-fwd_tree[len(par_rates)-i-1][j])*FV)/(1+fwd_tree[len(par_rates)-i-1][j]) \
                         for j in range(len(swap_values[-1])-1)])
    CFs = [[(c-fwd_tree[i][j])*FV for j in range(0,i+1)] for i in range(0,len(forwards))]
    EpCFs = [[max(x,0) for x in CFs[i]] for i in range(len(CFs))]
    EnCFs = [[max(-x,0) for x in CFs[i]] for i in range(len(CFs))]
    import math
    def comb(n,k):
        return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    probs_tree = [[comb(n,k)/2**n for k in range(0,n+1)] for n in range(0,len(forwards))]
    EpEs = [np.dot(EpCFs[i],probs_tree[i]) for i in range(len(EpCFs))]
    EnEs = [np.dot(EnCFs[i],probs_tree[i]) for i in range(len(EnCFs))]
    CVA = (1-R2) * PD2 * np.dot(discounts,EpEs)
    DVA = (1-R1) * PD1 * np.dot(discounts,EnEs)
    return fwd_tree,swap_values,CVA,DVA,EpEs,EnEs