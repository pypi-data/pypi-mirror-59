# smugapi

a few smug api endpoints that may be useful

# quickstart

The fastest way to get started is to use the docker image.

```
docker pull threatsimple/smugapi:latest
export SMUG_WEATHERBIT_KEY=YourWeatherKey
export SMUG_WORLDTRADINGDATA_KEY=YourStockQuoteKey
docker run -p 8088 \
    -e SMUG_WEATHERBIT_KEY -e SMUG_WORLDTRADINGDATA_KEY -it \
    threatsimple/smugapi:latest
```

The other option is to use the package in pypi.org.

```
pip3 install smugapi
export SMUG_WEATHERBIT_KEY=YourWeatherKey
export SMUG_WORLDTRADINGDATA_KEY=YourStockQuoteKey
smugapi run
```

Either way, you'll have the api running and listening on localhost, port 8088.

# running the service

There is a command line tool, `smugapi` that allows for easy starting of the api
service.

```
smugapi run
```

This will run the web service and bind to localhost.


This doesn't get you anything useful, though.  You'll want to pass api keys via
either the cmd line or environment variables, as discussed in the endpoints
section below.

# endpoints

## weather

Current weather and forecasts are provided by the very excellent
https://weatherbit.io folks.  They have a free plan that works for most
channels, but if you have a larger volume, they offer a paid option.

To use the weather endpoints, set your api key via either the command line with
the `--weatherbit` option `smugapi run` or via the `SMUG_WEATHERBIT_KEY`
environment variable.

```
export SMUG_WEATHERBIT_KEY=<Your API Key Here>
smugapi run
```

## stock price lookups

Global stock prices can be looked up.  The data is provided by the excellent
folks at worldtradingdata.com.  They have a free account that can provide for
most channels, and a paid option is available for larger demands.

To use the stock price endpoint, set your api key either the command line with
the `--worldtradingdata` option to `smugapi run` or with the
`SMUG_WORLDTRADINGDATA_KEY` environment variable.

```
export SMUG_WORLDTRADINGDATA_KEY=<Your API Key Here>
smugapi run
```

# developing

All development related tasks are managed via the Makefile.

## dev environment

```
make dev
```

This creates a python virtualenv in `pyvenv` and installs the required libs, as
referenced in `reqs.pip`.

This also sets up the current source directory as the `smugapi` module in the
venv for ease of development.

## testing

```
make test
```

Assuming you've run `make dev`, you can use `make test` to run tests. This
will handle the executing the tests in the virtualenv for you, so no need to
handle that in your shell.


