from mredu.simul import map_red, input_file, run
from re import split


def mymap(_, v):
    words = list(filter(lambda s: s != '', split(r'\W', v)))
    return [(word.lower(), 1) for word in words]


def myred(k, vs):
    return k, len(vs)


if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mymap, myred)
    run(process)
