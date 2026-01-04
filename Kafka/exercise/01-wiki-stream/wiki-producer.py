import json
import sys
import textwrap
import time
from pprint import pprint as pp

import requests
from confluent_kafka import Producer
from sseclient import SSEClient

producer_conf = {"bootstrap.servers": "localhost:9092"}
kafka_topic = "wikipedia-changes"

# TODO: Read docs about Wikipedia edit stream: https://www.mediawiki.org/wiki/Manual:RCFeed


def delivery_report(err, msg):
    if err:
        print("ERROR: Message failed delivery: {}".format(err))
    else:
        print(
            textwrap.dedent(f"""
        Produced event to topic {msg.topic()}:
        key = {msg.key().decode("utf-8")}
        value = {msg.value().decode("utf-8")}
        """)
        )


def main():
    url = "https://stream.wikimedia.org/v2/stream/recentchange"

    # Wikimedia requires a User-Agent header
    headers = {"User-Agent": "kafka-edu-client/1.0"}
    session = requests.Session()
    session.headers.update(headers)

    print(f"Starting to consume Wikipedia recent changes from {url} \nand produce to Kafka topic '{kafka_topic}'...")

    producer = Producer(producer_conf)
    messages = SSEClient(url, session=session)

    try:
        for event in messages:
            if event.event == "message" and event.data:
                try:
                    data = json.loads(event.data)
                except json.JSONDecodeError:
                    continue

                if data["type"] != "edit":
                    continue

                # pp(data)

                # TODO: Produce a Kafka messages from a Wikistream update message
                # * Parse the input message
                # * Extract fields you need to write
                # * Create a JSON object for a new Kafka even
                # * Write a messages to a Kafka topic
                #

                message = {
                    "title": data["title"],
                    "type": data["type"],
                    "user": data["user"],
                    "bot": data["bot"],
                    "minor": data["minor"],
                }
                producer.produce(
                    topic=kafka_topic,
                    value=json.dumps(message).encode("utf-8"),
                    callback=delivery_report,
                    key=data["title"].encode("utf-8"),
                )
                producer.poll(0)
                # To test your producer, run the following command:
                #
                # ```
                # kafka-console-consumer --bootstrap-server localhost:9092 --topic wikipedia-changes --from-beginning
                # ```
    except KeyboardInterrupt:
        print("\nUser cancelled.")
    finally:
        print("Flushing messages...")
        producer.flush()


if __name__ == "__main__":
    main()
