# PostProcessor
Postprocessing of logfiles from field work.
## LandSurveyor
Processes NMEA  0183 v4.11 GNSS data only, GGA, RMC and GST.

Alpha version code, requires verification and validation.

Creates a CSV file with: 
- date_of_fix in DDMMYY
- gps_time in HH:MM:SS.ss
- dd_longitude_degrees to 8 decimal places
- dd_latitude_degrees to 8 decimal places
- altitude to 3 decimal places 
- sog in m/s
- cmg in degrees
- sigma_latitude
- sigma_longitude
- sigma_altitude

### ToBeDone
- DEVOPS stuff
- Tests
- Documentation
