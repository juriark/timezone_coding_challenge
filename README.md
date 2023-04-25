# Timezone Coding Challenge

## Problem Definition

Create a microservice that has the following endpoint

```
/timezones
** Delivers all available timezones  
/timezones?lat=y&lon=x    
** Deliver timezone for specified coordinate given a geographic latitude/longitude in EPSG:4326 coordinate reference system  
```

As a data source the timezone world shapefile from http://efele.net/maps/tz/world/ should be used.
The endpoint shall return a meaningful timezones for uninhabited zones.

The microservice shall be developed in python and be install/runnable on Ubuntu.
You can use any frameworks/libraries you desire

## Setup

### Prerequisites

- Have `docker compose` installed, see https://docs.docker.com/compose/install/linux/

### Run the service

- From the project's root directory, run `docker compose build`. This will download the postgis base image, and build
  a custom image from the `Dockerfile`.
- To spinup the containers, run `docker compose up`, which will start a docker network running a postgres/postgis
  container and a container hosting the API. This might take some time, because the inital spinup will write the data
  from `./data/world` to the database.
- Once the uvicorn server is available, visit the interactive API documentation at [http://0.0.0.0:8000/docs]()

## Stack

- `poetry`: dependency management of third party libraries
- `fastapi`, `uvicorn`: API development
- `geopandas`: writing vectordata to postgis database
- `sqlalchemy`, `geoalchemy2`: ORM
- `pytest`: unit testing
- `mypy`, `pylint`: type annotations and linting
