# Configuration file for PLC tags

# List of all tags to be monitored
TAG_LIST = [
    # Sequence tags from base_experiance
    "CV104_SEQUENCE",
    "R20_DI02.6", "R20_DI02.4", "R24_DI03.4", "R20_DI02.7", "R20_DI03.3",
    "R20_DI03.1", "R20_DI03.2", "R20_DI05.7", "R20_DI06.1", "R20_DI04.4",
    "R20_DI04.5", "R20_DI06.4", "R20_DI06.5", "R20_DI06.6", "R20_DI04.0",
    "R20_DI04.2", "R20_DI05.6", "R20_DI06.0", "R20_DI04.3", "R20_DI04.1",
    "R20_DI04.6", "R20_DI04.7", "R20_DI12.5", "R20_DI01.0", "R20_DI01.1",
    "R20_DI01.6", "R23_DI03.4", "R24_DI03.3", "R23_DI04.0", "R24_DI03.4",
    "R24_DI03.2", "R20_DI03.5", "R23_DI04.7", "R24_DI01.4", "R24_DI01.5",
    "R24_DI01.0", "R24_DI01.2", "R24_DI01.3", "R24_DI02.4", "R24_DI02.1",
    "R24_DI02.5", "R24_DI02.6", "R24_DI01.6", "R24_DI01.7", "R24_DI02.0", 
    "R24_DI02.2", "R24_DI02.3", "R24_DI03.1", "R81_DI01.1", "R81_DI01.2", 
    "R25_DI01.0", "R25_DI02.1", "R25_DI02.4", "R25_DI02.0", "R25_DI02.5", 
    "R25_DI02.6", "R25_DI02.3", "R24_DI04.5", "R24_DI04.1", "R24_DI04.4", 
    "R25_DI01.6", "R25_DI02.2", "R24_DI04.3", "R25_DI02.7", "R25_DI01.4", 
    "R24_DI04.6", "R24_DI04.2", "R24_DI04.0", "R20_DI03.4", "SECT100_AUTO", 
    "SECT100_START", "CV104_FAULT", "LI401_UD_R.POS_1_OK", "LI401_SAFE_CV104", 
    "CV104_2_CART_RDY", "ALWAYS_ON", "CV104_2_BUSY"	, "CV104_SEARCH.DN", 
    "CV104_PARK_ON", "LI401_MOVE_RQ_CV104", "CV103_RTS_CV104", "SECT100_PROD",
    "CV112_SYNC_CV104_RQ", "LI401_RTS_CV104", "CV101_FREE", "CV102_FREE",
    "CV103_FREE", "PARKING_MODE_CV", "MODE_EXCHANGE_PROD_STOCK1", 
    "TRACK_CV104[1].DEST1", "TRACK_CV104[1].DEST2", "TRACK_CV104[1].DEST4", 
    "TRACK_CV104[1].DEST8", "TRACK_CV104[1].LARGE", "CV104_SLIDING_TIME.DN",
    "CV104_CENTERING_TIME.DN", "CV104_STEP2_DONE", "CV104_TAK_TIME.DN", 
    "LI401_LIFTING_CV104", "CV104_MAG_CV112_OK", "LI401_SD_CV104", 
    "CV104_STEP3_DONE", "CV112_SYNC_CV104_OK", "CV101_SYNC_CV104_OK", 
    "CV102_SYNC_CV104_OK", "CV103_SYNC_CV104_OK", "CV112_PARK_ON", "CV101_PARK_ON", 
    "CV102_PARK_ON", "CV103_PARK_ON", "CV104_EMPTY.DN", "CV104_STOP_TIME.DN", 
    "CV104_STEP1_DONE", "PARKING_OFF" 

    # Additional tags can be added here
    # "TAG1", "TAG2", "TAG3", ...
]

# Function to distribute tags across processes and threads
def distribute_tags(num_processes=4, num_threads=2):
    """Distribute tags evenly across processes and threads without a fixed limit per thread"""
    result = {}
    total_threads = num_processes * num_threads
    
    # Calculate how many tags each thread should handle (evenly distributed)
    tags_per_thread = max(1, len(TAG_LIST) // total_threads)
    # Calculate remainder for distributing extra tags
    remainder = len(TAG_LIST) % total_threads
    
    for process_id in range(num_processes):
        result[process_id] = {}
        for thread_id in range(num_threads):
            # Calculate the thread's global index
            thread_index = process_id * num_threads + thread_id
            
            # Calculate start index for this thread
            start_idx = thread_index * tags_per_thread
            # Add extra tags from remainder to earlier threads
            start_idx += min(thread_index, remainder)
            
            # Calculate end index for this thread
            # If this thread should get an extra tag from remainder, add 1
            extra = 1 if thread_index < remainder else 0
            end_idx = start_idx + tags_per_thread + extra
            end_idx = min(end_idx, len(TAG_LIST))
            
            # Assign tags to this thread
            if start_idx < len(TAG_LIST):
                result[process_id][thread_id] = TAG_LIST[start_idx:end_idx]
            else:
                result[process_id][thread_id] = []
    
    return result