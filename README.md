# MREDU

[![PyPI version](https://badge.fury.io/py/mredu.svg)](https://pypi.org/project/mredu/)
[![Python versions](https://img.shields.io/pypi/pyversions/mredu.svg)](https://pypi.org/project/mredu/)
[![License](https://img.shields.io/github/license/ramonpin/mredu.svg)](https://github.com/ramonpin/mredu/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A simple simulator of a system which implements map/reduce paradigm similarly to
how Apache Hadoop does.
Its objective is to be used as an educational tool to learn how to code
map/reduce algorithms without needing to install complex components.

## Installation

**Requirements**: Python 3.8 or higher.

Install `mredu` from PyPI:

**With pip:**

```bash
pip install mredu
```

**With [uv](https://docs.astral.sh/uv/) (recommended):**

```bash
uv add mredu
```

## Examples

There are several examples of use of the simulator in the examples directory.

* example1: Does some calculations from a list of tuples.
* example2: Calculates the histogram of the number of words per line in the
    file quijote.txt from data folder.
* example3: The ubiquitous word-count example written to run on the simulator
    and applied to the same quijote.txt file.
* example4: Inverse k,v -> v,k agrupation

To run an example with uv:

```bash
uv run python examples/example3.py
```

## Development

To contribute to this project, you will need to set up a development environment.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ramonpin/mredu.git
    cd mredu
    ```

2. **Install uv (if not already installed):**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3. **Install dependencies:**

    Install all dependencies including dev dependencies:

    ```bash
    uv sync
    ```

    This will:
    * Create a virtual environment in `.venv/`
    * Install the package in editable mode
    * Install all runtime and development dependencies
    * Create a `uv.lock` file for reproducible builds

4. **Run the tests:**

    To make sure everything is working correctly, run the test suite:

    ```bash
    uv run pytest
    ```

    To run tests with coverage:

    ```bash
    uv run pytest --cov=mredu
    ```

5. **Setup code quality tools (recommended for contributors):**

    Install pre-commit hooks to automatically check code quality before commits:

    ```bash
    uv run pre-commit install
    ```

    This will run `ruff` (linter + formatter) and `mypy` (type checker) automatically.

    You can also run quality checks manually:

    ```bash
    uv run ruff check .          # Lint code
    uv run ruff format .         # Format code
    uv run mypy mredu/ tests/    # Type check
    ```

    Or use [just](https://github.com/casey/just) for convenience (if installed):

    ```bash
    just check-all    # Run all quality checks
    just test         # Run tests
    just format       # Format code
    ```

    See `justfile` or run `just --list` for all available commands.

6. **Interactive task runner (optional but recommended):**

    For an enhanced developer experience, install [gum](https://github.com/charmbracelet/gum):

    ```bash
    # On macOS
    brew install gum

    # On Linux
    # See https://github.com/charmbracelet/gum#installation
    ```

    With `gum` installed, simply running `just` will present an interactive menu to select and execute tasks. Without `gum`, it will display the standard command list.

## Docs

`mredu` simulates a MapReduce environment. The process is as follows:

1. **Input**: You start with an input sequence of `(key, value)` pairs. `mredu`
   provides helper functions to read data from files into this format.
2. **Map**: A `mapper` function is applied to each `(key, value)` pair,
   producing a new sequence of `(key, value)` pairs.
3. **Shuffle & Sort**: The framework automatically groups the pairs from the
   map phase by key.
4. **Reduce**: A `reducer` function is applied to each key and its list of
   associated values, producing the final result.

### Core Functions

* `input_file(path)`: Reads a text file line by line, producing a sequence of
`(line_number, line_content)` pairs.
* `input_kv_file(path, sep)`: Reads a text file line by line, splitting each
line by `sep` to produce `(key, value)` pairs.
* `map_red(input_sequence, mapper, reducer)`: Chains together the map,
shuffle/sort, and reduce steps. It takes an input sequence and the mapper and
reducer functions as arguments.
* `run(map_red_process)`: Executes the full MapReduce process and prints the
resulting `(key, value)` pairs to the console, separated by a tab.

### Example: Word Count

Here is how you would implement the classic word count example using `mredu`.

First, you define your `mapper` function. It takes a key and a value as input
(in this case, line number and line text). It splits the line into words, and
for each word, it returns a `(word, 1)` pair.

```python
import re

def mymap(_, v):
    words = list(filter(lambda s: s != '', re.split(r'\W', v)))
    return [(word.lower(), 1) for word in words]
```

Next, you define your `reducer` function. It takes a key (a word) and a list of
values (a list of 1s) and returns a pair with the word and the sum of the
values.

```python
def myred(k, vs):
    return k, len(vs)
```

Finally, you tie it all together. You create an input source from a file, pass
it to `map_red` with your mapper and reducer, and then use `run` to execute the
process.

```python
from mredu.simul import map_red, input_file, run

# assuming mymap and myred are defined as above

if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mymap, myred)
    run(process)
```

This will output the word counts to the console.
