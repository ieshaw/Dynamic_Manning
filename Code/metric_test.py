import numpy as np
import pandas as pd
import pref_metrics as prem
import post_metrics as posm

# read in csv files
A = pd.read_csv('A_med.csv',index_col=0)
M = pd.read_csv('M_med.csv',index_col=0)
O = pd.read_csv('O_med.csv',index_col=0)
S = pd.read_csv('S_med.csv',index_col=0)

# exclude 0's
O = O.replace(0, np.NaN)
S = S.replace(0, np.NaN)

## preference metrics

# test specialization
print('\n\nTesting Specialization\n')
print(prem.specialization(O.copy()))

# test correlation
print('\n\nTesting Correlation\n')
print(prem.correlation(O,S))
#print('\nTesting Correlation (cont.)\n')
#print(prem.correlation(O,S,axis=1))

# test competitiveness
print('\n\nTesting Competitiveness')
print(prem.competitiveness(S))


## post metrics

#