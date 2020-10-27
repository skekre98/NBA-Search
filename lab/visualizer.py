from datetime import datetime
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
    
    # Function to save plt to file 
    def save(self, file="figure"):
        if file != "figure":
            name = "{}.png".format(file)
        else:
            T = datetime.now().strftime('%H:%M:%S')
            name = "{}-{}.png".format(file, T)
        self.plt.savefig(name)
        print("Image successfully saved as PNG")