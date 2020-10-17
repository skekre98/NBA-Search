from visualizer import Visualizer

class TableBuilder(Visualizer):

    def __init__(self, file):
        super().__init__()
        self.csv = file

    # This function is to build a pie chart of the labels
    # in current csv file and load into plot 
    def build_pie(self):
        # TODO
        pass