# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:26:40 2020

@author: Theodor
"""

def test_swap_CVA():
    import numpy.linalg as la
    import numpy as np
    A = np.array([[1.01,0,0,0,0],[0.02,1.02,0,0,0],[0.025,0.025,1.025,0,0],\
                  [0.028,0.028,0.028,1.028,0],[0.03,0.03,0.03,0.030,1.03]])
    b = np.array([1,1,1,1,1]).T
    discounts = np.dot(la.inv(A),b)
    
    b_fix = np.dot(discounts,[4,4,4,4,104])
    v_swap = b_fix - 100
    print(v_swap)
    sig = 0.2
    FV = 100
    forwards = [1/discounts[0]-1 if i==0 else discounts[i-1]/discounts[i]-1 \
                for i in range(0,5)]
    
    forwards_down = [2**i * forwards[i]/(np.exp(2*sig)+1)**i for i in range(1,5)]
    fwd_tree = [[forwards_down[i]*np.exp(j*2*sig) for j in range(0,i+2)] \
                 for i in range(0,4)]
    fwd_tree.insert(0,[forwards[0]])
    swap_values = []
    swap_values.append([(0.04-fwd_tree[4][j])*FV/(1+fwd_tree[4][j]) for j in range(0,5)])
    swap_values.append([(1/2*(swap_values[-1][j]+swap_values[-1][j+1])+\
                         (0.04-fwd_tree[3][j])*FV)/(1+fwd_tree[3][j]) \
                         for j in range(len(swap_values[-1])-1)])
    swap_values.append([(1/2*(swap_values[-1][j]+swap_values[-1][j+1])+\
                         (0.04-fwd_tree[2][j])*FV)/(1+fwd_tree[2][j]) \
                         for j in range(len(swap_values[-1])-1)])
    swap_values.append([(1/2*(swap_values[-1][j]+swap_values[-1][j+1])+\
                         (0.04-fwd_tree[1][j])*FV)/(1+fwd_tree[1][j]) \
                         for j in range(len(swap_values[-1])-1)])
    swap_values.append([(1/2*(swap_values[-1][j]+swap_values[-1][j+1])+\
                         (0.04-fwd_tree[0][j])*FV)/(1+fwd_tree[0][j]) \
                         for j in range(len(swap_values[-1])-1)])
    print(swap_values)
    print(fwd_tree)
    c = 0.04
    CFs = [[(c-fwd_tree[i][j])*FV for j in range(0,i+1)] for i in range(0,len(forwards))]
    EpCFs = [[max(x,0) for x in CFs[i]] for i in range(len(CFs))]
    EnCFs = [[max(-x,0) for x in CFs[i]] for i in range(len(CFs))]
    print("Cashflows",CFs)
    print("Expected positive cash flows",EpCFs)
    import math
    def comb(n,k):
        return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    probs_tree = [[comb(n,k)/2**n for k in range(0,n+1)] for n in range(0,5)]
    print(probs_tree)
    EpEs = [np.dot(EpCFs[i],probs_tree[i]) for i in range(len(EpCFs))]
    EnEs = [np.dot(EnCFs[i],probs_tree[i]) for i in range(len(EnCFs))]
    R,PD = 0.4,0.025
    CVA = (1-R)*PD*np.dot(discounts,EpEs)
    DVA = (1-R)*PD* np.dot(discounts,EnEs)
    print(CVA,DVA)
test_swap_CVA()
#%%
from swap_tree_xVA import swap_tree

def swap_tree_test():
    r"""
    In this test, we check that the swap is value correctly using binomial trees 
    and standard par model. 
    """
    par_rates = [0.01,0.02,0.025,0.028,0.036]
    maturities = [1,2,3,4,5]
    sig,FV,c = 0.1743,100,0.04
    fwd_tree,swap_values,CVA,DVA,EpEs,EnEs = swap_tree(par_rates,maturities,sig,FV,c,0.5,\
                                             0.4,0.025,0.01)
    print("Credit and debit adjusted value of swap",swap_values[-1][0]+DVA-CVA)
    print("The values of CVA and DVA respectively are ",CVA,DVA)
    print("Expected positive exposures",EpEs)
    print("Expected negative exposures",EnEs)
    r"""
    Now we check manually that the swap value has been computed correctly, independent 
    of the model used. 
    """
    import numpy.linalg as la
    import numpy as np
    A = np.array([[1.01,0,0,0,0],[0.02,1.02,0,0,0],[0.025,0.025,1.025,0,0],\
                  [0.028,0.028,0.028,1.028,0],[0.036,0.036,0.036,0.036,1.036]])
    b = np.array([1,1,1,1,1]).T
    discounts = np.dot(la.inv(A),b)
    b_fix = np.dot(discounts,[4,4,4,4,104])
    v_swap = b_fix - 100
    print("Model independent value of swap:",v_swap)
    print("Binomial value of the swap",swap_values[-1][0])
    
swap_tree_test()
#%%
def test_swap_FRAs():
    import numpy.linalg as la
    import numpy as np
    A = np.array([[1.01,0,0,0,0],[0.02,1.02,0,0,0],[0.025,0.025,1.025,0,0],\
                  [0.028,0.028,0.028,1.028,0],[0.036,0.036,0.036,0.036,1.036]])
    b = np.array([1,1,1,1,1]).T
    discounts = np.dot(la.inv(A),b)
    forwards = [1/discounts[0]-1 if i==0 else discounts[i-1]/discounts[i]-1 \
                for i in range(0,5)]
    print(forwards)
    FRAs = [100*(0.04-forwards[i])*discounts[i] for i in range(len(forwards))]
    print(FRAs)
    print(sum(FRAs))
    import pandas as pd
    indexes = ["F({0},{1})".format(i,i+1) for i in range(0,5)]
    df = pd.DataFrame(FRAs,index=indexes,columns = ['value'])
    print(df)
test_swap_FRAs()