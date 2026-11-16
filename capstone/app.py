"""Home / landing page for the ECG Abnormality Screening app.

Run with:  streamlit run app.py
"""
import html as _html
import streamlit as st

st.set_page_config(
    page_title="ECG Screening",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='8' fill='%230f2240'/><polyline points='5,50 20,50 28,30 36,70 44,50 52,20 60,80 68,50 80,50 95,50' stroke='%2360a5fa' stroke-width='7' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* ── reset & base ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
html { scroll-behavior: smooth; overflow-x: hidden; }
body, [class*="css"] {
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
    color: #0f2240;
    overflow-x: hidden;
}
.main .block-container { padding: 0 !important; max-width: 100% !important; }
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── NAV ── */
.nav {
    position: sticky; top: 0; z-index: 100;
    background: #0f2240;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 3rem; height: 64px;
    box-shadow: 0 1px 0 rgba(255,255,255,0.06);
}
.nav-logo {
    display: flex; align-items: center; gap: 0.6rem; text-decoration: none;
}
.nav-logo svg { flex-shrink: 0; }
.nav-logo-text {
    font-size: 1.1rem; font-weight: 700; color: #fff; letter-spacing: -0.02em;
}
.nav-logo-text span { color: #60a5fa; }
.nav-links {
    display: flex; align-items: center; gap: 2rem; list-style: none;
}
.nav-links a {
    color: #94a3b8; text-decoration: none; font-size: 0.85rem; font-weight: 500;
}
.nav-links a:hover { color: #fff; }
.nav-cta {
    background: #1a56db; color: #fff !important; padding: 0.5rem 1.25rem;
    border-radius: 4px; font-weight: 600; font-size: 0.85rem; text-decoration: none;
}
.nav-cta:hover { background: #1d4ed8 !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(130deg, #0f2240 0%, #1a3a6b 55%, #1a56db 100%);
    padding: 6.5rem 3rem 5.5rem; min-height: 480px;
    display: flex; align-items: center;
}
.hero-inner { max-width: 780px; }
.hero-h1 {
    font-size: clamp(2.1rem, 4vw, 3.2rem); font-weight: 800; line-height: 1.1;
    color: #fff; letter-spacing: -0.03em; margin-bottom: 1.4rem;
}
.hero-sub {
    font-size: 1rem; color: #bfdbfe; line-height: 1.7;
    max-width: 620px; margin-bottom: 2.2rem;
}
.hero-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.btn-primary {
    background: #fff; color: #1a56db; padding: 0.8rem 1.75rem; border-radius: 4px;
    font-weight: 700; font-size: 0.9rem; text-decoration: none;
}
.btn-primary:hover { background: #f1f5f9; color: #1a56db; }
.btn-secondary {
    background: transparent; color: #bfdbfe; padding: 0.8rem 1.75rem;
    border-radius: 4px; font-weight: 600; font-size: 0.9rem;
    text-decoration: none; border: 1.5px solid rgba(255,255,255,0.25);
}
.btn-secondary:hover { border-color: rgba(255,255,255,0.5); }

/* ── STAT STRIP ── */
.stat-strip {
    background: #0a1628;
    display: flex; justify-content: center;
}
.stat-item {
    flex: 1; max-width: 220px; text-align: center;
    padding: 1.75rem 1rem; border-right: 1px solid #1e3a5f;
}
.stat-item:last-child { border-right: none; }
.stat-number {
    font-size: 2rem; font-weight: 800; color: #60a5fa;
    letter-spacing: -0.03em; line-height: 1;
}
.stat-label { font-size: 0.72rem; color: #475569; margin-top: 0.4rem; line-height: 1.4; }

/* ── ABOUT ── */
.about { background: #fff; padding: 5.5rem 3rem; }
.about-inner {
    max-width: 1100px; margin: 0 auto;
    display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center;
}
.about-visual {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    overflow: hidden; display: flex; align-items: center; justify-content: center;
    min-height: 300px; padding: 2rem;
}
.about-text h2 {
    font-size: 1.7rem; font-weight: 800; color: #0f2240;
    letter-spacing: -0.025em; margin-bottom: 1rem; line-height: 1.2;
}
.about-text p { font-size: 0.88rem; line-height: 1.8; color: #475569; margin-bottom: 0.9rem; }
.about-text strong { color: #0f2240; }

/* ── HOW IT WORKS ── */
.how { background: #f8fafc; padding: 5.5rem 3rem; }
.how-inner { max-width: 1100px; margin: 0 auto; }
.section-title {
    font-size: 1.5rem; font-weight: 800; color: #0f2240;
    letter-spacing: -0.025em; margin-bottom: 0.4rem;
}
.section-sub { font-size: 0.84rem; color: #64748b; margin-bottom: 2.5rem; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }
.step { background: #fff; border-radius: 6px; padding: 2rem; border: 1px solid #e2e8f0; }
.step-num {
    width: 32px; height: 32px; background: #0f2240; color: #fff;
    border-radius: 4px; display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 1rem;
}
.step h3 { font-size: 0.95rem; font-weight: 700; color: #0f2240; margin-bottom: 0.5rem; }
.step p { font-size: 0.82rem; color: #64748b; line-height: 1.65; }

/* ── FINDINGS ── */
.findings { background: #fff; padding: 5.5rem 3rem; }
.findings-inner { max-width: 1100px; margin: 0 auto; }
.findings-grid {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: 1rem; margin-top: 2.5rem;
}
.finding-card {
    border-radius: 6px; padding: 1.5rem 1.25rem;
    border-top-width: 3px; border-top-style: solid;
}
.finding-card h4 {
    font-size: 0.82rem; font-weight: 700; color: #0f2240;
    margin-bottom: 0.5rem; line-height: 1.3;
}
.finding-card p { font-size: 0.72rem; color: #64748b; line-height: 1.55; }
.fc-norm { background: #f0fdf4; border-top-color: #22c55e; border: 1px solid #bbf7d0; border-top: 3px solid #22c55e; }
.fc-mi   { background: #fff1f2; border: 1px solid #fecdd3; border-top: 3px solid #e11d48; }
.fc-sttc { background: #fff7ed; border: 1px solid #fed7aa; border-top: 3px solid #f97316; }
.fc-cd   { background: #eff6ff; border: 1px solid #bfdbfe; border-top: 3px solid #3b82f6; }
.fc-hyp  { background: #f5f3ff; border: 1px solid #ddd6fe; border-top: 3px solid #7c3aed; }

/* ── DISCLAIMER ── */
.disclaimer {
    background: #fff7ed; border-top: 2px solid #fcd34d; border-bottom: 2px solid #fcd34d;
    padding: 1.25rem 3rem;
}
.disclaimer p { font-size: 0.8rem; color: #78350f; line-height: 1.6; }

/* ── CTA ── */
.cta-band { background: #0f2240; padding: 5rem 3rem; text-align: center; }
.cta-band h2 {
    font-size: 1.9rem; font-weight: 800; color: #fff;
    letter-spacing: -0.025em; margin-bottom: 0.75rem;
}
.cta-band p { font-size: 0.9rem; color: #64748b; margin-bottom: 1.75rem; }

/* ── FOOTER ── */
.footer {
    background: #07111f; padding: 2rem 3rem;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem;
    border-top: 1px solid #1e3a5f;
}
.footer-left { font-size: 0.75rem; color: #334155; line-height: 1.6; }
.footer-left strong { color: #64748b; }
.footer-right { font-size: 0.75rem; color: #334155; }

/* ── mobile ── */
@media (max-width: 768px) {
    .nav { padding: 0 1.25rem; }
    .nav-links li:not(:last-child) { display: none; }
    .hero { padding: 4rem 1.25rem 3.5rem; }
    .about-inner { grid-template-columns: 1fr; gap: 2.5rem; }
    .about-visual { min-height: 200px; }
    .steps { grid-template-columns: 1fr; }
    .findings-grid { grid-template-columns: repeat(2, 1fr); }
    .stat-strip { flex-wrap: wrap; }
    .stat-item { max-width: 50%; border-right: none; border-bottom: 1px solid #1e3a5f; }
    .about, .how, .findings { padding: 3.5rem 1.25rem; }
    .footer { padding: 1.5rem 1.25rem; flex-direction: column; }
    .cta-band { padding: 3.5rem 1.25rem; }
}
</style>
""", unsafe_allow_html=True)

# ── ECG logo SVG (no emoji) ───────────────────────────────────────────────────
LOGO_SVG = """<svg width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
  <rect width="28" height="28" rx="5" fill="#1a56db"/>
  <polyline points="2,14 7,14 10,7 13,21 16,14 19,5 22,23 24,14 26,14"
    stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<nav class="nav">
  <a class="nav-logo" href="/" target="_self">
    {LOGO_SVG}
    <span class="nav-logo-text">ECG<span>Screen</span></span>
  </a>
  <ul class="nav-links">
    <li><a href="/" target="_self">Home</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#how">How it works</a></li>
    <li><a href="./Screening" target="_self" class="nav-cta">Open screener</a></li>
  </ul>
</nav>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="hero">
  <div class="hero-inner">
    <h1 class="hero-h1">
      12-lead ECG screening<br>for five cardiac findings,<br>in under a second
    </h1>
    <p class="hero-sub">
      A 1D CNN-BiLSTM classifier trained on 17,441 recordings from the PTB-XL dataset.
      Upload a 10-second ECG, get a scored report for myocardial infarction,
      ST/T change, conduction disturbance, hypertrophy, and normal sinus rhythm.
    </p>
    <div class="hero-actions">
      <a href="./Screening" target="_self" class="btn-primary">Open the screener</a>
      <a href="#about" class="btn-secondary">Read the background</a>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── STAT STRIP ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
  <div class="stat-item">
    <div class="stat-number">17,441</div>
    <div class="stat-label">Training recordings<br>from PTB-XL</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">5</div>
    <div class="stat-label">Diagnostic groups<br>classified</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">12</div>
    <div class="stat-label">ECG leads<br>processed</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">100 Hz</div>
    <div class="stat-label">Input sampling<br>rate required</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">&lt; 1 s</div>
    <div class="stat-label">Inference time<br>on CPU</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ABOUT ────────────────────────────────────────────────────────────────────
ECG_SVG = """
<svg viewBox="0 0 500 160" xmlns="http://www.w3.org/2000/svg" width="100%">
  <defs>
    <pattern id="g1" width="10" height="10" patternUnits="userSpaceOnUse">
      <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#fecdd3" stroke-width="0.5"/>
    </pattern>
    <pattern id="g5" width="50" height="50" patternUnits="userSpaceOnUse">
      <rect width="50" height="50" fill="url(#g1)"/>
      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#fca5a5" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="500" height="160" fill="#fff1f2"/>
  <rect width="500" height="160" fill="url(#g5)"/>
  <polyline
    points="0,80 25,80 35,74 45,80 58,80 61,80 63,28 65,105 69,80
            85,80 105,63 128,80 155,80 185,80
            198,74 208,80 225,80
            233,80 235,28 237,105 241,80
            255,80 275,63 298,80 325,80 355,80
            368,74 378,80 395,80
            403,80 405,28 407,105 411,80
            425,80 445,63 468,80 500,80"
    fill="none" stroke="#0f2240" stroke-width="2.2"
    stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="10" y1="115" x2="10" y2="55" stroke="#9f1239" stroke-width="1.5"/>
  <line x1="10" y1="115" x2="60" y2="115" stroke="#9f1239" stroke-width="1.5"/>
  <text x="14" y="113" font-size="8" fill="#9f1239" font-family="monospace">1 mV / 0.2 s</text>
</svg>"""

st.markdown(f"""
<section class="about" id="about">
  <div class="about-inner">
    <div class="about-visual">{ECG_SVG}</div>
    <div class="about-text">
      <h2>Why ECG screening matters</h2>
      <p>
        Cardiovascular diseases account for <strong>17.9 million deaths per year</strong>,
        32% of all deaths globally. Most cardiac events are preceded by measurable changes
        in the ECG signal that a trained reader can identify. Access to cardiologists is
        uneven, and manual reading at scale is not feasible in many settings.
      </p>
      <p>
        A 12-lead ECG captures the heart's electrical activity from twelve spatial angles.
        Patterns in the QRS complex, ST segment, and T wave carry the diagnostic signal for
        infarction, conduction block, hypertrophy, and other findings.
      </p>
      <p>
        This prototype shows how a <strong>1D CNN-BiLSTM</strong> trained on the PTB-XL
        dataset can replicate much of that screening automatically, flagging recordings that
        warrant review by a qualified clinician.
      </p>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown("""
<section class="how" id="how">
  <div class="how-inner">
    <h2 class="section-title">How it works</h2>
    <p class="section-sub">From raw signal to scored report in three steps</p>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <h3>Load a recording</h3>
        <p>
          Choose one of 26 built-in PTB-XL test recordings, or upload your own:
          a <code>.npy</code> array (12 x 1000, millivolts, 100 Hz) or a WFDB
          <code>.hea</code> + <code>.dat</code> pair at 100 Hz.
        </p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h3>Automatic quality checks</h3>
        <p>
          Before inference, the app checks for missing values, flat leads,
          out-of-range amplitudes, and units that look wrong for millivolts.
          Problems are reported with specific messages, not generic errors.
        </p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h3>Scored report</h3>
        <p>
          The classifier returns a score in [0, 1] for each diagnostic group.
          A group is flagged when its score reaches its validation-tuned threshold.
          The 12-lead trace is rendered on standard ECG graph paper for review.
        </p>
      </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── FINDINGS ─────────────────────────────────────────────────────────────────
st.markdown("""
<section class="findings">
  <div class="findings-inner">
    <h2 class="section-title">Five diagnostic groups</h2>
    <p class="section-sub">The model scores every recording against all five groups simultaneously</p>
    <div class="findings-grid">
      <div class="finding-card fc-norm">
        <h4>Normal ECG</h4>
        <p>No significant deviation from sinus rhythm or standard conduction norms</p>
      </div>
      <div class="finding-card fc-mi">
        <h4>Myocardial infarction</h4>
        <p>ST elevation or depression and Q-wave patterns associated with infarction</p>
      </div>
      <div class="finding-card fc-sttc">
        <h4>ST/T change</h4>
        <p>Non-specific ST segment and T-wave morphology abnormalities</p>
      </div>
      <div class="finding-card fc-cd">
        <h4>Conduction disturbance</h4>
        <p>Bundle branch blocks, AV blocks, and axis deviations</p>
      </div>
      <div class="finding-card fc-hyp">
        <h4>Hypertrophy</h4>
        <p>Voltage criteria and repolarisation patterns of ventricular hypertrophy</p>
      </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ── DISCLAIMER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
  <p>
    <strong>Not a medical device.</strong> This prototype has not been clinically validated and
    must not be used to inform any decision about a patient's health or treatment.
    It was built for the CSA47 capstone and trained solely on the PTB-XL research dataset.
    Model scores are not verified probabilities of disease.
  </p>
</div>
""", unsafe_allow_html=True)

# ── CTA ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-band">
  <h2>Upload an ECG and see the scores</h2>
  <p>26 example recordings are included. No account required.</p>
  <a href="./Screening" target="_self" class="btn-primary"
     style="display:inline-block;padding:0.85rem 2.25rem;font-weight:700;
            font-size:0.95rem;border-radius:4px;text-decoration:none;
            background:#1a56db;color:#fff;">
    Open the screener
  </a>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="footer">
  <div class="footer-left">
    <strong>ECGScreen</strong> — CSA47 Capstone, 2026<br>
    Trained on PTB-XL (Wagner et al., PhysioNet, 2019). Not a medical device.
  </div>
  <div class="footer-right">
    1D CNN-BiLSTM, PyTorch
  </div>
</footer>
""", unsafe_allow_html=True)
