"""
Logging utility for Party Pool application.
Provides centralized logging setup for server, client, and root components.
"""

import logging
import os
import config


def setup_logger(name: str, log_file=None, level=None):
    """
    Setup and return a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        log_file: Path to log file (uses config default if None)
        level: Logging level (uses config default if None)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if log_file is None:
        log_file = config.SERVER_LOG
    
    if level is None:
        level = config.LOG_LEVEL
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Check if handlers already exist
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(config.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def get_logger(name: str):
    """Get a logger instance by name."""
    return logging.getLogger(name)
