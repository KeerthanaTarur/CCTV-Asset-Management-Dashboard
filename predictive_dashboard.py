import streamlit as st
import pandas as pd
import time
from data_generator import AssetDataGenerator
from analytics import AssetPredictiveEngine

# 1. Initialize Page Setup and Frameworks
st.set_page_config(page_title="Industrial Asset Predictive Maintenance", layout="wide")
st.title("Enterprise Asset Health & Predictive Maintenance Dashboard")
st.markdown("---")

# Initialize backend classes in session state to persist data across reruns
if "generator" not in st.session_state:
    st.session_state.generator = AssetDataGenerator()
if "engine" not in st.session_state:
    st.session_state.engine = AssetPredictiveEngine()

# 2. Sidebar Configuration Controls
st.sidebar.header("Dashboard Configurations")
selected_asset = st.sidebar.selectbox("Select Asset to Monitor", ["HVAC", "Chiller", "Pump"])

st.sidebar.markdown("---")
st.sidebar.subheader(" Simulation Controls")
# This toggle allows you to simulate failure modes to the CTO on demand
inject_fault = st.sidebar.toggle("Inject Mechanical Fault Pattern")

if inject_fault:
    fault_severity = st.sidebar.slider("Fault Severity Multiplier", 0.1, 1.0, 0.5, step=0.1)
    st.sidebar.warning(f" Injecting live failure anomaly (Severity: {fault_severity})")
else:
    fault_severity = 0.0

# Initialize an in-memory historical queue for charts if it doesn't exist
if f"history_{selected_asset}" not in st.session_state:
    # Seed with 30 periods of historical normal data so charts aren't blank at launch
    st.session_state[f"history_{selected_asset}"] = st.session_state.generator.generate_historical_batch(selected_asset, 30)

# 3. Stream Live Ingestion Frame
# Generate either a normal stream or an anomaly stream based on sidebar toggle
if inject_fault:
    new_reading = st.session_state.generator.generate_fault_reading(selected_asset, fault_severity)
else:
    new_reading = st.session_state.generator.generate_normal_reading(selected_asset)

# Run the raw metrics through the Analytics Predictive Engine
analysis_results = st.session_state.engine.analyze_sensor_reading(selected_asset, {
    k: v for k, v in new_reading.items() if k not in ['timestamp', 'asset_type']
})

# Append new live data frame to our historical tracking data frame
new_row_df = pd.DataFrame([new_reading])
history_df = st.session_state[f"history_{selected_asset}"]
history_df = pd.concat([history_df, new_row_df], ignore_index=True).tail(50) # Maintain rolling window of 50
st.session_state[f"history_{selected_asset}"] = history_df

# Run statistical Z-score anomaly scanning on our historical data
history_with_anomalies = st.session_state.engine.detect_statistical_anomalies(history_df)

# 4. UI Layout: Top Tier Metric Callouts
score = analysis_results["health_score"]
status = analysis_results["status"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Monitored Asset Class", value=selected_asset)
with col2:
    # Dynamically change metric colors depending on severity state
    if score > 85:
        st.metric(label="Composite Health Score", value=f"{score}/100", delta="Healthy")
    elif score > 50:
        st.metric(label="Composite Health Score", value=f"{score}/100", delta="- Warning Status", delta_color="inverse")
    else:
        st.metric(label="Composite Health Score", value=f"{score}/100", delta="- Critical Failure Risk", delta_color="inverse")
with col3:
    st.metric(label="Operational Assessment", value=status)

st.markdown("---")

# 5. UI Layout: Middle Tier Raw Metrics & Alerts Grid
st.subheader("Live Sensor Telemetry feeds")
sensor_cols = st.columns(4)
sensors_list = list(analysis_results["sensor_analysis"].keys())

for idx, sensor_name in enumerate(sensors_list):
    sensor_data = analysis_results["sensor_analysis"][sensor_name]
    with sensor_cols[idx]:
        st.metric(
            label=sensor_name.upper(), 
            value=sensor_data["value"], 
            delta=None if sensor_data["status"] == "NORMAL" else sensor_data["status"],
            delta_color="normal" if sensor_data["status"] == "NORMAL" else "inverse"
        )

# 6. UI Layout: Bottom Tier Historical Real-time Charts
st.markdown("---")
st.subheader(" Historical Trends & Statistical Anomaly Tracking (Z-Score)")

# Create side-by-side charts tracking asset states over time
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Thermal & Mechanical Load Profiles**")
    st.line_chart(history_with_anomalies.set_index("timestamp")[["temperature", "vibration"]])

with chart_col2:
    st.markdown("**Pressure & Current Profiles**")
    st.line_chart(history_with_anomalies.set_index("timestamp")[["pressure", "current"]])

# Force a 1-second delay and refresh the dashboard loop automatically to mimic live streams
time.sleep(1)
st.rerun()