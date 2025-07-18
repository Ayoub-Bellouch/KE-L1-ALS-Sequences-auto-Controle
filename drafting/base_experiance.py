def ALS(commALS):
    print("start: collectALS")
    ALS = dict()
    ALS["time"] = datetime.datetime.utcnow() + timedelta(hours=1)
    # ALS["time"] = datetime.datetime.utcnow()
    
    # ## SS ## Simulation !
    # ALS.extend([123, 87, "Model X", 26.33])
    # return ALS
    # ## SS ##
    
    # Static Logic !
    #     EntryLif = commALS.Read("LI106_GLASS_counter").Value
    # Dynamic Logic !
    ALS["EntryLif_stats"] = commALS.Read("LI106_GLASS_counter_stats").Value
    # ALS["EntryLif_stats_ls"] = commALS.Read("LI106_GLASS_counter_stats_ls").Value
    
    # Static Logic !
    #     Exitlif = commALS.Read("LI202_SENDING_GLASS_counter").Value
    # Dynamic Logic !
    ALS["Exitlif_stats"] = commALS.Read("LI202_SENDING_GLASS_counter_stats").Value
    # ALS["Exitlif_stats_ls"] = commALS.Read("LI202_SENDING_GLASS_counter_stats_ls").Value
    
     # Static Logic !
    ALS["LiveALS_ModelName"] = commALS.Read("RCP_KINEMATIC_ACTUAL.NAME").Value
    
    # Static Logic !
    ALS["LiveALS_ModelCycle_Time"]  = commALS.Read("CV109_W.RCP.CYCLE_TIME").Value
    
    print("end: collecALS \n Values : ", ALS)
    return(ALS)


from plotly_resampler import FigureResampler
from dash.dependencies import Input, Output
from dash_extensions import WebSocket
import plotly.graph_objects as go
from dash import Dash, dcc, html
from psycopg2 import sql
from pylogix import PLC
from config import *
import pandas as pd
import websockets
import psycopg2
import datetime
import asyncio
import copy
import time
import json
import os


tags_list =  ["RCP_KINEMATIC_ACTUAL.NAME", "RCP_KINEMATIC_ACTUAL.NAME.DATA"]+\
             ["BR105_SEQUENCE", "BR111_SEQUENCE", "CV101_SEQUENCE", "CV102_SEQUENCE", "CV103_SEQUENCE"] +\
             [ "CV104_SEQUENCE", "CV104_SUB_SEQUENCE", "CV109_SEQUENCE", "CV112_SEQUENCE", "CV203_SEQUENCE"] +\
             [ "CV302_SEQUENCE", "CV303_SEQUENCE", "CV304_SEQUENCE", "CV403_SEQUENCE", "CV403_SUB_SEQUENCE"] +\
             [ "LI106_SEQUENCE", "LI110_SEQUENCE", "LI202_SEQUENCE", "LI401_SEQUENCE", "LI405_SEQUENCE"] +\
             [ "ONS_SEQUENCE1", "SH107_SEQUENCE", "SH201_SEQUENCE", "SH402_SEQUENCE", "SH404_SEQUENCE"]

commSource = PLC()
commSource.IPAddress= "10.212.49.130"
commSource.ProcessorSlot = 1

connection = psycopg2.connect(
        port     = 5432,
        host     = "RHKEN702",
        database = "P01GES",
        user     = "uwipuser",
        password = "P@ss1m1@n"
)

global global_df
global_df = pd.DataFrame()

def sequences_tracking(commSource, tags_list):
    Seq = dict()
    
    Seq["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Seq["values"] = dict()
    for tag in tags_list:
        value = commSource.Read(tag).Value
        Seq["values"].update({
                                f"{tag}": f"{value}"
                            }
                        )
    return Seq


def track_seq_changes_(commSource, tags_list):
    previous_values = {}

    while True:
        current_result = sequences_tracking(commSource, tags_list)
        time_value = current_result.get("time", "Unknown Time")
        current_values = {"values": current_result.get("values", {})}

        if current_values != previous_values:
            print({"time": time_value, **current_values})
            previous_values = current_values


## Insert to the Database:
db_params = {
                'dbname': 'P01GES',
                'user': 'uwipuser',
                'password': 'P@ss1m1@n',
                'host': 'RHKEN702',  
                'port': '5432'
            }

def sanitize_keys(data):
    """
    Sanitize dictionary keys by replacing periods with underscores and converting to lowercase.
    """
    return {k.replace('.', '_').lower(): v for k, v in data.items()}

def insert_data_to_db(conn, data):
    """
    Insert sanitized data into the als_entry_sequences table.
    """
    sanitized_data = sanitize_keys(data)
    
    # Define the table name
    table_name = 'als_entry_sequences'
    
    # Extract columns and values
    columns = sanitized_data.keys()
    values = [sanitized_data[column] for column in columns]
    
    # Create the SQL query
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, values)
        conn.commit()

def remove_key_temporarily(data, key):
    """Creates a deep copy of the JSON and removes the specified key for comparison."""
    temp_data = copy.deepcopy(data)  # Preserve original structure
    if isinstance(temp_data, dict):
        temp_data.pop(key, None)  # Remove key if present
    return temp_data

def track_seq_changes(commSource, tags_list):
    previous_values = {}

    # Establish database connection
    conn = psycopg2.connect(**db_params)

    try:
        while True:
            current_result = sequences_tracking(commSource, tags_list)
            time_value = current_result.get("time", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            current_values = current_result.get("values", {})
            current_values['time'] = time_value  # Add time to the current values
            
#             if remove_key_temporarily(current_values_, "time") != remove_key_temporarily(previous_values_, "time"):
            if current_values != previous_values:
                try:
                    if None in list(current_values.values()):
                        continue
                    else:
                        insert_data_to_db(conn, current_values)
                except Exception as e:
                    print(f"Error inserting data: {e}")
                
                previous_values = current_values
#                 print(previous_values)
#             time.sleep(1)  # Add a delay to prevent excessive CPU usage
    finally:
        conn.close()

track_seq_changes(commSource, tags_list)

