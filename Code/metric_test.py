import numpy as np
import pandas as pd
import pref_metrics

# read in csv files
A = pd.read_csv('A_med.csv',index_col=0)
M = pd.read_csv('M_med.csv',index_col=0)
O = pd.read_csv('O_med.csv',index_col=0)
S = pd.read_csv('S_med.csv',index_col=0)

# exclude 0's
O = O.replace(0, np.NaN)
S = S.replace(0, np.NaN)

# test specialization
print('\n\nTesting Specialization\n')
print(pref_metrics.specialization(O.copy()))

# test correlation
print('\n\nTesting Correlation\n')
print(pref_metrics.correlation(O,S))
print('\nTesting Correlation (cont.)\n')
print(pref_metrics.correlation(O,S,axis=1))
