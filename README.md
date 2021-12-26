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

## GUI Example
![image](https://i.imgur.com/s8MhtOM.png)


## UML
![uml](https://i.imgur.com/51xr2pf.png)

## How to Run:
Option 1:
Download the zip, extract the files, open the project and run the main.py class or the tests classes in the tests directory.

Option 2:
Download the zip, extract the files, open terminal / cmd, use the cd command to change directory to src folder for example:
```sh
cd C:\Users\97250\PycharmProjects\Ex3\src
```
now type:
```sh
python main.py
```
> aside from the 3 check functions given, we added a check4 function, to use check4() you can type: "python main.py 20 4",
> this check inits a random graph into the algorithm using our random graph function and run center and isconnected on it. the first argument (20) stands for the amount of nodes in the random graph
> and then second argument (4) stands for the average amount of out edges per node.
```sh
python main.py 20 4
```
