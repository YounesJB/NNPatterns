#!/usr/bin/env python3.7

import numpy as np
import pandas as pd 
import keras
import os
import re
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn import preprocessing, model_selection
from sklearn.datasets import make_moons
from sklearn.datasets import make_circles
from sklearn import datasets
from tensorflow.keras.datasets import mnist

## Renvoyer les données prédits correctement
def get_goodXy(X,y):
    ynew = model.predict_classes(X)
    X_good =[]
    y_good=[]
    for i in range(len(X)):
        if (ynew[i]==0 and y[i]==1) or (ynew[i]==1 and y[i]==0):
            print ("error prediction for X=%s, Predicted=%s, Real=%s"% (X[i], ynew[i], y[i]))
        else :
            X_good.append(X[i])
            y_good.append(y[i])
    return X_good,y_good 

## Renvoyer les sorties de chaque layer
def get_result_layers(model,X):
    result_layers=[]
    for i in range (len(model.layers)-1):
        hidden_layers= keras.backend.function(
                [model.layers[0].input],   
                [model.layers[i].output] 
                )
        result_layers.append(hidden_layers(np.array(X))[0])  
    return result_layers

## Enregistrer le resultat dans un seul fichier
def save_result_layers(filename,X,y,result_layers):
    f = open(filename, "w")
    for nb_X in range (len(X)):
        #my_string=""
        my_string=str(y[nb_X])+','
        for nb_layers in range (len(model.layers)-1):
            my_string+="<b>,"
            for j in range (len(result_layers[nb_layers][nb_X])):
                my_string+=str(result_layers[nb_layers][nb_X][j])+','
            my_string+="</b>,"    
        my_string=my_string [0:-1]
        my_string+='\n'
        f.write(my_string)    
    f.close()

url="https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['SepalLengthCm', 'SepalWidthCm', 
         'PetalLengthCm', 'PetalWidthCm', 
         'Species']

data = pd.read_csv(url, names=names)
#Classification binaire sur Virginica et Setosa seulement

data=data[data['Species'].isin(['Iris-virginica', 'Iris-setosa'])]

i = 8
data_to_predict = data[:i].reset_index(drop = True)
predict_species = data_to_predict.Species 
predict_species = np.array(predict_species)
prediction = np.array(data_to_predict.drop(['Species'],axis= 1))
data = data[i:].reset_index(drop = True)

X = data.drop(['Species'], axis = 1)
X = np.array(X)
y = data['Species']
encoder = LabelEncoder()
y=encoder.fit_transform(y)
train_X, test_X, train_y, test_y = model_selection.train_test_split(X,y,test_size = 0.1, random_state = 0)
# Utilisation de keras comme classifieur
# mettre sigmoid comme fonction car binaire. Attention 1 seul neurone en sortie
input_dim = len(data.columns) - 1
model = Sequential()
model.add(Dense(8, input_dim = input_dim , activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(8, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'] )

model.fit(train_X, train_y, epochs = 10, batch_size = 2)

scores = model.evaluate(test_X, test_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
# Récupération seulement des bons classés
X_good,y_good=get_goodXy (train_X, train_y)
# Récupération des valeurs de tous les layers sauf le dernier
result_layers=get_result_layers(model,X_good)
# Sauvegarde du fichier
# structure :
# 0/1 = valeur de la classe
# chaque valeur de layer est entourée par un []
save_result_layers("iris_8_10_8_tmp",X_good,y_good,result_layers)
# tri du fichier
os.system ('sort iris_8_10_8_tmp > iris_8_10_8_.csv')
# effacer le fichier intermédiaire
os.system ('rm iris_8_10_8_tmp')
X, y = make_moons(n_samples=1000, noise=0.05, random_state=0)

validation_size=0.6 #40% du jeu de données pour le test

testsize= 1-validation_size
seed=30
# séparation jeu d'apprentissage et jeu de test
train_X, test_X, train_y, test_y=model_selection.train_test_split(X, 
                                               y, 
                                               train_size=validation_size, 
                                               random_state=seed,
                                               test_size=testsize)

# Utilisation de keras comme classifieur
# mettre sigmoid comme fonction car binaire. Attention 1 seul neurone en sortie
input_dim = 2

model = Sequential()
model.add(Dense(3, input_dim = input_dim , activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(3, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'] )

model.fit(train_X, train_y, epochs = 40, batch_size = 64)

scores = model.evaluate(test_X, test_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
# Récupération seulement des bons classés
X_good,y_good=get_goodXy (train_X, train_y)
# Récupération des valeurs de tous les layers sauf le dernier
result_layers=get_result_layers(model,X_good)

# Sauvegarde du fichier
# structure :
# 0/1 = valeur de la classe
# chaque valeur de layer est entourée par une étoile *
save_result_layers("makemoons_3_10_10_3_tmp",X_good,y_good,result_layers)
# tri du fichier
os.system ('sort makemoons_3_10_10_3_tmp > makemoons_3_10_10_3_.csv')
# effacer le fichier intermédiaire
os.system ('rm makemoons_3_10_10_3_tmp')

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train_sample=X_train[0:100]
y_train_sample=y_train[0:100]

X_train=X_train_sample
y_train=y_train_sample
X_train = X_train.reshape(100, 784)
X_train = X_train.astype('float32')
X_train /= 255


X_01=[]
y_01=[]
nb_X=0
for i in range(X_train.shape[0]):
    if (y_train[i]==0 or y_train[i]==1):
        
        nb_X+=1
        X_01.append(X_train[i])
        y_01.append(y_train[i])

       
train_X=np.asarray(X_01)

train_y=y_01

encoder = LabelEncoder()
train_y=encoder.fit_transform(train_y)

input_dim = 784

model = Sequential()
model.add(Dense(512, input_dim = input_dim , activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'] )

model.fit(train_X, train_y, epochs = 40, batch_size = 32)

X_good,y_good=get_goodXy (train_X, train_y)

# Récupération des valeurs de tous les layers sauf le dernier
result_layers=get_result_layers(model,X_good)

# Sauvegarde du fichier
# structure :
# 0/1 = valeur de la classe
# chaque valeur de layer est entourée par une étoile *
save_result_layers("mnist_512_tmp",X_good,y_good,result_layers)
# tri du fichier
os.system ('sort mnist_512_tmp > mnist_512_.csv')
# effacer le fichier intermédiaire
os.system ('rm mnist_512_tmp')

def get_directory_layers_from_csv(filename):
    tokens=filename.split("_")
    df = pd.read_csv(filename, sep = ',', header = None) 
    
    # creation d'un répertoire pour sauver tous les fichiers
    repertoire=filename[0:-4]
    os.makedirs(repertoire, exist_ok=True)
    string = repertoire+'/'+tokens[0]+'_'
    f=[]
    filenames=[]
    for nb_tokens in range (1,len(tokens)-1):
        name_file=string+'l'+str(nb_tokens)+'_'+tokens[nb_tokens]+'.csv'
        f.append(open(name_file, "w"))
        filenames.append(name_file)
        
        
    # sauvegarde du dataframe dans une chaîne de caracteres
    ch = df.to_string(header=False,
                  index=False,
                  index_names=False).split('\n')
    vals = [','.join(ele.split()) for ele in ch]
    
    # sauvegarde dans des fichiers spécifiques par layer
    token_layer=[]
    token_exemples=[]
    for nb_exemples in range (len(vals)):
        deb=str(df[0][nb_exemples])+','
        # 1 ligne correspond à une chaine
        s=vals[nb_exemples]
        listoftokens=re.findall(r'<b>,(.+?),</b>', s)
        nb_layers=len(listoftokens)
        
        for nb_token in range (nb_layers):
            save_token=''
            save_token=deb+str(listoftokens[nb_token])+'\n'
            
            f[nb_token].write(save_token)

#Create a directory with a specific file for all the layers
filename="iris_8_10_8_.csv"    
get_directory_layers_from_csv(filename)    

filename='makemoons_3_10_10_3_.csv'
get_directory_layers_from_csv(filename) 

filename='mnist_512_.csv'
get_directory_layers_from_csv(filename) 
