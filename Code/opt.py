import cvxpy as cp
import numpy as np
import pandas as pd

#import all the data
S_df = pd.read_csv('Data/S.csv', index_col=0)  
O_df = pd.read_csv('Data/O.csv', index_col=0)  
D_df = pd.read_csv('Data/D.csv', index_col=0)  
A_df = pd.read_csv('Data/A.csv', index_col=0)  
C_df = pd.read_csv('Data/C.csv', index_col=0)  
# Infer all the terms of the optimization funciton
P_S = S_df.values
P_O = O_df.values
A = A_df.values
m = S_df.shape[0] 
n = S_df.shape[1]
print(A.shape)
nc = int(0.5 * C_df['Partner_id'].apply(lambda x: bool(x>0)).sum())
X = cp.Variable((n,m), boolean=True)
f = 2 *cp.trace(cp.matmul(X.T,P_O)) + cp.trace(cp.matmul(X,P_S))
#TODO: Add constraint: sum,sum X == min(n,m)
#TODO: Add constraint: D(X) <= 0.5
obj = cp.Problem(cp.Minimize(f),
        [cp.atoms.affine.reshape.reshape(cp.sum(X,axis=1),(m,1)) <= A])
obj.solve()
print(X.value)
