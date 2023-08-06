# smugapi

a few smug api endpoints that may be useful

# command line

All development related tasks are managed via the `Makefile`.

Managing the app at runtime is handled via the `smugapi` command.

# running the service

```
smugapi run
```

This will run the web service and bind to localhost.


You'll want to pass api keys via either the cmd line or environment variables.


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


