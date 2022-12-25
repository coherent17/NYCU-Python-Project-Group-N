import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

def get_song(val_data, song_names):
    'randomly select a song from a {song_names}'
    index = list(val_data.index.values.astype(int))
    row = np.random.randint(low = 0, high = 858)
    while row not in index:
        row = np.random.randint(low = 0, high = 858)
    
    'get name of one song and get corresponding validtion data'
    name = song_names.loc[row, 'File Name']
    val = val_data.iloc[row:row+1, 1:]
    print(val)
    'assign and load models'
    dt_classifier = DecisionTreeClassifier(random_state=0)
    kn_classifier = KNeighborsClassifier(n_neighbors=3)
    rf_classifier = RandomForestClassifier(random_state=0)
    
    rf_classifier = pickle.load(open('models/random_forest.pkl', 'rb'))
    kn_classifier = pickle.load(open('models/k_neighbours.pkl', 'rb'))
    dt_classifier = pickle.load(open('models/decision_tree.pkl', 'rb'))
    
    'predic the scale based on the input validation'
    rd_pred = rf_classifier.predict(val)[0]
    kn_pred = kn_classifier.predict(val)[0]
    dt_pred = dt_classifier.predict(val)[0]


    if sum([rd_pred, kn_pred, dt_pred]) >= 2:
        scale = 1
    else:
        scale = 0
    
    'return row in the csv files (list.csv and val_data.csv)'
    'return name of the track in .wav format'
    'return scale (major/minor)'
    return row, name, scale