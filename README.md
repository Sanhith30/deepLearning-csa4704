# Deep Learning — CSA4704

This repository contains coursework, laboratory experiments, assignment reports,
notebooks, generated results, and the CSA4704 ECG screening capstone.

## Repository layout

| Folder | Contents |
| --- | --- |
| [`Assignments/`](Assignments/) | Course-outcome assignments CO1–CO5 |
| [`Lab Exp/`](Lab%20Exp/) | Laboratory notebooks, reports, and experiments 1–30 |
| [`capstone/`](capstone/) | PTB-XL ECG abnormality screening prototype |

## Working with the repository

Each assignment and the capstone has its own README with local setup and
execution instructions. Most runnable Python projects provide a
`requirements.txt`; install dependencies from the relevant project directory:

```bash
python -m pip install -r requirements.txt
```

Jupyter notebooks can be opened with Jupyter or Google Colab. PDF, DOCX, CSV,
image, model, and NumPy files are included as supporting reports or recorded
outputs.

## Notes

- Results may depend on Python, package versions, hardware, random seeds, and
  locally available datasets.
- Some assignment READMEs document dataset limitations and demonstration data;
  those limitations should be checked before treating an output as a final
  submission result.
- The capstone is a research prototype and is **not a clinically validated
  medical device**.
