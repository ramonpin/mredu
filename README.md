MREDU
=====

A simple simulator of a system which implements map/reduce paradigm similarly to
how Apache Hadoop does.
Its objective is to be used as an educational tool to learn how to code
map/reduce algorithms without needing to install complex components.

Requirements
============
To use it you will need:

  * A Python 3.8+ interpreter.
  * Install required packages from PyPi:

    $> pip install mredu

Examples
========
There are several examples of use of the simulator in the examples directory.

  * example1: Does some calculations from a list of tuples.
  * example2: Calculates the histogram of the number of words per line in the
    file quijote.txt from data folder.
  * example3: The ubiquitous word-count example written to run on the simulator
    and applied to the same quijote.txt file.
  * example4: Inverse k,v -> v,k agrupation

Development
-----------

To contribute to this project, you will need to set up a development environment.

1.  **Clone the repository and create a virtual environment:**

    ```bash
    git clone https://github.com/ramonpin/mredu.git
    cd mredu
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**

    Install the required dependencies, including the ones for development and testing:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the package in editable mode:**

    This will allow you to import the package in your tests and run it as if it were installed, but your local changes will be reflected immediately.

    ```bash
    pip install -e .
    ```

4.  **Run the tests:**

    To make sure everything is working correctly, run the test suite:

    ```bash
    pytest
    ```

Docs
====
`mredu` simulates a MapReduce environment. The process is as follows:

1.  **Input**: You start with an input sequence of `(key, value)` pairs. `mredu` provides helper functions to read data from files into this format.
2.  **Map**: A `mapper` function is applied to each `(key, value)` pair, producing a new sequence of `(key, value)` pairs.
3.  **Shuffle & Sort**: The framework automatically groups the pairs from the map phase by key.
4.  **Reduce**: A `reducer` function is applied to each key and its list of associated values, producing the final result.

### Core Functions

-   `input_file(path)`: Reads a text file line by line, producing a sequence of `(line_number, line_content)` pairs.
-   `input_kv_file(path, sep)`: Reads a text file line by line, splitting each line by `sep` to produce `(key, value)` pairs.
-   `map_red(input_sequence, mapper, reducer)`: Chains together the map, shuffle/sort, and reduce steps. It takes an input sequence and the mapper and reducer functions as arguments.
-   `run(map_red_process)`: Executes the full MapReduce process and prints the resulting `(key, value)` pairs to the console, separated by a tab.

### Example: Word Count

Here is how you would implement the classic word count example using `mredu`.

First, you define your `mapper` function. It takes a key and a value as input (in this case, line number and line text). It splits the line into words, and for each word, it returns a `(word, 1)` pair.

```python
import re

def mymap(_, v):
    words = list(filter(lambda s: s != '', re.split(r'\W', v)))
    return [(word.lower(), 1) for word in words]
```

Next, you define your `reducer` function. It takes a key (a word) and a list of values (a list of 1s) and returns a pair with the word and the sum of the values.

```python
def myred(k, vs):
    return k, len(vs)
```

Finally, you tie it all together. You create an input source from a file, pass it to `map_red` with your mapper and reducer, and then use `run` to execute the process.

```python
from mredu.simul import map_red, input_file, run

# assuming mymap and myred are defined as above

if __name__ == '__main__':
    process = map_red(input_file('data/quijote.txt'), mymap, myred)
    run(process)
```
This will output the word counts to the console.
