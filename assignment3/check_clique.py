DATA_FILE = "/home/ori/computer_science/data_science/assignment3/cliqua_data.txt"


def check_clique():
    with open(DATA_FILE, "rb") as f:
        data = dict([x.strip().split('->') for x in f.readlines()])

    N = len(data)
    for connected_points in data.values():
        if len(connected_points.split()) != N - 1:
            return False
    return True

if __name__ == '__main__':
    print check_clique()
