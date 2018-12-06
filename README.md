# atag-one-collector
Collects data from the ATAG ONE thermostat and writes it to influxdb using a Python script. 

Thanks to https://github.com/kozmoz/atag-one-api for figuring out the protocol.

## Parameters

The following environment variables can be used to configure the collector.

* ATAG_ONE: The hostname or IP of the ATAG One thermostat.
* INTERVAL: The time in seconds between each collection (defaults to 60s if not set).
* INFLUX_HOST: The hostname or IP the InfluxDB instance (defaults to `influxdb`).
* INFLUX_DATABASE: The name of the database to post metrics to in Influx (defaults to `atagone`).

## Sample JSON

```
{
	'measurement': 'atag_one',
 	'time': 1544131195000000000,
	'fields': {
		'boiler_heating': False,
        'boiler_return_temp': 61.2,
        'boiler_temp': 64.5,
        'burning_hours': 216.1,
        'ch_heating': False,
        'ch_mode_temp': 14.0,
        'ch_return_temp': 18.1,
        'ch_setpoint': 0.0,
        'ch_status': 41,
        'ch_water_pres': 1.1,
        'ch_water_temp': 18.1,
        'current': 59,
        'dhw_heating': True,
        'dhw_status': 45,
        'dhw_temp_setp': 52.0,
        'dhw_water_temp': 54.5,
        'max_boiler_temp': 80.0,
        'overshoot': 0.0,
        'power_cons': 4920,
        'rel_mod_level': 0,
        'room_temp': 18.1
    }
 }
```