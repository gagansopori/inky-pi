import logging
import sys
from pathlib import Path


class CustomLogger:
    """
    A unified logger for the InkyPi application.
    Prevents duplicate handlers and supports Console or File output.
    """

    def __init__(self, name, log_to_file=False):
        self.logger = logging.getLogger(name)

        # If this logger name is already configured, don't add handlers again
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            # Create Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            if log_to_file:
                # File Logging (used for background process/production)
                log_path = Path(__file__).resolve().parent.parent / "data" / "app.log"
                log_path.parent.mkdir(parents=True, exist_ok=True)
                handler = logging.FileHandler(log_path)
            else:
                # Console Logging (used for lifecycle/dev)
                handler = logging.StreamHandler(sys.stdout)

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def critical(self, msg):
        self.logger.critical(msg)