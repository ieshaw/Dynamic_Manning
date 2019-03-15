import json
import math
import os
import pandas as pd
import sys

def matched_list(S_df, O_df, X_df):
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
    output: Pandas DataFrame with columns ['Seeker','Job','Seeker_Pref','Job_Pref']
    '''
    out_dict = {}
    seekers = S_df.columns
    jobs = O_df.columns
    for seeker in seekers:
        for job in jobs:
            if X_df.at[job,seeker] == 1:
                out_dict[seeker] = {'Job': job,
                                'Seeker_Pref': S_df.at[job,seeker],
                                'Job_Pref': O_df.at[seeker,job]
                                }
    out_df = pd.DataFrame.from_dict(out_dict, orient='index')
    out_df.index.name = 'Seeker'
    return out_df

def main():
    if len(sys.argv) != 2:
        raise ValueError('''
                    Provide relative or abolute path to data directory
                        with files 'A.csv' , 'O.csv', and 'S.csv'

                    example:
                        run.py path/to/data/
                    ''')

    data_dir = sys.argv[1]
    '''
    output_dir = data_dir + 'results/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    '''
    S_df = pd.read_csv(data_dir + 'S.csv', index_col=0)  
    S_df.index = S_df.index.map(str)
    O_df = pd.read_csv(data_dir + 'O.csv', index_col=0)  
    O_df.index = O_df.index.map(str)
    A_df = pd.read_csv(data_dir + 'A.csv', index_col=0)  
    S_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    #algo = 'MIP'
    #x_str = output_dir + 'X_{}.csv'.format(algo)
    x_str = data_dir + 'X.csv'
    X_df = pd.read_csv(x_str, index_col=0)
    X_df.sort_index(axis=0).sort_index(axis=1,inplace=True)
    A_df.sort_index(inplace=True)
    print(matched_list(S_df, O_df, X_df))

if __name__ == '__main__':
    main()
