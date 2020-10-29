import itertools
import numpy as np
from lab.visualizer import Visualizer

class GraphBuilder(Visualizer):

    def __init__(self, xlabels):
        super().__init__()
        
        self.xlabels = xlabels

        # Line Graph 
        self.lines = []
        self.line_labels = []
        self.marker = itertools.cycle(('+', '.', 'o', '*', '1', '2', '3', '4'))

        # Bar Graph 
        self.bar_vals = []

    # Function to add line to current list of lines 
    def add_line(self, line, label):
        if len(line) != len(self.xlabels):
            raise ValueError("Length of line was larger than configured x-axis")
        self.lines.append(line)
        self.line_labels.append(label)

    # Function to plot line graph 
    def build_line_graph(self):
        x = np.arange(1, len(self.xlabels)+1)
        self.plt.xticks(x, self.xlabels)
        for i, line in enumerate(self.lines):
            self.plt.plot(x, line, label=self.line_labels[i], marker=next(self.marker))
        self.plt.legend()
    
    # Function to add bar label/val to list of bars 
    def add_bar(self, val):
        self.bar_vals.append(val)
    
    def build_bar_graph(self):
        self.plt.bar(self.xlabels, self.bar_vals)

