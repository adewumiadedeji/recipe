import pika
import sys
import os
import time
import service as _service

RABBITMQ_URL = os.environ.get("RABBITMQ_URL")


try:
    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_URL))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        try:
            err = _service.notification(body)
            if err:
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue="notification_service", on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()
except KeyboardInterrupt:
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)