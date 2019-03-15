import json
import math
import os
import pandas as pd
import sys

def mu_metrics(S_df, O_df, X_df):
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
    output mu_s: float, average preference for job seeker
    output mu_o: float, average preference for job owner
    '''
    S_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    O_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    X_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    placements = X_df.sum().sum()
    mu_s =round((S_df.values * X_df.values).sum().sum()/placements,4)
    mu_o = round((O_df.values.T * X_df.values).sum().sum()/placements,4)
    return mu_s,mu_o

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
    S_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    X_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    A_df.sort_index(inplace=True)
    n, m = X_df.shape
    n_options = n
    a_sum = m
    S_np = S_df.values
    if p_type == 'o':
        S_np = S_np.T
        n_options = m
        a_sum = n
        single = A_df.empty
        if not single:
            a_sum = A_df.sum().values[0]
    top_dict = {}
    ranks = pd.DataFrame((X_df.values*S_np)).stack().value_counts().sort_index()
    ranks.drop(index=0,inplace=True)
    divisor = float(ranks.sum())
    top_dict['{}_participants'.format(p_type)] = a_sum 
    top_dict['{}_matched_count'.format(p_type)] = divisor 
    top_dict['{}_matched_ratio'.format(p_type)] = round(float(divisor)/a_sum,4) 
    unmatched_count = a_sum - divisor
    top_dict['{}_unmatched_count'.format(p_type)] = unmatched_count 
    top_dict['{}_unmatched_ratio'.format(p_type)] = round(float(unmatched_count)/a_sum,4) 
    cum_sum = 0
    i = 0
    rank_list = [1]
    rank_list.extend([ 5 * i for i in range(1,math.ceil(float(n_options)/5) + 1)])
    r = len(rank_list)
    for index,value in ranks.iteritems():
        if i < r:
            curr_rank = rank_list[i]
            rank_str = str(curr_rank) + '_' + p_type
            if index > curr_rank:
                top_dict[rank_str + '_count'] = cum_sum
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/a_sum, 4)
                cum_sum += value
                i += 1
            elif index == curr_rank:
                cum_sum += value
                top_dict[rank_str + '_count'] = cum_sum
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/a_sum, 4)
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
                top_dict[rank_str + '_ratio'] = round(float(cum_sum)/a_sum, 4)
        prev_rank = rank
    return top_dict

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
    matchings = ['mip', 'da_o', 'da_s']
    x_dict = {}
    for algo in matchings:
        x_str = output_dir + 'X_{}.csv'.format(algo)
        if os.path.exists(x_str):
            x_dict[algo] = pd.read_csv(x_str, index_col=0)
    p_dict = {'s': S_df, 'o': O_df}
    out_dict = {}
    for x in x_dict:
        mu_s, mu_o = mu_metrics(S_df, O_df, x_dict[x])
        out_dict[x] = {'mu_s': mu_s, 'mu_o': mu_o, 'mu_combined': mu_s + mu_o,'gap_mu': mu_s - mu_o}
        for p in p_dict:
            out_dict[x].update(top_perc(p_dict[p], p, x_dict[x], A_df))
    out_df = pd.DataFrame.from_dict(out_dict)
    print(out_df)

if __name__ == '__main__':
    main()
