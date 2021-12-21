from DiGraph import *
from GraphAlgo import GraphAlgo

if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json('../data/A4.json')
    print(algo.centerPoint())
    algo.save_to_json("234234")