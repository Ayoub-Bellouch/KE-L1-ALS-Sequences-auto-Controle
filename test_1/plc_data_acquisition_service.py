# Import necessary libraries
from datetime import datetime  # For timestamping data readings
import multiprocessing as mp    # For creating multiple parallel processes
import threading               # For creating multiple threads within each process
import queue                   # For thread-safe data exchange between threads
from pylogix import PLC        # Library for communicating with Allen-Bradley PLCs
import time                    # For implementing delays
import psycopg2                # PostgreSQL database connector
import sys                     # For system-level operations like exiting the program
import logging                 # For logging to files
import os                      # For file path operations
from logging.handlers import RotatingFileHandler  # For log file rotation

# Import configuration from separate modules
from tag_config import distribute_tags                          # Function to distribute PLC tags across processes and threads
from db_config import DB_PARAMS, TABLE_NAME, initialize_database  # Database connection parameters and setup
from plc_config import PLC_SETTINGS, READING_INTERVAL  # PLC connection settings

# Configure logging
def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log file path with date in filename
    log_file = os.path.join(log_dir, f'plc_data_collection_{datetime.now().strftime("%Y-%m-%d")}.log')
    
    # Configure logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create rotating file handler (10 MB max size, keep 5 backup files)
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter with timestamp
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logging()

class PLCReader:
    """Class for connecting to and reading data from a PLC"""
    def __init__(self, ip_address: str, slot: int = 1):
        # Initialize with PLC connection parameters
        self.ip_address = ip_address  # IP address of the PLC
        self.slot = slot              # Processor slot number
        self.plc = None               # Will hold the PLC connection object

    def connect(self):
        """Establish connection to the PLC"""
        try:
            self.plc = PLC()                      # Create PLC object
            self.plc.IPAddress = self.ip_address  # Set IP address
            self.plc.ProcessorSlot = self.slot    # Set processor slot
            return True                           # Return success
        except Exception as e:
            logger.error(f'Error connecting to PLC: {e}')
            return False                          # Return failure

    def read_tags(self, tags):
        """Read multiple tags from the PLC"""
        if not self.plc:  # Check if PLC connection exists
            return {}
        try:
            # Read all tags in a single request
            results = self.plc.Read(tags)
            # Create dictionary mapping tag names to their values
            return {tag: result.Value for tag, result in zip(tags, results)}
        except Exception as e:
            logger.error(f'Error reading tags: {e}')
            return {}  # Return empty dictionary on error

    def close(self):
        """Close the PLC connection"""
        if self.plc:
            self.plc.Close()

class TagReaderThread(threading.Thread):
    """Thread class for reading a specific set of tags from the PLC"""
    def __init__(self, process_id, thread_id, plc_reader, tags, results_queue):
        super().__init__()  # Initialize the Thread parent class
        self.process_id = process_id        # ID of the parent process
        self.thread_id = thread_id          # ID of this thread
        self.plc_reader = plc_reader        # PLC reader object to use
        self.tags = tags                    # List of tags to read
        self.results_queue = results_queue  # Queue for sending results back
        self.running = True                 # Flag to control thread execution

    def run(self):
        """Main thread execution - continuously read tags and put results in queue"""
        while self.running:  # Run until stopped
            # Read all assigned tags
            readings = self.plc_reader.read_tags(self.tags)
            # Put readings in the queue with metadata
            self.results_queue.put({
                'process_id': self.process_id,
                'thread_id': self.thread_id,
                'timestamp': datetime.now(),  # Current timestamp
                'readings': readings          # Tag values
            })
            # Wait before next reading cycle
            time.sleep(READING_INTERVAL)
    
    def stop(self):
        """Signal the thread to stop"""
        self.running = False

class DataCollectorProcess(mp.Process):
    """Process class for collecting data from PLC using multiple threads"""
    def __init__(self, process_id, plc_settings, tag_distribution, db_params):
        super().__init__()  # Initialize the Process parent class
        self.process_id = process_id              # ID for this process
        self.plc_settings = plc_settings          # PLC connection settings
        self.tag_distribution = tag_distribution  # Tags assigned to this process's threads
        self.db_params = db_params                # Database connection parameters
        self.running = mp.Event()                 # Event for controlling process execution

    def run(self):
        """Main process execution - start threads and process their results"""
        self.running.set()  # Set the running flag
        
        # Create and connect to PLC
        plc_reader = PLCReader(self.plc_settings['ip_address'], self.plc_settings['processor_slot'])
        if not plc_reader.connect():
            logger.error(f"Process {self.process_id}: Failed to connect to PLC")
            return

        try:
            # Connect to database
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            results_queue = queue.Queue()  # Queue for collecting results from threads
            threads = []                   # List to track active threads

            # Start threads for this process
            for thread_id, tags in self.tag_distribution[self.process_id].items():
                if not tags:  # Skip if no tags assigned to this thread
                    continue
                    
                # Create and start thread
                thread = TagReaderThread(
                    process_id=self.process_id,
                    thread_id=thread_id,
                    plc_reader=plc_reader,
                    tags=tags,
                    results_queue=results_queue
                )
                threads.append(thread)
                thread.start()
                logger.info(f"Process {self.process_id}, Thread {thread_id} started with {len(tags)} tags")

            # Process results from queue
            while self.running.is_set():  # Run until signaled to stop
                try:
                    # Get result from queue (timeout to check running flag periodically)
                    result = results_queue.get(timeout=1)
                    timestamp = result['timestamp']
                    process_id = result['process_id']
                    thread_id = result['thread_id']
                    
                    # Insert readings into database
                    for tag_name, value in result['readings'].items():
                        value_type = type(value).__name__  # Get the data type name
                        cursor.execute(f"""
                            INSERT INTO {TABLE_NAME} 
                            (time, process_id, thread_id, tag_name, value, value_type) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (timestamp, process_id, thread_id, tag_name, str(value), value_type))
                    
                    conn.commit()  # Commit the transaction
                    logger.info(f"Process {process_id}, Thread {thread_id}: Saved {len(result['readings'])} readings at {timestamp}")
                    
                except queue.Empty:
                    continue  # No data in queue, continue checking
                except Exception as e:
                    logger.error(f"Process {self.process_id} error: {e}")
                    conn.rollback()  # Rollback on error

        finally:
            # Cleanup when process is stopping
            # Stop all threads
            for thread in threads:
                thread.stop()
            
            # Wait for threads to finish
            for thread in threads:
                thread.join()
                
            # Close connections
            if 'conn' in locals():
                conn.close()
            plc_reader.close()
            logger.info(f"Process {self.process_id}: Shutdown complete")

def main():
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

# Entry point of the script
if __name__ == '__main__':
    main()