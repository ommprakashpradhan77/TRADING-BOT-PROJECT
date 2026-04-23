import logging
import os

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )
        
        # Determine log file path (in the root of trading_bot)
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bot.log')
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
    return logger
