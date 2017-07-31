from random import uniform
import numpy as np
import matplotlib.pyplot as plt
import mincemeat

DATA_FILE = "/home/ori/computer_science/data_science/assignment3/kmeans_data.txt"
CENTROIDS_FILE = "/home/ori/computer_science/data_science/assignment3/centroids.txt"
K = 5

SERVER_PORT = 10001
SERVER_PASSWORD = "pass"


def generate_centroids(k):
    with open(DATA_FILE, "rb") as f:
        data = [line.strip().split(',') for line in f.readlines()]
    min_x = float(min(data, key=lambda x: x[0])[0])
    min_y = float(min(data, key=lambda x: x[1])[1])
    max_x = float(max(data, key=lambda x: x[0])[0])
    max_y = float(max(data, key=lambda x: x[1])[1])
    centroids = list()
    for i in xrange(k):
        centroids.append((uniform(min_x, max_x), uniform(min_y, max_y)))
    return tuple(centroids)


def map_func(k, (centroids, v)):
    def _euclidean(a, b):
        import math
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    min_centroid = min(centroids, key=lambda x: _euclidean(x, v))
    yield tuple(min_centroid), tuple(v)


def reduce_func(k, vs):
    sum_x, sum_y = 0., 0.
    for v in vs:
        sum_x += v[0]
        sum_y += v[1]
    return sum_x / len(vs), sum_y / len(vs)


def main():
    with open(CENTROIDS_FILE, "wb") as f:
        centroids = generate_centroids(K)
    with open(DATA_FILE, "rb") as f:
        data = [map(float, x.strip().split(',')) for x in f.readlines()]
    s = mincemeat.Server()
    s.mapfn = map_func
    s.reducefn = reduce_func
    old_results = list()
    results = list()
    while not old_results or old_results != results:
        plt.scatter(*np.array(data).T)
        plt.scatter(*np.array(centroids).T, color="g", s=500)
        plt.show()
        old_results = results
        s.datasource = dict(enumerate(zip((centroids, ) * len(data), data)))
        results = s.run_server(password=SERVER_PASSWORD, port=SERVER_PORT)
        centroids = results.values()
        print(results)

if __name__ == '__main__':
    main()

