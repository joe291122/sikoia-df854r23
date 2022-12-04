# sikoia-df854r23

## Getting started

To start, the app, simply run:

```
docker-compose up
```

This will spin up a container with the app listening to `localhost:8000`.

To run tests - both unit and integration - do the same but using the test profile. This will start an additional container that runs the unit tests inside that container, and will then run integration tests that call the app running inside the first container:

```
docker-compose --profile test up
```

## Work-ons

### Synchronous vs asynchronous

As we only a maximum of two APIs to call, I have done this in series. To scale further, these should be asynchronous calls.

When building a data platform, instead of a standalone API, depending on how fresh the datasets must be, I would consider a streaming application with a set of microservices to pull data from 3rd parties and update our view of a company/people/etc, which has been cached in a data store. We could also push the our view to a stream which could be consumed directly by 3rd parties.

### Merging datasets & data structures

When we call multiple 3rd party APIs and combining the results, we need a methodology for merging these results together and producing the final output.

In this case, I've taken a simple approach by merging two dicts. I've prioritised any data from 3rd party A over 3rd party B. We should do this data item by data item, e.g. from one source, we only get month of birth rather than date of birth.

### Parameter validation efficiency

There is very basic parameter validation, but this is far from efficient and not extensible at all. A DB/API endpoint should be made available to validate that company numbers/country codes from incoming requests are correct.

### Performance & caching

Response times are typically in the range of 0.1-0.5 seconds. This will not scale very well. 

API requests - both to our APIs, and to 3rd party APIs - should be cached and cached data used if it is still deemed to be "live".

### Logging

There is no logging in this app. We should track requests, when we call 3rd party APIs, and what we return.

### Exception handling

There is no exception handling. Exceptions should be handled, retried and an appropriate response should be returned to the user.

### Authentication & authorisation

This is out of scope so hasn't been considered

### Autoscaling & load balancing

This is a Docker application so can be deployed into any containerisation environment