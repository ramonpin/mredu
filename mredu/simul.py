import re
import codecs
from toolz.itertoolz import groupby
from itertools import count


def __flatten(ls):
    """
    Aux function to flatten lists and remove None from result (k, v) sequences
    :param ls: original list
    :return: flattened list
    """
    for e in ls:
        if type(e) is list:
            for i in e:
                yield i
        elif type(e) is tuple:
            yield e


def __input_file(path):
    """
    Aux generator function to read text files lazily
    :param path: path of the file to read
    :return: generator that gives us a line each time we call __next__
    """
    f = codecs.open(path, encoding='utf-8')
    for line in f:
        yield line.strip()
    f.close()


def input_file(path):
    """
    Read common text file as a stream of (k, v) pairs where k is line number
    and v is line text
    :param path: path to the file to read
    :return: lazy seq of pairs
    """
    return zip(count(), __input_file(path))


def input_kv_file(path, sep="\t"):
    """
    Read common text file as a stream of pairs (k, v) where k is the first
    sequence of characters in the line until sep and v is contains the rest of
    characters after removing that first sep.
    :param path: path to the file to read
    :param sep: optional separator to use during k, v pair resolution
    :return: lazy seq of pairs
    """
    return map(lambda line: re.split(sep, line, maxsplit=1, flags=re.UNICODE),
               __input_file(path))


def process_mapper(in_seq, func):
    """
    Simulates mapper function application
    :param in_seq: (k, v) pairs to operate on
    :param func: mapper function to apply f(k, v)
    :return: sequence of transformed (k, v)
    """
    return __flatten(
        map(lambda t: func(t[0], t[1]), in_seq))


def process_shuffle_sort(in_seq):
    """
    Simulates shuffle-sort phase
    :param in_seq: (k, v) pairs from mapper application
    :return: shuffle-sorted (k, [v, v, v...]) pairs to be used for reduce
    """
    grp = groupby(lambda t: t[0], in_seq)
    for k, vs in grp.items():
        yield((k, [v[1] for v in vs]))


def process_reducer(in_seq, func):
    """
    Simulates mapper function application
    :param in_seq: (k, [v, v, v, ...]) pairs from
    :param func: reducer function to apply f(k, vs)
    :return: sequence of transformed (k, v)
    """
    return __flatten(
        map(lambda t: func(t[0], t[1]), in_seq))


def identity_mapper(k, v):
    """
    This is the identity mapper, just lets (k, v) pass to the next phase
    :param k: key
    :param v: value
    :return: (k,v) as a pair
    """
    return k, v


def identity_reducer(k, vs):
    """
    This is the identity reducer, unrolls the values and recreates all the
    (k, v) pairs again.
    :param k: key
    :param vs: list of values
    :return: (k,v) as a pair
    """
    return [(k, v) for v in vs]


def map_red(in_seq, mapper=identity_mapper, reducer=identity_reducer):
    """
    Full map_red process definition
    :param in_seq: input (k, v) sequence
    :param mapper: mapper function to apply
    :param reducer: reducer function to apply
    :return: (k, v) resulting sequence
    """
    return process_reducer(
        process_shuffle_sort(process_mapper(in_seq, mapper)),
        reducer)


def run(mp_proc, sep="\t"):
    """
    Lazily executes the mapred process and outputs into the console
    :param mp_proc:
    :param sep: optional k and v separator
    :return:
    """
    for k, v in mp_proc:
        print('%s%s%s' % (k, sep, v))
