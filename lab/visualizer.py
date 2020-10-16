import matplotlib.pyplot as plt

class Visualizer(object):

    def __init__(self):
        self.plot = plt

    # Function to clear current figure in plot 
    def clear(self):
        self.plot.clf()

    # Function to display current plot 
    def display():
        self.plot.show()