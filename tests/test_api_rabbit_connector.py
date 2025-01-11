import json
from unittest import mock, TestCase
from api_rabbit_connector.rabbit_connector import RabbitConnector

class TestRabbitMQMock(TestCase):
    @mock.patch('api_rabbit_connector.rabbit_connector.pika.BlockingConnection')
    def test_rabbit_connector(self, MockBlockingConnection):
        # Configuring mock objects
        mock_connection = MockBlockingConnection.return_value
        mock_channel = mock_connection.channel.return_value
        
        # Configuration settings and callback functions
        config = {
            'RABBITMQ_HOST': 'localhost',
            'RABBITMQ_PORT': '5672',
            'RABBITMQ_USER': 'user',
            'RABBITMQ_PASSWORD': 'password',
            'RABBITMQ_INPUT_QUEUE': 'input_queue'
        }
        
        def mock_process_message_callback(message):
            message['status'] = 'processed'
            return message
        
        # Creating an instance of RabbitConnector
        connector = RabbitConnector(config, mock_process_message_callback)
        
        # Configuring mock behavior for basic_get
        mock_channel.basic_get.return_value = (mock.Mock(), mock.Mock(), json.dumps({'name': 'example_config', 'version': 1.0}).encode())
        
        # Call on_message directly for testing
        method = mock.Mock()
        properties = mock.Mock()
        properties.reply_to = 'reply_queue'
        body = json.dumps({'name': 'example_config', 'version': 1.0}).encode()
        
        connector.on_message(mock_channel, method, properties, body)
        
        # Checking that basic_publish was called with the correct reply-to
        self.assertEqual(mock_channel.basic_publish.call_count, 1)
        self.assertEqual(mock_channel.basic_publish.call_args[1]['routing_key'], 'reply_queue')
        
        # Checking that the message has been processed and sent
        sent_message = json.loads(mock_channel.basic_publish.call_args[1]['body'])
        self.assertEqual(sent_message['status'], 'processed')

if __name__ == '__main__':
    import unittest
    unittest.main()
