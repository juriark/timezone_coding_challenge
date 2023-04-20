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

## Documentation
### Stack
- `poetry`: dependency management of third party libraries

### Notes
The shapefile does not contain neither territorial seas nor oceans - clarify if these shall be reconstructed or not.

Both the database as well as the API are containerized together. For scalability it might make sense to build separate
containers that can easily be deployed separately. I will refrain from doing it here though, because I don't know if the
`docker compose` plugin is installed on the Ubuntu machine this code will run on.


## Keep in mind:
- write tests
- do linting, use types


## Questions
- The shapefile does not contain neither territorial seas nor oceans. Shall these be constructed? If yes, how shall they be reconstructed (e.g. longitude)