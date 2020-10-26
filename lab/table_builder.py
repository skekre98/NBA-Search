from lab.visualizer import Visualizer

class TableBuilder(Visualizer):

    def __init__(self,  columns_labels):
        super().__init__()
        self.cell_txt = []
        self.rows = []
        self.column_labels = columns_labels

    # This function is to build a table with 
    # the rows and column labels
    def build_table(self):
        try:
            self.plt.axis('off')
            self.plt.table(self.cell_txt,cellLoc='center',colLabels=self.column_labels,loc='center')
        except Exception:
            print('An error occurred while generating the table.')

    #A function to add a list to list of rows
    def add_row(self,row):
        if len(row)!=len(self.column_labels):
            raise ValueError('Number of elements in row does not match header')
        else:
            self.rows.append(row)
            self.cell_txt.append([f'{cell}' for cell in row])
