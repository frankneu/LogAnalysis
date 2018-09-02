#coding=utf-8

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

#批次大小，批次大小过小会导致结果难以收敛，批次大小过大则有可能超出内存限制
batch_size = 128
#分类结果数
num_classes = 10
#训练次数
epochs = 2


#假如训练集有1000个样本，batchsize=10，那么： 训练完整个样本集需要： 100次iteration，1次epoch。具体的计算公式为： one epoch = numbers of iterations = N = 训练样本的数量/batch_size

# input image dimensions
img_rows, img_cols = 28, 28

# the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()


#K是后端引擎，可以为theano（Université de Montréal）／tensorflow(google)／cntk(microsoft)
#K.image_data_format获取图片的维度顺序，（‘channels_last’或‘channels_first’）
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

#label为0~9共10个类别，keras要求格式为binary class matrices
y_train = keras.utils.np_utils.to_categorical(y_train, num_classes)
y_test = keras.utils.np_utils.to_categorical(y_test, num_classes)


#创建model
model = Sequential()
#Conv2D卷积神经网络，二维卷积层，即对图像的空域卷积。该层对二维输入进行滑动窗卷积，当使用该层作为第一层时，应提供input_shape参数。例如input_shape = (128,128,3)代表128*128的彩色RGB图像
#具体参数表可参考此链接 http://keras-cn.readthedocs.io/en/latest/layers/convolutional_layer/
#卷积核的窗口选用3*3像素窗口
model.add(Conv2D(32,(3,3),
                 activation='relu',
                 input_shape=input_shape))
#添加了第二个卷积网络层
model.add(Conv2D(64, (3,3),
                 activation='relu'))
#激活函数可以为linear、sigmoid、hard_sigmoid、tanh、softplus、relu、softplus、softmax
#在keras.layers.advanced_activations下，有新的激活函数LeakyReLU/PReLU/ThresholdedReLU

#池化层对信号进行最大值池化，cnn中Pooling 层则对Filter的特征进行降维操作，形成最终特征
#具体内容可参考此链接  http://keras-cn.readthedocs.io/en/latest/layers/pooling_layer/
model.add(MaxPooling2D(pool_size=(2, 2)))
#dropout是指在深度学习网络的训练过程中将神经网络单元按照一定的概率将其暂时从网络中丢弃。
#注意是暂时，对于随机梯度下降来说由于是随机丢弃，故而每一个mini-batch都在训练不同的网络。
#dropout是CNN中防止过拟合提高效果
model.add(Dropout(0.35))
#把多维输入转换为1维输入,名字很形象,就是把输入给压平了
model.add(Flatten())
#添加全连接层
#Dense层具体参数参考此链接 http://keras-cn.readthedocs.io/en/latest/layers/core_layer/
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
#输出层，得到结果
model.add(Dense(num_classes, activation='softmax'))
#损失函数 http://keras-cn.readthedocs.io/en/latest/other/objectives/
#优化器 http://keras-cn.readthedocs.io/en/latest/other/optimizers/
#性能评估 http://keras-cn.readthedocs.io/en/latest/other/metrics/
model.compile(loss=keras.metrics.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
#对模型进行训练
model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
          verbose=1, validation_data=(x_test, y_test))
#结果评估，model的操作 http://keras-cn.readthedocs.io/en/latest/models/sequential/
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save('mnist_cnn.h5')



