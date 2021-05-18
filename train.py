import pandas as pd
import numpy as np
from minisom import MiniSom
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import plotly.graph_objects as go
import random
from collections import Counter

SPLITLENGTH = 5
dir = "data/data.csv"
MAX = 0
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
# trainData = pd.read_csv(dir)
#

trainDataClean = []


#dataPassword = pd.read_csv("data/Passwords.csv").sample(n = 500)
#
#trainDataPassword = list(dataPassword["PASSWORD"])
#for x in range(len(trainDataPassword)):
#    trainDataPassword[x] = "PASSWORD" + trainDataPassword[x]
#
#dataUsername = pd.read_csv("data/Usernames.csv").sample(n = 500)
#
#trainDataUsername = list(dataUsername["USERNAME"])
#for x in range(len(trainDataUsername)):
#    trainDataUsername[x] = "USERNAME" + trainDataUsername[x]
#
#
#dataProduct = pd.read_csv("data/Products.csv").sample(n = 500)
#trainDataProduct = list(dataProduct["PRODUCTNUMBER"])
#for x in range(len(trainDataProduct)):
#    trainDataProduct[x] = "PRODUCTNUMBER" + trainDataProduct[x]
#
#trainData = trainDataPassword + trainDataProduct + trainDataUsername

#trainData = list(pd.read_csv("encrypted_data/RawData.csv")["Raw"][0:20,500:520,1000:1020])

#trainData = list(pd.read_csv("encrypted_data/CaesarCipher.csv")["Caesar"])

#trainData = list(pd.read_csv("encrypted_data/VernamCipher7.csv")["Vernam7"])
#
#trainData = list(pd.read_csv("encrypted_data/VernamCipher10.csv")["Vernam10"])

trainData = list(pd.read_csv("encrypted_data/ElGamal.csv")["ElGamal"])

#trainData = list(pd.read_csv("encrypted_data/VernamThenPermute.csv")["VernamThenPermute"])

#trainData = list(pd.read_csv("encrypted_data/PermuteThenVernam.csv")["PermuteThenVernam"])


passKey = trainData[0][0:5].lower()
passKeyEl = [trainData[0][0:5].lower(), trainData[0][5:10].lower()]
passUser = trainData[-1][0:5].lower()
passProduct = trainData[720][0:5].lower()

random.shuffle(trainData)

print(trainData[:10], len(trainData))

for line in trainData:
    cleanTemp, count = split(line)
    trainDataClean.append(cleanTemp)

print(len(trainData))
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

high = k.most_common(45)
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

som.train(dataTrain, 100000)

#
#win_map = som.win_map(dataTrain)
#size=som.distance_map().shape[0]
#qualities=np.empty((size,size))
#qualities[:]=np.NaN
#for position, values in win_map.items():
#    qualities[position[0], position[1]] = np.mean(abs(values-som.get_weights()[position[0], position[1]]))
#
#layout = go.Layout(title='quality plot')
#fig = go.Figure(layout=layout)
#fig.add_trace(go.Heatmap(z=qualities, colorscale='Viridis'))
#fig.show()

import matplotlib.pyplot as plt

plt.figure(figsize=(7, 7))
frequencies = som.activation_response(dataTrain)
plt.pcolor(frequencies.T, cmap='Blues')
plt.colorbar()
plt.show()

som_shape = (1, 3)
winner_coordinates = [[0,0,0],[0,0,0],[0,0,0]]
print(passKey, passUser, passProduct, wordInd[passKey[0]], wordInd[passUser], wordInd[passProduct])
for x in dataTrain:
    winningCluster = som.winner(x)[0]
    if wordInd[passKey] == x[0]: # and  wordInd[passKeyEl[1]] == x[1]:
        winner_coordinates[winningCluster][0] += 1
    elif wordInd[passUser] == x[0]:
        winner_coordinates[winningCluster][1] += 1
    else:
        winner_coordinates[winningCluster][2] += 1

print(winner_coordinates)


winner_coordinates_pic = np.array([som.winner(x) for x in dataTrain]).T
# with np.ravel_multi_index we convert the bidimensional
# coordinates to a monodimensional index
cluster_index = np.ravel_multi_index(winner_coordinates_pic, (3,1))

# plotting the clusters using the first 2 dimentions of the data
for c in np.unique(cluster_index):
    plt.scatter(dataTrain[cluster_index == c, 0],
                dataTrain[cluster_index == c, 8], label='cluster='+str(c), alpha=.7)

# plotting centroids
for centroid in som.get_weights():
    plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
                s=80, linewidths=3, color='k', label='centroid')
plt.legend();
plt.show()

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
