"""Run or review the reproducible experiment for Assignment 3, Question 6.

Default: restore completed metrics and the 20-grid + 20-random search results.
Use --retrain to execute all 40 GRU hyperparameter trials again.
"""
import argparse
from assignment_experiments import q6_metrics_and_search

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--retrain", action="store_true", help="rerun the 40 hyperparameter-search trials")
    args = parser.parse_args()
    q6_metrics_and_search(retrain=args.retrain)
