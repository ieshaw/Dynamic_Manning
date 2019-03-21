import cvxpy as cp
import numpy as np
import pandas as pd
import sys
from check import check_inputs

def mip(S_df, O_df, A_df, print_to_screen=True):
    '''
    input S_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of sailor j of job i
    input O_df: Pandas DataFrame with row index sailors, column headers jobs
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of owner j of sailor i
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    output X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    '''
    # Infer all the terms of the optimization funciton
    S_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    O_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    A_df.sort_index()
    #S_norm_df = (S_df-S_df.min())/(S_df.max()-S_df.min())
    #O_norm_df = (O_df-O_df.min())/(O_df.max()-O_df.min())
    #P_S = S_norm_df.pow(0.5).values
    #P_O = O_norm_df.pow(0.5).values
    #P_S = S_norm_df.values
    #P_O = O_norm_df.values
    #P_S = S_df.pow(2).values
    #P_O = O_df.pow(2).values
    P_S = S_df.values
    P_O = O_df.values
    A = A_df.values
    m,n = S_df.shape 
    m_a = A_df.sum().sum()
    k = min(n,m_a)
    X = cp.Variable((m,n), boolean=True)
    f = cp.trace(cp.matmul(X, (P_S.T + P_O)))
    obj = cp.Problem(cp.Minimize(f),
            [cp.atoms.affine.reshape.reshape(cp.sum(X,axis=1),(m,1)) <= A,
                cp.atoms.affine.reshape.reshape(cp.sum(X,axis=0),(1,n)) <= 1,
                cp.sum(X) <= k + 0.5, cp.sum(X) >= k - 0.5] )
    #mip_solvers for cvxpy [CBC, GLPK_MI, CPLEX, ECOS_BB, GUROBI]
    obj.solve(solver=cp.ECOS_BB, verbose=False, mi_max_iters=1000)
    status = obj.status
    if status in ['optimal', 'optimal_inaccurate']:
        X_df = pd.DataFrame(X.value, index=S_df.index, columns=S_df.columns)
        X_df.fillna(0,inplace=True)
        X_df = X_df.round()
        #Get Rid of Negatives
        X_df = X_df ** 2
        X_df = X_df.astype(int)
        if print_to_screen:
            print('''
                    Time to Solve MIP: {}
                    Obj value: {}
                    Solution status: {}
                    Num om Assignments given: {}
                    Num of Assigments expected: {}
                    '''.format(obj.solver_stats.solve_time, obj.value,obj.status,X_df.sum().sum(),k))
    else:
        raise ValueError('''
                        Problem considered {}.
                        '''.format(status))
    return X_df

def sim_data():
    data_dir = 'test_data'
    S_df = pd.read_csv(data_dir + '/S.csv', index_col=0)  
    O_df = pd.read_csv(data_dir + '/O.csv', index_col=0)  
    A_df = pd.read_csv(data_dir + '/A.csv', index_col=0)  
    check_inputs(S_df, O_df, A_df)
    X_df = mip(S_df, O_df, A_df)
    X_df.to_csv(data_dir + '/X.csv', header=True, index=True)

def doc_data():
    data_dir = 'test_data/med/med_' 
    S_df = pd.read_csv(data_dir + 'S.csv', index_col=0)  
    O_df = pd.read_csv(data_dir + 'O.csv', index_col=0)  
    A_df = pd.read_csv(data_dir + 'A.csv', index_col=0)  
    check_inputs(S_df, O_df, A_df)
    X_df = mip(S_df, O_df, A_df)
    X_df.to_csv(data_dir + 'X.csv', header=True, index=True)

def main():
    doc_data()
    #sim_data()

if __name__ == '__main__':
    main()
