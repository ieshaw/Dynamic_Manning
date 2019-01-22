import pandas as pd

def comp(df):
    comp_dict = {}
    n_jobs = 10
    n_seekers = len(df)
    for index,row in df.iterrows():
        mu = (row ** 0.5).mean()
        a = 1
        comp_dict[index] =  1 - mu/((a**0.5) * (n_seekers**0.5) * n_jobs)
    return comp_dict

df = pd.DataFrame({'O_1':[1,1,1,1,5]  , 'O_2':[2,2,2,2,1]})
print(comp(df.transpose()))
df = pd.DataFrame({'O_1':[3,3,3,2,1]  , 'O_2':[4,3,4,2,1]})
print(comp(df.transpose()))
