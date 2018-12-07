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
    'time': 1544171517000000000,
    'fields': {
        'boiler_errors': '',
        'boiler_heating': True,
        'boiler_return_temp': 55.7,
        'boiler_temp': 59.2,
        'burning_hours': 218.1,
        'ch_control_mode': 0,
        'ch_heating': False,
        'ch_mode': 2,
        'ch_mode_temp': 17.0,
        'ch_return_temp': 17.6,
        'ch_setpoint': 0.0,
        'ch_status': 41,
        'ch_time_to_temp': 0,
        'ch_water_pres': 1.3,
        'ch_water_temp': 17.6,
        'current': 48,
        'dbg_outside_temp': 20.4,
        'device_errors': '',
        'dhw_flow_rate': 0.0,
        'dhw_heating': True,
        'dhw_mode': 1,
        'dhw_mode_temp': 150.0,
        'dhw_status': 45,
        'dhw_temp_setp': 52.0,
        'dhw_water_pres': 0.0,
        'dhw_water_temp': 42.2,
        'max_boiler_temp': 80.0,
        'overshoot': 0.859,
        'pcb_temp': 24.3,
        'power_cons': 120,
        'rel_mod_level': 0,
        'room_temp': 17.6
    }
}

```