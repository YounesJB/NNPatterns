#!/usr/bin/env python3.7
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
get_directory_layers_from_csv("iris_8_10_8_.csv")

# X contient les valeurs réelles, X_1_0 contient les valeurs réelles X cryptées en 0 et 1
X,X_1_0,y = readXy("iris_8_10_8_/iris_l1_8_l2_10_l3_8_.csv",True)
X_1 = [X_1_0[i] for i in range(len(X_1_0)) if y[i]==1]
X_0 = [X_1_0[i] for i in range(len(X_1_0)) if y[i]==0]
#print("X_0 : \n",X_0)
#print("\nX_1 :\n",X_1)
#enc_val_sig = encrypting_value_signature(X_1_0)
enc_sig_val = encrypting_signature_value(X_1_0)
#print("encrypting X_1_0 into a dict value:signature : (enc_val_sig)\n", enc_val_sig,"\n\nencrypting X_1_0 into a dict signature:value : (enc_sig_val)\n", enc_sig_val)

#switching_sig_val_to_val_sig = switchs_keys_values(enc_sig_val)
#print("\nswitching vals and signatures of enc_sig_val:\n", switching_sig_val_to_val_sig)

encrypting_X_0 = X_to_encrypted_X(X_0,enc_sig_val)
encrypting_X_1 = X_to_encrypted_X(X_1,enc_sig_val)
print("\nencrypting X_0 :\n", encrypting_X_0,"\nencrypting X_1 : \n", encrypting_X_1)

Histogram(encrypting_X_1,"X1cr.png")
Histogram(encrypting_X_0,"X0cr.png")

#Histogram(X_1,"X1.png")
#Histogram(X_0,"X0.png")
## exemple d’utilisation 
df=discretise_dataset('iris_8_10_8_/iris_l1_8_l2_10_l3_8_.csv',8)
df.to_csv("iris_8_10_8_/iris_l1_8_l2_10_l3_8_disc.csv", sep=',', encoding='utf-8',index=False)
# df is a pandas_core_frame_DataFrame 

df_X,df_y = pandas_core_frame_DataFrame_to_list(df)
print("\nfile's data into lists of X :\n", df_X, "\nand into lists of y :\n" , df_y)

bins = [2,4,6,8,10]
hists_files("iris_8_10_8_/iris_l1_8_l2_10_l3_8_.csv",bins)