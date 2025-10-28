#!/bin/bash

# This script creates the necessary Kafka topics for the law data pipeline
# using `docker-compose`. It must be run from the project root directory
# where the docker-compose.yml file is located.

set -e

echo "Creating Kafka topic: laws_topic..."
docker-compose exec kafka kafka-topics.sh --create \
    --topic laws_topic \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists

echo "Creating Kafka topic: law_details_topic..."
docker-compose exec kafka kafka-topics.sh --create \
    --topic law_details_topic \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists

echo "Kafka topics created successfully."
