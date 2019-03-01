import os
import json
import os
import pandas as pd
import sys
from da import da
from opt import check_inputs, opt
from post_match import gap_metric, top_perc
from pref_metrics import pref_metrics, correlation

'''
When this script runs, you will point it to a directory with 3 csv's
    
    S.csv, O.csv, A.csv

    S.csv: columns seeker names, rows jobs names,
            entries ordinal preferences of seekers for jobs

    O.csv: columns job names, rows seeker names,
            entries ordinal preferences of jobs for seekers

    A.csv: columns 'Job' and 'Num_Positions', 
            indicating how many positions available at each job

After running this script the input directory will have a sub directory

    results/

In this sub directory there will be several files

    Metrics_s.csv, Metrics_o.csv, Similarity_o.csv, Similarity_s.csv
    Corr_s.csv, Corr_o.csv, X_mip.csv, X_da_s.csv, X_da_o.csv, 
    post_match.csv

    Metrics_s.csv: columns 'Competitiveness' and 'Specialization'
            rows are seeker names

    Metrics_o.csv: columns 'Competitiveness' and 'Specialization'
            rows are job names

    Similarity_s.csv: rows and columns are seeker names
            entries are their similarity, diagonal are 1's

    Similarity_o.csv: rows and columns are job names
            entries are their similarity, diagonal are 1's

    Corr_s.csv: rows are seeker names, values are correlation
            of a seeker's preferences with the preferences expressed
            for them by jobs

    Corr_o.csv: rows are job names, values are correlation
            of a job's preferences with the preferences expressed
            for them by seekers

    X_mip.csv: columns seeker names, rows jobs names,
            assignments by MIP
            1 indicates assinment, 0 otherwise

    X_da_s.csv: columns seeker names, rows jobs names,
            assignments by Deferred Acceptance, seeker optimal
            1 indicates assinment, 0 otherwise

    X_da_o.csv: columns seeker names, rows jobs names,
            assignments by Deferred Acceptance, job optimal
            1 indicates assinment, 0 otherwise

    post_match.csv: rows metrics, columns matching algorithms
            metrics are the gap_mu and top 1/5/10 counts and ratios
            matching algos are mip, da_s, da_o
    '''

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
    x_dict = {'mip': X_mip, 'da_s': X_da_s, 'da_o': X_da_o}
    p_dict = {'s': S_df, 'o': O_df}
    out_dict = {}
    for x in x_dict:
        print('Matching type: {}'.format(x))
        out_dict[x] = {'gap_mu': gap_metric(S_df, O_df, x_dict[x])}
        for p in p_dict:
            out_dict[x].update(top_perc(p_dict[p], p, x_dict[x], A_df))
    out_df = pd.DataFrame.from_dict(out_dict)
    print(out_df)
    out_df.to_csv(output_dir + 'post_match.csv', header=True, index=True)

if __name__ == '__main__':
    main()
