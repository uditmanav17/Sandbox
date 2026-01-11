import argparse
import json
import logging
import threading
import time

from confluent_kafka import Consumer, KafkaException

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class ConsumerWorker(threading.Thread):
    def __init__(self, config, topic, name):
        super().__init__(name=name)
        self.config = config
        self.topic = topic
        self.daemon = True  # Daemon threads exit when main program exits
        self.running = True
        self.consumer = None

    def run(self):
        # Create a unique consumer instance for this thread
        # confluent_kafka.Consumer is NOT thread-safe!
        try:
            self.consumer = Consumer(self.config)
            self.consumer.subscribe([self.topic])
            logger.info(f"Worker {self.name} started")

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Worker {self.name} error: {msg.error()}")
                    continue

                process_message(self.name, msg)

        except KafkaException as e:
            logger.error(f"Worker {self.name} crashed: {e}")
        finally:
            logger.info(f"Worker {self.name} stopping...")
            if self.consumer:
                self.consumer.close()

    def stop(self):
        self.running = False


def process_message(consumer_name, msg):
    try:
        value = msg.value()
        order = json.loads(value.decode("utf-8"))
        price = order.get("total_price", 0)
        if price < 250:
            return

        print(
            f"[{consumer_name}] [partition={msg.partition()}] Received order price={price}"
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}")


def main():
    parser = argparse.ArgumentParser(description="Test Kafka consumer with threading")
    parser.add_argument("--group-id", "-g", required=True, help="Consumer group ID")
    parser.add_argument("--topic-name", "-t", required=True, help="Topic name")
    parser.add_argument(
        "--workers", "-w", type=int, default=1, help="Number of consumer threads"
    )

    args = parser.parse_args()

    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": args.group_id,
        "auto.offset.reset": "earliest",
    }

    workers = []
    try:
        # Start worker threads
        for i in range(args.workers):
            worker_name = f"worker-{i + 1}"
            worker = ConsumerWorker(consumer_config, args.topic_name, worker_name)
            worker.start()
            workers.append(worker)

        # Keep main thread alive to handle KeyboardInterrupt
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Stopping consumers...")
        for worker in workers:
            worker.stop()

        # Wait for threads to finish
        for worker in workers:
            worker.join()

        logger.info("All consumers stopped.")


if __name__ == "__main__":
    main()
