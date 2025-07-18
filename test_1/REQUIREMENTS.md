# PLC Data Acquisition Service - Requirements

## Required Files

Ensure all these files are present in the same directory:

- `plc_data_acquisition_service.py` - Main script
- `db_config.py` - Database configuration
- `plc_config.py` - PLC connection settings
- `tag_config.py` - Tag list and distribution function

## Python Requirements

- Python 3.6 or higher
- Required packages:
  - pylogix (for Allen-Bradley PLC communication)
  - psycopg2 (for PostgreSQL database connection)
  - logging (standard library)
  - multiprocessing (standard library)
  - threading (standard library)
  - queue (standard library)
  - datetime (standard library)
  - os (standard library)
  - sys (standard library)

## Installation

Install required packages:

```bash
pip install pylogix psycopg2
```

## Configuration

### PLC Configuration

Verify in `plc_config.py`:
- PLC IP address is accessible from the target computer
- Processor slot is correct
- Timeout and retry settings are appropriate

### Database Configuration

Verify in `db_config.py`:
- Database server is accessible from the target computer
- Database credentials are correct
- Database and table exist or can be created

## Network Requirements

- Network access to PLC at IP address specified in `plc_config.py`
- Network access to PostgreSQL database server specified in `db_config.py`

## Running the Script

```bash
python plc_data_acquisition_service.py
```

The script will:
1. Create a `logs` directory if it doesn't exist
2. Initialize the database if needed
3. Start collecting data from the PLC
4. Log operations to both console and log files

## Troubleshooting

- If connection to PLC fails, verify IP address and network connectivity
- If database connection fails, verify database settings and credentials
- Check log files in the `logs` directory for detailed error messages