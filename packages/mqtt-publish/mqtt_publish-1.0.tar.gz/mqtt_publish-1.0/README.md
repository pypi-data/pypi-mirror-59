# mqtt_publish

A command line utility for quickly publishing a single MQTT message.

## Installation

Via pip, with `pip install mqtt_publish`.

## Usage

From `--help`:

```shell
usage: mqtt_publish [-h] [--broker-port BROKER_PORT]
                    broker_address topic message

Command line utility for quick MQTT publishes

positional arguments:
  broker_address
  topic
  message

optional arguments:
  -h, --help            show this help message and exit
  --broker-port BROKER_PORT
```

## Example

Once installed, the CLI should be available in path (assuming python is in path).

```shell
mqtt_publish home-server.lan bedroom/smart-plug/set on
```

The `mqtt_publish` CLI is available via the python executable with the `-m` flag.

```shell
path/to/python -m mqtt_publish home-server.lan bedroom/smart-plug/set off
```
