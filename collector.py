"""Collect stats from an ATAG One thermostat and post to InfluxDB."""
import json
import os
import pytz
import time
from datetime import timedelta, datetime
from urllib import request

from influxdb import InfluxDBClient

ATAG_ONE = os.environ['ATAG_ONE']
INTERVAL = int(os.environ.get('INTERVAL', 60))
INFLUX_HOST = os.environ.get('INFLUXDB', 'influxdb')
INFLUX_DATABASE = os.environ.get('INFLUX_DATABASE', 'atagone')

# from https://github.com/kozmoz/atag-one-api/
MESSAGE_INFO_CONTROL = 1
MESSAGE_INFO_SCHEDULES = 2
MESSAGE_INFO_CONFIGURATION = 4
MESSAGE_INFO_REPORT = 8
MESSAGE_INFO_STATUS = 16
MESSAGE_INFO_WIFISCAN = 32
MESSAGE_INFO_EXTRA = 64


def atag_time_to_datetime(atag_time):
    base = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    return base + timedelta(seconds=atag_time)


def atag_request_data():
    data = json.dumps({
        'retrieve_message': {
            'seqnr': 0,
            'account_auth': {
                'user_account': "",
                'mac_address': "01:23:45:67:89:01"
            },
            'info': (MESSAGE_INFO_CONTROL +
                     MESSAGE_INFO_REPORT +
                     MESSAGE_INFO_EXTRA)
        }
    })

    # post request
    req = request.Request(
        "http://" + ATAG_ONE + ":10000/retrieve", data=str.encode(data))
    resp_raw = request.urlopen(req, timeout=10).read()
    resp = json.loads(resp_raw)['retrieve_reply']

    assert resp['acc_status'] == 2
    return resp


def create_influxdb_point(atag_resp):
    r = atag_resp['report']
    c = atag_resp['control']
    d = atag_resp['report']['details']

    # some fields are disabled because they did not provide any useful
    # information for me
    point = {
        'measurement': 'atag_one',
        'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'fields': {
            'boiler_time': int(int(
                atag_time_to_datetime(r['report_time']).strftime('%s')) * 1e9),
            'boiler_errors': r['boiler_errors'],
            'device_errors': r['device_errors'],
            'burning_hours': r['burning_hours'],
            'room_temp': r['room_temp'],
            'outside_temp': r['outside_temp'],
            'dbg_outside_temp': r['dbg_outside_temp'],
            'pcb_temp': r['pcb_temp'],
            'ch_setpoint': r['ch_setpoint'],
            'dhw_water_temp': r['dhw_water_temp'],
            'ch_water_temp': r['ch_water_temp'],
            'dhw_water_pres': r['dhw_water_pres'],
            'ch_water_pres': r['ch_water_pres'],
            'ch_return_temp': r['ch_return_temp'],
            'boiler_heating': r['boiler_status'] & 8 == 8,
            'ch_heating': r['boiler_status'] & 2 == 2,
            'dhw_heating': r['boiler_status'] & 4 == 4,
            'dhw_flow_rate': r['dhw_flow_rate'],
            'ch_time_to_temp': r['ch_time_to_temp'],
            'power_cons': r['power_cons'],
            'current': r['current'],
            'boiler_temp': d['boiler_temp'],
            'boiler_return_temp': d['boiler_return_temp'],
            'rel_mod_level': d['rel_mod_level'],
            'overshoot': d['overshoot'],
            'max_boiler_temp': d['max_boiler_temp'],
            'ch_control_mode': c['ch_control_mode'],
            'ch_mode': c['ch_mode'],
            'ch_mode_temp': c['ch_mode_temp'],
            'ch_status': c['ch_status'],
            'dhw_mode': c['dhw_mode'],
            'dhw_mode_temp': c['dhw_mode_temp'],
            'dhw_status': c['dhw_status'],
            'dhw_temp_setp': c['dhw_temp_setp'],
        }
    }

    if point['fields']['outside_temp'] <= -100:
        del point['fields']['outside_temp']
    return point

client = InfluxDBClient(INFLUX_HOST, database=INFLUX_DATABASE)

while True:
    client.write_points([create_influxdb_point(atag_request_data())])
    time.sleep(INTERVAL)
