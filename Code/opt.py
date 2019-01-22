import cvxpy as cp
import numpy as np
import pandas as pd

def opt(S_df, O_df, A_df, C_df,D_df):
    '''
    input S_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of sailor j of job i
    input O_df: Pandas DataFrame with row index sailors, column headers jobs
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of owner j of sailor i
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    input C_df: Pandas DataFrame with index 'Seeker_id' and columns ['Seeker','Partner','Partner_id'] 
    ouyput Z_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    '''
    # Infer all the terms of the optimization funciton
    P_S = S_df.values
    P_O = O_df.values
    A = A_df.values
    m = S_df.shape[0] 
    if m < len(D_df):
        D = D_df.values[:m,:m]
    else:
        D = D_df.values
    n = S_df.shape[1]
    k = max(n,m)
    nc = int(0.5 * C_df['Partner_id'].apply(lambda x: bool(x>0)).sum())
    X = cp.Variable((n,m), boolean=True)
    f = 2 *cp.trace(cp.matmul(X.T,P_O)) + cp.trace(cp.matmul(X,P_S))
    H = cp.Variable((m,m))
    n_c = 0
    C_df['Partner_id'] = C_df['Partner_id'].astype(int)
    for index, row in C_df.iterrows():
        if row['Partner_id'] != 0:
            n_c += 1
            #(mx1)x(1xm) to make an (mxm) then sum accross all these couples, then hadamard 
            #product with D, then filter if above 50 miles
            H += X[:,index].T * X[:, row['Partner_id']]
    #Here we do the hadamard product, divide by two since each couple was counted twice
    #Then max/min to get eveything over 49 miles to a value of 1
    H = cp.minimum((cp.maximum(cp.multiply(H,0.5 * D),49) - 49),1)
    n_c *= 0.5
    obj = cp.Problem(cp.Minimize(f),
            [cp.atoms.affine.reshape.reshape(cp.sum(X,axis=1),(m,1)) <= A,
                cp.sum(X) == k] )
    '''
    #With the couples distance constraint
    obj = cp.Problem(cp.Minimize(f),
            [cp.atoms.affine.reshape.reshape(cp.sum(X,axis=1),(m,1)) <= A,
                cp.sum(X) == k, cp.sum(H) >= n_c * 0.95] )
    '''
    #obj.solve(solver=cp.ECOS_BB)
    obj.solve()
    X_df = pd.DataFrame(X.value, index=S_df.index, columns=S_df.columns)
    X_df = X_df.round()
    return X_df

def main():
    #import all the data
    S_df = pd.read_csv('Data/S.csv', index_col=0)  
    O_df = pd.read_csv('Data/O.csv', index_col=0)  
    D_df = pd.read_csv('Data/D.csv', index_col=0)  
    A_df = pd.read_csv('Data/A.csv', index_col=0)  
    C_df = pd.read_csv('Data/C.csv', index_col=0)  
    X_df = opt(S_df, O_df, A_df, C_df, D_df)
    X_df.to_csv('Data/X.csv', header=True, index=True)

if __name__ == '__main__':
    main()
