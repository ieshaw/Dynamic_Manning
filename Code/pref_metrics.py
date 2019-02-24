import pandas as pd


def competitiveness(df, A_df=pd.DataFrame()):
    '''
    input df: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
            If only single assignment, don't pass.
    output: dictionary, keys are slate options, enteries are the competitiveness scores
    '''
    #weighted scaling competitiveness score
    comp_dict = {}
    single = A_df.empty
    if not single:
        M = A_df['Num_Positions'].sum()
    n,m = df.shape
    for index,row in df.iterrows():
        if not single:
            a_j = A_df.at[index, 'Num_Positions']
            f = 1 - a_j / M
        else: 
            f = 1
        s = 1 - (1/(n*m))*((row ** 0.5).sum())
        comp_dict[index] =  round(f*s,4)
    return comp_dict

'''
Sciorintino competitiveness Score

comp_dict = {}
for index,row in df.iterrows():
    mu = row.mean()
    sigma = (((row - mu).apply(lambda x: max(x,0)))**2).sum()
    comp_dict[index] = (mu * (len(row)**2))/(sigma)
return comp_dict
'''

def similarity(df):
    '''
    input: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    output: sim_df, Pandas DataFrame with row index deciders, column headers deciders
            the entries are the similarities. Entry at row i, column j is the 
            similarity of decider j of decider i
    '''
    sim_df = pd.DataFrame(data=-1,index=df.columns, columns=df.columns, dtype=float)
    n_d = len(df.columns)
    nn_d = 2 * n_d
    sim_coeff = (1/((n_d - 1) **2))*(1/(nn_d))
    for i in df:
        for j in df:
            if i == j:
                sim_df[i][i] = 1
            elif sim_df[i][j] == -1:
                s = 1 - sim_coeff * ((nn_d - (df[i] + df[j])) * ((df[i] - df[j])**2)).sum()
                sim_df[i][j] = s
                sim_df[j][i] = s
    return sim_df

def specialization(df):
    '''
    input: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    output: dictionary, keys are slate options, enteries are the competitiveness scores
    '''
    spec_dict = {}
    for index,row in df.iterrows():
        spec_dict[index] = row.min()
    return spec_dict

def pref_metrics(df):
    '''
    input: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    output: metric_df, Pandas DataFrame with row index metric names, column headers slate options
            the entries are the metric values. 
    output: sim_df, Pandas DataFrame with row index slate options, column headers slate options
            the entries are the similarities. Entry at row i, column j is the 
            similarity of slate option j of slate option i
    '''
    comp_dict = competitiveness(df)
    spec_dict = specialization(df)
    metric_dict = {'Competitiveness': comp_dict, 
                    'Specialization': spec_dict}
    metric_df = pd.DataFrame.from_dict(metric_dict)
    sim_df = similarity(df) 
    return metric_df, sim_df

def main():
    print_to_screen = True
    save_to_file = False

    seeker_df = pd.read_csv('Data/seeker_prefs.csv', header=0, index_col=0)
    metric_df, sim_df = pref_metrics(seeker_df)

    if print_to_screen:
        print('-----------------------------------')
        print('Job Metrics')
        print('-----------------------------------')
        print(metric_df.head())
        print('-----------------------------------')
        print('Seeker Similarity')
        print('-----------------------------------')
        print(sim_df.head())
        print('-----------------------------------')

    if save_to_file:
        metric_df.to_csv('Data/job_metrics.csv', header=True, index=True)
        sim_df.to_csv('Data/seeker_similarity.csv', header=True, index=True)

    owner_df = pd.read_csv('Data/owner_prefs.csv', header=0, index_col=0)
    metric_df, sim_df = pref_metrics(owner_df)
    
    if print_to_screen:
        print('Seeker Metrics')
        print('-----------------------------------')
        print(metric_df.head())
        print('-----------------------------------')
        print('Job Similarity')
        print('-----------------------------------')
        print(sim_df.head())
        print('-----------------------------------')

    if save_to_file:
        metric_df.to_csv('Data/seeker_metrics.csv', header=True, index=True)
        sim_df.to_csv('Data/job_similarity.csv', header=True, index=True)

if __name__ == '__main__':
    main()
