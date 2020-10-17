import itertools
import numpy as np
from lab.visualizer import Visualizer

class GraphBuilder(Visualizer):

    def __init__(self, xlabels):
        super().__init__()
        self.lines = []
        self.line_labels = []
        self.xlabels = xlabels

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
            self.plt.plot(x, line, label=self.line_labels[i])
            print(x)
        self.plt.legend()