import pandas as pd


def top_perc(S_df, X_df, rank_list=[1,5,10]):
    '''
    input S_df: Pandas DataFrame with row index slate options, column headers deciders
            the entries are the preferences. Entry at row i, column j is the 
            preference ranking of decider j of slate option i
    input X_df: Pandas DataFrame with row index job, column headers sailors
            the entries are the job placements. Entry at row i, column j is 
            1 is sailor j has job i, 0 otherwise
    input rank_list: list of ints, integers of which ranks to look for
    output top_dict: dictionary, keys from rank_list, entries are tuples, (count, ratio) of those participants who were assigned that preference or higher
    '''
    n,m = X_df.shape
    if S_df.shape[1] == n:
        S_df = S_df.T
    total = n * m
    top_dict = {}
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
    X_mip = pd.read_csv(output_dir + 'X_mip.csv', index_col=0)
    top_dict = top_perc(S_df, X_mip, rank_list=[1,5,10])

if __name__ == '__main__':
    main()
