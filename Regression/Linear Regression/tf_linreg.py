import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Generating random linear data
# There will be 50 data points ranging from 0 to 50
x = np.linspace(0, 50, 50)
y = np.linspace(0, 50, 50)
 
# Adding noise to the random linear data
x += np.random.uniform(-4, 4, 50)
y += np.random.uniform(-4, 4, 50)
 
n = len(x) # Number of data points
optimizer = tf.train.GradientDescentOptimizer()
tf.add()
tf.trai


# Plot of Training Data
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title("Training Data")
plt.show()