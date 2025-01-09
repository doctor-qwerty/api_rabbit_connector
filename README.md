# API Rabbit Connector:
The Rabbit Connector API is a package for interacting with RabbitMQ to process incoming messages and send the results back. The package can be easily integrated into other projects via a configuration dictionary.

## Project structure

```
api_rabbit_connector/  
├── api_rabbit_connector/  
│ ├── **init**.py  
│ ├── rabbit_connector.py  
├── tests/  
│ ├── **init**.py  
│ ├── test_api_rabbit_connector.py  
│ ├── test_real_api_rabbit_connector.py  
├── .gitignore  
├── pyproject.toml  
└── README.md
```
## File description

- **api_rabbit_connector/rabbit_connector.py**: The main module that manages the connection to RabbitMQ and message handling.
- **tests/test_api_rabbit_connector.py**: Unit tests for testing RabbitConnector functionality using mock objects.

- **tests/test_real_api_rabbit_connector.py**: Integration tests to verify interaction with a real RabbitMQ server.

- **api_rabbit_connector/__init__.py**: Initializes the package by granting access to the class `RabbitConnector`.


## Installation

Add the following dependency to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = "^3.8"
api_rabbit_connector = { git = "https://github.com/doctor-qwerty/api_rabbit_connector.git", branch = "master" }
```

Install dependencies using Poetry:
```
poetry install
```

## Integration example

Create a file `main.py` in your project and use `api_rabbit_connector` as follows:

```python
from api_rabbit_connector import RabbitConnector

def process_message(message):
    """
    Processes the incoming message and returns the result.
    """
    command = message.get("command")
    data = message.get("data")
    print(f"Processing command: {command} with data: {data}")

    # Example of data processing
    processed_data = f"Processed {data} for command {command}"
    return {"status": "success", "result": processed_data}

if __name__ == "__main__":
    config = {
        'RABBITMQ_HOST': os.getenv('RABBITMQ_HOST', 'localhost'),
        'RABBITMQ_PORT': int(os.getenv('RABBITMQ_PORT', 5672)),
        'RABBITMQ_USER': os.getenv('RABBITMQ_USER', 'user'),
        'RABBITMQ_PASSWORD': os.getenv('RABBITMQ_PASSWORD', 'pessword'),
        'RABBITMQ_INPUT_QUEUE': 'input_queue',
        'RABBITMQ_OUTPUT_QUEUE': 'output_queue'
    }

    connector = RabbitConnector(config, process_message)
    connector.start_consuming()
```
## Instructions for use

1.  **Configuration**: Specify the RabbitMQ connection and queue parameters in the configuration dictionary.
    
2.  **Processing function**: Define a function that will process incoming messages and return the results.
    
3.  **Launch**: Create an instance  `RabbitConnector`  with the configuration and processing function, then call  `start_consuming()`  to start processing messages.

## Testing

To run the tests, use:
```
poetry run pytest
```
The test_real_api_rabbit_connector.py test will run without errors only with a real connection to Rabbitmq

