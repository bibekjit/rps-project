# -*- coding: utf-8 -*-
"""rps.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17QP0w6ne9y54f-G7LyaImMZYSjm-xjBZ
"""

# creating a model that will classify images as 'rock','paper' or 'scissors'
# for the game, rock-paper-scissors
# for this, we used the built-in rock-paper-scissor dataset

import tensorflow_datasets as tfds

ds_train=tfds.load('rock_paper_scissors',split='train')
ds_test=tfds.load('rock_paper_scissors',split='test')

# to see eg. 
# tfds.show_examples(tfds.builder('rock_paper_scissors').info,ds_train)

# iterating over the train set and the test set
import numpy as np
train_img=np.array([example['image'].numpy() for example in ds_train])
test_img=np.array([example['image'].numpy() for example in ds_test])

# print(train_img.shape,test_img.shape)

# because we are concerend with edges of the pictures
# we'll only take one color channel 

train_img=np.array([example['image'].numpy()[:,:,0] for example in ds_train])
test_img=np.array([example['image'].numpy()[:,:,0] for example in ds_test])

train_lab=np.array([example['label'].numpy() for example in ds_train])
test_lab=np.array([example['label'].numpy() for example in ds_test])

# print(train_img.shape,test_img.shape)

train_img=np.expand_dims(train_img,-1)
test_img=np.expand_dims(test_img,-1)

# train_img.max()

# the values in the arrays are int values
# as we have to work within the range 0 to 1
# we first convert the int to float and then divide 
# it by the max value, 255

train_img=train_img/255.0
test_img=test_img/255.0

train_img.dtype

train_img[0].shape

import tensorflow
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Flatten,Dense
from tensorflow.keras.layers import Input,GlobalMaxPooling2D,Dropout
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

model=Sequential()
model.add(Input(shape=(300,300,1)))

model.add(MaxPooling2D(3,3))
model.add(Conv2D(32,(5,5),activation='relu'))
model.add(MaxPooling2D(3,3))
model.add(Conv2D(64,(5,5),activation='relu'))
model.add(MaxPooling2D(3,3))
model.add(Conv2D(128,(5,5),activation='relu'))

model.add(Flatten())
model.add(Dense(1024,activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(3,activation='softmax'))

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

data_gen=ImageDataGenerator(width_shift_range=0.1,height_shift_range=0.1,horizontal_flip=True)
train_gen=data_gen.flow(train_img,train_lab,batch_size=32)
model.fit(train_gen,validation_data=(test_img,test_lab),steps_per_epoch=train_img.shape[0]//32,epochs=3)

model.evaluate(test_img,test_lab)

pred=np.argmax(model.predict(test_img),axis=-1)

import seaborn as sb
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# visualising the performace using the heatmap
plt.figure(figsize=(10,6))
sb.heatmap(confusion_matrix(test_lab,pred),annot=True,cmap='Blues')
plt.show()

# miss-classified values
missed=np.where(pred!=test_lab)[0]
i=np.random.choice(missed)
plt.imshow(test_img[i].reshape(300,300),cmap='gray')
plt.title('true - {}, pred - {}'.format(test_lab[i],pred[i]))
plt.show()





