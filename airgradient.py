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

@app.route('/sensors/airgradient:<device_id>/measures', methods=['POST'])
def airgradient_data(device_id):
    data = request.get_json()

    # Extract temperature, humidity, WiFi signal, pollution, and CO2 values from the data
    atmp = data.get('atmp')
    rhum = data.get('rhum')
    wifi = data.get('wifi')
    pm02 = data.get('pm02')
    rco2 = data.get('rco2')

    # Dump data for debugging
    print('Temp: ', atmp)
    print('Hum: ', rhum)
    print('wifi: ', wifi)
    print('PM 2.5: ', pm02)
    print('CO2:', rco2)

    # Update the Prometheus gauges with the received values
    atmp_gauge.labels(device_id=device_id).set(atmp)
    rhum_gauge.labels(device_id=device_id).set(rhum)
    wifi_gauge.labels(device_id=device_id).set(wifi)
    pm02_gauge.labels(device_id=device_id).set(pm02)
    rco2_gauge.labels(device_id=device_id).set(rco2)

    return 'Data received successfully'

@app.route('/metrics')
def metrics():
    # Generate Prometheus metrics including custom metrics
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
