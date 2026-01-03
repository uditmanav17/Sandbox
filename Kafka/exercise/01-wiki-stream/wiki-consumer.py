import json
import sys

from confluent_kafka import Consumer

consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "wiki-consumer-group",
    "auto.offset.reset": "earliest",
}
kafka_topic = "wikipedia-changes"


def main():
    consumer = Consumer(consumer_conf)
    consumer.subscribe([kafka_topic])

    print(f"Consuming messages from topic '{kafka_topic}'")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                print(f"Error: {msg.error()}", file=sys.stderr)
                continue

            value = msg.value().decode("utf-8")
            data = json.loads(value)

            # TODO: Print a message about a Wikipedia edit if two conditions are true:
            # * If a change was made by a bot
            # * If a change is not minor
            #
            if data["bot"] and not data["minor"]:
                print(f"🤖 {data['user']} made a non-minor change to {data['title']}")
            # if not data["bot"]:
            #     print(
            #         f"👤 {data['user']} made a {'minor' if data['minor'] else 'non-minor'} change to {data['title']}"
            #     )
            # The printed messages should include the name of an author making a change and
            # the title of a changed page

    except KeyboardInterrupt:
        print("\nUser cancelled consumer.")
    finally:
        print("Closing consumer...")
        consumer.close()


if __name__ == "__main__":
    main()
