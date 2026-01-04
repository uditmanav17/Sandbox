# Kafka + Debezium CDC Stack

This directory contains a complete Docker Compose stack for running Kafka with Debezium CDC (Change Data Capture) from a Postgres database.

## Components

*   **Kafka**: The event streaming platform (KRaft mode).
*   **Kafka Connect**: Runs the Debezium Postgres connector.
*   **Postgres**: The source database containing an `orders` table.
*   **Connect Init**: An automated helper service that configures the connector on startup.

## How to Run

To start the full stack including Connect and Postgres:

```bash
docker compose --profile connect up
```

To stop:

```bash
docker compose --profile connect down
```

## Automation Logic

### 1. Database Initialization
The `postgres` service mounts `data.sql` to `/docker-entrypoint-initdb.d/data.sql`.
*   **Behavior**: When the container starts **for the first time** (i.e., with an empty data volume), Postgres runs this script.
*   **Result**: It creates the `orders` table and seeds initial data.

### 2. Connector Configuration
The `connect-init` service acts as a sidecar automation:
*   **Behavior**: It waits for `kafka-connect` to become healthy (HTTP 200).
*   **Action**: Once ready, it automatically POSTs the configuration from `config_debezium.json` to the Connect API.
*   **Result**: The `postgres-debezium-connector` is automatically registered without manual `curl` commands.

## Verification

After starting the stack, you can verify the setup:

1.  **Check Connector**:
    ```bash
    curl http://localhost:8083/connectors
    # Should return ["postgres-debezium-connector"]
    ```

2.  **Check Topics**:
    ```bash
    docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
    # Should see "postgres-.public.orders"
    ```

3.  **Consume Events**:
    ```bash
    docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic postgres-.public.orders --from-beginning
    ```
