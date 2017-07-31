import mincemeat

DATA_FILE = "/home/ori/computer_science/data_science/assignment3/synon_data.txt"

SERVER_PORT = 10001
SERVER_PASSWORD = "pass"


def map_func_phase_one(k, sentence):
    split_sentence = sentence.split()
    for i in range(len(split_sentence)):
        yield " ".join(split_sentence[:i] + split_sentence[i + 1:]), split_sentence[i]


def reduce_func_phase_one(k, vs):
    if len(vs) > 1:
        return vs


def map_func_phase_two(k, relevant_words):
    for i in range(len(relevant_words)):
        for j in range(i + 1, len(relevant_words)):
            yield "%s - %s" % (relevant_words[i], relevant_words[j]), 1


def reduce_func_phase_two(k, vs):
    sum_vs = sum(vs)
    if sum_vs > 1:
        return sum_vs


def main():
    with open(DATA_FILE, "r") as f:
        data = map(str.strip, f.readlines())
    s = mincemeat.Server()
    s.mapfn = map_func_phase_one
    s.reducefn = reduce_func_phase_one
    s.datasource = dict(enumerate(data))
    results = s.run_server(password=SERVER_PASSWORD, port=SERVER_PORT)
    results = filter(None, results.values())

    s.mapfn = map_func_phase_two
    s.reducefn = reduce_func_phase_two
    s.datasource = dict(enumerate(results))
    results = s.run_server(password=SERVER_PASSWORD, port=SERVER_PORT)
    for key, num_of_ref in results.items():
        if num_of_ref:
            print("%s (%s)" % (key, num_of_ref))

if __name__ == '__main__':
    main()
