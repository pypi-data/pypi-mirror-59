# dreamscreen-weather

package supports the HP DreamScreen tablet 'weather' application, providing both a data access layer and a data provider service. 

Requires:
1.  user/developer will need to run a web server on a server (local/remote) to host the data provider service.
2.  change to home router configuration, to override the weatherbug DNS alias, to point to the user's server that is runnign the data provider service.
3.  weatehrunderground API for the data provider service to pull weather data from internet weather underground as the source.



