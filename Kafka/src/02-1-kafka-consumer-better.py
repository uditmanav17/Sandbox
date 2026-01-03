import argparse
import json
import signal
from datetime import datetime

from confluent_kafka import Consumer, KafkaError, KafkaException
from loguru import logger

# Configure loguru to write to a file as well as stderr (default)
logger.add("consumer.log", rotation="1 MB")

running = True


def signal_handler(sig, frame):
    """Handles system signals for graceful shutdown."""
    global running
    logger.info("Shutdown signal received. Stopping consumer...")
    running = False


def main():
    parser = argparse.ArgumentParser(description="Test Kafka consumer")
    parser.add_argument("--group-id", "-g", required=True, help="Consumer group ID")
    parser.add_argument("--topic-name", "-t", required=True, help="Topic name")
    parser.add_argument("--name", "-n", default="consumer-1", help="Name of this consumer")

    args = parser.parse_args()

    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": args.group_id,
        "auto.offset.reset": "earliest",
        # 'enable.auto.commit': False, # Uncomment if doing manual commits
    }

    consumer = Consumer(consumer_config)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info(f"Subscribing to topic: {args.topic_name}")
    consumer.subscribe([args.topic_name])

    try:
        while running:
            # poll(timeout) to allow frequent checking of 'running' flag
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not a real error
                    logger.debug(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                continue

            process_message(args.name, msg)

    except KafkaException as e:
        logger.error(f"Critical Kafka exception: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("Closing consumer...")
        consumer.close()


def process_message(consumer_name, msg):
    """
    Process the message using safe decoding logic.
    Always assume the incoming message might be malformed.
    """
    try:
        key = msg.key().decode("utf-8") if msg.key() else None
        offset = msg.offset()
        partition = msg.partition()
        topic = msg.topic()
        _, ts = msg.timestamp()
        ts_human = datetime.fromtimestamp(ts / 1000).isoformat() if ts else "N/A"

        raw_val = msg.value()

        if raw_val is None:
            logger.warning(f"[{consumer_name}] Received None value message")
            return

        order = json.loads(raw_val.decode("utf-8"))

        # Validation
        if "total_price" not in order:
            logger.warning(f"[{consumer_name}] Malformed order: missing total_price")
            return

        price = order.get("total_price", 0)

        # Business logic
        if price < 250:
            return

        logger.info(
            f"[{consumer_name}] topic={topic} partition={partition} offset={offset} "
            f"key={key} time={ts_human} price={price}"
        )

    except json.JSONDecodeError as e:
        logger.error(f"[{consumer_name}] Failed to decode JSON: {e} | Body: {raw_val}")
    except UnicodeDecodeError as e:
        logger.error(f"[{consumer_name}] Failed to decode bytes: {e}")
    except Exception as e:
        logger.exception(f"[{consumer_name}] Error processing message: {e}")


if __name__ == "__main__":
    main()