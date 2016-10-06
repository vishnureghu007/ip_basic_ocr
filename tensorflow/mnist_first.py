import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
#None means dimension can be of any length --when we give input to tensor flow the network should expect a 2d float array 1dim=num of images 784=28*28

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
#weights and bias--initial value is zero this case
#Notice that W has a shape of [784, 10] because we want to multiply the 784-dimensional image vectors by it to produce 10-dimensional vectors of evidence for the difference classes. b has a shape of [10] so we can add it to the output


y = tf.nn.softmax(tf.matmul(x, W) + b)
#model definition

y_ = tf.placeholder(tf.float32, [None, 10])
#cross entropy
#cross-entropy is measuring how inefficient our predictions are for describing the truth

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
#optimization algorithm to modify the variables and reduce the loss
#backpropogation
#In this case, we ask TensorFlow to minimize cross_entropy using the gradient descent algorithm with a learning rate of 0.5

init = tf.initialize_all_variables()
#operation to initialize the variables we created

sess = tf.Session()
sess.run(init)
#launch the model in a Session, and now we run the operation that initializes the variables:


for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
