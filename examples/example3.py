# -*- coding: UTF-8 -*-

from mredu.simul import map_red, input_file, run
import re

stopwords = [u'así', u'para', u'sus', u'una', u'ni', u'porque', u'sin', u'tan', u'al',
             u'si', u'me', u'un', u'más', u'es', u'del', u'lo', u'las', u'le', u'mas',
             u'por', u'su', u'con', u'los', u'se', u'no', u'en', u'el', u'la', u'a', u'y',
             u'de', u'que', u'muy', u'qué', u'como', u'mi', u'o', u'aquel', u'ya',
             u'pues', u'cuando', u'cual', u'pero', u'este', u'esto', u'aquí',
             u'aquella', u'aquello']


def mymap(_, v):
    words = list(filter(lambda s: s != '', re.split(r'\W', v, flags=re.UNICODE)))
    return [(word.lower(), 1) for word in words if word not in stopwords]


def myred(k, vs):
    return k, len(vs)


if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mymap, myred)
    run(process)
