# Quantcast Coding Exercise

## To run my code
`$ python3 main.py data/cookie_log.csv -d 2018-12-09`

Note: the logging output of my code can be found in `processor.log`

## To run tests
`$ cd tests/`

`$ pytest test_log_processor.py`

## Prerequisite
Libraries used:
`logging`, `argparse`, `pytest`.

See `requirements.txt`, only `pytest` requires installation


## Project Structure
`main.py`: command line interface

`log_processor/`: contains the core code logic in `log_processor/core.py`

`tests/`: contains unit tests and integration tests

`data/`: contains some sample cookie log csv files
