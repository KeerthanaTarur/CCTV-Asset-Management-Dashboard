import numpy as np
import pandas as pd
from datetime import datetime

class AssetDataGenerator:
    def __init__(self):
        # Establish realistic normal baseline operation parameters (Mean, Std Dev)
        self.baselines = {
            "CNC Milling Machine": {
                "temperature": {"mean": 33.0, "std": 1.5},
                "vibration": {"mean": 3.0, "std": 0.5},
                "pressure": {"mean": 85.0, "std": 4.0},
                "current": {"mean": 42.0, "std": 2.0}
            },
            "Robotic Arm": {
                "temperature": {"mean": 28.0, "std": 1.0},
                "vibration": {"mean": 2.5, "std": 0.3},
                "pressure": {"mean": 40.0, "std": 1.0},
                "current": {"mean": 18.0, "std": 1.0}
            },
            "Hydraulic Press": {
                "temperature": {"mean": 55.0, "std": 2.5},
                "vibration": {"mean": 4.0, "std": 0.6},
                "pressure": {"mean": 220.0, "std": 8.0},
                "current": {"mean": 70.0, "std": 3.0}
            }
        }

    def generate_normal_reading(self, asset_type: str) -> dict:
        """Generates a single time-step of steady-state operational data."""
        if asset_type not in self.baselines:
            raise ValueError(f"Unknown asset type: {asset_type}")
            
        specs = self.baselines[asset_type]
        reading = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "asset_type": asset_type
        }
        
        # Draw values from a normal (Gaussian) distribution
        for sensor, params in specs.items():
            reading[sensor] = np.random.normal(params["mean"], params["std"])
            
        return reading

    def generate_fault_reading(self, asset_type: str, severity: float) -> dict:
        """
        Generates data simulating an ongoing mechanical failure pattern.
        Severity acts as a multiplier (0.0 to 1.0) to ramp up the fault over time.
        """
        # Start with a standard normal reading
        reading = self.generate_normal_reading(asset_type)
        
        # Inject specific domain engineering failure modes
        if asset_type == "HVAC":
            # Simulation: Airflow restriction / Fan imbalance
            # Causes gradual temperature drift and severe spikes in vibration
            reading["temperature"] += (6.0 * severity)
            reading["vibration"] += (5.5 * severity)
            reading["current"] += (15.0 * severity) # Motor works harder
            
        elif asset_type == "Chiller":
            # Simulation: Refrigerant leak or condenser fouling
            # Causes pressure to skyrocket and thermal cooling efficiency to decay
            reading["pressure"] += (95.0 * severity)
            reading["temperature"] += (5.0 * severity)
            reading["current"] += (60.0 * severity)
            
        elif asset_type == "Robotic Arm":
            # Simulation: Joint actuator overload and servomotor drift
            reading["temperature"] += (10.0 * severity)
            reading["vibration"] += (3.5 * severity)
            reading["current"] += (8.0 * severity)
            reading["pressure"] += (5.0 * severity)
        elif asset_type == "Hydraulic Press":
            # Simulation: Fluid contamination or cylinder seal degradation
            reading["pressure"] += (40.0 * severity)
            reading["temperature"] += (18.0 * severity)
            reading["vibration"] += (3.0 * severity)
            reading["current"] += (12.0 * severity)
        elif asset_type == "CNC Milling Machine":
            # Simulation: Tool wear / spindle imbalance
            reading["temperature"] += (12.0 * severity)
            reading["vibration"] += (4.5 * severity)
            reading["current"] += (10.0 * severity)
            reading["pressure"] += (8.0 * severity)
            
        return reading

    def generate_historical_batch(self, asset_type: str, timesteps: int = 50) -> pd.DataFrame:
        """
        Generates a clean historical baseline dataframe.
        Useful for seeding charts when the Streamlit app first loads.
        """
        records = []
        base_time = time_step = pd.Timestamp.now() - pd.Timedelta(minutes=timesteps)
        
        for i in range(timesteps):
            reading = self.generate_normal_reading(asset_type)
            # Override string timestamp with historical incremental timestamp
            reading["timestamp"] = (base_time + pd.Timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
            records.append(reading)
            
        return pd.DataFrame(records)