from mredu.simul import input_kv_file, map_red, run


def mymap(k, v):
    return v, k


def myred(k, vs):
    return k, len(vs)


if __name__ == '__main__':
    process = map_red(input_kv_file('data/palabras.txt'), mymap, myred)  # type: ignore[arg-type]
    run(process)
