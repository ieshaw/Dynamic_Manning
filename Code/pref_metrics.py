import pandas as pd

def competitiveness(df):
    '''
    input: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    output: dictionary, keys are slate options, enteries are the competitiveness scores
    '''
    #weighted scaling competitiveness score
    comp_dict = {}
    n_jobs = 10
    n_seekers = len(df)
    for index,row in df.iterrows():
        mu = (row ** 0.5).mean()
        #TODO: Read in A_df for 'a' value
        a = 1
        comp_dict[index] =  round(1 - mu/((a**0.5) * (n_seekers**0.5) * n_jobs),4)
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

def correlation(df1, df2, axis=0):
    '''
    input:  Two Pandas DataFrames with transposed rows and columns. Zeros converted
            np.NaN. If axis=0 (default) then labels will be the column headers
            of the first dataframe. If axis=1 then headers of second dataframe.
    output: Pandas DataFrame with pearson standard correlation of two dataframes.
    '''

    # labels become header of df2
    if axis:
        tf1 = df1.copy().transpose()
        return df2.corrwith(tf1)
    # labels become header of df1
    else:
        tf2 = df2.copy().transpose()
        return df1.corrwith(tf2)



def generalism(df):
    '''
    input: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    output: dictionary, keys are slate options, enteries are the competitiveness scores
    '''
    gen_dict = {}
    for index,row in df.iterrows():
        gen_dict[index] = row.var()
    return gen_dict

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
    output: dictionary, keys are slate options, enteries are the specialization scores

    WILL ADD MEAN, MIN, SPEC COLUMNS TO DF. Pass a copy if you do not want this.
    '''

    # helper function to do math on each row
    def spec_calc(row):
        return (row['mean']-row['min']) / (row['mean']+row['min'])

    df['mean'] = df.mean(axis=1)
    df['min'] = df.min(axis=1)

    df['spec'] = df.apply(spec_calc, axis=1)

    return df['spec']

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
    gen_dict = generalism(df)
    spec_dict = specialization(df)
    metric_dict = {'Competitiveness': comp_dict, 
                    'Generalism': gen_dict,
                    'Specialization': spec_dict}
    metric_df = pd.DataFrame.from_dict(metric_dict)
    sim_df = similarity(df) 
    return metric_df, sim_df

def main():
    seeker_df = pd.read_csv('Data/seeker_prefs.csv', header=0, index_col=0)
    metric_df, sim_df = pref_metrics(seeker_df)

    metric_df.to_csv('Data/job_metrics.csv', header=True, index=True)
    sim_df.to_csv('Data/seeker_similarity.csv', header=True, index=True)

    owner_df = pd.read_csv('Data/owner_prefs.csv', header=0, index_col=0)
    metric_df, sim_df = pref_metrics(owner_df)

    metric_df.to_csv('Data/seeker_metrics.csv', header=True, index=True)
    sim_df.to_csv('Data/job_similarity.csv', header=True, index=True)

if __name__ == '__main__':
    main()
