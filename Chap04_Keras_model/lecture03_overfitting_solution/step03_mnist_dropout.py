# -*- coding: utf-8 -*-
"""
step03_mnist_dropout.py

Dropout : 무작위 네트워크 삭제 -> 과적합 최소화 

형식) model.add(Dropout(rate = 비율))
"""

from tensorflow.keras.datasets.mnist import load_data # MNIST dataset 
from tensorflow.keras.utils import to_categorical # Y변수 : encoding
from tensorflow.keras import Sequential # model 생성
from tensorflow.keras.layers import Dense, Dropout # DNN layer 구축 
import matplotlib.pyplot as plt # images 

import tensorflow as tf
import numpy as np 
import random as rd 

################################
### keras 내부 seed 적용 
################################
tf.random.set_seed(123)
np.random.seed(123)
rd.seed(123)


# 1. mnist dataset laod 
(x_train, y_train), (x_val, y_val) = load_data() # (images, labels)

x_train.shape # (60000, 28, 28) 
y_train.shape # (60000,)



# 2. x,y변수 전처리 

# 1) x변수 : 정규화 & reshape(3d -> 2d)
x_train = x_train / 255.
x_val = x_val / 255.


# 3d -> 2d : [수정]
x_train = x_train.reshape(-1, 784) # 28 * 28 = 784
x_train.shape # (60000, 784)

x_val = x_val.reshape(-1, 784)


# 2) y변수 : one hot encoding 
y_train = to_categorical(y_train) 
y_val = to_categorical(y_val) 



# 3. keras model & layer 구축
model = Sequential()


input_shape = (784,) 

'''
Dropout 적용 전  
model.add(Dropout(rate = 비율))
'''

# hidden layer1 : [784, 128] -> [input, output]
model.add(Dense(units=128, input_shape = input_shape, activation = 'relu')) # 1층 
model.add(Dropout(rate = 0.3)) # 30% 삭제 

# hidden layer2 : [128, 64] -> [input, output]
model.add(Dense(units=64, activation = 'relu')) # 2층 
model.add(Dropout(rate = 0.1)) # 10% 삭제

# hidden layer3 : [64, 32] -> [input, output]
model.add(Dense(units=32, activation = 'relu')) # 3층
model.add(Dropout(rate = 0.1)) # 10% 삭제

# output layer : [32, 10] -> [input, output]
model.add(Dense(units=10, activation = 'softmax')) # 4층 
# output layer에는 Dropout 적용하지 않는다.


# 4. model compile : 학습과정 설정(다항분류기) 
model.compile(optimizer='adam',
              loss = 'categorical_crossentropy',  
              metrics=['accuracy'])


# 5. model training : train(60,000) vs val(10,000)
model_fit = model.fit(x=x_train, y=y_train, # 훈련셋 
          epochs=15, # 반복학습 
          batch_size = 100, # mini batch
          verbose=1, # 출력여부 
          validation_data=(x_val, y_val)) # 검증셋 



# 6. model evaluation : val dataset 
print('='*30)
print('model evaluation')
model.evaluate(x=x_val, y=y_val)
# 적용 전 : 1s 1ms/step - loss: 0.0934 - accuracy: 0.9795
# 적용 후 : 1s 1ms/step - loss: 0.0754 - accuracy: 0.9792

# 7. model history 
print(model_fit.history.keys())


# loss vs val_loss 
plt.plot(model_fit.history['loss'], 'y', label='train loss')
plt.plot(model_fit.history['val_loss'], 'r', label='val loss')
plt.xlabel('epochs')
plt.ylabel('loss value')
plt.legend(loc='best')
plt.show()


# accuracy vs val_accuracy 
plt.plot(model_fit.history['accuracy'], 'y', label='train acc')
plt.plot(model_fit.history['val_accuracy'], 'r', label='val acc')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend(loc='best')
plt.show()

















