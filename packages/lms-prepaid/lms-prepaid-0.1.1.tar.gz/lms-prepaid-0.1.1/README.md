# lms-prepaid

A python script to retrieve balances for last mile solutions electric car charging prepaid card (this includes Entega prepaid cards)

## Installation

`pip install lms-prepaid`

## Development

`lms-prepaid` uses [poetry](https://python-poetry.org/)

## Usage

`lms-prepaid -c AB-123456-X`

See also: `lms-prepaid --help`

### Poetry setup

- Install poetry: `pip install poetry` (see the poetry homepage for alternatives)
- Install `lms-prepaid`: `poetry install`
- Run: `poetry run lms-prepaid --help`


## Environment variables

The script will use the following environment variables:

- `LMS_PREPAID_DATABASE` for the path to the sqlite database
  - defaults to `lms-prepaid.sqlite` int the CWD
- `LMS_PREPAID_CARD` for the card number
- `LMS_PREPAID_GOTIFY_URL` for the gotify notification server
- `LMS_PREPAID_GOTIFY_TOKEN` for the gotify app token
- `LMS_PREPAID_GOTIFY_PRIO` for the gotify notification priority

## Docker usage

- Build the docker image:
  - `docker build -t lms-prepaid .`
- Launch the image with with set environment variables:
  - `docker run -e LMS_PREPAID_CARD=AB-CDE-123456-X lms-prepaid`