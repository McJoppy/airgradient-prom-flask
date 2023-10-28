# Airgradient Prometheus Flask App

[Airgradient](https://www.airgradient.com/) is an open air quality monitoring solution with DIY offerings utilising an ESP8266 microcontroller.

The [example DIY code](https://github.com/airgradienthq/arduino/blob/master/examples/DIY_BASIC/DIY_BASIC.ino#L42) defaults to sending metrics to Airgradient.

## `airgradient.py`

This is a very simple (probably bad!) Flask app to act as a receiver for Airgradient metrics for those who change `APIROOT` in the root to point to this app (as long as it's accessible).

Prometheus can then be configured to collect metrics using the exporter at `/metrics`.

The app should work with multiple devices.

## Metrics and Labels

The metrics received are

- `atmp`: Temperature
- `rhum`: Humidity
- `wifi`: Wifi signal strength
- `pm02`: Particulate Matter (PM2.5)
- `rco2`: CO2

Each metric has an associated label of `device_id` to help identify metrics for a specific device.

## Testing

Run via flask in a local dev environment with eg. `DEBUG=true python -m flask --app airgradient --debug run --host 0.0.0.0`.

If you use WSL2 then look at port forwarding to WSL with `netsh`.

### Docker

In project root directory you can build the image with `docker -t <tag> build .` then run with eg. `docker run -it`.