import pandas as pd


class dynamic_manning:

    def __init__(self, S_df, O_df, A_df=pd.DataFrame()):
        if A_df.empty:
            A_df = pd.DataFrame(1,index=S_df.index, columns=['Num_Positions'])
            A_df.index.name = 'Job'
        S_df.index = S_df.index.map(str)
        O_df.index = O_df.index.map(str)
        A_df.index = A_df.index.map(str)
        S_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
        O_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
        A_df.sort_index()
        dynamic_manning.check_inputs(S_df,O_df,A_df)
        self.S_df = S_df.copy(deep=True)
        self.O_df = O_df.copy(deep=True)
        self.A_df = A_df.copy(deep=True)

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
        S_seeker_set=set(list(S_df.columns))
        O_seeker_set=set(list(O_df.index))
        S_job_set=set(list(S_df.index))
        O_job_set=set(list(O_df.columns))
        A_job_set=set(list(A_df.index))
        if len(S_seeker_set.union(O_seeker_set) - 
                S_seeker_set.intersection(O_seeker_set)) != 0:
            raise ValueError('Seeker lists for S_df and O_df do not match')
        if len(S_job_set.union(O_job_set) - 
                S_job_set.intersection(O_job_set)) != 0:
            raise ValueError('Job lists for S_df and O_df do not match')
        if len(S_job_set.union(A_job_set) - 
                S_job_set.intersection(A_job_set)) != 0:
            raise ValueError('Job lists for S_df and A_df do not match')

