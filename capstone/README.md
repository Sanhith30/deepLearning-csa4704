# ECG abnormality screening (research prototype)

A Streamlit app for the CSA47 capstone. It reads a 10-second, 12-lead ECG sampled at 100 Hz
and scores five groups of findings: normal ECG, myocardial infarction, ST/T change,
conduction disturbance and hypertrophy.

**This is not a medical device.** It has not been clinically validated.

## Folder layout

Put these files together in one folder:

```
ecg_app/
  app.py                  the app
  model.py                the CNN-BiLSTM definition (must match the notebook)
  preprocessing.py        file reading, checks, normalisation
  requirements.txt
  .streamlit/config.toml  colours
  final_cnn_bilstm.pt     }
  config.json             }  exported from the notebook
  lead_mean.npy           }  (folder ecg_app_files on Google Drive)
  lead_std.npy            }
  app_samples.npz         }
```

The last five files come from the export cell in the notebook. Download them from
`ecg_app_files` on Google Drive and copy them next to `app.py`.

## Run it

```
pip install -r requirements.txt
streamlit run app.py
```

If the default PyTorch download is large, install the CPU build first from pytorch.org,
then run the command above. The model is small and runs on a CPU.

## Input formats

- **Example recording:** pick one of the saved PTB-XL test recordings.
- **.npy file:** a 12 x 1000 (or 1000 x 12) array in millivolts, 100 Hz, lead order
  I, II, III, aVR, aVL, aVF, V1 to V6.
- **WFDB pair:** upload the `.hea` and `.dat` files together (for example the PTB-XL
  100 Hz files ending in `_lr`). The `.dat` file must keep the name written in the `.hea` file.

Recordings that are not 100 Hz, not 12 leads, or not exactly 10 seconds are rejected
with a message that says what to change.

## What the app checks

Missing values (rejected), flat leads, signal size that looks wrong for millivolts, and very
large amplitudes that often mean noise (warnings).

## Known limits

Trained and tested on PTB-XL only. Hypertrophy is the weakest group. Accuracy differed between
age groups and between women and men in the project analysis. Large amplitude changes and heavy
noise lowered accuracy. Scores are model outputs, not verified probabilities of disease.
