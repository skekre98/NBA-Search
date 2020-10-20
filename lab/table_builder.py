from visualizer import Visualizer

class TableBuilder(Visualizer):

    def __init__(self,  columns_labels,cell_txt):
        super().__init__()
        self.rows = []
        self.column_labels = columns_labels
        self.cell_txt = []

    # This function is to build a table with 
    # the rows and column labels
    def build_table(self):
        # TODO
        try:
            self.plt.table(self.cell_txt,cellLoc='center',colLabels=self.column_labels)
            # pass
        except Exception:
            print('An error occurred while generating the table.')

    #A function to add a list to list of rows
    def add_row(self,row):
        if len(row)!=len(self.column_labels):
            raise  Exception('Number of columns is not exact')
        else:
            self.rows.append(row)
            self.cell_txt.append([f'{cell}' for cell in row])