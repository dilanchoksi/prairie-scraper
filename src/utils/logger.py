import logging
import os
from datetime import datetime

def setup_logger():
    """Set up logging configuration"""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(
                f'logs/monitor_{datetime.now().strftime("%Y%m%d")}.log'
            ),
            logging.StreamHandler()
        ]
    )