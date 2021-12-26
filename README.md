# Ex3-OOP - DirectedWeightedGraphs
#### Authors: Lior Shacohach & Moriya Barel

In this project we were required to implement directed weighted graph, graphic representation of the graph as well as various applicable algorithms.

## Graph Implementation

We represent the graph using a dictionary, the keys of the dictionary are the vertice's id and the values are the vertices themselfs, each vertice v holds two dictionaries with a tweak, each dictionary contains edges corresponding to the vertices adjacent to v, the keys of the adjancency dictionary are integers representing the destination's node id of the edge and the values are the weights of the edge. For example:

| Class | Description |
| ------ | ------ |
| mynode | Represents the graphs vertices |
| DiGraph | Represents the Directed Weighted Graph |
| GraphAlgo | Holds a DiGraph to run desired algorithms on |

GUI Example:
![image](https://i.imgur.com/s8MhtOM.png)
