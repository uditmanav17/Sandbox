import json
import textwrap
import time
from datetime import datetime

from confluent_kafka import Producer
from faker import Faker

fake = Faker()


def generate_order():
    """ Generates a random order dictionary containing mock transaction data. """
    order = {
        "order_id": fake.random_int(min=1000, max=9999),
        "customer_id": fake.random_int(min=1, max=10),
        "total_price": round(fake.pyfloat(min_value=20.0, max_value=1000.0, right_digits=2), 2),
        "customer_country": fake.country(),
        "merchant_country": fake.country(),
        "order_date": datetime.now().isoformat(),
    }
    return order

def main():
    # Kafka producer configuration targeting the local broker
    config = {
        "bootstrap.servers": "localhost:9092"
    }

    # Instantiate the Kafka producer with the specified configuration
    producer = Producer(config)

    topic = "orders"

    def delivery_callback(err, msg):
        """
        Optional per-message delivery callback (triggered by poll() or flush())
        when a message has been successfully delivered or permanently failed.
        """
        if err:
            print("ERROR: Message failed delivery: {}".format(err))
        else:
            print(
                textwrap.dedent(
                f"""
                    Produced event to topic {msg.topic()}:
                    key = {msg.key().decode('utf-8')}
                    value = {msg.value().decode('utf-8')}
                """)
            )

    # Main loop to generate and send messages indefinitely
    try:
        while True:
            order = generate_order()
            print(f"Sending order: {order}")

            # Asynchronously produce a message to the Kafka topic
            producer.produce(
                topic,
                key=str(order["customer_id"]),
                value=json.dumps(order),
                callback=delivery_callback,
            )

            # Polls the producer for events and calls corresponding callbacks
            producer.poll(0)

            # Wait for 1 second to simulate a stream of incoming orders
            time.sleep(2)

    except KeyboardInterrupt:
        print("User cancelled.")
    finally:
        print("Flushing producer...")
        # Wait for all messages to be delivered
        producer.flush()

if __name__ == "__main__":
    main()