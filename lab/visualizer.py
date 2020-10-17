import matplotlib.pyplot as plt

class Visualizer(object):

    def __init__(self):
        self.plt = plt

    # Function to clear current figure in plot 
    def clear(self):
        self.plt.clf()

    # Function to display current plot 
    def display(self):
        self.plt.show()