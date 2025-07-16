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

## TODO 
    PLC Remarques: 
    - ip adress 10.212.49.130
    - Only tags with Nomination LLNNN_SEQUENCE

    Dev Sequences; 
    - Get ASCCI Codefication for decoding data, (better visualisation only, data training or AI involving needs to be numerical)