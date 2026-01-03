from confluent_kafka.admin import AdminClient, NewTopic


def create_topic(topic_name, num_partitions=3, replication_factor=1):
    admin_client = AdminClient(
        {
            "bootstrap.servers": "localhost:9092",
        }
    )

    # Define the new topic
    new_topic = NewTopic(
        topic=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )

    # Trigger creation
    futures = admin_client.create_topics([new_topic])

    # Wait for result
    for topic, future in futures.items():
        try:
            future.result()  # Result is None on success
            print(f"Topic '{topic}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic}': {e}")


if __name__ == "__main__":
    create_topic("my-new-topic")
