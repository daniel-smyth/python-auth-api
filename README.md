# FastAPI with Authentication

[![E2E tests](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovatebot.com/)

### Python 3 | FastAPI | MongoDB | Pytest

| Library  | Website                           |
| -------- | --------------------------------- |
| Python 3 | https://docs.python.org/3/        |
| FastAPI  | https://fastapi.tiangolo.com/     |
| MongoDB  | https://www.mongodb.com/          |
| Pytest   | https://docs.pytest.org/en/7.2.x/ |

FastAPI template with authentication implemented in MongoDB. Pytest included for all routes. Utility folder with modules for AWS file management, local file managment, lists and MongoDB.

### Installation

> Note: `DB_URL`, `DB_NAME` (and more) are required in `.env` to run locally. See `.sample.env`.

Create a virtual enviroment.

```sh
python -m venv env
```

Install dependencies found in `requirements.txt`.

```sh
pip install -r requirements.txt
```

Start the server in development mode http://locahost:8888.

```sh
python main.py
```

[//]: # "These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen."
[python]: https://www.python.org/downloads
[time series api]: https://tigerspider.atlassian.net/wiki/spaces/~628119259/pages/2292318263/Tiger+Spider+Time+Series+API
[time series documents]: https://timeseries-api.azurewebsites.net/api/docs
