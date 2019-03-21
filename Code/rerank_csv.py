import pandas as pd
import sys

#filename = input('File to rerank prefs: ')
filename = sys.argv[1]
df = pd.read_csv(filename,index_col=0)
df = df.rank(axis=0,method='first')
df.to_csv(filename,header=True,index=True)
