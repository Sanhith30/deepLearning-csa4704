DEEP LEARNING — ASSIGNMENT 4 (CO4)
Complete experimental project and editable Word report
Report date: 17 November 2026

CONTENTS
  Final_Assignment_4.docx     30-page editable Word report: all Q1–Q7, theory,
                              actual program results, figures and complete Python listings.
  Programs/                   Q1–Q7 Python programs, shared probability helpers,
                              and a regression-verification program.
  Datasets/                   Wine standardized CSV, noisy Wine CSV, source signals,
                              machine mixtures, sparse codes and dictionary,
                              simulated examination days and SFA signals.
  Outputs/                    Executed JSON results, comparison CSV tables and
                              exact 128-state distribution for the extended network.
  Graphs/                     Data-based experimental plots and image grids.
  Diagrams/                   Q5 and Q7 Bayesian network diagrams.
  Logs/                       Console output of each executed experiment.
  Original_Assignment_4.txt   Original assignment statement supplied by the user.
  requirements.txt            Python package dependencies.
  build_report.py             Rebuilds the Word report from the experiment outputs.

RUNNING
  1. Install Python 3.10+.
  2. Open a terminal in the project folder.
  3. Run: python -m pip install -r requirements.txt
  4. Run experiments in order:
       python Programs/Q1_PCA_PPCA.py
       python Programs/Q2_Factor_Analysis.py
       python Programs/Q3_ICA.py
       python Programs/Q4_Sparse_Coding.py
       python Programs/Q5_Bayesian_Network.py
       python Programs/Q6_SFA_And_Sampling.py
       python Programs/Q7_Extended_Network.py
  5. Run consistency checks:
       python Programs/verify_results.py
  6. Optional Word report rebuild:
       python build_report.py

Each program writes its tabular results to Outputs/ and plots to Graphs/ or
Diagrams/. Random seeds and chosen model parameters are in the program files.
All experiments were executed successfully for the supplied report; console
logs record measured outcomes. CPU execution times depend on the host.

DATA AND ACADEMIC HONESTY
  • The Wine and digits data are built into scikit-learn.
  • Q2 deliberately adds controlled random noise to Wine measurements.
  • Q3 and Q6 construct the source signals required by the assignment.
  • Q5–Q7 generate observations from specified conditional probability models.
  • The Q7 new-event probabilities are proposed assumptions, not measured
    operational statistics from any real examination service.
  • Q7's two draft design proposals are examples for students to review, NOT
    independently verified contributions from Student A and Student B.
  • Student names, register numbers, institution and actual pair contribution
    records were not provided. The report does not invent these details.

NOTES
  The 36-atom sparse coding dictionary is learned once and shared across
  the three regularization strengths to isolate the effect of changing λ.
  ICA sources can be recovered with reversed signs or swapped components;
  source matching uses absolute correlation and an optimal assignment.
  Four-event Bayesian graph: 7 CPD parameters vs 15 free joint parameters.
  Seven-event graph: 17 CPD parameters vs 127 free joint parameters.
