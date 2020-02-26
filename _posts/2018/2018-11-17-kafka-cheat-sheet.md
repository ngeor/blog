---
layout: post
title: Kafka cheat sheet
date: 2018-11-17
categories:
  - tech
---

A cheat sheet for Apache Kafka.

## Using Docker

Using Docker allows starting Kafka locally without having to install anything
extra on your system. This works the same on every OS.

For more information, please see the documentation of the Docker image we'll be
using: https://github.com/wurstmeister/kafka-docker

As Kafka is a message broker, it can't be owned by a single project. Create the
following `docker-compose.yml` file and store it in a folder of your choosing.

```yaml
version: "2"
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: localhost
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
```

Then, open a terminal in that folder and run `docker-compose up`.

That should give you Kafka up and running ready to be used.

## Working with the Kafka CLI

You can download the official CLI here: http://kafka.apache.org/quickstart

Unzip it somewhere, e.g. `C:\opt\kafka`

### Connecting to Azure Event Hub

You will need a configuration file like this:

```ini
bootstrap.servers=my-host.servicebus.windows.net:9093

# tip: put a suffix to your consumer group like '-dev',
# to avoid interfering with the ones deployed on DTAP
group.id=my-service-dev

# Security options
security.protocol=SASL_SSL
sasl.mechanism=PLAIN

# Connection String. Mind the trailing semicolon.
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="the full connection string from Azure";
```

Save it in `C:\opt\kafka\config\azure.properties` (for example)

### Inspecting the consumer groups

You can see the active consumer groups like this:

```
C:\opt\kafka_2.11-2.0.1> .\bin\windows\kafka-consumer-groups.bat \
  --bootstrap-server my-host.servicebus.windows.net:9093 \
  --command-config .\config\azure.properties \
  --list

my-service
```

### Reset the consumer group's offset

This operation will reset the consumer group offset, which will cause your
application to read all messages from the beginning of time. Useful for local
development.

```
C:\opt\kafka_2.11-2.0.1> .\bin\windows\kafka-consumer-groups.bat \
  --bootstrap-server my-host.servicebus.windows.net:9093 \
  --command-config .\config\azure.properties \
  --group my-service-dev \
  --topic clients \
  --reset-offsets --execute --to-earliest

TOPIC                          PARTITION  NEW-OFFSET
clients                        0          0
clients                        1          0
```
