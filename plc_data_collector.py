from datetime import datetime
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
import multiprocessing as mp
import threading
import hashlib
import queue
from pylogix import PLC
import psycopg2
from psycopg2.extras import execute_batch

@dataclass
class TagReading:
    """Represents a single tag reading with its metadata"""
    tag_name: str
    value: any  # Changed from bool to any to handle any type of value
    process_id: int
    thread_id: int

@dataclass
class CycleData:
    """Represents a complete cycle of readings for all tags"""
    start_time: datetime
    end_time: datetime
    readings: Dict[str, any]  # Changed from bool to any

    def get_hash(self) -> str:
        """Generate a hash of the readings for deduplication"""
        sorted_items = sorted(self.readings.items())
        data_str = ''.join(f"{k}:{str(v)}" for k, v in sorted_items)  # Changed to str(v) to handle any type
        return hashlib.md5(data_str.encode()).hexdigest()

class PLCReader:
    """Handles PLC connection and tag reading"""
    def __init__(self, ip_address: str, slot: int = 1):
        self.ip_address = ip_address
        self.slot = slot
        self.plc = None

    def connect(self) -> bool:
        """Establish connection to the PLC"""
        try:
            self.plc = PLC()
            self.plc.IPAddress = self.ip_address
            self.plc.ProcessorSlot = self.slot
            return True
        except Exception as e:
            print(f'Error connecting to PLC: {e}')
            return False

    def read_tags(self, tags: List[str]) -> Dict[str, any]:
        """Read a list of tags from the PLC"""
        if not self.plc:
            return {}
        try:
            results = self.plc.Read(tags)
            return {tag: result.Value for tag, result in zip(tags, results)}  # Removed bool conversion
        except Exception as e:
            print(f'Error reading tags: {e}')
            return {}

    def close(self):
        """Close the PLC connection"""
        if self.plc:
            self.plc.Close()

class DataDeduplicator:
    """Handles deduplication of cycle data"""
    def __init__(self, cache_size: int = 100):
        self.previous_hashes: Set[str] = set()
        self.cache_size = cache_size

    def is_duplicate(self, cycle_data: CycleData) -> bool:
        """Check if the cycle data is a duplicate"""
        current_hash = cycle_data.get_hash()
        
        if current_hash in self.previous_hashes:
            return True

        self.previous_hashes.add(current_hash)
        if len(self.previous_hashes) > self.cache_size:
            self.previous_hashes.pop()
        return False

class TagReaderThread(threading.Thread):
    """Thread for reading a subset of PLC tags"""
    def __init__(self, process_id: int, thread_id: int,
                 plc_reader: PLCReader, tags: List[str],
                 results_queue: queue.Queue):
        super().__init__()
        self.process_id = process_id
        self.thread_id = thread_id
        self.plc_reader = plc_reader
        self.tags = tags
        self.results_queue = results_queue

    def run(self):
        """Read assigned tags and put results in the queue"""
        readings = self.plc_reader.read_tags(self.tags)
        for tag_name, value in readings.items():
            reading = TagReading(
                tag_name=tag_name,
                value=value,
                process_id=self.process_id,
                thread_id=self.thread_id
            )
            self.results_queue.put(reading)

class DataCollectorProcess(mp.Process):
    """Process for managing tag reading threads"""
    def __init__(self, process_id: int, plc_ip: str,
                 tags: List[str], shared_dict: mp.Manager().dict()):
        super().__init__()
        self.process_id = process_id
        self.plc_ip = plc_ip
        self.tags = tags
        self.shared_dict = shared_dict

    def run(self):
        """Start threads and collect their results"""
        plc_reader = PLCReader(self.plc_ip)
        if not plc_reader.connect():
            return

        try:
            mid_point = len(self.tags) // 2
            thread_tags = [
                self.tags[:mid_point],
                self.tags[mid_point:]
            ]

            results_queue = queue.Queue()
            threads = []

            for thread_id, tags in enumerate(thread_tags):
                thread = TagReaderThread(
                    process_id=self.process_id,
                    thread_id=thread_id,
                    plc_reader=plc_reader,
                    tags=tags,
                    results_queue=results_queue
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            while not results_queue.empty():
                reading = results_queue.get()
                self.shared_dict[reading.tag_name] = reading.value

        finally:
            plc_reader.close()

class DatabaseHandler:
    """Handles PostgreSQL database operations"""
    def __init__(self, db_params: Dict[str, str]):
        self.db_params = db_params
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f'Database connection error: {e}')
            return False

    def save_cycle_data(self, cycle_data: CycleData) -> bool:
        """Save cycle data to PostgreSQL"""
        try:
            query = """
                INSERT INTO plc_readings 
                (tag_name, value, value_type, timestamp) 
                VALUES (%s, %s, %s, %s)
            """  # Added value_type column
            data = [
                (tag_name, str(value), type(value).__name__, cycle_data.start_time)
                for tag_name, value in cycle_data.readings.items()
            ]
            execute_batch(self.cursor, query, data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f'Error saving to database: {e}')
            self.conn.rollback()
            return False

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

class PLCDataCollector:
    """Main class for coordinating PLC data collection"""
    def __init__(self, plc_ip: str, tag_list: List[str], db_params: Dict[str, str]):
        self.plc_ip = plc_ip
        self.tag_list = tag_list
        self.db_params = db_params
        self.deduplicator = DataDeduplicator()
        self.db_handler = DatabaseHandler(db_params)

    def distribute_tags(self) -> List[List[str]]:
        """Distribute tags across processes"""
        tags_per_process = len(self.tag_list) // 4
        distributed_tags = []
        
        for i in range(4):
            start_idx = i * tags_per_process
            end_idx = start_idx + tags_per_process if i < 3 else len(self.tag_list)
            distributed_tags.append(self.tag_list[start_idx:end_idx])
        
        return distributed_tags

    def collect_cycle(self) -> Optional[CycleData]:
        """Collect one complete cycle of tag readings"""
        start_time = datetime.now()
        
        manager = mp.Manager()
        shared_dict = manager.dict()

        processes = []
        distributed_tags = self.distribute_tags()
        
        for process_id, tags in enumerate(distributed_tags):
            process = DataCollectorProcess(
                process_id=process_id,
                plc_ip=self.plc_ip,
                tags=tags,
                shared_dict=shared_dict
            )
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = datetime.now()

        return CycleData(
            start_time=start_time,
            end_time=end_time,
            readings=dict(shared_dict)
        )

    def run(self, interval_seconds: float = 1.0):
        """Run the data collection loop"""
        if not self.db_handler.connect():
            return

        try:
            while True:
                cycle_data = self.collect_cycle()
                if cycle_data and not self.deduplicator.is_duplicate(cycle_data):
                    self.db_handler.save_cycle_data(cycle_data)
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print('\nStopping data collection...')
        finally:
            self.db_handler.close()

def main():
    # Configuration
    PLC_IP = '10.212.49.130'
    
    # Actual PLC tags from the system
    TAG_LIST = [
        'SECT100_AUTO', 'CV104_FAULT', 'CV104_2_CART_RDY',
        'CV104_MAG_CV112_OK', 'CV112_SYNC_CV104_RQ', 'CV104_EMPTY.DN',
        'CV104_STOP_TIME.DN', 'CV104_STEP1_DONE', 'CV104_PARK_ON',
        'PARKING_OFF', 'PARKING_MODE_CV', 'LI401_MOVE_RQ_CV104',
        'R20_DI04.4', 'R20_DI04.5', 'R20_DI06.4', 'R20_DI06.5',
        'R20_DI06.6', 'R20_DI03.1', 'R20_DI05.7', 'R20_DI06.1',
        'R20_DI04.0', 'R20_DI04.2', 'R20_DI03.3', 'CV104_2_BUSY',
        'ALWAYS_ON'
        # Add remaining tags here to reach 115 total
    ]

    DB_PARAMS = {
        'dbname': 'plc_data',
        'user': 'postgres',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432'
    }

    collector = PLCDataCollector(PLC_IP, TAG_LIST, DB_PARAMS)
    collector.run()

if __name__ == '__main__':
    main()