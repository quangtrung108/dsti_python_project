# DSTI - Python project group
# 📖 Introduction

This project focuses on cybersecurity data analysis, specifically preparing a network attack log for machine learning applications. The goal is to classify attack, identify attack type, and develop models to detect anomalies or malicious activity.

# DATASET

Dataset: cybersecurity_attacks.csv with 40,000 entries and 25 columns.

Data Content: Contains details such as source/destination IP, ports, protocols, packet lengths, and security alerts.

Initial Analysis: Checked data types, missing values, and data distribution. Some columns showed high cardinality (IP, payload data), while others had low variance and were deemed uninformative (e.g., Firewall Logs, IDS/IPS Alerts).

📊 Exploratory Data Analysis (EDA): Cleaning and analyzing network logs.

    Anomaly Detection (IQR Method): Identified outliers in destination ports, packet lengths, and anomaly scores.

    Correlation Analysis: Weak relationships among numerical features suggest limited linear dependencies.

    Attack Type Distribution: Balanced distribution of attack types (DDoS, Malware, Intrusion).

    Geolocation Analysis: No significant regional differences in network traffic patterns.


🔍 Feature Engineering: Extracting relevant features for model training.

    Handling Missing Values: Imputed missing values, excluding uniform columns.

    Timestamp Conversion: Converted timestamps, removed duplicates, and extracted time-based features.

    Feature Engineering: Created new features such as Is Source Private, Is Night Traffic, Destination Port Category to enhance predictive capability.

🤖 Machine Learning Modeling: Building models to classify attacks type.
    
    XGBoost: Best-performing model (~40% accuracy), though still low.

    Random Forest: Inferior to XGBoost, especially in distinguishing attack types.

    Logistic Regression: Simple model with the lowest accuracy (~33.8%).

💻 Streamlit App: A web interface for visualizing attack data and model predictions.
    
    Tool Used: Streamlit for building an interactive web interface.
## 📹 Video Demo
[![Demo Video](https://img.youtube.com/vi/tGoqZqluvN0/maxresdefault.jpg)](https://youtu.be/tGoqZqluvN0)
## 🚀 How to Run the Project

1.  Install the required Python libraries by running :

    ```bash
    pip install -r requirements.txt

2. Run EDA Notebook

    ```bash
    jupyter notebook ./EDA+ML/Cybersecurity_Analysis_Modeling-1.ipynb

## 🚀 Run the Streamlit app, follow these steps:

1. Install Streamlit (if you haven't already):

   ```bash
   pip install streamlit

2. Navigate to the directory where your app.py file is located.


3. Run the app with the following command
    
    ```bash
    streamlit run app.py

4. The app will open automatically in your default browser at http://localhost:8501. If not, open it manually.