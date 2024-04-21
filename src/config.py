# config.py
import time
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

VIDEO_CHOICES = ["1080p", "Audio", "Combine"]

def timelogger(func):
    """
    A decorator that logs the duration of time a function takes to execute.
    
    Args:
    func (function): The function to wrap with timing and logging.

    Returns:
    function: A wrapper function that logs time and executes the provided function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Function {func.__name__} executed in {duration:.4f} seconds")
        return result
    return wrapper
