# sikoia-df854r23

# Getting started

To start, the app, simply run:

```
docker-compose up
```

This will spin up a container with the app listening to `localhost:8000`.

To run tests - both unit and integration - do the same but using the test profile. This will start an additional container that runs the unit tests inside that container, and will then run integration tests that call the app running inside the first container:

```
docker-compose --profile test up
```