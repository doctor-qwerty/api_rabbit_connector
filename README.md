# API Rabbit Connector:
The Rabbit Connector API is a package for interacting with RabbitMQ to process incoming messages and send the results back. The package can be easily integrated into other projects via a configuration dictionary.It works as a constant listener of messages in the queue, i.e. in an infinite loop until stopped.

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
api_rabbit_connector = { git = "https://github.com/doctor-qwerty/api_rabbit_connector.git"}
```

Install dependencies using Poetry:
```
poetry install
```

## Integration example

Create a file `main.py` in your project and use `api_rabbit_connector` as follows:

```python
from api_rabbit_connector import RabbitConnector

#from my_project.api import search  # Import the search function from the api module
#or write the function here in the file
def search(config):
    """
    Executes basic logic based on the configuration.
    Here you can implement your own logic.
    """
    # Example of configuration processing
    print(f"Performing search with config: {config}")
    # Simulated machining
    result = f"Search results for config: {config}"
    return result

def process_message(message):
    """
    Processes the incoming message using the search function and returns the result.
    """
    # Getting the configuration from the message
    config = message.get("config")
    
    # Execute basic logic using search
    result = search(config)
    
    # Return the result in JSON format
    return {"status": "success", "result": result}

def main():
    config = {
        'RABBITMQ_HOST': 'localhost',
        'RABBITMQ_PORT': '5672',
        'RABBITMQ_USER': 'user',
        'RABBITMQ_PASSWORD': 'password',
        'RABBITMQ_INPUT_QUEUE': 'input_queue'
    }

    connector = RabbitConnector(config, process_message)
    connector.start_consuming()

if __name__ == "__main__":
    main()
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

