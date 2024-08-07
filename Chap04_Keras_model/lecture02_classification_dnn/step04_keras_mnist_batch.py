# -*- coding: utf-8 -*-
"""
step04_keras_mnist_batch.py

1. Mnist dataset 다항분류기 
2. Full batch vs Mini batch 
"""

from tensorflow.keras.datasets import mnist # mnist load 
from tensorflow.keras.utils import to_categorical # Y변수 : encoding 
from tensorflow.keras import Sequential # keras model 생성 
from tensorflow.keras.layers import Dense # DNN layer 구축 

################################
## keras 내부 w,b변수 seed 적용 
################################
import tensorflow as tf
import numpy as np 
import random as rd

tf.random.set_seed(123)
np.random.seed(123)
rd.seed(123)


# 1. mnist dataset load 
(x_train, y_train), (x_val, y_val) = mnist.load_data() # (images, labels)

# images : X변수 
x_train.shape # (60000, 28, 28) - (size, h, w) : 2d 제공 
x_val.shape # (10000, 28, 28)

x_train[0] # 0~255
x_train.max() # 255

# labels : y변수 
y_train.shape # (60000,)
y_train[0] # 5


# 2. X,y변수 전처리 

# 1) X변수 : 정규화 & reshape(2d -> 1d)
x_train = x_train / 255. # 정규화 
x_val = x_val / 255.


# reshape(2d -> 1d)
x_train = x_train.reshape(-1, 784) # (60000, 28*28)
x_val = x_val.reshape(-1, 784) # (10000, 28*28)


# 2) y변수 : class(10진수) -> one-hot encoding(2진수)
y_train = to_categorical(y_train)
y_val = to_categorical(y_val)



# 3. keras layer & model 생성
model = Sequential()

x_train.shape # (60000, 784)

input_dim = (784, ) # 1d

# hidden layer1 : w[784, 128]
model.add(Dense(units=128, input_shape=input_dim, activation='relu'))# 1층 

# hidden layer2 : w[128, 64]
model.add(Dense(units=64, activation='relu'))# 2층 

# hidden layer3 : w[64, 32]
model.add(Dense(units=32, activation='relu'))# 3층

# output layer : w[32, 10]
model.add(Dense(units=10, activation='softmax'))# 4층

#  model layer 확인 
model.summary()


# 4. model compile : 학습과정 설정(다항분류기) 
model.compile(optimizer='adam', 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])


# 5. model training : train(70) vs val(30)
model.fit(x=x_train, y=y_train, # 훈련셋 
          epochs=10, # 1epoch : 전체 데이터셋을 1회 소진 -> 600,000장 이미지   
          batch_size=100, # 1회 모델 공급 크기(100*600=60,000) 
          verbose=1, # 출력여부 
          validation_data= (x_val, y_val)) # 검증셋

'''
Epoch 10/10
600/600 [==============================] - 1s 2ms/step 
- loss: 0.0237 - accuracy: 0.9920 - val_loss: 0.0784 - val_accuracy: 0.9785
'''

# 6. model evaluation : val dataset 
print('model evaluation')
model.evaluate(x=x_val, y=y_val) # 10,000장 이미지 




