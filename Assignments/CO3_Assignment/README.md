# Deep Learning Assignment 3 – Code and Reproducible Results

This package contains the Python programs, executed result files, plots and architecture diagrams used in the accompanying solved report.

## Requirements

- Python 3.10 or newer
- numpy, pandas, matplotlib, torch, scikit-learn

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Run all questions

```bash
python run_all.py
```

The launcher executes Q1, Q2, Q4 and Q5 again. Q3, Q6 and Q7 restore the completed long-running measurements packaged in `results/` by default, so the full run is practical on a CPU-only computer.

Run one question using `python q1_experiment.py` through `python q7_experiment.py`.

For optional full retraining of the longer experiments:

```bash
python q3_experiment.py --retrain
python q6_experiment.py --retrain
python q7_experiment.py --retrain
```

Q3 repeats the 12 RNN/LSTM/GRU lag configurations. Q6 repeats the 20 grid-search and 20 random-search GRU trials, plus the overfitting diagnostic. Q7 retrains the lag-aware model and the direct 2,016-step LSTM baseline; the direct baseline is CPU-intensive.

## Data and limitations

Synthetic data is used for the metro time series, delayed-trigger task, review-like sentiment task and fraud task. The assignment permits synthetic hourly data for Q1 and synthetic imbalanced sequences for Q6. Q4 asks for a public review-sentiment corpus such as IMDB; the runtime could not obtain that corpus, so Q4 uses a clearly labelled synthetic review-like dataset instead. These scores must not be described as IMDB results. Replace the synthetic Q4 corpus with the required public dataset before final submission if the lecturer requires it.

Q6 includes a 2% fraud dataset, a top-50 alert policy, a numerically unstable loss demonstration and a GRU overfitting demonstration (100% training accuracy versus 58% validation accuracy on independent random-label sequences). The cached CSV/JSON files and figures preserve the measured outcomes used in the report.

## Reproducibility

The complete implementation is in `assignment_experiments.py`. Fixed seeds are used throughout. `results/` contains numerical outputs, metrics, parameter counts, gradient norms, hyperparameter-search records and diagnostic outputs. `figures/` contains the plots and architecture diagrams inserted into the report.

The Q3 longest-lag GRU was executed separately to avoid accumulated recurrent-workspace pressure in one long process. The Q3, Q6 and Q7 default launchers restore their completed packaged measurements; use the `--retrain` options above to repeat those longer runs. Measured wall-clock times and CPU latency depend on the hardware and runtime. They are not guarantees for a different laptop, station kiosk or production deployment.
