"""A script for running a fake data simulation study."""

from datetime import datetime
import os

import pandas as pd
from src.model_configurations_to_try import MODEL_CONFIGURATIONS
from src.fake_data_generation import generate_fake_measurements
from src.fitting import generate_samples


# Where to save fake data
FAKE_DATA_DIR = os.path.join("data", "fake")
REAL_DATA_DIR = os.path.join("data", "prepared")


def main():
    """Run a simulation study."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    study_name = f"sim_study-{now}"
    print("Generating fake data...")
    real_data = pd.read_csv(os.path.join(REAL_DATA_DIR, "scores_prepared.csv"))
    measurements = generate_fake_measurements(real_data)
    fake_data_file = os.path.join(FAKE_DATA_DIR, f"fake_data-{study_name}.csv")
    print(f"Writing fake data to {fake_data_file}")
    measurements.to_csv(fake_data_file)
    generate_samples(study_name, measurements, MODEL_CONFIGURATIONS)


if __name__ == "__main__":
    main()
