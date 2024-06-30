#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------
from buffered import Buffer
from mqtt_node_network.initialize import initialize
from mqtt_node_network.client import MQTTClient
from fast_database_clients.fast_influxdb_client import FastInfluxDBClient


config = initialize(
    config="config/config.toml", secrets=".env", logger="config/logger.yaml"
)


def start_client():

    import time

    # Initialize the buffer for passing data from the mqtt client to the database client
    buffer = Buffer(maxlen=100_000)

    # Initialize the database client
    database_client = FastInfluxDBClient.from_config_file(
        buffer=buffer, config_file="config/.influx.toml"
    )
    # Start periodic writing to the database
    database_client.start()

    # Initialize the MQTT client
    mqtt_client_config = config["mqtt"]["client"]
    mqtt_client = MQTTClient(
        broker_config=config["mqtt"]["broker"],
        buffer=buffer,
        node_id=mqtt_client_config["node_id"],
        topic_structure=config["mqtt"]["node_network"]["topic_structure"],
    ).connect()
    mqtt_client.subscribe(
        topic=mqtt_client_config["subscribe_topics"],
        qos=mqtt_client_config["subscribe_qos"],
    )
    while True:
        time.sleep(1)


if __name__ == "__main__":
    start_client()
