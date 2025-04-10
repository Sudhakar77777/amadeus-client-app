import logging

# Set up logger
logger = logging.getLogger('dev_logger')
logger.setLevel(logging.DEBUG)

# Create a console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the console handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# This logger can now be imported in other scripts
logger.debug('Initialized App Logger...')