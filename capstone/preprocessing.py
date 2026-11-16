"""Loading, checking and normalising ECG recordings for the screening app (NumPy only)."""
import os
import tempfile

import numpy as np

LEAD_NAMES = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
N_LEADS, N_SAMPLES, SAMPLING_RATE = 12, 1000, 100


class ECGInputError(ValueError):
    """An input problem, worded so the person can fix it."""


def _orient(arr):
    """Return a (12, 1000) float32 array from a (12, 1000) or (1000, 12) input."""
    arr = np.asarray(arr)
    if arr.ndim == 3 and arr.shape[0] == 1:
        arr = arr[0]
    if arr.shape == (N_LEADS, N_SAMPLES):
        return arr.astype(np.float32)
    if arr.shape == (N_SAMPLES, N_LEADS):
        return arr.T.astype(np.float32)
    raise ECGInputError(
        f"Expected 12 leads with 1000 samples each (10 seconds at 100 Hz), "
        f"but the file holds an array of shape {arr.shape}. "
        f"Resample to 100 Hz and cut or pad to exactly 10 seconds before uploading.")


def load_npy(file_like):
    """Read a .npy file holding a 12 x 1000 (or 1000 x 12) array in millivolts."""
    try:
        arr = np.load(file_like, allow_pickle=False)
    except Exception as exc:
        raise ECGInputError("The .npy file could not be read. Save it with numpy.save "
                            "as a plain numeric array.") from exc
    if not np.issubdtype(arr.dtype, np.number):
        raise ECGInputError("The .npy file must contain numbers only.")
    return _orient(arr)


def _reorder_leads(sig, names):
    """Put the leads in the standard order when the header names all 12 of them."""
    wanted = [n.upper() for n in LEAD_NAMES]
    found = [str(n).upper() for n in (names or [])]
    if sorted(found) == sorted(wanted):
        return sig[:, [found.index(n) for n in wanted]]
    return sig


def load_wfdb(files):
    """Read a WFDB record from {file name: bytes} holding one .hea and one .dat file."""
    hea = [n for n in files if n.lower().endswith(".hea")]
    dat = [n for n in files if n.lower().endswith(".dat")]
    if len(hea) != 1 or len(dat) != 1:
        raise ECGInputError("Upload exactly one .hea file and one .dat file together, "
                            "or a single .npy file.")
    import wfdb

    with tempfile.TemporaryDirectory() as tmp:
        for name, data in files.items():
            with open(os.path.join(tmp, os.path.basename(name)), "wb") as fh:
                fh.write(data)
        base = os.path.splitext(os.path.basename(hea[0]))[0]
        try:
            rec = wfdb.rdrecord(os.path.join(tmp, base))
        except Exception as exc:
            raise ECGInputError(
                "The record could not be read. The .dat file must keep the name written "
                "inside the .hea file (for example 00001_lr.dat for 00001_lr.hea).") from exc
    if rec.p_signal is None or rec.p_signal.ndim != 2 or rec.p_signal.shape[1] != N_LEADS:
        raise ECGInputError("The record must contain 12 leads.")
    if int(round(rec.fs)) != SAMPLING_RATE:
        raise ECGInputError(f"The record is sampled at {rec.fs:g} Hz. This prototype needs "
                            f"100 Hz recordings (for example PTB-XL files ending in _lr).")
    return _orient(_reorder_leads(rec.p_signal, rec.sig_name))


def normalise(raw, lead_mean, lead_std):
    """Scale each lead with the training-set statistics. raw: (12, 1000) in millivolts."""
    return ((raw - lead_mean.reshape(N_LEADS, 1)) / lead_std.reshape(N_LEADS, 1)).astype(np.float32)


def check_quality(raw, norm, amp_threshold=None):
    """Return a list of {'level': 'error' | 'warning', 'message': str}."""
    issues = []
    if not np.isfinite(raw).all():
        issues.append({"level": "error",
                       "message": "The recording contains missing or infinite values. "
                                  "Fix or interpolate them and upload it again."})
        return issues
    flat = [LEAD_NAMES[i] for i in range(N_LEADS) if raw[i].std() < 1e-4]
    if flat:
        issues.append({"level": "warning",
                       "message": f"Lead(s) {', '.join(flat)} look flat. Scores may be unreliable."})
    typical = float(np.median(raw.std(axis=1)))
    if typical > 5 or typical < 0.005:
        issues.append({"level": "warning",
                       "message": "The signal size looks unusual for millivolts. "
                                  "Check the units: the model expects millivolts."})
    if amp_threshold is not None and float(np.abs(norm).max()) > amp_threshold:
        issues.append({"level": "warning",
                       "message": "This recording has unusually large amplitudes, which often "
                                  "means noise or an electrode artifact. Treat the scores with extra caution."})
    return issues
