import pytest
from mredu import simul


def test_identity_map_red():
    data = [('a', 1), ('b', 2), ('a', 3)]
    process = simul.map_red(data)
    result = list(process)
    # The identity map_red should return the same pairs, though possibly in a different order
    assert set(result) == set(data)


def test_word_count():
    data = [
        (1, "hello world"),
        (2, "hello again"),
    ]

    def mymap(_, v):
        words = v.split()
        return [(word, 1) for word in words]

    def myred(k, vs):
        return k, sum(vs)

    process = simul.map_red(data, mymap, myred)
    result = dict(process)

    assert result['hello'] == 2
    assert result['world'] == 1
    assert result['again'] == 1


def test_flatten():
    data = [[('a', 1)], ('b', 2), [('c', 3), ('d', 4)]]
    result = list(simul.__flatten(data))
    assert result == [('a', 1), ('b', 2), ('c', 3), ('d', 4)]


def test_input_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("line1\nline2")

    process = simul.input_file(str(p))
    result = list(process)

    assert (0, "line1") in result
    assert (1, "line2") in result

def test_input_kv_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("key1\tvalue1\nkey2\tvalue2")

    process = simul.input_kv_file(str(p))
    result = list(process)

    assert ['key1', 'value1'] in result
    assert ['key2', 'value2'] in result


def test_run_with_error(capsys):
    def error_generator():
        yield "a", 1
        raise ValueError("Test error")

    simul.run(error_generator())
    captured = capsys.readouterr()
    assert "Test error" in captured.out
