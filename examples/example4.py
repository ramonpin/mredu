# -*- coding: UTF-8 -*-

from mredu.simul import map_red, input_kv_file, run
from re import split


def mymap(k, v):
    return v, k


def myred(k, vs):
    return k, len(vs)


if __name__ == '__main__':
    process = map_red(input_kv_file('data/palabras.txt'), mymap, myred)
    run(process)
