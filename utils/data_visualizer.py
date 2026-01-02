"""
SignSpeak - Data Visualization Utilities
Tools for visualizing sensor data and model performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import ML_DATASET_PATH

def plot_sensor_data(csv_file: str, gesture_label: str = None):
    """
    Plot sensor data from CSV file
    
    Args:
        csv_file: Path to CSV file
        gesture_label: Optional gesture label to filter
    """
    df = pd.read_csv(csv_file)
    
    if gesture_label:
        df = df[df['label'] == gesture_label]
    
    # Plot flex sensor data
    flex_cols = [col for col in df.columns if 'flex' in col.lower() or any(f in col.lower() for f in ['thumb', 'index', 'middle', 'ring', 'pinky'])]
    
    if flex_cols:
        plt.figure(figsize=(12, 6))
        for col in flex_cols[:5]:  # First 5 flex sensors
            if '_mean' in col:
                plt.plot(df[col], label=col.replace('_mean', ''))
        plt.xlabel('Sample')
        plt.ylabel('Value')
        plt.title('Flex Sensor Data')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_gesture_distribution(dataset_path: Path = None):
    """
    Plot distribution of gestures in dataset
    
    Args:
        dataset_path: Path to dataset directory
    """
    if dataset_path is None:
        dataset_path = ML_DATASET_PATH
    
    # Load all CSV files
    dataframes = []
    for file in dataset_path.glob("*_dynamic.csv"):
        df = pd.read_csv(file)
        dataframes.append(df)
    
    if not dataframes:
        print("No dataset files found!")
        return
    
    data = pd.concat(dataframes, ignore_index=True)
    
    # Count gestures
    gesture_counts = data['label'].value_counts()
    
    # Plot
    plt.figure(figsize=(10, 6))
    gesture_counts.plot(kind='bar')
    plt.xlabel('Gesture')
    plt.ylabel('Number of Samples')
    plt.title('Gesture Distribution in Dataset')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()
    
    print(f"\nTotal samples: {len(data)}")
    print(f"Gestures: {list(gesture_counts.index)}")
    print(f"\nSample counts:")
    for gesture, count in gesture_counts.items():
        print(f"  {gesture}: {count}")

def plot_model_accuracy_history():
    """Plot model training accuracy over time (if available)"""
    # This would require saving training history
    # Placeholder for future implementation
    pass

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize SignSpeak data")
    parser.add_argument("--plot-sensors", type=str, help="CSV file to plot")
    parser.add_argument("--plot-distribution", action="store_true", help="Plot gesture distribution")
    
    args = parser.parse_args()
    
    if args.plot_sensors:
        plot_sensor_data(args.plot_sensors)
    elif args.plot_distribution:
        plot_gesture_distribution()
    else:
        print("Use --plot-sensors <file> or --plot-distribution")

