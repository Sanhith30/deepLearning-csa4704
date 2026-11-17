"""Run or review the reproducible experiment for Assignment 3, Question 3.

Default: load the completed 12-run measurement table and regenerate the figure.
Use --retrain to execute the full 60-epoch sweep again (this is CPU intensive).
"""
import argparse
from assignment_experiments import q3_lag_experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrain", action="store_true", help="retrain every RNN/LSTM/GRU lag configuration")
    args = parser.parse_args()
    q3_lag_experiment(retrain=args.retrain)
