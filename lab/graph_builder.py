from visualizer import Visualizer

class GraphBuilder(Visualizer):

    def __init__(self, xlabels):
        super().__init__()
        self.lines = []
        self.line_labels = []
        self.xlabels = xlabels

    def add_line(self, line, label):
        if len(line) != len(self.xlabels):
            raise ValueError("Length of line was larger than configured x-axis")
        self.lines.append(line)
        self.line_labels.append(label)

    def build_line_graph(self):
        # TODO
        pass