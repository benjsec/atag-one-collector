# atag-one-collector
Collects data from the ATAG ONE thermostat and writes it to influxdb using a Python script. 

Thanks to https://github.com/kozmoz/atag-one-api for figuring out the protocol.

## Parameters

The following environment variables can be used to configure the collector.

* ATAG_ONE: The hostname or IP of the ATAG One thermostat.
* INTERVAL: The time in seconds between each collection (defaults to 60s if not set).
* INFLUX_HOST: The hostname or IP the InfluxDB instance (defaults to `influxdb`).
* INFLUX_DATABASE: The name of the database to post metrics to in Influx (defaults to `atagone`).
