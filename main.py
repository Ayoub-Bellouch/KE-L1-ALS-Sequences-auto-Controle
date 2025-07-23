# main.py
import sys
import os
import logging
from datetime import datetime
import multiprocessing as mp

# Add necessary imports for PLC data acquisition
from pylogix import PLC
import psycopg2
import time

# Import configuration from separate modules
from tag_config import distribute_tags
from db_config import DB_PARAMS, TABLE_NAME, initialize_database
from plc_config import PLC_SETTINGS, READING_INTERVAL

# Import the PLC data acquisition service components
from plc_data_acquisition_service import (
    setup_logging, PLCReader, TagReaderThread, DataCollectorProcess
)

# Initialize logger
logger = setup_logging()

def plc_data_main():
    """Main function to start the data collection system"""
    # Log startup
    logger.info("Starting PLC data collection system")
    
    # Validate PLC settings
    try:
        # Check if IP address is valid format
        ip_parts = PLC_SETTINGS['ip_address'].split('.')
        if len(ip_parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
            logger.error("Invalid IP address format in PLC settings")
            sys.exit(1)
            
        # Check if processor slot is valid
        if not isinstance(PLC_SETTINGS['processor_slot'], int) or PLC_SETTINGS['processor_slot'] < 0:
            logger.error("Invalid processor slot in PLC settings")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error validating PLC settings: {e}")
        sys.exit(1)
    
    # Distribute tags across processes and threads
    tag_distribution = distribute_tags(num_processes=4, num_threads=2)
    
    # Initialize database
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        if not initialize_database(conn):
            logger.error("Failed to initialize database")
            sys.exit(1)
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        sys.exit(1)
    
    # Start processes
    processes = []
    for process_id in range(4):
        process = DataCollectorProcess(
            process_id=process_id,
            plc_settings=PLC_SETTINGS,
            tag_distribution=tag_distribution,
            db_params=DB_PARAMS
        )
        processes.append(process)
        process.start()
        logger.info(f"Process {process_id} started")

    try:
        # Wait for all processes to complete
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        logger.info("\nStopping all processes...")
        for process in processes:
            process.running.clear()  # Signal process to stop
            process.join(timeout=5)  # Wait up to 5 seconds
            if process.is_alive():
                process.terminate()  # Force terminate if still running
        logger.info("All processes stopped")

def main():
    """
    Entry point of the application.
    Add your main logic here.
    """
    # Your other main logic can go here
    
    # Run the PLC data acquisition service
    plc_data_main()


if __name__ == "__main__":
    main()
    
# This application integrates the PLC data acquisition service which handles:
# - PLC connection and tag reading
# - Multi-process and multi-threaded data collection
# - Database storage of collected PLC data
# - Graceful shutdown on interruption