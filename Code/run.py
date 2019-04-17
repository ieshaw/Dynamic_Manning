import os
import json
import os
import pandas as pd
import sys
from check import check_inputs, X_check 
from da import da
from mip import mip
from post_match import mu_metrics, top_perc

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

    X_mip.csv, X_da_s.csv, X_da_o.csv, post_match.csv

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

def old_main():
    print('Matching MIP')
    X_mip = mip(S_df, O_df, A_df)
    X_check(X_mip, A_df)
    X_mip.to_csv(output_dir + 'X_mip.csv', header=True, index=True)
    print('Matching DA Seeker Optimal')
    X_da_s = da(S_df, O_df, A_df, optimal='s')
    X_check(X_da_s, A_df)
    X_da_s.to_csv(output_dir + 'X_da_s.csv', header=True, index=True)
    print('Matching DA Job Owner Optimal')
    X_da_o = da(S_df, O_df, A_df, optimal='o')
    X_check(X_da_o, A_df)
    X_da_o.to_csv(output_dir + 'X_da_o.csv', header=True, index=True)
    x_dict = {'mip': X_mip, 'da_s': X_da_s, 'da_o': X_da_o}
    p_dict = {'s': S_df, 'o': O_df}
    out_dict = {}
    for x in x_dict:
        print('Matching type: {}'.format(x))
        mu_s, mu_o = mu_metrics(S_df, O_df, x_dict[x])
        out_dict[x] = {'mu_s': mu_s, 'mu_o': mu_o, 'mu_combined': round(mu_s + mu_o,4),'gap_mu': round(mu_s - mu_o,4)}
        for p in p_dict:
            out_dict[x].update(top_perc(p_dict[p], p, x_dict[x], A_df))
    out_df = pd.DataFrame.from_dict(out_dict)
    print(out_df)
    out_df.to_csv(output_dir + 'post_match.csv', header=True, index=True)

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
    A_df = pd.read_csv(data_dir + 'A.csv', index_col=0, names=['Job','Num_Positions'],skiprows=1)
    check_inputs(S_df, O_df, A_df)
    print('Matching DA')
    X_da = da(S_df, O_df, A_df, optimal='s')
    X_check(X_da, A_df)
    X_da.to_csv(output_dir + 'X_da.csv', header=True, index=True)
    tp_dict = top_perc(S_df,'s', X_da ,A_df)
    windows = [1,5,10]
    pref_window_dict = {'s': {}, 'o': {}}
    for window in windows:
        pref_window_dict['s'][str(window)] = tp_dict['{}_s_count'.format(str(window))]
    tp_dict = top_perc(O_df,'o', X_da ,A_df)
    for window in windows:
        pref_window_dict['o'][str(window)] = tp_dict['{}_o_count'.format(str(window))]
    print('Matching MIP')
    X_mip = mip(S_df, O_df, A_df, pref_window_dict, print_to_screen=False)
    X_mip.to_csv(output_dir + 'X_mip.csv', header=True, index=True)
    x_dict = {'mip': X_mip, 'da': X_da}
    p_dict = {'s': S_df, 'o': O_df}
    out_dict = {}
    for x in x_dict:
        print('Matching type: {}'.format(x))
        mu_s, mu_o = mu_metrics(S_df, O_df, x_dict[x])
        out_dict[x] = {'mu_s': mu_s, 'mu_o': mu_o, 'mu_combined': round(mu_s + mu_o,4),'gap_mu': round(mu_s - mu_o,4)}
        for p in p_dict:
            out_dict[x].update(top_perc(p_dict[p], p, x_dict[x], A_df))
    out_df = pd.DataFrame.from_dict(out_dict)
    print(out_df)
    out_df.to_csv(output_dir + 'post_match.csv', header=True, index=True)

if __name__ == '__main__':
    main()
