from os import environ
from flask import Flask, request
from prometheus_client import start_http_server, Gauge, generate_latest, REGISTRY
import json

app = Flask(__name__)

# Create Prometheus gauges for temperature, humidity, WiFi signal, and pollution
atmp_gauge = Gauge('temperature', 'Current temperature in Celsius', labelnames=['device_id'])
rhum_gauge = Gauge('humidity', 'Current relative humidity percentage', labelnames=['device_id'])
wifi_gauge = Gauge('wifi', 'Current WiFi signal strength in dBm', labelnames=['device_id'])
pm02_gauge = Gauge('particulate_matter', 'Current PM level (PM2.5)', labelnames=['device_id'])
rco2_gauge = Gauge('co2', 'Current CO2 level in ppm', labelnames=['device_id'])
tvoc_gauge = Gauge('tvoc', 'Current TVOC count in bbp', labelnames=['device_id'])

@app.route('/sensors/airgradient:<device_id>/measures', methods=['POST'])
def airgradient_data(device_id):
    data = request.get_json()

    # Check for debugging
    if environ.get("DEBUG") == "true":
        print(data)

    # Extract and update temperature, humidity, WiFi signal, pollution, and CO2 values from the data
    if 'atmp' in data:
        atmp = data.get('atmp')
        atmp_gauge.labels(device_id=device_id).set(atmp)
    if 'rhum' in data:
        rhum = data.get('rhum')
        rhum_gauge.labels(device_id=device_id).set(rhum)
    if 'pm02' in data:
        pm02 = data.get('pm02')
        pm02_gauge.labels(device_id=device_id).set(pm02)
    if 'rco2' in data:
        rco2 = data.get('rco2')
        rco2_gauge.labels(device_id=device_id).set(rco2)
    if 'tvoc' in data:
        tvoc = data.get('tvoc')
        tvoc_gauge.labels(device_id=device_id).set(tvoc)
    if 'wifi' in data:
        wifi = data.get('wifi')
        wifi_gauge.labels(device_id=device_id).set(wifi)

    return 'Data received successfully'

@app.route('/metrics')
def metrics():
    # Generate Prometheus metrics including custom metrics
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
