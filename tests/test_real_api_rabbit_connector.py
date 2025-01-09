import os
import json
import unittest
#from dotenv import load_dotenv
import pika

class TestRabbitMQIntegration(unittest.TestCase):
    def setUp(self):
        # Loading environment variables from the .env file
        #load_dotenv()

        # Configuration settings from environment variables
        self.config = {
            'RABBITMQ_HOST': os.getenv('RABBITMQ_HOST', 'localhost'),
            'RABBITMQ_PORT': int(os.getenv('RABBITMQ_PORT', 5672)),
            'RABBITMQ_USER': os.getenv('RABBITMQ_USER', 'user'),
            'RABBITMQ_PASSWORD': os.getenv('RABBITMQ_PASSWORD', 'password'),
            'RABBITMQ_INPUT_QUEUE': 'input_queue',
            'RABBITMQ_OUTPUT_QUEUE': 'output_queue'
        }

        credentials = pika.PlainCredentials(
            self.config['RABBITMQ_USER'],
            self.config['RABBITMQ_PASSWORD']
        )
        self.connection_params = pika.ConnectionParameters(
            host=self.config['RABBITMQ_HOST'],
            port=self.config['RABBITMQ_PORT'],
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

        # Declaring queues
        self.channel.queue_declare(queue=self.config['RABBITMQ_INPUT_QUEUE'])
        self.channel.queue_declare(queue=self.config['RABBITMQ_OUTPUT_QUEUE'])

    def tearDown(self):
        # Closing the connection
        self.connection.close()

    def process_message_callback(self, message):
        # Message processing
        message['status'] = 'processed'
        return message

    def test_message_processing(self):
        # Sending a message to input_queue
        initial_message = {'name': 'example_config', 'version': 1.0}
        self.channel.basic_publish(
            exchange='',
            routing_key=self.config['RABBITMQ_INPUT_QUEUE'],
            body=json.dumps(initial_message)
        )

        # Receiving and processing a message
        method_frame, header_frame, body = self.channel.basic_get(
            queue=self.config['RABBITMQ_INPUT_QUEUE'], auto_ack=True
        )
        if body:
            received_message = json.loads(body)
            processed_message = self.process_message_callback(received_message)

            # Sending the processed message to output_queue
            self.channel.basic_publish(
                exchange='',
                routing_key=self.config['RABBITMQ_OUTPUT_QUEUE'],
                body=json.dumps(processed_message)
            )

        # Checking that the message is in output_queue
        method_frame, header_frame, body = self.channel.basic_get(
            queue=self.config['RABBITMQ_OUTPUT_QUEUE'], auto_ack=True
        )
        self.assertIsNotNone(body, "Message not found in output queue")
        final_message = json.loads(body)
        self.assertEqual(final_message['status'], 'processed')
        self.assertEqual(final_message['name'], 'example_config')
        self.assertEqual(final_message['version'], 1.0)

if __name__ == '__main__':
    unittest.main()
