from mredu.simul import map_red, input_file, run
from re import split

stopwords = ['así', 'para', 'sus', 'una', 'ni', 'porque', 'sin', 'tan', 'al',
             'si', 'me', 'un', 'más', 'es', 'del', 'lo', 'las', 'le', 'mas',
             'por', 'su', 'con', 'los', 'se', 'no', 'en', 'el', 'la', 'a', 'y',
             'de', 'que', 'muy', 'qué', 'como', 'mi', 'o', 'aquel', 'ya',
             'pues', 'cuando', 'cual', 'pero', 'este', 'esto', 'aquí',
             'aquella', 'aquello']


def mymap(_, v):
    words = list(filter(lambda s: s != '', split(r'\W', v)))
    return [(word.lower(), 1) for word in words if word not in stopwords]


def myred(k, vs):
    return k, len(vs)


if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mymap, myred)
    run(process)
