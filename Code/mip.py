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
    P_S = S_df.values
    P_O = O_df.values
    A = A_df.values
    m,n = S_df.shape 
    m_a = A_df.sum().sum()
    k = min(n,m_a)
    X = cp.Variable((m,n), boolean=True)
    f = cp.trace(cp.matmul(P_O,X)) + cp.trace(cp.matmul(X.T,P_S))
    #f = cp.sum(cp.multiply(X.T, P_O),cp.multiply(X,P_S))
    #f = 2 *cp.trace(cp.matmul(X,P_O)) + cp.trace(cp.matmul(X.T,P_S))
    obj = cp.Problem(cp.Minimize(f),
            [cp.atoms.affine.reshape.reshape(cp.sum(X,axis=1),(m,1)) <= A,
                cp.sum(X) <= k + 0.5, cp.sum(X) >= k - 0.5] )
    #mip_solvers for cvxpy [CBC, GLPK_MI, CPLEX, ECOS_BB, GUROBI]
    obj.solve(solver=cp.ECOS_BB)
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
                    Solution status: {}
                    Num om Assignments given: {}
                    Num of Assigments expected: {}
                    '''.format(obj.status,X_df.sum().sum(),k))
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
