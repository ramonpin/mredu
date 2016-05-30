# -*- coding: UTF-8 -*-

from mredu import simul

l = [('a', 1), ('b', 2), ('a', 3), ('c', 9), ('b', 6)]

print('Sum all values by key...')
print('-' * 50)
process = simul.map_red(l, reducer=lambda k, v: (k, sum(v)))
simul.run(process, sep=',')

print()
print('Unrolls key by value...')
print('-' * 50)
process = simul.map_red(l, mapper=lambda k, v: [(k, 1) for _ in range(v)])
simul.run(process, sep=',')
