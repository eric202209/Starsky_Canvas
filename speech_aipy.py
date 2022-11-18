# -*- coding: utf-8 -*-
"""語音辨識20221030.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y6M-vVix6L2ulpqVW35KGhu7xo75kBVx
"""

# !pip install librosa

# !pip install NumBa -U

# !apt-get install python3.5 #可裝可不裝

from google.colab import drive
drive.mount('/content/drive')

import librosa
import os
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np

# # DATA_PATH = "./data" #原version
DATA_PATH = "/content/drive/MyDrive/團專/語音辨識/wav_for_train/" #尾巴記得加"/"
NPY_PATH = "/content/drive/MyDrive/test/"

#Testing datapath:
# DATA_PATH = "/content/drive/MyDrive/緯育AI課程03期/團專/語音辨識/testing/train/"
# NPY_PATH = "/content/drive/MyDrive/緯育AI課程03期/團專/語音辨識/testing/npy/"


# Input: NPY 資料夾
# Output: Tuple (Label, Indices of the labels, one-hot encoded labels)
#取得資料夾名稱
def get_labels(path=DATA_PATH):
    labels_temp = os.listdir(path)
    labels = []
    npy_labels=[]
    for label in labels_temp:
      if len(label)>=3:
        if (label[-3]+label[-2]+label[-1]) == "npy": #npy檔案
          npy_labels.append(label)
        else:
          labels.append(label)
      else:
        labels.append(label)

    label_indices = np.arange(0, len(labels))
    print("labels: ",labels)
    return labels, label_indices, to_categorical(label_indices)

def get_npys(path=NPY_PATH):
    labels_temp = os.listdir(path)
    npy_labels=[]
    for label in labels_temp:
      if len(label)>=3:
        if (label[-3]+label[-2]+label[-1]) == "npy": #npy檔案
          npy_labels.append(label)
      else:
        print("###There are none npy file in the NPY_PATH###")

    label_indices = np.arange(0, len(npy_labels))
    print("npy_labels:",npy_labels)
    return npy_labels, label_indices, to_categorical(label_indices)
  
def get_npy_count(path=NPY_PATH):
    labels_temp = os.listdir(path)
    npy_labels=[]
    for label in labels_temp:
      if len(label)>=3:
        if (label[-3]+label[-2]+label[-1]) == "npy": #npy檔案
          npy_labels.append(label)
      else:
        print("###There are none npy file in the NPY_PATH###")
    npy_count = len(npy_labels)
    return npy_count


# Handy function to convert wav2mfcc: 主要是長度要一樣
# 輸入語音wav 驗證用
#max_pad_len 這感覺跟音質有關係
#用低音值學習就要用低音質去預測才比較準，高音質學習就用高音質去預測。->口音問題...?
def wav2mfcc(file_path, max_pad_len=50):
    wave, sr = librosa.load(file_path, mono=True, sr=None)
    # print(wave.shape) #(112014,)
    wave = wave[::3] 
    print("wave[::3].shape:",wave.shape) #(37338,) (除3 ??)
    mfcc = librosa.feature.mfcc(wave, sr=16000) #SR 採樣頻率
    print("mfcc.shape in wav2mfcc before padding:",mfcc.shape) #(20 ,73)
    pad_width = max_pad_len - mfcc.shape[1] #11 -73
    # pad_width =  mfcc.shape[1] - max_pad_len  #差距73-11 = 62
    if pad_width <0:
      mfcc = mfcc[:,0:max_pad_len]
      print("mfcc.shape pad_width>11",mfcc.shape)
    else:
      mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    print("mfcc.shape in wav2mfcc after padding:",mfcc.shape) #(20 ,73)
    return mfcc

# save mfcc_vecs to npy
def save_data_to_array(path=DATA_PATH, max_pad_len=50):
    labels, _, _ = get_labels(path)
    # print("label[-4],",labels[0][-4]) # .

    for label in labels:
        # Init mfcc vectors
        mfcc_vectors = []

        wavfiles = [path + label + '/' + wavfile for wavfile in os.listdir(path + label)]
        for wavfile in wavfiles:
            mfcc = wav2mfcc(wavfile, max_pad_len=max_pad_len)
            mfcc_vectors.append(mfcc)
        
        completeName = os.path.join(NPY_PATH, label+".npy") #先存在各自的資料夾試試
        with open(completeName , 'wb') as f:
          np.save(f, mfcc_vectors)
        # print("mfcc_vectors: ",mfcc_vectors)
        # np.save(label[0:-4] + '.npy', mfcc_vectors)
        
        
        
        """
        # Init mfcc vectors
        mfcc_vectors = []

        # wavfiles = [path + label + '/' + wavfile for wavfile in os.listdir(path + '/' + label)] # 原 version
        wavfiles = [path + '/' + label for wavfile in os.listdir(path)] # colab version
        print("wavfiles:", wavfiles) #test

        for wavfile in wavfiles:
            mfcc = wav2mfcc(wavfile, max_pad_len=max_pad_len)
            mfcc_vectors.append(mfcc)
        
        completeName = os.path.join(DATA_PATH, label[0:-4]+".npy")
        with open(completeName , 'wb') as f:
          np.save(f, mfcc_vectors)
        print("mfcc_vectors: ",mfcc_vectors)
        # np.save(label[0:-4] + '.npy', mfcc_vectors)
"""
### 注意路徑,要在NPY資料夾
def get_train_test(split_ratio=0.6, random_state=42):
    # Get available labels
    labels, indices, _ = get_npys()

    # Getting first arrays
    X = np.load(NPY_PATH + labels[0]) ###注意路徑
    y = np.zeros(X.shape[0])
    
    # Append all of the dataset into one single array, same goes for y
    for i, label in enumerate(labels[1:]):
        x = np.load(NPY_PATH + label) ###逐一讀取npy檔案
        X = np.vstack((X, x))     #通通疊加在 X 
        y = np.append(y, np.full(x.shape[0], fill_value= (i + 1)))

    print("X.shape[0]:",X.shape[0])
    print("len(y):",len(y))

    assert X.shape[0] == len(y), "Oh no! This assertion failed!"

    
    return train_test_split(X, y, test_size= (1 - split_ratio), random_state=random_state, shuffle=True)


#trans wavs in dirs to MFCC datasets
def prepare_dataset(path=DATA_PATH):
    labels, _, _ = get_labels(path)
    print("Start prepare datasets: labels:", labels) #test
    data = {}
    for label in labels:
        data[label] = {}
        data[label]['path'] = [path  + label + '/' + wavfile for wavfile in os.listdir(path + label)]

        vectors = []

        for wavfile in data[label]['path']:
            wave, sr = librosa.load(wavfile, mono=True, sr=None)
            # Downsampling
            wave = wave[::3]
            mfcc = librosa.feature.mfcc(wave, sr=16000) #擷取WAV檔案成 MFCC Vectors
            vectors.append(mfcc)

        data[label]['mfcc'] = vectors

    return data

#wavs to MFCC vectors DATA_SET: [wavname1, mfcc_vec1, wavname2, mfcc_vec2...]
def load_dataset(path=DATA_PATH):
    data = prepare_dataset(path)

    dataset = []

    for key in data:
        for mfcc in data[key]['mfcc']:
            dataset.append((key, mfcc))
    print("Wavs for training loaded.")  #test
    return dataset[:100] #dataset = ["dir_name1",array1[....], "dir_name2", array2[....]]


# print(prepare_dataset(DATA_PATH))
# get_train_test()

#訓練自己的語音語音
dataset = load_dataset()
# print("dataset:",dataset)
save_data_to_array()

#SpeechRecognition.py
# 導入函式庫
# from preprocess import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical

#依照訓練的資料如何寫入：原作者用11
max_pad_len=50

# 載入 data 資料夾的訓練資料，並自動分為『訓練組』及『測試組』
X_train, X_test, y_train, y_test = get_train_test()
X_train = X_train.reshape(X_train.shape[0], 20, max_pad_len, 1)
X_test = X_test.reshape(X_test.shape[0], 20, max_pad_len, 1)


# 類別變數轉為one-hot encoding
y_train_hot = to_categorical(y_train)
y_test_hot = to_categorical(y_test)


# 建立簡單的線性執行的模型
model = Sequential()
# 建立卷積層，filter=32,即 output size, Kernal Size: 2x2, activation function 採用 relu
model.add(Conv2D(32, kernel_size=(2, 2), activation='relu', input_shape=(20, max_pad_len, 1)))
# 建立池化層，池化大小=2x2，取最大值
model.add(MaxPooling2D(pool_size=(2, 2)))
# Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例:0.25
model.add(Dropout(0.25))
# Flatten層把多維的輸入一維化，常用在從卷積層到全連接層的過渡。
model.add(Flatten())
# 全連接層: 128個output  
model.add(Dense(256, activation='relu'))                           ####單人50份資料，256效果好像還不錯0.75。7人350份資料，256 512好像都還行
model.add(Dropout(0.25))
# Add output layer
count = get_npy_count()
print("category count: ",count)
model.add(Dense(count, activation='softmax')) #len(npy_labels): npy檔案數
# 編譯: 選擇損失函數、優化方法及成效衡量方式
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# 進行訓練, 訓練過程會存在 train_history 變數中
model.fit(X_train, y_train_hot, batch_size=100, epochs=200, verbose=1, validation_data=(X_test, y_test_hot))


X_train = X_train.reshape(X_train.shape[0], 20, max_pad_len, 1)
X_test = X_test.reshape(X_test.shape[0], 20, max_pad_len, 1)
score = model.evaluate(X_test, y_test_hot, verbose=1)

# 模型存檔
from keras.models import load_model
model.save('ASR.h5')  # creates a HDF5 file 'model.h5'


# # 預測(prediction)
# mfcc = wav2mfcc('./data/happy/012c8314_nohash_0.wav')
# mfcc_reshaped = mfcc.reshape(1, 20, 11, 1)
# print("labels=", get_labels())
# print("predict=", np.argmax(model.predict(mfcc_reshaped)))

#預測
mfcc = wav2mfcc('/content/drive/MyDrive/eraser/e_g66.wav')  #這裡放上自己的語音檔
mfcc_reshaped = mfcc.reshape(1, 20, max_pad_len, 1)
print("labels=", get_npys())
print("predict=", np.argmax(model.predict(mfcc_reshaped)))

#預測
mfcc = wav2mfcc('/content/drive/MyDrive/mark_pen/m_g60.wav')  #這裡放上自己的語音檔
mfcc_reshaped = mfcc.reshape(1, 20, max_pad_len, 1)
print("labels=", get_npys())
print("predict=", np.argmax(model.predict(mfcc_reshaped)))

#預測原檔案(不用管)
mfcc = wav2mfcc('/content/drive/MyDrive/緯育AI課程03期/團專/語音辨識/test_wav/data_bed_012c8314_nohash_0.wav')
mfcc_reshaped = mfcc.reshape(1, 20, , 1)
print("labels=", get_npys())
print("predict=", np.argmax(model.predict(mfcc_reshaped)))

#預測原檔案
mfcc = wav2mfcc('/content/drive/MyDrive/緯育AI課程03期/團專/語音辨識/test_wav/data_cat_05cf43ef_nohash_0.wav')
mfcc_reshaped = mfcc.reshape(1, 20, 11, 1)
print("labels=", get_npys())
print("predict=", np.argmax(model.predict(mfcc_reshaped)))