import numpy as np
import pandas as pd
from datetime import datetime

class AssetDataGenerator:
    def __init__(self):
        # Establish realistic normal baseline operation parameters (Mean, Std Dev)
        self.baselines = {
            "HVAC": {
                "temperature": {"mean": 21.0, "std": 0.8},
                "vibration": {"mean": 2.1, "std": 0.4},
                "pressure": {"mean": 105.0, "std": 3.0},
                "current": {"mean": 38.0, "std": 1.5}
            },
            "Chiller": {
                "temperature": {"mean": 7.2, "std": 0.3},
                "vibration": {"mean": 1.5, "std": 0.2},
                "pressure": {"mean": 290.0, "std": 5.0},
                "current": {"mean": 155.0, "std": 4.0}
            },
            "Pump": {
                "temperature": {"mean": 45.0, "std": 2.0},
                "vibration": {"mean": 2.8, "std": 0.5},
                "pressure": {"mean": 50.0, "std": 1.2},
                "current": {"mean": 24.0, "std": 0.8}
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
            
        elif asset_type == "Pump":
            # Simulation: Bearing degradation / Cavitation
            # Massive friction spikes bearing temperature and mechanical vibration
            reading["temperature"] += (38.0 * severity)
            reading["vibration"] += (6.0 * severity)
            reading["pressure"] -= (15.0 * severity) # Loss of discharge pressure
            
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