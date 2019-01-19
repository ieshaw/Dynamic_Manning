import itertools
import math
import numpy as np
import pandas as pd

def haversine(origin, destination):
    '''
    input origin: tuple of floats, (lat,long)
    input destination: tuple of floast, (lat, long)
    output: float, miles between the two points
    '''
    # Using the Haversine funtion
    # Author: Wayne Dyck
    # https://gist.github.com/rochacbruno/2883505
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    #convert km to miles
    d *= 0.621371
    return d

def base_distance():
    '''
    Output: Pandas DataFrame with columns and index Navy Bases, entries the mile between them
    '''
    nb_df = pd.read_csv('Data/naval_bases.csv',index_col=0)
    base_list = nb_df.index.values
    D_df = pd.DataFrame(data=0,index=nb_df.index, columns=base_list, dtype=float)
    for base_pair in itertools.combinations(base_list,2):
        b_1 = base_pair[0]
        b_2 = base_pair[1]
        dist = haversine((float(nb_df.at[b_1,'Lat']),float(nb_df.at[b_1,'Lon'])),
                        (float(nb_df.at[b_2,'Lat']),float(nb_df.at[b_2,'Lon'])))
        D_df.at[b_1,b_2] = dist
        D_df.at[b_2,b_1] = dist
    return D_df

def main():
    D_df = base_distance()
    D_df.to_csv('Data/D.csv', index=True, header=True)

if __name__ == '__main__':
    main()
