# This is where you should implement the visualization classes / functions
# that will be used display data in the Expert System.

# A simple visualizer is implemented below as an example.
# Please refer to the Code Library located at ES-Shell/Helpers/Code_Library for additional examples.

import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot(self):
        plt.plot(self.data)
        plt.show()

# Example usage (run as "main" to test if the visualizer works as intended for example data):
if __name__ == "__main__":

    data = [1, 2, 3, 4, 5]
    visualizer = Visualizer(data)
    visualizer.plot()