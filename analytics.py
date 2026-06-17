import numpy as np
import pandas as pd

class AssetPredictiveEngine:
    def __init__(self):
        # Define baseline operational thresholds based on MEP engineering standards
        self.thresholds = {
            "HVAC": {
                "temperature": {"warn": 24.0, "critical": 28.0},  # °C
                "vibration": {"warn": 4.5, "critical": 7.1},     # mm/s (ISO 10816)
                "pressure": {"warn": 120.0, "critical": 150.0},  # PSI
                "current": {"warn": 45.0, "critical": 55.0}      # Amps
            },
            "Chiller": {
                "temperature": {"warn": 9.0, "critical": 12.0},   # Chilled water outlet °C
                "vibration": {"warn": 3.5, "critical": 5.5},
                "pressure": {"warn": 320.0, "critical": 380.0},  # High-pressure side PSI
                "current": {"warn": 180.0, "critical": 210.0}
            },
            "Pump": {
                "temperature": {"warn": 65.0, "critical": 80.0},  # Bearing temp °C
                "vibration": {"warn": 5.0, "critical": 8.5},
                "pressure": {"warn": 60.0, "critical": 75.0},   # Discharge PSI
                "current": {"warn": 30.0, "critical": 38.0}
            }
        }

    def analyze_sensor_reading(self, asset_type: str, sensor_data: dict) -> dict:
        """
        Processes a single frame of sensor data, calculates anomalies, 
        and computes an overall asset health score.
        """
        if asset_type not in self.thresholds:
            raise ValueError(f"Unknown asset type: {asset_type}")
            
        asset_rules = self.thresholds[asset_type]
        sensor_status = {}
        penalty_points = 0
        
        # 1. Evaluate individual sensors against threshold bands
        for sensor, value in sensor_data.items():
            if sensor not in asset_rules:
                continue
                
            warn_limit = asset_rules[sensor]["warn"]
            crit_limit = asset_rules[sensor]["critical"]
            
            if value >= crit_limit:
                status = "CRITICAL"
                penalty_points += 25
            elif value >= warn_limit:
                status = "WARNING"
                penalty_points += 10
            else:
                status = "NORMAL"
                
            sensor_status[sensor] = {
                "value": round(value, 2),
                "status": status
            }
            
        # 2. Calculate Composite Health Score (Starts at 100, decays based on penalties)
        # We cap the health score between 0 and 100
        health_score = max(0, 100 - penalty_points)
        
        # 3. Determine Overall Asset Status
        if health_score <= 50:
            overall_status = "Critical Failure Risk"
        elif health_score <= 85:
            overall_status = "Maintenance Required"
        else:
            overall_status = "Healthy"
            
        return {
            "asset_type": asset_type,
            "sensor_analysis": sensor_status,
            "health_score": health_score,
            "status": overall_status
        }

    def detect_statistical_anomalies(self, history_df: pd.DataFrame, rolling_window: int = 10) -> pd.DataFrame:
        """
        Moving beyond static thresholds: detects statistical anomalies (drifts/spikes)
        using a rolling Z-score method. Perfect for showcasing Phase 3 potential to your CTO.
        """
        if len(history_df) < rolling_window:
            return history_df # Not enough data yet to calculate rolling stats
            
        # Clone df to avoid modifying original data
        df_analyzed = history_df.copy()
        
        numeric_cols = [c for c in history_df.columns if c not in ['timestamp', 'asset_id', 'asset_type']]
        
        for col in numeric_cols:
            # Calculate rolling mean and standard deviation
            rolling_mean = df_analyzed[col].rolling(window=rolling_window, min_periods=1).mean()
            rolling_std = df_analyzed[col].rolling(window=rolling_window, min_periods=1).std()
            
            # Avoid division by zero if variance is zero
            rolling_std = rolling_std.replace(0, 0.001)
            
            # Z-Score calculation
            z_score = (df_analyzed[col] - rolling_mean) / rolling_std
            
            # Flag statistical anomalies (where reading is > 2.5 standard deviations away)
            df_analyzed[f"{col}_zscore_anomaly"] = np.abs(z_score) > 2.5
            
        return df_analyzed