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

def main():
    doctor_dir = "test_data/med/"
    #Sailors
    med_S_df = pd.read_csv(doctor_dir + "med_S.csv", index_col=0)
    #Job Owners
    med_O_df = pd.read_csv(doctor_dir + "med_O.csv", index_col=0)
    #Availability
    med_A_df = pd.read_csv(doctor_dir + "med_A.csv", header=None, index_col=0, 
            names = ['Job', 'Num_Positions'], skiprows=1)
    
    comp_dict = competitiveness(med_S_df,med_A_df)
    print(comp_dict)
    comp_dict = competitiveness(med_O_df)
    print(comp_dict)

if __name__ == '__main__':
    main()
