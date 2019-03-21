import pandas as pd

def check_inputs(S_df, O_df, A_df):
    '''
    input S_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of sailor j for job i
    input O_df: Pandas DataFrame with row index sailors, column headers jobs
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of owner j for sailor i
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    output X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    '''
    m_s, n_s = S_df.shape 
    n_o, m_o = O_df.shape 
    m_a, t_a = A_df.shape 
    if m_s != m_o or n_s != n_o:
        raise ValueError('''
                        S_df has dimensions ({}x{}) and O_df has dimensions ({}x{}) \n 
                        S_df and O_df.T should have the same dimensions
                        '''.format(m_s,n_s,n_o,m_o))
    if m_a != m_s or t_a != 1:
        raise ValueError('''
                        A_df has dimensions ({}x{}) but should have dimensions ({}x1)
                        '''.format(m_a,t_a,m_s))

def X_check(X_df, A_df):
    '''
    Throws error if X_df 
     - Assigns more A_j seekers to job j
     - Assigns a seeker to more than 1 job
     - Has entries besides {0,1}
     - Assigns less than min(sum(A), n) jobs

    input X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    '''
    if X_df.sum(axis=0).max() > 1:
        raise ValueError('''
                    X_df incorrect. Only one job assignment per seeker.
                    ''')
    if (X_df.sum(axis=1) - A_df['Num_Positions']).sum() > 0:
        raise ValueError('''
                    X_df incorrect. At least one position over filled.
                    ''')
    if set(X_df.stack().values) != {0,1}:
        raise ValueError('''
                    X_df incorrect. Should be binary.
                    ''')
    m,n = X_df.shape
    curr_assignments = X_df.sum().sum()
    exp_assignments = min(n,A_df.sum().sum())
    if curr_assignments != exp_assignments:
        raise ValueError('''
                    X_df incorrect. 
                    Expected Assignments : {}
                    Acutal Assignments: {}
                    '''.format(exp_assignments, curr_assignments))

def main():
    print('This is a script holding functions to check inputs and outputs, nothing to see here.')
        
if __name__ == '__main__':
    main()

