from visualizer import Visualizer

class TableBuilder(Visualizer):

    def __init__(self, rows, columns_labels):
        super().__init__()
        self.rows = rows
        self.column_labels = columns_labels

    # This function is to build a table with 
    # the rows and column labels
    def build_table(self):
        # TODO
        pass