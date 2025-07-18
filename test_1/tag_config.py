# Configuration file for PLC tags

# List of all tags to be monitored
TAG_LIST = [
    # Sequence tags from base_experiance
    "tag_ids"
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