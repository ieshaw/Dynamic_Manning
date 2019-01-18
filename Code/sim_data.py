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

def main():
    num_seekers = 5
    num_jobs = 5

    seekers = [str(i) for i in range(1,num_seekers + 1)]
    jobs = [str(i) for i in range(1,num_jobs + 1)]

    seeker_prefs = sim_prefs(decider=seekers, slate=jobs)
    owner_prefs = sim_prefs(decider=jobs, slate=seekers)

    seeker_prefs.to_csv('Data/seeker_prefs.csv', header=True, index=True)
    owner_prefs.to_csv('Data/owner_prefs.csv', header=True, index=True)

if __name__ == '__main__':
    main()

