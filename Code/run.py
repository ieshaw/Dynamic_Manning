import os
import pandas as pd
import sys
from da import da
from opt import check_inputs, opt
from pref_metrics import pref_metrics, correlation

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
    check_inputs(S_df, O_df, A_df)
    metrics_s, sim_o = pref_metrics(O_df)
    metrics_s.to_csv(output_dir + 'Metrics_s.csv', header=True, index=True)
    sim_o.to_csv(output_dir + 'Similarity_o.csv', header=True, index=True)
    metrics_o, sim_s = pref_metrics(S_df)
    metrics_o.to_csv(output_dir + 'Metrics_o.csv', header=True, index=True)
    sim_s.to_csv(output_dir + 'Similarity_s.csv', header=True, index=True)
    corr_s = correlation(S_df,O_df)
    corr_s.to_csv(output_dir + 'Corr_s.csv', header=True, index=True)
    corr_o = correlation(S_df,O_df)
    corr_o.to_csv(output_dir + 'Corr_o.csv', header=True, index=True)
    X_mip = opt(S_df, O_df, A_df)
    X_mip.to_csv(output_dir + 'X_mip.csv', header=True, index=True)
    X_da_s = da(S_df, O_df, A_df, optimal='s')
    X_da_s.to_csv(output_dir + 'X_da_s.csv', header=True, index=True)
    X_da_o = da(S_df, O_df, A_df, optimal='o')
    X_da_o.to_csv(output_dir + 'X_da_o.csv', header=True, index=True)

if __name__ == '__main__':
    main()
