import json
import math
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

def top_perc(S_df, p_type, X_df, A_df=pd.DataFrame()):
    '''
    input S_df: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input p_type: str, 's' or 'o', 's' indicates S_df and X_df have the same column headers/indices
                    'o' indicates S_df indices correspond to X_df column headers and vice versa
    input X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
            If only single assignment, don't pass.
    output top_dict: dictionary, keys from rank_list, entries are tuples, (count, ratio) of those participants who were assigned that preference or higher
    '''
    n, m = X_df.shape
    n_options = n
    a_sum = m
    if p_type == 'o':
        S_df = S_df.T
        n_options = m
        a_sum = n
        single = A_df.empty
        if not single:
            a_sum = A_df.sum().values[0]
    top_dict = {}
    ranks = (X_df * S_df).stack().value_counts().sort_index()
    ranks.drop(index=0,inplace=True)
    rank_list = [1]
    rank_list.extend([ 5 * i for i in range(1,math.ceil(float(n_options)/5) + 1)])
    divisor = float(ranks.sum())
    top_dict['{}_participants'.format(p_type)] = a_sum 
    top_dict['{}_matched_count'.format(p_type)] = divisor 
    top_dict['{}_matched_ratio'.format(p_type)] = round(float(divisor)/a_sum,4) 
    unmatched_count = a_sum - divisor
    top_dict['{}_unmatched_count'.format(p_type)] = unmatched_count 
    top_dict['{}_unmatched_ratio'.format(p_type)] = round(float(unmatched_count)/a_sum,4) 
    cum_sum = 0
    i = 0
    r = len(rank_list)
    for index,value in ranks.iteritems():
        if i < r:
            curr_rank = rank_list[i]
            rank_str = str(curr_rank) + '_' + p_type
            if index > curr_rank:
                top_dict[rank_str + '_count'] = cum_sum
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/divisor, 4)
                cum_sum += value
                i += 1
            elif index == curr_rank:
                cum_sum += value
                top_dict[rank_str + '_count'] = cum_sum
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/divisor, 4)
                i += 1
            else:
                cum_sum += value
            last_rank_added = index
    #Finish out the rank list
    prev_rank = 1
    for rank in rank_list:
        if rank >= curr_rank:
            rank_str = str(rank) + '_' + p_type
            if rank < last_rank_added:
                prev_rank_str = str(prev_rank) + '_' + p_type
                top_dict[rank_str + '_count'] = top_dict[prev_rank_str + '_count']
                top_dict[rank_str + '_ratio'] = top_dict[prev_rank_str + '_ratio']
            else:
                top_dict[rank_str + '_count'] = cum_sum
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/divisor, 4)
        prev_rank = rank
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
    x_dict = {'mip': X_mip}
    p_dict = {'s': S_df, 'o': O_df}
    out_dict = {}
    for x in x_dict:
        out_dict[x] = {'gap_mu': gap_metric(S_df, O_df, x_dict[x])}
        for p in p_dict:
            out_dict[x].update(top_perc(p_dict[p], p, x_dict[x], A_df))
    out_df = pd.DataFrame.from_dict(out_dict)
    print(out_df)

if __name__ == '__main__':
    main()
