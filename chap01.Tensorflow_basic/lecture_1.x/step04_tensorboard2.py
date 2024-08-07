# -*- coding: utf-8 -*-
"""
step03_tensorboard2.py

name_scope 이용
 - 영역별 tensorboard 시각화 
"""

import tensorflow.compat.v1 as tf # ver1.x 사용 
tf.disable_v2_behavior() # ver2.x 사용 안함 

# tensorboard 초기화 
tf.reset_default_graph()

''' Graph 모델 정의 '''

# name : [텐서의 이름] 한글, 공백, 특수문자 사용불가 
# 텐서보드에서 확인할 수 있음
X = tf.constant(5.0, name = 'x_data') # 입력변수 
a = tf.constant(10.1, name = 'a') # 기울기 
b = tf.constant(4.45, name = 'b') # 절편 
Y = tf.constant(55.0, name = 'y_data') # 출력(정답)변수 

# name_scope : 한글, 공백, 특수문자 사용불가  
'''
with 구문 : 리소그 관리 문법 
세션을 열고 작업을 수행한 후 자동으로 세션을 닫아줌
'''
with tf.name_scope('regress_model') as scope :
    model = (X * a) + b # 회귀방정식 : 예측치  
    
with tf.name_scope('model_error') as scope :
    model_err = model - Y # err = (예측치-정답)

with tf.name_scope('model_eval') as scope :
    square = tf.square(model_err) # 오차 제곱 
    mse = tf.reduce_mean(square) # 오차 제곱 평균 

''' Graph 모델 실행  '''
with tf.Session() as sess :
    # 각 영역별 실행 결과 
    print('Y = ', sess.run(Y))
    y_pred = sess.run(model)
    print('y pred =', y_pred)
    err = sess.run(model_err)
    print('model error =', err)
    print('MSE = ', sess.run(mse))    
    '''
    오차에 제곱 ? 
    Penalty 효과 : 1보다 작은 값은 더 작게, 1보다 큰 값은 더 크게 
    '''
    
    # tensorboard graph 생성 과정 
    tf.summary.merge_all() # 상수,식 모으는 역할 
    writer = tf.summary.FileWriter("C:/ITWILL/7_Tensorflow/graph", sess.graph)
    writer.close()





