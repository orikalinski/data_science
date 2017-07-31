import mincemeat

DATA_FILE = "/home/ori/computer_science/data_science/assignment3/synon_data.txt"

SERVER_PORT = 10001
SERVER_PASSWORD = "pass"


def map_func_phase_one(k, sentence):
    split_sentence = sentence.split()
    for i in xrange(len(split_sentence)):
        yield " ".join(split_sentence[:i] + split_sentence[i + 1:]), split_sentence[i]


def reduce_func_phase_one(k, vs):
    if len(vs) > 1:
        return vs


def map_func_phase_two(k, relevant_words):
    for word in relevant_words:
        yield word, 1


def reduce_func_phase_two(k, vs):
    if sum(vs) > 1:
        return k


def main():
    with open(DATA_FILE, "rb") as f:
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
    results = filter(None, results.values())
    print "%s (%s)" % (" - ".join(results), len(results))

if __name__ == '__main__':
    main()
