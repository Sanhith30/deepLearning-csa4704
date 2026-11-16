"""ECG abnormality screening tool.

Part of the ECGScreen multi-page app.
Run the whole app with:  streamlit run app.py
"""
import html as _html
import io
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import streamlit as st

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model import load_model, predict
from preprocessing import (
    LEAD_NAMES, SAMPLING_RATE, ECGInputError,
    check_quality, load_npy, load_wfdb, normalise,
)

APP_DIR = Path(__file__).resolve().parent.parent

FINDING = {
    "NORM": "Normal ECG",
    "MI":   "Myocardial infarction",
    "STTC": "ST/T change",
    "CD":   "Conduction disturbance",
    "HYP":  "Hypertrophy",
}
ECG_LAYOUT = [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11]]

st.set_page_config(
    page_title="ECG Screener",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='8' fill='%230f2240'/><polyline points='5,50 20,50 28,30 36,70 44,50 52,20 60,80 68,50 80,50 95,50' stroke='%2360a5fa' stroke-width='7' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
    overflow-x: hidden;
}
[data-testid="stSidebar"] { background: #0f2240; border-right: none; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #f1f5f9 !important; font-weight: 700;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #1e3a5f !important; border-color: #334d6e !important;
}
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

/* page header */
.page-header {
    border-bottom: 2px solid #0f2240;
    padding-bottom: 0.6rem; margin-bottom: 0.4rem;
    display: flex; align-items: baseline; gap: 1rem;
}
.page-header h1 {
    font-size: 1.45rem; font-weight: 800; color: #0f2240;
    letter-spacing: -0.025em; margin: 0;
}
.page-header .meta { font-size: 0.8rem; color: #64748b; margin: 0; }

/* disclaimer bar */
.disc-bar {
    background: #fff7ed; border-left: 3px solid #f59e0b;
    padding: 0.45rem 0.9rem; border-radius: 0 3px 3px 0;
    font-size: 0.78rem; color: #78350f; margin-bottom: 1.2rem;
}

/* verdict banners */
.verdict { border-radius: 4px; padding: 0.75rem 1rem; font-size: 0.88rem;
    font-weight: 700; margin-bottom: 1rem; }
.v-abn  { background: #fff1f2; border: 1.5px solid #fda4af; color: #9f1239; }
.v-norm { background: #f0fdf4; border: 1.5px solid #86efac; color: #14532d; }
.v-und  { background: #f8fafc; border: 1.5px solid #cbd5e1; color: #334155; }

/* score rows */
.score-row {
    display: grid; grid-template-columns: 7.5rem 1fr 3rem 5.5rem;
    align-items: center; gap: 0.5rem;
    padding: 0.45rem 0; border-bottom: 1px solid #f1f5f9;
}
.score-label { font-size: 0.82rem; color: #334155; }
.bar-wrap { height: 6px; background: #e2e8f0; border-radius: 2px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 2px; }
.score-num {
    font-size: 0.78rem; font-family: "Courier New", monospace;
    color: #475569; text-align: right;
}
.score-flag {
    font-size: 0.68rem; font-weight: 700; padding: 2px 6px;
    border-radius: 3px; text-align: center;
}
.flag-y { background: #ffe4e6; color: #be123c; }
.flag-n { background: #f1f5f9; color: #94a3b8; }

/* misc */
.section-label {
    font-size: 0.7rem; font-weight: 600; color: #94a3b8;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.4rem;
}
.quality-warn {
    background: #fffbeb; border: 1px solid #fcd34d; color: #92400e;
    font-size: 0.75rem; padding: 0.3rem 0.7rem; border-radius: 3px;
    margin-bottom: 0.4rem; display: block;
}
.truth-row { font-size: 0.82rem; color: #475569; padding: 0.3rem 0; }
.truth-row strong { color: #0f2240; }
.perf-note { font-size: 0.78rem; color: #64748b; line-height: 1.6; }
.back-link {
    font-size: 0.78rem; color: #1a56db; text-decoration: none;
    display: inline-block; margin-bottom: 0.9rem;
}

@media (max-width: 768px) {
    .score-row { grid-template-columns: 1fr 1fr; }
    .score-num, .score-flag { display: none; }
}
</style>
""", unsafe_allow_html=True)

# ── back link ─────────────────────────────────────────────────────────────────
st.markdown('<a class="back-link" href="/" target="_self">Back to home</a>',
            unsafe_allow_html=True)


# ── asset loading ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model weights...")
def load_assets():
    cfg  = json.loads((APP_DIR / "config.json").read_text())
    mean = np.load(APP_DIR / "lead_mean.npy").reshape(12, 1)
    std  = np.load(APP_DIR / "lead_std.npy").reshape(12, 1)
    with np.load(APP_DIR / "app_samples.npz", allow_pickle=False) as d:
        samples = {k: d[k] for k in d.files}
    net = load_model(APP_DIR / "final_cnn_bilstm.pt")
    return cfg, mean, std, samples, net


config, lead_mean, lead_std, samples, net = load_assets()
classes    = config["classes"]
thresholds = np.array(config["thresholds"])


# ── ECG plot ──────────────────────────────────────────────────────────────────
def plot_ecg_paper(raw: np.ndarray) -> plt.Figure:
    PAPER_BG  = "#fff1f2"
    MINOR_COL = "#fecdd3"
    MAJOR_COL = "#fca5a5"
    TRACE_COL = "#0f2240"

    t = np.arange(raw.shape[1]) / SAMPLING_RATE
    fig, axes = plt.subplots(
        3, 4, figsize=(14, 6.0), facecolor=PAPER_BG,
        gridspec_kw={"hspace": 0.08, "wspace": 0.04},
    )
    for r in range(3):
        for c in range(4):
            idx = ECG_LAYOUT[r][c]
            ax  = axes[r, c]
            sig = raw[idx]
            ax.set_facecolor(PAPER_BG)
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.04))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(0.20))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
            ax.grid(which="minor", color=MINOR_COL, linewidth=0.4)
            ax.grid(which="major", color=MAJOR_COL, linewidth=0.9)
            ax.set_axisbelow(True)
            ax.plot(t, sig, lw=0.9, color=TRACE_COL, solid_capstyle="round")
            sig_mid = float(np.median(sig))
            half    = max(1.0, float(np.abs(sig - sig_mid).max()) * 1.2)
            ax.set_ylim(sig_mid - half, sig_mid + half)
            ax.set_xlim(t[0], t[-1])
            ax.text(0.012, 0.88, LEAD_NAMES[idx], transform=ax.transAxes,
                    fontsize=8, fontweight="bold", color=TRACE_COL, va="top")
            ax.tick_params(
                which="both",
                bottom=(r == 2), top=False, left=False, right=False,
                labelbottom=(r == 2), labelleft=False,
                labelsize=6, colors="#9f1239",
            )
            for sp in ax.spines.values():
                sp.set_visible(False)
    for ax in axes[-1]:
        ax.set_xlabel("seconds", fontsize=7, color="#9f1239", labelpad=2)
    return fig


# ── sidebar ───────────────────────────────────────────────────────────────────
raw, example_index = None, None

with st.sidebar:
    st.markdown("## ECG Screener")
    st.markdown("---")
    st.markdown("**Select source**")
    mode = st.radio("source", ["Example recording", "Upload a file"],
                    label_visibility="collapsed")

    if mode == "Example recording":
        labels = []
        for k in range(len(samples["ids"])):
            tag = " (high amplitude)" if samples["flagged"][k] else ""
            labels.append(
                f"ECG {int(samples['ids'][k])} | "
                f"{samples['age'][k]:.0f} y, {str(samples['sex'][k]).lower()}{tag}"
            )
        example_index = st.selectbox(
            "Recording", range(len(labels)), format_func=lambda k: labels[k]
        )
        raw = samples["X"][example_index].astype(np.float32)
    else:
        st.caption(
            "Upload a .npy array (12 x 1000, millivolts, 100 Hz) "
            "or a WFDB pair (.hea + .dat) at 100 Hz."
        )
        files = st.file_uploader(
            "ECG file(s)", type=["npy", "hea", "dat"],
            accept_multiple_files=True, label_visibility="collapsed",
        )
        if files:
            try:
                npy_f = [f for f in files if f.name.lower().endswith(".npy")]
                if npy_f:
                    if len(files) > 1:
                        raise ECGInputError(
                            "Upload either one .npy file or a .hea/.dat pair, not both.")
                    raw = load_npy(io.BytesIO(npy_f[0].getvalue()))
                else:
                    raw = load_wfdb({f.name: f.getvalue() for f in files})
            except ECGInputError as err:
                st.error(str(err))

    st.markdown("---")
    st.caption("Research prototype. CSA47 capstone.\nTrained on PTB-XL (PhysioNet).")


# ── page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1>ECG abnormality screening</h1>
  <p class="meta">1D CNN-BiLSTM | PTB-XL | 5 diagnostic groups</p>
</div>
<div class="disc-bar">
  Not a medical device. Not clinically validated.
  Do not use to inform clinical decisions.
</div>
""", unsafe_allow_html=True)

if raw is None:
    st.info("Select an example recording in the sidebar, or upload your own ECG file.")
    st.stop()


# ── normalise + quality + predict ─────────────────────────────────────────────
norm    = normalise(raw, lead_mean, lead_std)
issues  = check_quality(raw, norm, config.get("amp_threshold"))

if any(i["level"] == "error" for i in issues):
    for i in issues:
        st.error(i["message"])   # streamlit's own renderer — no raw HTML needed
    st.stop()

scores   = predict(net, norm)[0]
flagged  = scores >= thresholds
abnormal = [FINDING[c] for c, f in zip(classes, flagged) if f and c != "NORM"]


# ── layout ────────────────────────────────────────────────────────────────────
col_ecg, col_res = st.columns([62, 38], gap="large")

# LEFT — trace
with col_ecg:
    st.markdown('<p class="section-label">12-lead ECG  |  10 s  |  25 mm/s  |  10 mm/mV</p>',
                unsafe_allow_html=True)

    # quality warnings — escape the message text before inserting into HTML
    for iss in issues:
        safe_msg = _html.escape(iss["message"])
        st.markdown(f'<span class="quality-warn">Warning: {safe_msg}</span>',
                    unsafe_allow_html=True)

    fig = plot_ecg_paper(raw)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    buf    = io.BytesIO()
    fig_dl = plot_ecg_paper(raw)
    fig_dl.savefig(buf, format="png", dpi=180, bbox_inches="tight",
                   facecolor=fig_dl.get_facecolor())
    plt.close(fig_dl)
    buf.seek(0)
    st.download_button("Download ECG image (PNG)", data=buf,
                       file_name="ecg_12lead.png", mime="image/png")

# RIGHT — results
with col_res:
    if abnormal:
        safe_ab = _html.escape(", ".join(abnormal))
        st.markdown(
            f'<div class="verdict v-abn">Flagged for review: {safe_ab}</div>',
            unsafe_allow_html=True)
    elif flagged[classes.index("NORM")]:
        st.markdown(
            '<div class="verdict v-norm">No abnormal group flagged</div>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="verdict v-und">Undecided — no group reached its threshold</div>',
            unsafe_allow_html=True)

    st.markdown('<p class="section-label">Scores</p>', unsafe_allow_html=True)

    score_html = ""
    for cls, score, thresh, is_flagged in zip(classes, scores, thresholds, flagged):
        pct   = int(score * 100)
        ratio = min(score / (thresh + 1e-9), 1.0)
        r_ = int(14  + ratio * 176)
        g_ = int(34  + ratio * -16)
        b_ = int(64  + ratio * -4)
        flag_cls = "flag-y" if is_flagged else "flag-n"
        flag_txt = "Flagged" if is_flagged else f"thr {thresh:.2f}"
        # FINDING[cls] comes from a fixed dict — safe; score/thresh are floats — safe
        score_html += (
            f'<div class="score-row">'
            f'<span class="score-label">{FINDING[cls]}</span>'
            f'<div class="bar-wrap"><div class="bar-fill" '
            f'style="width:{pct}%;background:rgb({r_},{g_},{b_})"></div></div>'
            f'<span class="score-num">{score:.3f}</span>'
            f'<span class="score-flag {flag_cls}">{flag_txt}</span>'
            f'</div>'
        )
    st.markdown(score_html, unsafe_allow_html=True)

    st.caption(
        "Scores are model outputs in [0, 1]. Thresholds were chosen on the validation "
        "split to balance sensitivity and precision. They are not verified probabilities of disease."
    )

    if example_index is not None:
        with st.expander("Dataset label for this recording"):
            truth     = [FINDING[c] for c, v in zip(classes, samples["y"][example_index]) if v]
            truth_str = ", ".join(truth) if truth else "no diagnostic group"
            age = samples["age"][example_index]
            sex = str(samples["sex"][example_index]).lower()
            # escape age/sex/truth_str before HTML insertion
            st.markdown(
                f"<div class='truth-row'><strong>PTB-XL label:</strong> "
                f"{_html.escape(truth_str)}</div>"
                f"<div class='truth-row'><strong>Patient:</strong> "
                f"{_html.escape(f'{age:.0f} y, {sex}')}</div>"
                f"<div class='truth-row' style='color:#94a3b8;font-size:0.72rem'>"
                f"The model never saw this label during training or threshold selection.</div>",
                unsafe_allow_html=True,
            )

    with st.expander("About this model"):
        info = config.get("model_info", {})
        arch = _html.escape(info.get("architecture", "1D CNN with a bidirectional LSTM"))
        recs = _html.escape(str(info.get("training_records", "~17,000")))
        st.markdown(
            f"<p class='perf-note'>"
            f"Architecture: <strong>{arch}</strong><br>"
            f"Training set: <strong>{recs}</strong> PTB-XL recordings (100 Hz, 10 s, 12 leads).<br>"
            f"No patient appears in both train and test sets.</p>",
            unsafe_allow_html=True,
        )
        perf = config.get("test_performance")
        if perf:
            st.dataframe(pd.DataFrame({
                "Finding":     [FINDING[c]                       for c in classes],
                "ROC-AUC":     [round(perf[c]["auc"], 3)         for c in classes],
                "Sensitivity": [round(perf[c]["sensitivity"], 3) for c in classes],
                "Precision":   [round(perf[c]["precision"], 3)   for c in classes],
            }), hide_index=True, use_container_width=True)
        st.markdown(
            "<ul class='perf-note' style='padding-left:1rem;margin-top:0.6rem'>"
            "<li>Trained and tested on one dataset — results may not transfer to other devices or hospitals.</li>"
            "<li>Hypertrophy is the weakest group; check the sensitivity figure above.</li>"
            "<li>Accuracy differed between age groups and by sex.</li>"
            "<li>Heavy noise or large amplitudes lower reliability.</li>"
            "</ul>",
            unsafe_allow_html=True,
        )
