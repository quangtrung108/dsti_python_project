import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Set the title
st.title("CSV Upload & Model Prediction")

# Upload CSV and Model File
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
uploaded_model = st.file_uploader("Upload Model File (.pkl)", type=["pkl"])

if uploaded_file is not None and uploaded_model is not None:
    try:
        # Read CSV file
        data = pd.read_csv(uploaded_file)

        # Convert timestamp column to datetime format
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        
        # Extracting time-based features
        data['Hour'] = data['Timestamp'].dt.hour
        data['DayOfWeek'] = data['Timestamp'].dt.dayofweek
        data['Month'] = data['Timestamp'].dt.month
        data['Year'] = data['Timestamp'].dt.year
        
        # Remove duplicate records
        data = data.drop_duplicates()
        
        # Transform "Severity Level" to numeric value
        severity_mapping = {"Low": 1, "Medium": 2, "High": 3}
        data["Severity Level Numeric"] = data["Severity Level"].map(severity_mapping)
        
        # Extract browser from "Device Information"
        data["Browser"] = data["Device Information"].str.split("/").str[0]
        
        # Function to extract OS type
        def extract_os(user_agent):
            user_agent = user_agent.lower()
            if "windows" in user_agent:
                return "Windows"
            elif "mac os" in user_agent or "macintosh" in user_agent:
                return "MacOS"
            elif "linux" in user_agent:
                return "Linux"
            elif "android" in user_agent:
                return "Android"
            elif "iphone" in user_agent or "ipad" in user_agent:
                return "iOS"
            else:
                return "Other"
        
        # Apply function to extract OS
        data['Operating System'] = data['Device Information'].apply(extract_os)
        
        # Identify private IPs
        private_ip_ranges = [10, 172, 192]
        data['Is Source Private'] = data['Source IP Address'].apply(lambda x: int(x.split('.')[0]) in private_ip_ranges).astype(int)
        data['Is Destination Private'] = data['Destination IP Address'].apply(lambda x: int(x.split('.')[0]) in private_ip_ranges).astype(int)
        
        # Convert ports to categorical types
        def categorize_port(port):
            if port <= 1023:
                return "Well-known"
            elif port <= 49151:
                return "Registered"
            else:
                return "Dynamic"
        
        data['Source Port Category'] = data['Source Port'].apply(categorize_port)
        data['Destination Port Category'] = data['Destination Port'].apply(categorize_port)
        
        # Create new time-based features
        data['Is Night Traffic'] = ((data['Hour'] >= 18) | (data['Hour'] <= 6)).astype(int)
        data['Is Weekend'] = data['DayOfWeek'].isin([6, 7]).astype(int)
        
        # Map "Attack Type" to numeric value
        attack_type_mapping = {"DDoS": 0, "Malware": 1, "Intrusion": 2}
        data["Attack Type Numeric"] = data["Attack Type"].map(attack_type_mapping)
        
        y_true = data["Attack Type Numeric"]
        df = data.drop(columns=["Attack Type", "Attack Type Numeric"])
        
        # Select relevant columns
        selected_columns = ["Protocol", "Packet Length","Packet Type","Traffic Type","Malware Indicators",
                            "Anomaly Scores","Alerts/Warnings","Attack Signature","Action Taken",
                            "Network Segment","Firewall Logs","IDS/IPS Alerts","Log Source","Hour","DayOfWeek","Month",
                            "Year","Severity Level","Browser","Operating System","Is Source Private","Is Destination Private",
                            "Source Port Category","Destination Port Category","Is Night Traffic","Is Weekend"]
        df = df[selected_columns]
        
        # One-Hot Encoding for categorical data
        categorical_columns = ["Protocol", "Packet Type","Traffic Type","Malware Indicators",
                               "Alerts/Warnings","Attack Signature","Action Taken",
                               "Network Segment","Firewall Logs","IDS/IPS Alerts","Log Source","Severity Level",
                               "Browser","Operating System",
                               "Source Port Category","Destination Port Category"]
        
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_array = encoder.fit_transform(df[categorical_columns])
        encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(categorical_columns))
        df = df.drop(columns=categorical_columns).reset_index(drop=True)
        df = pd.concat([df, encoded_df], axis=1)
        
        st.write("### Processed Data Preview:")
        st.write(df.head())
        
        # Load trained model
        model = joblib.load(uploaded_model)
        expected_features = model.get_booster().feature_names
        st.write(f"Expected features: {expected_features}")
        
        # Check for missing features
        missing_features = [col for col in expected_features if col not in df.columns]
        if missing_features:
            st.warning(f"Missing columns: {missing_features}")
            for col in missing_features:
                df[col] = 0
        
        # Reorder columns to match model's expected input
        df = df[expected_features]
        
        # Make predictions
        predictions = model.predict(df)
        df["Predictions"] = predictions
        
        # Display Predictions
        st.write("### Model Predictions:")
        st.write(df.head())
        
        # Plot Predictions Distribution
        st.write("### Prediction Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(df["Predictions"], bins=20, kde=True)
        plt.title("Prediction Distribution")
        st.pyplot(plt)
        
        # Evaluate Model
        y_pred = df['Predictions']
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')
        
        st.write("\n ### Optimized Model Evaluation Metrics:")
        st.write(f"Accuracy: {accuracy:.4f}")
        st.write(f"Precision: {precision:.4f}")
        st.write(f"Recall: {recall:.4f}")
        st.write(f"F1-Score: {f1:.4f}")
        
    except Exception as e:
        st.error(f"Error processing the files: {e}")
else:
    st.info("Please upload both a CSV file and a model (.pkl) file.")
