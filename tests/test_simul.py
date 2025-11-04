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
        (1, 'hello world'),
        (2, 'hello again'),
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
    result = list(simul.__flatten(data))  # type: ignore[arg-type]
    assert result == [('a', 1), ('b', 2), ('c', 3), ('d', 4)]


def test_input_file(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'hello.txt'
    p.write_text('line1\nline2')

    process = simul.input_file(str(p))
    result = list(process)

    assert (0, 'line1') in result
    assert (1, 'line2') in result


def test_input_kv_file(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'hello.txt'
    p.write_text('key1\tvalue1\nkey2\tvalue2')

    process = simul.input_kv_file(str(p))
    result = list(process)

    assert ('key1', 'value1') in result
    assert ('key2', 'value2') in result
    # Verify that result contains tuples, not lists
    assert all(isinstance(item, tuple) for item in result)


def test_run_with_error(capsys):
    def error_generator():
        yield 'a', 1
        raise ValueError('Test error')

    simul.run(error_generator())
    captured = capsys.readouterr()
    assert 'Test error' in captured.out


def test_input_file_not_found():
    """Test FileNotFoundError is raised with clear message"""
    with pytest.raises(FileNotFoundError, match='File not found'):
        list(simul.input_file('nonexistent_file.txt'))


def test_input_file_with_pathlib(tmp_path):
    """Test that Path objects work correctly"""
    p = tmp_path / 'test.txt'
    p.write_text('line1\nline2')

    process = simul.input_file(p)  # Pass Path object
    result = list(process)

    assert (0, 'line1') in result
    assert (1, 'line2') in result


def test_input_kv_file_with_pathlib(tmp_path):
    """Test that Path objects work correctly with input_kv_file"""
    p = tmp_path / 'test_kv.txt'
    p.write_text('key1\tvalue1\nkey2\tvalue2')

    process = simul.input_kv_file(p)
    result = list(process)

    assert ('key1', 'value1') in result
    assert ('key2', 'value2') in result
    # Verify that result contains tuples, not lists
    assert all(isinstance(item, tuple) for item in result)


def test_run_with_file_not_found_error(capsys):
    """Test that FileNotFoundError is caught and displayed"""

    def error_generator():
        yield 'a', 1
        raise FileNotFoundError('test.txt not found')

    simul.run(error_generator())
    captured = capsys.readouterr()
    assert 'File error' in captured.out


def test_run_with_permission_error(capsys):
    """Test that PermissionError is caught and displayed"""

    def error_generator():
        yield 'a', 1
        raise PermissionError('Permission denied')

    simul.run(error_generator())
    captured = capsys.readouterr()
    assert 'Permission error' in captured.out


def test_run_with_value_error_in_run(capsys):
    """Test that ValueError is caught and displayed in run()"""

    def error_generator():
        yield 'a', 1
        raise ValueError('Invalid value')

    simul.run(error_generator())
    captured = capsys.readouterr()
    assert 'Value error' in captured.out


def test_input_kv_file_edge_cases(tmp_path):
    """Test edge cases: lines without separator, empty lines"""
    p = tmp_path / 'edge_cases.txt'
    p.write_text('key1\tvalue1\nkey_without_value\n\nkey2\tvalue2')

    process = simul.input_kv_file(p)
    result = list(process)

    # Lines with separator
    assert ('key1', 'value1') in result
    assert ('key2', 'value2') in result
    # Line without separator should have empty value
    assert ('key_without_value', '') in result
    # Empty lines should be skipped
    assert len(result) == 3
