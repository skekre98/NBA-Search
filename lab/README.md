# Lab Environment

These objects can be used to simplify experimentation related to NBA data.

## GraphBuilder

These are examples of how to use *GraphBuilder*.

#### Line Graph
```python
from lab.graph_builder import GraphBuilder

xlabels = ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5", "Game 6"]
jb_line = [23.0, 25.0, 40.0, 22.0, 35.0, 12.0]
lbj_line = [25.0, 33.0, 25.0, 28.0, 40.0, 28.0]
gb = GraphBuilder(xlabels)
gb.add_line(jb_line, "Jimmy Butler")
gb.add_line(lbj_line, "LeBron James")
gb.build_line_graph()
gb.display()
```

#### Bar Graph
```python
from lab.graph_builder import GraphBuilder

champs = {
    "Boston\nCeltics": 17,
    "Los Angeles\nLakers": 17,
    "Chicago\nBulls": 6,
    "Golden\nState\nWarriors": 6,
    "San\nAntonio\nSpurs": 5
}

gb = GraphBuilder([team for team in champs])
for val in champs.values():
    gb.add_bar(val)

gb.build_bar_graph()
gb.plt.title('NBA Teams with the Most Championships')
gb.display()
```
