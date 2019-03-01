'''
Thank you to the following repository

https://github.com/daffidwilde/matching

'''
import matching
import numpy as np
import pandas as pd
import sys

def da(S_df, O_df, A_df, optimal='s'):
    '''
    This is the Deferred Accetance Algorithm developed by Gale and Shapely
    input S_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of sailor j of job i
    input O_df: Pandas DataFrame with row index sailors, column headers jobs
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of owner j of sailor i
    input A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    input optimal: string, 's' or 'o', whether the result will be seeker optimal or owner optimal
    output X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    '''
    # Infer all the terms of the optimization funciton
    X_df = pd.DataFrame(0, index=S_df.index, columns=S_df.columns)
    job_owners = gen_players(O_df, True, A_df)
    seekers = gen_players(S_df)
    hr = matching.HospitalResident(suitors=seekers, reviewers=job_owners)
    if optimal == 's':
        solved = hr.solve(optimal='suitor')
    elif optimal == 'o':
        solved = hr.solve(optimal='reviewer')
    else:
        raise ValueError('optimal must be either s or o')
    for key,value in solved.items():
        for v in value:
            X_df.at[str(key),str(v)] = 1
    return X_df

def gen_players(player_df, capacity=False, capacity_df=None):
    '''
    input player_df: Pandas DataFrame with row index job, column headers players
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of player j of job i
    input capacity_df: False or pandas dataframe; none if capacity for all players is 1
            if more than one, Pandas DataFrame with columns 'Job'(players, strings) 
            and 'Num_Positions' (capacity,integers) 
    return: list of players
    '''
    players = []
    cap = False
    if capacity:
        cap = True
        cap_dict = capacity_df.to_dict()[capacity_df.columns[0]]
    for col in player_df.columns:
        prefs = list(player_df[col].sort_values().index.astype(str).values)
        if cap:
            players.append(matching.Player(str(col), prefs, capacity=cap_dict[col]))
        else: 
            players.append(matching.Player(str(col), prefs))
    return players

def normal_main():
    if len(sys.argv) != 2:
        raise ValueError('One argument needed. Data Directory.')
    data_dir = sys.argv[1]
    S_df = pd.read_csv(data_dir + '/S.csv', index_col=0)  
    O_df = pd.read_csv(data_dir + '/O.csv', index_col=0)  
    A_df = pd.read_csv(data_dir + '/A.csv', index_col=0)  
    X_df = da(S_df, O_df, A_df, optimal='s')
    X_df.to_csv(data_dir + '/X.csv', header=True, index=True)

def main():
    normal_main()

if __name__ == '__main__':
    main()
