import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess(path_to_stat,path_to_spks):
    stat=np.load(path_to_stat,allow_pickle=True)
    pos=normalize_positions(stat)
    spks=np.load(path_to_spks)
    spks_=normalize_spks(spks)
    return spks_,pos

def normalize_positions(stat):
    N=len(stat)
    print(N)
    ypos = np.array([stat[n]['med'][0] for n in range(len(stat))])
    # (notice the python list comprehension [X(n) for n in range(N)])
    xpos = np.array([stat[n]['med'][1] for n in range(len(stat))])
    scaler_x = MinMaxScaler()
    xpos_scaled=scaler_x.fit_transform(xpos.reshape(-1,1))
    scaler_y=MinMaxScaler()
    ypos_scaled=scaler_y.fit_transform(ypos.reshape(-1,1))

    pos_z=np.ones((N,1))

    pos=np.vstack((xpos_scaled.flatten(),ypos_scaled.flatten(),pos_z.flatten())).T
    return pos

def normalize_spks(spks):
    scaler = MinMaxScaler()
    print('spks shape: ', spks.shape)
    spks_=scaler.fit_transform(spks)
    return spks_
