'''
문3) digits 데이터셋을 이용하여 다음과 같이 keras 모델을 생성하시오.
  조건1> keras layer
       L1 =  64 x 32
       L2 =  32 x 16
       L3 =  16 x 10
  조건2> output layer 활성함수 : softmax     
  조건3> optimizer = 'adam',
  조건4> loss = 'categorical_crossentropy'
  조건5> metrics = 'accuracy'
  조건6> epochs = 100 
  조건7> model save : keras_model_digits.h5
'''

import tensorflow as tf # ver 2.0
from sklearn.datasets import load_digits # dataset load
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
from tensorflow.keras.utils import to_categorical # y변수 one hot
from tensorflow.keras import Sequential # keras model 
from tensorflow.keras.layers import Dense # model layer
from tensorflow.keras.models import load_model # saved model file -> loading


# 1. digits dataset loading
digits = load_digits()

x_data = digits.data
y_data = digits.target

print(x_data.shape) # (1797, 64) : matrix
print(y_data.shape) # (1797,) : vector

# x_data : 정규화 
x_data = minmax_scale(x_data) # 0~1

# y변수 one-hot-encoding 
y_one_hot = to_categorical(y_data)
y_one_hot
'''
[1., 0., 0., ..., 0., 0., 0.],
'''
y_one_hot.shape # (1797, 10)


# 2. 공급 data 생성 : 훈련용, 검증용 
x_train, x_val, y_train, y_val = train_test_split(
    x_data, y_one_hot, test_size = 0.3)


from tensorflow.keras.layers import Input # input layer
from tensorflow.keras.models import Model # DNN Model 생성


# 3. DNN model layer 구축 (Functional API 방식) 
input_dim = 64 # input data 차원
output_dim = 10 # output data 차원

# 1) input layer
inputs = Input(shape=(input_dim,)) # Input 클래스 이용

# 2) hidden layer1
hidden1 = Dense(units=32, activation='relu')(inputs) # 1층

# 3) hidden layer2
hidden2 = Dense(units=16, activation='relu')(hidden1) # 2층

# 4) output layer
outputs = Dense(units=output_dim, activation ='softmax')(hidden2)# 3층 

# model 생성 
model = Model(inputs, outputs) # Model 클래스 이용

model.summary()
'''
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 64)]              0   -> 입력층       
                                                                 
 dense_6 (Dense)             (None, 32)                2080 -> 은닉층1      
                                                                 
 dense_7 (Dense)             (None, 16)                528  -> 은닉층2      
                                                                 
 dense_8 (Dense)             (None, 10)                170  -> 출력층      
                                                                 
=================================================================
Total params: 2,778
'''


# 4. model compile : 학습과정 설정(다항 분류기)
model.compile(optimizer='adam', 
              loss = 'categorical_crossentropy', 
              metrics=['accuracy'])

# 5. model training : training dataset
model.fit(x=x_train, y=y_train, # 훈련셋 
          epochs=100, # 반복학습 
          verbose=1, # 출력여부 
          validation_data=(x_val, y_val)) # 검증셋

# 6. model evaluation : validation dataset
print('='*30)
print('model evaluation')
model.evaluate(x=x_val, y=y_val)
# - 0s 972us/step - loss: 0.0894 - accuracy: 0.9741

# 7. model save : file save - HDF5 파일 형식 
model.save('keras_model_digits.h5')
print('file saved...')

# model load 
new_model = load_model('keras_model_digits.h5')
new_model.evaluate(x=x_val, y=y_val) 
# - 0s 972us/step - loss: 0.0894 - accuracy: 0.9741







