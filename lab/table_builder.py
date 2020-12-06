# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lab.visualizer import Visualizer


class TableBuilder(Visualizer):
    def __init__(self, columns_labels):
        super().__init__()
        self.cell_txt = []
        self.rows = []
        self.column_labels = columns_labels

    # This function is to build a table with
    # the rows and column labels
    def build_table(self):
        try:
            self.plt.axis("off")
            self.plt.table(
                self.cell_txt,
                cellLoc="center",
                colLabels=self.column_labels,
                loc="center",
            )
        except Exception:
            print("An error occurred while generating the table.")

    # A function to add a list to list of rows
    def add_row(self, row):
        if len(row) != len(self.column_labels):
            raise ValueError("Number of elements in row does not match header")
        else:
            self.rows.append(row)
            self.cell_txt.append([f"{cell}" for cell in row])
