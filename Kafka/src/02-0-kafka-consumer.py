import argparse
import json
from datetime import datetime

from confluent_kafka import Consumer


def main():
    parser = argparse.ArgumentParser(description="Test Kafka consumer")
    parser.add_argument("--group-id", "-g", help="Consumer group ID")
    parser.add_argument("--topic-name", "-t", help="Topic name ")
    parser.add_argument("--name", "-n", help="Name of this consumer")

    args = parser.parse_args()

    group_id = args.group_id
    topic_name = args.topic_name
    consumer_name = args.name

    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                # No new messages
                continue
            if msg.error():
                # Error while reading messages
                print(f"[{consumer_name}]Error encountered: {msg.error()}")
                continue

            process_message(consumer_name, msg)

    finally:
        consumer.close()


def process_message(consumer_name, msg):
    key = msg.key().decode("utf-8") if msg.key() else None
    offset = msg.offset()
    partition = msg.partition()
    topic = msg.topic()
    _, ts = msg.timestamp()
    ts_human = datetime.fromtimestamp(ts / 1000).isoformat() if ts else "N/A"

    order = json.loads(msg.value().decode("utf-8"))
    price = order.get("total_price", 0)

    if price < 250:
        return

    print(
        f"[{consumer_name}] topic={topic} partition={partition} offset={offset} "
        f"key={key} time={ts_human} price={price}"
    )


if __name__ == "__main__":
    main()