# alphanum

Simple Python library to generate pseudo-random alphanumeric strings of
arbitrary length. Requires Python 3.5+.

## Installation

alphanum can be obtained from PyPI with `pip install alphanum`.

Alternatively, build it with [Poetry](https://python-poetry.org/):

```bash
pip install poetry
git clone https://github.com/clpo13/alphanum
cd alphanum
poetry build
pip install dist/alphanum-x.y.z-py3-none-any.whl
```

## Usage

```python
import alphanum

foo = alphanum.generate(10)
print(foo)
```

## License

Copyright (c) 2020 Cody Logan. MIT licensed.
