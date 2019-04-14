import pandas as pd

def anon_dir(file_dir):
    s_filename = file_dir + 'S.csv'
    o_filename = file_dir + 'O.csv'
    a_filename = file_dir + 'A.csv'
    s_df = pd.read_csv(s_filename, index_col=0)
    o_df = pd.read_csv(o_filename, index_col=0)
    a_df = pd.read_csv(a_filename, index_col=0)
    seekers = ['s_{}'.format(i) for i in range(1,len(s_df.columns) + 1)]
    seeker_map = dict(zip(s_df.columns, seekers))
    owners = ['command_{}'.format(i) for i in range(1, len(s_df.index) + 1)]
    owner_map = dict(zip(list(s_df.index),owners))
    a_df.index.name = 'Job'
    a_df.columns = ['Num_Positions']
    s_df.rename(index=owner_map, columns=seeker_map, inplace=True)
    o_df.rename(index=seeker_map, columns=owner_map, inplace=True)
    a_df.rename(index=owner_map, inplace=True)
    s_df.to_csv(s_filename, index=True)
    o_df.to_csv(o_filename, index=True)
    a_df.to_csv(a_filename, index=True)

def main():
    data_dir = 'Data/'
    sources = ['cw', 'eod', 'med']
    subdirs = ['raw', 'complete']
    for source in sources: 
        for subdir in subdirs:
            file_dir = data_dir + '{}/{}/'.format(source, subdir)
            anon_dir(file_dir)

if __name__ == '__main__':
    main()
