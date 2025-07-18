# main.py
import sys
import os

# Add test_1 directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'test_1'))

# Import the PLC data acquisition service
from plc_data_acquisition_service import main as plc_data_main

def main():
    """
    Entry point of the application.
    Add your main logic here.
    """
    # Your other main logic can go here
    
    # Run the PLC data acquisition service
    run_plc_service()


# Function to run the PLC data acquisition service
def run_plc_service():
    plc_data_main()


if __name__ == "__main__":
    main()
    
# add comment !