from os import environ
from flask import Flask, request
# from prometheus_client import start_http_server, Gauge, generate_latest, REGISTRY
import prometheus_client as prom
import time
import json

app = Flask(__name__)

# Ignore default metrics from python client
prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

# Create Prometheus gauges for temperature, humidity, WiFi signal, and pollution
atmp_gauge = prom.Gauge('temperature', 'Current temperature in Celsius', labelnames=['device_id'])
rhum_gauge = prom.Gauge('humidity', 'Current relative humidity percentage', labelnames=['device_id'])
pm01_gauge = prom.Gauge('particulate_matter_01', 'Current PM level (PM1.0)', labelnames=['device_id'])
pm02_gauge = prom.Gauge('particulate_matter_02', 'Current PM level (PM2.5)', labelnames=['device_id'])
pm10_gauge = prom.Gauge('particulate_matter_10', 'Current PM level (PM10)', labelnames=['device_id'])
pm003_count_gauge = prom.Gauge('particulate_matter_3_count', 'Current PM count (PM3)', labelnames=['device_id'])
rco2_gauge = prom.Gauge('co2', 'Current CO2 level in ppm', labelnames=['device_id'])
tvoc_gauge = prom.Gauge('tvoc', 'Current TVOC count in bbp', labelnames=['device_id'])
tvoc_index_gauge = prom.Gauge('tvoc_index', 'Current TVOC index', labelnames=['device_id'])
nox_index_gauge = prom.Gauge('nox_index', 'Current NOX index', labelnames=['device_id'])
wifi_gauge = prom.Gauge('wifi', 'Current WiFi signal strength in dBm', labelnames=['device_id'])

# Keep track of all devices
devices = {}
device_timeout = 600

@app.route('/sensors/airgradient:<device_id>/measures', methods=['POST'])
def airgradient_data(device_id):
    devices[device_id] = int(time.time())
    data = request.get_json()

    # Check for debugging
    if environ.get("DEBUG") == "true":
        print(data)
        print(devices)

    # Extract and update temperature, humidity, WiFi signal, pollution, and CO2 values from the data
    if 'atmp' in data:
        atmp = data.get('atmp')
        atmp_gauge.labels(device_id=device_id).set(atmp)
    if 'rhum' in data:
        rhum = data.get('rhum')
        rhum_gauge.labels(device_id=device_id).set(rhum)
    if 'pm01' in data:
        pm01 = data.get('pm01')
        pm01_gauge.labels(device_id=device_id).set(pm01)
    if 'pm02' in data:
        pm02 = data.get('pm02')
        pm02_gauge.labels(device_id=device_id).set(pm02)
    if 'pm10' in data:
        pm10 = data.get('pm10')
        pm10_gauge.labels(device_id=device_id).set(pm10)
    if 'pm003_count' in data:
        pm003_count = data.get('pm10')
        pm003_count_gauge.labels(device_id=device_id).set(pm003_count)
    if 'rco2' in data:
        rco2 = data.get('rco2')
        rco2_gauge.labels(device_id=device_id).set(rco2)
    if 'tvoc' in data:
        tvoc = data.get('tvoc')
        tvoc_gauge.labels(device_id=device_id).set(tvoc)
    if 'tvoc_index' in data:
        tvoc_index = data.get('tvoc_index')
        tvoc_index_gauge.labels(device_id=device_id).set(tvoc_index)
    if 'nox_index' in data:
        nox_index = data.get('nox_index')
        nox_index_gauge.labels(device_id=device_id).set(nox_index)
    if 'wifi' in data:
        wifi = data.get('wifi')
        wifi_gauge.labels(device_id=device_id).set(wifi)

    return 'Data received successfully'

@app.route('/metrics')
def metrics():
    # Generate Prometheus metrics including custom metrics
    test_stale_devices()
    return prom.generate_latest(prom.REGISTRY)

def test_stale_devices():
    clear_devices = []
    for device in devices:
        if int(time.time()) - devices[device] >= device_timeout:
            clear_devices.append(device)
    clear_stale_device(clear_devices)

def clear_stale_device(clear_devices):
    print(devices)
    for device in clear_devices:
        if atmp_gauge.labels(device_id=device)._value.get():
            atmp_gauge.remove(device)
        if rhum_gauge.labels(device_id=device)._value.get():
            rhum_gauge.remove(device)
        if pm01_gauge.labels(device_id=device)._value.get():
            pm01_gauge.remove(device)
        if pm02_gauge.labels(device_id=device)._value.get():
            pm02_gauge.remove(device)
        if pm10_gauge.labels(device_id=device)._value.get():
            pm10_gauge.remove(device)
        if pm003_count_gauge.labels(device_id=device)._value.get():
            pm003_count_gauge.remove(device)
        if rco2_gauge.labels(device_id=device)._value.get():
            rco2_gauge.remove(device)
        if tvoc_gauge.labels(device_id=device)._value.get():
            tvoc_gauge.remove(device)
        if tvoc_index_gauge.labels(device_id=device)._value.get():
            tvoc_index_gauge.remove(device)
        if nox_index_gauge.labels(device_id=device)._value.get():
            nox_index_gauge.remove(device)
        if wifi_gauge.labels(device_id=device)._value.get():
            wifi_gauge.remove(device)
        del devices[device]

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
