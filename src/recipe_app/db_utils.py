# src/recipe_app/db_utils.py

import time
import random
import logging
import psycopg2
from psycopg2 import OperationalError, InterfaceError

logger = logging.getLogger(__name__)

def connect_with_retry(db_url, max_retries=5, backoff_factor=0.5):
    """
    Attempt to connect to PostgreSQL with exponential backoff retry logic.
    
    Args:
        db_url (str): Database connection URL
        max_retries (int): Maximum number of retry attempts
        backoff_factor (float): Factor to determine backoff time between retries
        
    Returns:
        connection: PostgreSQL connection object
        
    Raises:
        Exception: If connection fails after all retries
    """
    retries = 0
    last_exception = None
    
    while retries < max_retries:
        try:
            # Attempt connection
            conn = psycopg2.connect(db_url)
            
            # Configure connection settings
            conn.set_session(autocommit=True)
            
            logger.info("Successfully connected to Neon PostgreSQL database")
            return conn
            
        except (OperationalError, InterfaceError) as e:
            last_exception = e
            retries += 1
            
            # Calculate backoff time with jitter
            backoff_time = backoff_factor * (2 ** retries) + random.uniform(0, 0.5)
            
            if "rate limit" in str(e).lower():
                logger.warning(f"Hit Neon rate limit, retrying in {backoff_time:.2f} seconds (attempt {retries}/{max_retries})")
            else:
                logger.warning(f"Database connection error: {str(e)}. Retrying in {backoff_time:.2f} seconds (attempt {retries}/{max_retries})")
                
            # Sleep with backoff
            time.sleep(backoff_time)
    
    # If we exit the loop, we've failed to connect
    logger.error(f"Failed to connect to Neon PostgreSQL after {max_retries} attempts. Last error: {str(last_exception)}")
    raise last_exception
