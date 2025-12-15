# SuayLang tests

This repo uses Python’s built-in `unittest` (no extra dependencies).

## Run all tests

From the repo root:

```sh
python -m unittest discover -s tests -v
```

## Run a single test module

```sh
python -m unittest -v tests.test_lexer
python -m unittest -v tests.test_parser
python -m unittest -v tests.test_interpreter
```
