# ALS Furnace Anomaly Detection Project

## Overview

This project aims to revolutionize the monitoring and maintenance of the Advanced Lamination System (ALS) Furnace in automotive glass production. By leveraging high-frequency data from conveyor sequences and advanced anomaly detection techniques, we seek to minimize production downtime, reduce waste, and enhance overall operational efficiency.

## Problem Description

The ALS (Advanced Lamination System) Furnace is a critical component in the production line that shapes automotive glass through a sophisticated thermal process. With 2500 electrical resistances across 20 zones and 500 thermocouples for monitoring, this system processes glass through preheating, shaping, and cooling phases to create precisely formed windshields. As the production line's bottleneck, any furnace stoppage directly impacts overall productivity.

Currently, we face significant challenges in responding effectively to system failures, which affects our ability to maintain consistent production flow:

*   Lack of a centralized view of failure causes across the system
*   Difficulty in analyzing and understanding failure trends and correlations
*   Limited tools to support fast, data-driven decision-making

As a result, identifying the root cause of stoppages takes too long, leading to extended downtime, higher scrap, and increased energy consumption.

## Project Objectives

Our objective is to build a system that enables real-time monitoring, intelligent failure detection, and better decision-making across the production line. We aim to:

*   Develop a centralized monitoring system for the convoying system of the ALS furnace
*   Automate data collection and visualization of all key sequences and sensor conditions
*   Enable easy exploration of historical data through smart dashboards
*   Automatically retrieve and structure data (CSV, JSON, logs) for AI readiness
*   Identify recurring failure patterns using virtual traceability (linked to zones, components, or conditions)
*   Improve quality control by reacting faster to anomalies
*   Ultimately, reduce downtime, scrap rates, and energy costs, while delivering more consistent product quality.

## Scope

This project focuses on the ALS furnace and aims to implement a system for data collection, analysis, visualization, and alerting. It will cover the development of tools to process historical and real-time data, define sequence logic and sensor conditions, and support the detection of abnormal behavior. The scope is limited to monitoring and diagnostic support and does not include changes to the furnace’s automation or control systems.

## Key Features (Based on our discussions)

*   **High-Frequency Data Ingestion:** Capable of processing data at speeds up to 10 times per second to capture all critical events.
*   **Sequence Passport Concept:** A structured definition of normal and abnormal conveyor sequences, enabling precise anomaly detection.
*   **Advanced Anomaly Detection Algorithms:** Utilizing state-of-the-art machine learning and deep learning models (e.g., LSTM, GRU, Autoencoders, GNNs) to identify subtle deviations from normal operational patterns.
*   **Multivariate Correlation Analysis:** Ability to detect anomalies arising from complex interdependencies between different sensors and sequences.
*   **Real-time Alerting:** Providing immediate notifications to operators upon anomaly detection.
*   **Interactive Dashboards:** For historical data exploration, visualization of sequence patterns, and anomaly insights.
*   **Focus on Minimizing False Positives:** Strategies to ensure that detected anomalies are truly meaningful and actionable.

## Technologies (Potential Stack)

*   **Data Storage:** PostgreSQL (for time-series data)
*   **Data Processing:** Python (Pandas, NumPy)
*   **Machine Learning:** Scikit-learn, TensorFlow/Keras, PyTorch
*   **Visualization:** Dash, Plotly, Grafana
*   **Data Ingestion:** PLC/OPC interfaces

## Getting Started

*(This section will provide instructions on how to set up the project locally, install dependencies, and run initial scripts. Details to be added later.)*

## Contribution

*(This section will outline guidelines for contributing to the project, including coding standards, pull request process, etc. Details to be added later.)*

## License

*(This section will specify the project's license. Details to be added later.)*

## Understqnding our data 
RCP_KINEMATIC_ACTUAL_NAME_DATA : ALS_receipt 
CV104_SEQUENCE : CV_104
R20_DI02_6 : Return C/V1 End Cart Detect PH46 R20_DI02.6
R20_DI02_4 : Return C/V1 reduce PH13  R20_DI02.4
R24_DI03_4 : Dist.C/V CartDet.(Ret.CV1side) PH12 R24_DI03.4
R20_DI02_7 : Return C/V2 End Cart Detect PH45 R20_DI02.7
R20_DI03_1 : Return C/V3 Cart Detect PH14 R20_DI03.1
R20_DI03_3 : Return C/V4 Cart Det. (Hoist)PH16 R20_DI03.3
R20_DI03_2 : Return C/V4 Cart Det. (Lifter)PH15 R20_DI03.2
R20_DI05_7 : Ret.C/V4 Cart Lift-Upper Down PR R20_DI05.7
R20_DI06_1 : Ret.C/V4 Cart Lift-Lower Down PR R20_DI06.1
R20_DI04_4 : Ret.CV4 Cart Alignment L Pull PR R20_DI04.4
R20_DI04_5 : Ret.CV4 Cart Alignment R Pull PR  R20_DI04.5
R20_DI06_4 : Return C/V4 Stopper L (1450) PR R20_DI06.4
R20_DI06_5 : Return C/V4 Stopper R (1450) PR R20_DI06.5
R20_DI06_6 : Return C/V4 Stopper (1250) PR R20_DI06.6
R20_DI04_0 : Return C/V3 Cart Lifter-L Up PR R20_DI04.0
R20_DI04_2 : Return C/V3 Cart Lifter-R Up PR R20_DI04.2
R20_DI05_6 : Ret.C/V4 Cart Lifter-Upper Up PR R20_DI05.6
R20_DI06_0 : Ret.C/V4 Cart Lifter-Lower Up PR R20_DI06.0
R20_DI04_3 : Return C/V3 Cart Lifter-R Down P R20_DI04.3
R20_DI04_1 : Return C/V3 Cart Lifter-L Down P R20_DI04.1
R20_DI04_6 : ReturnCV4 Cart Stopper L UP PR R20_DI04.6
R20_DI04_7 : ReturnCV4 Cart Stopper R UP PR R20_DI04.7
R20_DI12_5 : Loading table cart detection R20_DI12.5
R20_DI01_0 : 1st Corner Small Cart Detect L R20_DI01.0
R20_DI01_1 : 1st Corner Large Cart Detect R R20_DI01.1
R20_DI01_6 : Loading Table Down Pos. PR R20_DI01.6
R23_DI03_4 : Separator Down PR R23_DI03.4
R24_DI03_3 : Distribution C/V Cart Detect PH11 R24_DI03.3
R23_DI04_0 : Exit Pos. 2nd Corner Detect PH4 R23_DI04.0
R24_DI03_2 : Dist.C/V Cart Det.(Buffer CV) PH10 R24_DI03.2
R20_DI03_5 : Return C/V3 reduce PH R20_DI03.5
R23_DI04_7 : Cooling C/V 1Pitch Detect R23_DI04.7
R24_DI01_4 : Cart Alignment Complete L PR R24_DI01.4
R24_DI01_5 : Cart Alignment Complete R PR R24_DI01.5
R24_DI01_0 : Exchange C/V Area Cart Detect PH5 R24_DI01.0
R24_DI01_2 : Exchange C/V Alignment Pull PR R24_DI01.2
R24_DI01_3 : Cart Alignment Complete Side PR R24_DI01.3
R24_DI02_4 : ExitLifterCV Cart Det.(Exc.CV)PH6 R24_DI02.4
R24_DI02_1 : ExitLifterCV CART DETECT(BUFFER) PH8 R24_DI02.1
R24_DI02_5 : ExitLifterCV Cart Det.(Lower)PH7 R24_DI02.5
R24_DI02_6 : ExitLifterCV Cart Det.(Buf.CV)PH9 R24_DI02.6
R24_DI01_6 : ExitLifterCV StopperL Down(Ent.) R24_DI01.6 
R24_DI01_7 : ExitLifterCV StopperR Down(Ent.) R24_DI01.7
R24_DI02_0 : ExitLifterCV StopperDownExit1250 R24_DI02.0
R24_DI02_2 : ExitLifterCV StopperL DnExit1450  PR R24_DI02.2
R24_DI02_3 : ExitLifterCV StopperR DnExit1450 PR R24_DI02.3
R24_DI03_1 : Buffer C/V Cart Lifter Down RR R24_DI03.1
R81_DI01_1 : STB12 RE INSERT CART OF BUFFER C/V PB R81_DI01.1
R81_DI01_2 : STB12  OUTSIDE CART OF BUFFER C/V PB R81_DI01.2
R25_DI01_0 : Ent.Exc.Lifter CartDet.(Upper)PH R25_DI01.0
R25_DI02_1 : Entrance Stock Fork Down PR R25_DI02.1
R25_DI02_4 : Stock C/V Ent. Stopper Down PR R25_DI02.4
R25_DI02_0 : Entrance Stock Fork Up PR R25_DI02.0
R25_DI02_5 : Stock C/V Alignment L Pull PR R25_DI02.5
R25_DI02_6 : Stock C/V Alignment R Pull PR R25_DI02.6
R25_DI02_3 : Entrance Stock Fork Cart Detect R25_DI02.3
R24_DI04_5 : Exit Stock Fork Cart Detect PH R24_DI04.5
R24_DI04_1 : StockC/V CartDet.(ExitLifterI/L) R24_DI04.1
R24_DI04_4 : Exit Stock Fork Cart END Detect PH R24_DI04.4
R25_DI01_6 : StockC/V CartDet.(Ent.LifterI/L) R25_DI01.6
R25_DI02_2 : Entrance Stock Fork END Cart Det. PH R25_DI02.2
R24_DI04_3 : Exit Stock Fork Down PR R24_DI04.3
R25_DI02_7 : Stock C/V cart detect speed down R25_DI02.7
R25_DI01_4 : RESERVE R25_DI01.4
R24_DI04_6 : Stock C/V Exit Stopper Down PR R24_DI04.6
R24_DI04_2 : Exit Stock Fork Up PR R24_DI04.2
R24_DI04_0 : ExitExc.Lifter CartDet.(Upper)PH R24_DI04.0
R20_DI03_4 : Return C/V2 reduce PH R20_DI03.4
SECT100_AUTO : SECT100_AUTO
SECT100_START : SECT100_START
CV104_FAULT : CV104_FAULT 
LI401_UD_R_POS_1_OK : LI401_UD_R.POS_1_OK
LI401_SAFE_CV104 : LI401_SAFE_CV104
CV104_2_CART_RDY : CV104_2_CART_RDY 
ALWAYS_ON : ALWAYS_ON
CV104_2_BUSY : CV104_2_BUSY 
CV104_SEARCH_DN : CV104_SEARCH.DN
CV104_PARK_ON : CV104_PARK_ON 
LI401_MOVE_RQ_CV104 :  LI401_MOVE_RQ_CV104
CV103_RTS_CV104 :  CV103_RTS_CV104
SECT100_PROD : SECT100_PROD
CV112_SYNC_CV104_RQ : CV112_SYNC_CV104_RQ
LI401_RTS_CV104 : LI401_RTS_CV104
CV101_FREE : CV101_FREE
CV102_FREE : CV102_FREE 
CV103_FREE : CV103_FREE  
PARKING_MODE_CV : PARKING_MODE_CV 
MODE_EXCHANGE_PROD_STOCK1 : MODE_EXCHANGE_PROD_STOCK1
TRACK_CV104[1]_DEST1 : TRACK_CV104[1].DEST1
TRACK_CV104[1]_DEST2 : TRACK_CV104[1].DEST2
TRACK_CV104[1]_DEST4 : TRACK_CV104[1].DEST4
TRACK_CV104[1]_DEST8 : TRACK_CV104[1].DEST8
TRACK_CV104[1]_LARGE : TRACK_CV104[1].LARGE
CV104_SLIDING_TIME_DN : CV104_SLIDING_TIME.DN
CV104_CENTERING_TIME_DN :  CV104_CENTERING_TIME.DN
CV104_STEP2_DONE : CV104_STEP2_DONE
CV104_TAK_TIME_DN : CV104_TAK_TIME.DN
LI401_LIFTING_CV104 : LI401_LIFTING_CV104
CV104_MAG_CV112_OK : CV104_MAG_CV112_OK
LI401_SD_CV104 : LI401_SD_CV104
CV104_STEP3_DONE : CV104_STEP3_DONE
CV112_SYNC_CV104_OK : CV112_SYNC_CV104_OK
CV101_SYNC_CV104_OK : CV101_SYNC_CV104_OK
CV102_SYNC_CV104_OK : CV102_SYNC_CV104_OK
CV103_SYNC_CV104_OK : CV103_SYNC_CV104_OK
CV112_PARK_ON : CV112_PARK_ON
CV112_PARK_ON : CV112_PARK_ON
CV102_PARK_ON : CV102_PARK_ON 
CV103_PARK_ON : CV103_PARK_ON
CV104_EMPTY_DN : CV104_EMPTY.DN 
CV104_STOP_TIME_DN : CV104_STOP_TIME.DN
CV104_STEP1_DONE : CV104_STEP1_DONE
PARKING_OFF : PARKING_OFF   


## TODO 
    PLC Remarques: 
    - ip adress 10.212.49.130
    - Only tags with Nomination LLNNN_SEQUENCE

    Dev Sequences; 
    - Get ASCCI Codefication for decoding data, (better visualisation only, data training or AI involving needs to be numerical)