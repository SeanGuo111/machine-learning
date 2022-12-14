import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
keras = tf.keras

#%% Initialization
def initialize_one_hot_encoded_y(x: np.ndarray):
    """Encodes the y values to binary vectors to represent categories."""
    array = np.zeros((x.shape[0], 10))
    for num in range(10):
        for indiv in range(500):
            array[(num*500) + indiv][num] = 1

    return array

def initialize_real_y():
    """Returns the real y values (non-binary). Just an array, not nd-array."""
    array = np.array([])
    for i in range(0, 10):
        array = np.concatenate((array, np.ones(500) * i))
    return array

def generate_data(X, y, real_y, percent_training, percent_validation, percent_testing, num_examples):
    """Generates data off of number of each example."""

    num_training = int(percent_training * num_examples)
    num_validation = int(percent_validation * num_examples)
    num_testing = int(percent_testing * num_examples)

    combined_data:np.ndarray = np.hstack((X, y, real_y))
    np.random.shuffle(combined_data)

    training_X = combined_data[:num_training,:400]
    training_y = combined_data[:num_training,400:410]
    training_real_y = combined_data[:num_training,410].tolist()

    validation_X = combined_data[num_training:num_training + num_validation,:400]
    validation_y = combined_data[num_training:num_training + num_validation,400:410]
    validation_real_y = combined_data[num_training:num_training + num_validation,410].tolist()

    testing_X = combined_data[num_training + num_validation:num_training + num_validation + num_testing,:400]
    testing_y = combined_data[num_training + num_validation:num_training + num_validation + num_testing,400:410]
    testing_real_y = combined_data[num_training + num_validation:num_training + num_validation + num_testing,410].tolist()

    return training_X, training_y, training_real_y, validation_X, validation_y, validation_real_y, testing_X, testing_y, testing_real_y

def graph_cost_accuracy(returned_history, epochs):
    """Graphs the cost and accuracy of the neural network."""
    plt.xlabel("Epoch")
    plt.ylabel("Cost")
    plt.title("Training and Validation Cost vs. Epochs")

    plt.plot(np.arange(epochs), returned_history.history["loss"], label = "Training Cost")
    plt.plot(np.arange(epochs), returned_history.history["val_loss"], label = "Validation Cost")
    plt.plot(np.arange(epochs), returned_history.history["accuracy"], label = "Training Accuracy")
    plt.plot(np.arange(epochs), returned_history.history["val_accuracy"], label = "Validation Accuracy")
    plt.legend()
    plt.show()

#%% Running

# numpy array
X: np.ndarray = np.loadtxt('C:\\Users\\swguo\\VSCode Projects\\Machine Learning\\Neural Networks\\First MNIST ANN\\digitsData.txt', delimiter = ',')
# LOAD DATA
X: np.ndarray = np.loadtxt('C:\\Users\\swguo\\VSCode Projects\\Machine Learning\\Neural Networks\\First MNIST ANN\\digitsData.txt', delimiter = ',')
y = initialize_one_hot_encoded_y(X)
real_y = np.reshape(initialize_real_y(), (-1,1))

# INITIALIZE DATA
percent_training = 0.7
percent_validation = 0.2
percent_testing = 0.1
num_examples = 5000
training_X, training_y, training_real_y, validation_X, validation_y, validation_real_y, testing_X, testing_y, testing_real_y = generate_data(X, y, real_y, percent_training, percent_validation, percent_testing, num_examples)

training_real_y = np.reshape(training_real_y, (-1, 1)) # transposed, 2d
validation_real_y = np.reshape(validation_real_y, (-1, 1)) 
testing_real_y = np.reshape(testing_real_y, (-1, 1)) 

model = keras.Sequential([
  keras.layers.Dense(80, input_shape=(400,), activation="sigmoid"),
  keras.layers.Dense(25, activation="sigmoid"),
  keras.layers.Dense(10, activation="softmax")
])

# Sparse cc uses integer labels, cc uses 1hot-encoded labels
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

epochs = 40
returned_history = model.fit(training_X, training_real_y, validation_data=(validation_X, validation_real_y), epochs=epochs)
test_loss, test_acc = model.evaluate(testing_X, testing_real_y, verbose=1)
print("Test Accuracy: ", test_acc)

graph_cost_accuracy(returned_history, epochs)
