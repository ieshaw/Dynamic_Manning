import numpy as np
import pandas as pd
import random

def sim_prefs(decider, slate):
    '''
    input decider: list
    input slate: list
    output: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    '''
    slate_n = len(slate)
    slate_ranking = list(range(1,len(slate) + 1))
    pref_dict = {}
    for i in decider:
        pref_dict[i] = random.sample(slate_ranking, slate_n) 
    return  pd.DataFrame(data = pref_dict, index=slate, columns=decider)

def sim_random_pref(num_seekers=5, num_jobs=5):
    '''
    input num_seekers: int
    input num_jobs: int
    
    output: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    Saves to CSV a table of seekers preferences and owner preferences
    '''
    seekers = [str(i) for i in range(1,num_seekers + 1)]
    jobs = [str(i) for i in range(1,num_jobs + 1)]
    seeker_prefs = sim_prefs(decider=seekers, slate=jobs)
    owner_prefs = sim_prefs(decider=jobs, slate=seekers)
    return seeker_prefs, owner_prefs

def sim_save_random_prefs(num_seekers=5, num_jobs=5, seeker_file='Data/seeker_prefs.csv', owner_file='Data/owner_prefs.csv'):
    '''
    input num_seekers: int
    input num_jobs: int
    input seeker_file: string
    input owner_file: string
    
    Saves to CSV a table of seekers preferences and owner preferences
    '''
    seeker_prefs, owner_prefs = sim_random_pref(num_seekers, num_jobs) 
    seeker_prefs.to_csv(seeker_file, header=True, index=True)
    owner_prefs.to_csv(owner_file, header=True, index=True)

def sim_navy(n_sailors=10, n_jobs=10, couple_ratio=0.2):
    '''
    input n_sailors: int
    input n_jobs: int
    input couple_ratio: float between 0 and 1, percent of seekers that are members of a couple
    output O_df: Pandas DataFrame with row index sailors, column headers jobs
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of owner j of sailor i
    output S_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of sailor j of job i
    output A_df: Pandas DataFrame with columns 'Job'i (strings)  and 'Num_Positions' (integers) 
    output C_df: Pandas DataFrame with index 'Seeker_id' and columns ['Seeker','Partner','Partner_id'] 
            where if single 'Partner'/'Partner_id' = 0
    '''
    #Read in the csv of Naval Base information: Name, Lat, Lon, Number of Billets
    naval_bases = pd.read_csv('Data/naval_bases.csv')
    num_bases = len(naval_bases)
    sailors = [str(i) for i in range(1,n_sailors + 1)]
    if n_jobs >= num_bases:
        # Run the normalize the number of billets for the desired number of simulated sailors
        naval_bases['Normalized'] = naval_bases['Billets'] / naval_bases['Billets'].sum()
        # Generate billets based on noramlized values
        naval_bases['Billets'] = (naval_bases['Normalized'] * n_jobs).apply(np.ceil).astype(int)
        jobs = naval_bases['Name'].values
        A_df = naval_bases[['Name','Billets']].copy()
        A_df = A_df.rename(mapper={'Name':'Job', 'Billets': 'Num_Positions'}, axis='columns')
    else:
        jobs = naval_bases['Name'].values[:n_jobs]
        A_df = pd.DataFrame({'Job': jobs, 'Num_Positions': [1 for i in range(n_jobs)]}) 
    A_df.set_index('Job', inplace=True)
    O_df = sim_prefs(jobs, sailors)
    S_df = sim_prefs(sailors, jobs)
    C_df = sim_couples(sailors,couple_ratio)
    return O_df, A_df, S_df, C_df

def sim_save_navy(n_sailors=10, n_jobs=10, couple_ratio=0.2,  O_file='Data/O.csv', S_file='Data/S.csv',
        A_file='Data/A.csv', C_file='Data/C.csv'):
    '''
    input n_sailors: int
    input n_jobs: int
    input O_file: string, saving place of O_df csv
    input S_file: string, saving place of S_df csv
    input A_file: string, saving place of A_df csv
    input C_file: string, saving place of C_df csv
    '''
    O_df, A_df, S_df, C_df = sim_navy(n_sailors, n_jobs, couple_ratio)
    O_df.to_csv(O_file, header=True, index=True)
    S_df.to_csv(S_file, header=True, index=True)
    A_df.to_csv(A_file, header=True, index=True)
    C_df.to_csv(C_file, header=True, index=True)

def sim_couples(seekers,couple_ratio=0.2):
    '''
    input seekers: list
    input couple_ratio: float between 0 and 1, percent of seekers that are members of a couple
    output: Pandas DataFrame with index 'Seeker_id' and columns ['Seeker','Partner','Partner_id'] 
            where if single 'Partner'/'Partner_id' = 0
    '''
    n_seekers = len(seekers)
    #n_couples is the number of seekers who are in a couple
    #Thus the number of couples is actually n_couples/2
    n_couples = int(np.ceil(n_seekers * couple_ratio))
    if n_couples % 2 !=0:
        n_couples +=1
    seeker_id=list(range(1,n_seekers + 1))
    zeroes = [0 for i in range(n_seekers)]
    C_df = pd.DataFrame({'Seeker_id':seeker_id, 'Seeker':seekers,'Partner':zeroes, 'Partner_id':zeroes})
    C_df.set_index('Seeker_id', inplace=True)
    couples = random.sample(seeker_id,n_couples)
    couples = list(zip(couples[:int(n_couples/2)], couples[int(n_couples/2):]))
    for couple in couples:
        C_df.at[couple[0],'Partner_id'] = couple[1]
        C_df.at[couple[0],'Partner'] = C_df.at[couple[1], 'Seeker']
        C_df.at[couple[1],'Partner_id'] = couple[0]
        C_df.at[couple[1],'Partner'] = C_df.at[couple[0], 'Seeker']
    return C_df

def main():
    #sim_save_random_prefs(num_seekers=5, num_jobs=5, seeker_file='Data/seeker_prefs.csv', owner_file='Data/owner_prefs.csv')
    sim_save_navy(n_sailors=10, n_jobs=10, couple_ratio=0.2,  O_file='Data/O.csv', S_file='Data/S.csv',
            A_file='Data/A.csv', C_file='Data/C.csv')

if __name__ == '__main__':
    main()

