# Stroke
While reading about the concept of dropout, I thought about removing weights between layers instead of removing data. So I created a custom Keras layer called "Stroke", which randomizes a set percentage of weights from the previous layer, sort of replicating what happens when a human has a stroke. The goal of the Stroke layer is to re-initialize weights that have begun to contribute to overfitting. 

An implementation of the Stroke layer on an MNIST classification model can be seen below:

```python
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from kerastroke import Stroke

model = Sequential()

model.add(Conv2D(32, 3, 3, input_shape = (28,28, 1), activation = 'relu'))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Conv2D(32,3,3, activation = 'relu'))
model.add(MaxPool2D(pool_size = (2,2)))

model.add(Flatten())

model.add(Dense(output_dim = 128, init = 'uniform', activation = 'relu'))
model.add(Stroke(model.get_layer(index=-1)))
model.add(Dense(10, init = 'uniform', activation = 'sigmoid'))

classifier.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

