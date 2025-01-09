import pika
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitConnector:
    def __init__(self, config, process_message_callback):
        self.config = config
        self.process_message_callback = process_message_callback

        self.connection_params = pika.ConnectionParameters(
            host=self.config['RABBITMQ_HOST'],
            port=int(self.config['RABBITMQ_PORT']),
            credentials=pika.PlainCredentials(
                self.config['RABBITMQ_USER'],
                self.config['RABBITMQ_PASSWORD']
            )
        )

    def on_message(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            logger.info(f"Received message: {message}")

            result = self.process_message_callback(message)

            ch.basic_publish(
                exchange='',
                routing_key=self.config['RABBITMQ_OUTPUT_QUEUE'],
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(result)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()

        channel.queue_declare(queue=self.config['RABBITMQ_INPUT_QUEUE'])
        channel.queue_declare(queue=self.config['RABBITMQ_OUTPUT_QUEUE'])

        channel.basic_consume(
            queue=self.config['RABBITMQ_INPUT_QUEUE'],
            on_message_callback=self.on_message
        )

        logger.info(f"Waiting for messages in queue: {self.config['RABBITMQ_INPUT_QUEUE']}")
        channel.start_consuming()
