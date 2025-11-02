from re import split

from mredu.simul import input_file, map_red, run


def mymap(k, v):
    words = list(filter(lambda s: s != '', split(r'\W', v)))
    return len(words), 1


def myred(k, vs):
    return k, sum(vs)


if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mapper=mymap, reducer=myred)
    run(process)
