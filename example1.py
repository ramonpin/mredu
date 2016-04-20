from mredu import simul

l = [('a', 1), ('b', 2), ('a', 3), ('c', 9), ('b', 6)]                                

print('Suma de los valores por clave...')
print('-' * 50)
process = simul.map_red(l, reducer=lambda k,v: (k, sum(v))) 
simul.run(process, sep=',')

print()
print('Despliege de la clave por el valor...')
print('-' * 50)
process = simul.map_red(l, mapper=lambda k, v: [(k, 1) for _ in range(v)])
simul.run(process, sep=',')
