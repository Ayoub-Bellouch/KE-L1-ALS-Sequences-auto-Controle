# Database configuration settings

# PostgreSQL connection parameters
DB_PARAMS = {
    'dbname': 'P01GES',
    'user': 'uwipuser',
    'password': 'P@ss1m1@n',
    'host': 'RHKEN702',
    'port': '5432'
}

# Table name for storing tag readings
TABLE_NAME = 'Table name'

# Function to create database tables if they don't exist
def initialize_database(conn):
    """Create necessary database tables if they don't exist"""
    try:
        cursor = conn.cursor()
        
        # Create table for tag readings if it doesn't exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                time TIMESTAMP NOT NULL,
                process_id INTEGER,
                thread_id INTEGER,
                tag_name TEXT,
                value TEXT,
                value_type TEXT
            )
        """)
        
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False