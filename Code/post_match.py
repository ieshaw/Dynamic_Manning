import json
import os
import pandas as pd
import sys

def gap_metric(S_df, O_df, X_df):
    '''
    input S_df: Pandas DataFrame, seeker preferences,  with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input O_df: Pandas DataFrame, owner preferences, with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    output gap_mu: float, average difference of preference for assigment between
            job seeker and job owner
    '''
    gap_df = (S_df * X_df) - (O_df.T * X_df)
    m, n = X_df.shape
    placements = m * n - X_df.sum().sum()
    gap_mu = round(gap_df.sum().sum() / placements, 4)
    return gap_mu

def top_perc(S_df, p_type, X_df, rank_list=[1,5,10]):
    '''
    input S_df: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input p_type: str, 's' or 'o', 's' indicates S_df and X_df have the same column headers/indices
                    'o' indicates S_df indices correspond to X_df column headers and vice versa
    input X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    input rank_list: list of ascending ints, integers of which ranks to look for
    output top_dict: dictionary, keys from rank_list, entries are tuples, (count, ratio) of those participants who were assigned that preference or higher
    '''
    if p_type == 'o':
        S_df = S_df.T
    top_dict = {}
    ranks = (X_df * S_df).stack().value_counts().sort_index()
    divisor = float(ranks.sum() - ranks.iloc[0])
    cum_sum = 0
    i = 0
    for index,value in ranks.iteritems():
        if index != 0:
            cum_sum += value
            if index == rank_list[i]:
                top_dict[rank_list[i]] = (cum_sum, round(float(cum_sum)/divisor, 4))
                i += 1
    return top_dict

#TODO: Pareto Efficiency

def main():
    if len(sys.argv) != 2:
        raise ValueError('''
                    Provide relative or abolute path to data directory
                        with files 'A.csv' , 'O.csv', and 'S.csv'

                    example:
                        run.py path/to/data/
                    ''')

    data_dir = sys.argv[1]
    output_dir = data_dir + 'results/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    S_df = pd.read_csv(data_dir + 'S.csv', index_col=0)  
    S_df.index = S_df.index.map(str)
    O_df = pd.read_csv(data_dir + 'O.csv', index_col=0)  
    O_df.index = O_df.index.map(str)
    A_df = pd.read_csv(data_dir + 'A.csv', index_col=0)  
    X_mip = pd.read_csv(output_dir + 'X_mip.csv', index_col=0)
    rank_list=[1,5,10]
    x_dict = {'mip': X_mip}
    p_dict = {'s': S_df, 'o': O_df}
    gap_dict = {}
    top_dict = {}
    for x in x_dict:
        gap_dict[x] = gap_metric(S_df, O_df, x_dict[x])
        for p in p_dict:
            top_dict['top_{}_{}'.format(x,p)] = top_perc(p_dict[p], p, x_dict[x], rank_list)
    out_dict = {'gap_mu' : gap_dict, 'top' : top_dict}
    print(out_dict)
    with open(output_dir + 'post_match.json', 'w') as fp:
            json.dump(out_dict, fp)

if __name__ == '__main__':
    main()
