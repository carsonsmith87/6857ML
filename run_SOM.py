import pandas as pd
import numpy as np
from minisom import MiniSom
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import plotly.graph_objects as go
import random
from collections import Counter
import matplotlib.pyplot as plt

from encrypt_data import *

#encryption schemes
caesar_cipher = CaesarCipher()
vernam_cipher = OTP(KEY_LEN)

#generate data
raw_data = get_data()
caesar_data = get_data(caesar_cipher)
vernam_data = get_data(vernam_cipher)

#print("Raw data: \n", raw_data)
#print("Caesar data: \n", caesar_data)
#print("Vernam data: \n", vernam_data)

print(raw_data[:10], len(raw_data))


SPLITLENGTH = 5
MAXWORDS = 1000000

def split(inputText):
    i = 0
    j = i+SPLITLENGTH
    ret = ""
    counter = 0
    while j <= len(inputText) -1:
        counter += 1
        ret += " " + inputText[i:j]
        i += SPLITLENGTH
        j += SPLITLENGTH
    if i != len(inputText):
        counter += 1
        ret += " " + inputText[i:]
    return ret[1:], counter

def getAllText(fullData):
    ret = ""
    for x in fullData:
        ret += " " + x
    return ret[1:]

#print(trainData[:10], len(trainData))

def run_model(trainData):

    trainDataClean = []
    random.shuffle(trainData)
    MAX = 0
    
    for line in trainData:
        cleanTemp, count = split(line)
        trainDataClean.append(cleanTemp)

    print(trainDataClean[:10], len(trainDataClean))
    tokenizer = Tokenizer(MAXWORDS)
    tokenizer.fit_on_texts(trainDataClean)


    seq = tokenizer.texts_to_sequences(trainDataClean)
    wordInd = tokenizer.word_index

    occur = {}
    for x in seq:
        for y in x:
            if y in occur:
                occur[y] += 1
            else:
                occur[y] = 1

    k = Counter(occur)

    # Finding 3 highest values
    high = k.most_common(8)
    print(high)

    highL = [x[0] for x in high]

    seqReal = []
    counter = 0
    for x in seq:
        seqReal.append([])
        for y in x:
            if y in highL:
                seqReal[counter].append(y)
        counter += 1

    for x in seqReal:
        if len(x) > MAX:
            MAX = len(x)
    dataTrain = pad_sequences(seqReal, padding = "post", maxlen = MAX, truncating = "post")


    som = MiniSom(3, 1, MAX, sigma=.98, learning_rate=0.56)

    som.train(dataTrain, 1000000)


    win_map = som.win_map(dataTrain)
    size=som.distance_map().shape[0]
    qualities=np.empty((size,size))
    qualities[:]=np.NaN
    
    for position, values in win_map.items():
        qualities[position[0], position[1]] = np.mean(abs(values-som.get_weights()[position[0], position[1]]))

    layout = go.Layout(title='quality plot')
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Heatmap(z=qualities, colorscale='Viridis'))
    fig.show()

    plt.figure(figsize=(7, 7))
    frequencies = som.activation_response(dataTrain)
    plt.pcolor(frequencies.T, cmap='Blues')
    plt.colorbar()
    plt.show()

    '''
    som_shape = (1, 3)
    winner_coordinates = [[0,0,0],[0,0,0],[0,0,0]]
    for x in dataTrain:
        winningCluster = som.winner(x)[0]
        if wordInd["passw"] in x:
            winner_coordinates[winningCluster][0] += 1
        elif wordInd["usern"] in x:
            winner_coordinates[winningCluster][1] += 1
        else:
            winner_coordinates[winningCluster][2] += 1

    print(winner_coordinates)
    '''

#run_model(raw_data)
#run_model(caesar_data)
#run_model(vernam_data)



    # winner_coordinates = np.array([som.winner(x) for x in dataTrain]).T

# cluster_index = np.ravel_multi_index(winner_coordinates, som_shape)




# for c in np.unique(cluster_index):
#     plt.scatter(dataTrain[cluster_index == c, 0],
#                 dataTrain[cluster_index == c, 1], label='cluster='+str(c), alpha=.7)
#
# # plotting centroids
# for centroid in som.get_weights():
#     plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
#                 s=80, linewidths=3, color='k', label='centroid')
# plt.legend();
# plt.show()
