import re
from toolz.itertoolz import groupby
from itertools import count
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Tuple,
    TypeVar,
    Union,
)
from rich.console import Console

console = Console()

Key = TypeVar("Key")
Value = TypeVar("Value")

# Type definitions for MapReduce components
Pair = Tuple[Key, Value]
MapperResult = Union[Pair, List[Pair]]
ReducerResult = Union[Pair, List[Pair]]
MapperFunction = Callable[[Key, Value], MapperResult]
ReducerFunction = Callable[[Key, List[Value]], ReducerResult]


def __flatten(ls: Iterable[Union[List[Pair], Pair]]) -> Iterable[Pair]:
    """
    Aux function to flatten lists of (k, v) pairs.
    The input can be a mix of (k, v) tuples and lists of (k, v) tuples.
    :param ls: original list
    :return: flattened list of pairs
    """
    for item in ls:
        if isinstance(item, list):
            yield from item
        elif isinstance(item, tuple):
            yield item


def __input_file(path: str) -> Iterable[str]:
    """
    Aux generator function to read text files lazily
    :param path: path of the file to read
    :return: generator that gives us a line each time we call __next__
    """
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def input_file(path: str) -> Iterable[Pair]:
    """
    Read common text file as a stream of (k, v) pairs where k is line number
    and v is line text
    :param path: path to the file to read
    :return: lazy seq of pairs
    """
    return zip(count(), __input_file(path))


def input_kv_file(path: str, sep: str = "\t") -> Iterable[List[str]]:
    """
    Read common text file as a stream of pairs (k, v) where k is the first
    sequence of characters in the line until sep and v is contains the rest of
    characters after removing that first sep.
    :param path: path to the file to read
    :param sep: optional separator to use during k, v pair resolution
    :return: lazy seq of pairs
    """
    return (re.split(sep, line, maxsplit=1) for line in __input_file(path))


def process_mapper(
    in_seq: Iterable[Pair], func: MapperFunction
) -> Iterable[Pair]:
    """
    Simulates mapper function application
    :param in_seq: (k, v) pairs to operate on
    :param func: mapper function to apply f(k, v)
    :return: sequence of transformed (k, v)
    """
    return __flatten(func(k, v) for k, v in in_seq)


def process_shuffle_sort(in_seq: Iterable[Pair]) -> Iterable[Tuple[Key, List[Value]]]:
    """
    Simulates shuffle-sort phase
    :param in_seq: (k, v) pairs from mapper application
    :return: shuffle-sorted (k, [v, v, v...]) pairs to be used for reduce
    """
    # if t[0] is a list needs to be casted as a tuple because lists can't be hash keys in python.
    def get_key(t: Pair) -> Any:
        return tuple(t[0]) if isinstance(t[0], list) else t[0]

    grp = groupby(get_key, in_seq)
    for k, vs in grp.items():
        yield ((k, [v[1] for v in vs]))


def process_reducer(
    in_seq: Iterable[Tuple[Key, List[Value]]], func: ReducerFunction
) -> Iterable[Pair]:
    """
    Simulates mapper function application
    :param in_seq: (k, [v, v, v, ...]) pairs from
    :param func: reducer function to apply f(k, vs)
    :return: sequence of transformed (k, v)
    """
    return __flatten(func(k, vs) for k, vs in in_seq)


def identity_mapper(k: Key, v: Value) -> Pair:
    """
    This is the identity mapper, just lets (k, v) pass to the next phase
    :param k: key
    :param v: value
    :return: (k,v) as a pair
    """
    return k, v


def identity_reducer(k: Key, vs: List[Value]) -> List[Pair]:
    """
    This is the identity reducer, unrolls the values and recreates all the
    (k, v) pairs again.
    :param k: key
    :param vs: list of values
    :return: (k,v) as a pair
    """
    return [(k, v) for v in vs]


def map_red(
    in_seq: Iterable[Pair],
    mapper: MapperFunction = identity_mapper,
    reducer: ReducerFunction = identity_reducer,
) -> Iterable[Pair]:
    """
    Full map_red process definition
    :param in_seq: input (k, v) sequence
    :param mapper: mapper function to apply
    :param reducer: reducer function to apply
    :return: (k, v) resulting sequence
    """
    return process_reducer(
        process_shuffle_sort(process_mapper(in_seq, mapper)), reducer
    )


def run(mp_proc: Iterable[Pair], sep: str = "\t") -> None:
    """
    Lazily executes the mapred process and outputs into the console
    :param mp_proc:
    :param sep: optional k and v separator
    :return:
    """
    try:
        for k, v in mp_proc:
            console.print(f"[green]{k}[/green]{sep}[yellow]{v}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]An error occurred during execution: {e}[/bold red]")
