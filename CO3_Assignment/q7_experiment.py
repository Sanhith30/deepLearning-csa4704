"""Run or review the reproducible experiment for Assignment 3, Question 7.

Default: restore the completed measurements saved with this package.
Use --retrain to train the lag-aware model and the full 2,016-step LSTM baseline.
"""
import argparse
from assignment_experiments import q7_long_horizon_experiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrain", action="store_true", help="retrain the long-horizon models")
    args = parser.parse_args()
    q7_long_horizon_experiment(retrain=args.retrain)
