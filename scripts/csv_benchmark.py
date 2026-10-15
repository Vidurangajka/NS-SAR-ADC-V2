#!/usr/bin/env python3
# ============================================================================
#  sar_adc_bench.py  --  8-bit SAR ADC benchmark from a transient code capture
#  Dependencies: numpy + matplotlib + Python standard library ONLY
#  (no pandas / scipy needed; works offline)
# ============================================================================
#
#  WHAT IT MEASURES
#    Dynamic : SNR, SNDR (SINAD), ENOB, ENOB(FS-referred), THD (H2..H9),
#              SFDR, noise floor, individual harmonics  -- coherent FFT
#              + IEEE 1241 sine-fit cross-check
#    Static  : transition levels, DNL, INL (best-fit and end-point),
#              missing codes, offset error, gain error, transfer curve
#              -- IEEE 1241 sine-wave histogram (code-density) test
#    Trust   : every metric is ALSO computed for an ideal N-bit ADC driven by
#              the same test-bench sine at the same instants ("ideal twin").
#              Twin == theory  -> the analysis is sound.
#              DUT vs twin     -> what the circuit really contributes.
#
# ----------------------------------------------------------------------------
#  TEST-BENCH SETUP (Cadence ADE / Maestro)  -- do all of this before running
# ----------------------------------------------------------------------------
#  1. DESIGN VARIABLES (same names as your ADE setup)
#       Fsam   = 8K                      sample rate
#       N      = 2048   (or 8192)        record length, MUST be a power of 2
#       M      = 3                       input cycles in the record:
#                                          * ODD (so gcd(M,N)=1 -> all N samples
#                                            hit different sine phases)
#                                          * low-f run : M = 3 (or any small odd)
#                                          * Nyquist run: M = N/2 - 3  (odd, e.g. 1021
#                                            for N=2048, 4093 for N=8192)
#       FIN    = M*Fsam/N                (never type FIN by hand -> keeps it coherent)
#       NDROP  = 2                       conversions thrown away at start-up
#       Tsim   = (N + NDROP + 1)/Fsam    simulate AT LEAST N+NDROP conversions
#       Fclk   = Fsam*12, TCLK = 1/(Fsam*12)   (unchanged)
#
#  2. INPUT SOURCE (fully differential, two vsin sources)
#       VINP = VSIG_CM + (VAMP/2)*sin(2*pi*FIN*t)
#       VINN = VSIG_CM - (VAMP/2)*sin(2*pi*FIN*t)
#       VSIG_CM = 0.9 V, phase 0, delay 0, NO damping
#       VAMP is the DIFFERENTIAL PEAK (VINP-VINN peak):
#         * static / INL-DNL run : VAMP = 1.8   (= full scale: codes 0 and 255
#                                   must both get hits; each pin swings 0..1.8 V)
#         * dynamic runs with mismatch/offset (Monte Carlo, corners):
#                                   VAMP = 1.70 (-0.5 dBFS) so offset can't clip
#       Put the SAME VAMP into VIN_PEAK_DIFF below (or pass --vamp).
#
#  3. OUTPUT CAPTURE (your adc_csv_logger VerilogA)
#       * write ONE row per conversion, on the EOC/DONE rising edge, AFTER the
#         output register has latched
#       * columns: Time,DecimalCode   (LSB-aligned code 0..2^NBITS-1)
#       * a repeated header line in the file is fine (it is skipped)
#
#  4. CONTROL SIGNALS
#       * ONE reset at t=0, released before the first sampling phase
#       * NO periodic reset / enable toggling during the run
#         (it gaps the record and makes the first code after each release stale)
#
#  5. SIMULATOR
#       * AMS/mixed-signal digital speed = 2  (speed 3 caused timing errors)
#       * transient accuracy: moderate or conservative; keep maxstep <= TCLK/20
#       * NOISE run  : enable transient noise (fmax >= 10*Fclk, fixed seed)
#       * MISMATCH   : Monte Carlo, mismatch only, >= 30 points, one CSV per point
#
#  6. RECOMMENDED RUN LIST
#       A  static + dynamic, low f   : M=3,  VAMP=1.8,  N=2048 (8192 for finer DNL)
#       B  near-Nyquist dynamic       : M=N/2-3, VAMP=1.8 (or 1.70)
#       C  A with transient noise
#       D  Monte Carlo mismatch on A  (then B on the worst MC point)
#       E  corners (SS/FF, -40/27/125 C, VDD +/-10 %) on B
#
#  DNL RESOLUTION: with coherent sampling the phases are spaced 2*pi/N, so a
#  transition level is located to within ~ 2*pi*2^(NBITS-1)/N LSB at mid-scale:
#       N = 2048 -> 0.39 LSB     N = 8192 -> 0.10 LSB     N = 16384 -> 0.05 LSB
#  The "ideal twin" curve shows this floor on every DNL/INL plot.
#
# ----------------------------------------------------------------------------
#  USAGE
#       python3 sar_adc_bench.py                       -> newest CSV under ./simulation
#       python3 sar_adc_bench.py adc_output.csv
#       python3 sar_adc_bench.py adc_output.csv --vamp 1.7 --no-show
#
#  OUTPUT (next to the CSV)
#       <name>_bench.png        all plots
#       <name>_report.txt       full text report (paste into your thesis log)
#       <name>_static.csv       per-code hits / transition level / DNL / INL
#
#  INTERACTIVE PLOT CONTROLS (needs a display + Tk; otherwise PNG only)
#       hover            read the value under the cursor
#       click a graph    expand it to full window;  click again / Esc = back
#       scroll on graph  zoom X at the cursor;  scroll left of Y-axis = zoom Y
#       r                reset zoom on the graph under the cursor
#       s                save the current view as PNG
# ============================================================================

import os
import sys
import csv
import argparse
from pathlib import Path

import numpy as np
import matplotlib

# ---------------------------------------------------------------------------
# USER CONFIGURATION  (command-line options override these)
# ---------------------------------------------------------------------------
CSV_FILE       = None     # None -> newest *.csv under ./simulation (or pass on command line)
N_BITS         = 8
VREF_P         = 1.8      # V
VREF_N         = 0.0      # V
VIN_PEAK_DIFF  = 1.8      # V, differential peak of the test-bench sine (= VAMP). None -> use fitted
FSAM           = None     # Hz. None -> taken from the CSV time stamps
N_FFT          = 2048     # record length N of the test bench
M_CYCLES       = None     # input cycles M. None -> detected from the FFT
N_DROP         = 2        # start-up conversions to discard (used only if the CSV has > N_FFT rows)
N_HARM         = 9        # harmonics H2..H_N_HARM in THD
SPEC = dict(              # pass/fail limits for the summary (edit to your spec)
    enob_min=7.5,         # bit
    dnl_max=0.5,          # |LSB|
    inl_max=0.5,          # |LSB|
    missing_codes=0,
)

# ---------------------------------------------------------------------------
# Backend: interactive if a display + Tk exist, else file-only
# ---------------------------------------------------------------------------
def _pick_backend(no_show):
    if no_show:
        matplotlib.use("Agg")
        return False
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        matplotlib.use("Agg")
        return False
    try:
        import tkinter  # noqa: F401
        matplotlib.use("TkAgg")
        return True
    except Exception:
        matplotlib.use("Agg")
        return False


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def find_csv():
    root = Path.cwd()
    cands = sorted(root.glob("../simulation/**/*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        cands = sorted(root.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        sys.exit("ERROR: no CSV given and none found under ./simulation or ./")
    return cands[0]


def load_csv(path):
    t, c, bad = [], [], 0
    with open(path, newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 2:
                bad += 1
                continue
            try:
                t.append(float(row[0]))
                c.append(int(round(float(row[1]))))
            except ValueError:
                bad += 1          # header lines (incl. repeated headers)
    if not t:
        sys.exit("ERROR: no numeric rows in CSV")
    return np.array(t), np.array(c, dtype=np.int64), bad


# ---------------------------------------------------------------------------
# Dynamic analysis
# ---------------------------------------------------------------------------
def bh4(n):
    k = np.arange(n)
    return (0.35875 - 0.48829 * np.cos(2 * np.pi * k / n) + 0.14128 * np.cos(4 * np.pi * k / n)
            - 0.01168 * np.cos(6 * np.pi * k / n))


def fold(b, n):
    b = b % n
    return n - b if b > n // 2 else b


def fft_analysis(codes, nbits, coherent, n_harm):
    """Single-sided power spectrum normalised so a full-scale sine = 0 dBFS."""
    n = len(codes)
    x = codes.astype(float) - codes.mean()
    if coherent:
        w, lobe = np.ones(n), 0
    else:
        w, lobe = bh4(n), 5
    X = np.fft.rfft(x * w)
    enbw = n * np.sum(w ** 2) / np.sum(w) ** 2   # 1 for rectangular, ~2.0 for BH4
    P = np.abs(X) ** 2 / (np.sum(w) ** 2) / enbw # summing a tone's lobe bins -> its true power
    P[1:] *= 2                                   # single-sided -> tone of amplitude A gives A^2/2
    P[0] = 0.0
    fs_amp = 2 ** (nbits - 1)
    p_fs = fs_amp ** 2 / 2                       # full-scale sine power (code^2)

    ks = int(np.argmax(P[1:])) + 1
    sig = set(range(max(1, ks - lobe), min(len(P), ks + lobe + 1)))
    claimed = set(range(0, lobe + 1)) | sig
    p_sig = P[list(sig)].sum()

    harm = []
    for h in range(2, n_harm + 1):
        hb = fold(h * ks, n)
        hbins = set(range(max(1, hb - lobe), min(len(P), hb + lobe + 1))) - claimed
        ph = P[list(hbins)].sum() if hbins else 0.0
        claimed |= hbins
        harm.append((h, hb, ph))
    p_harm = sum(ph for _, _, ph in harm)
    noise_bins = np.array([b for b in range(len(P)) if b not in claimed])
    # window: correct for its equivalent noise bandwidth and for the noise hidden
    # under the excluded lobes. Coherent (rectangular): plain sum, no correction.
    p_noise = P[noise_bins].sum()
    if not coherent:   # add back the noise hidden under the excluded lobes
        p_noise = p_noise * (len(P) - 1) / len(noise_bins)
    spur_bins = [b for b in range(lobe + 1, len(P)) if b not in sig]
    p_spur = P[spur_bins].max()
    b_spur = spur_bins[int(np.argmax(P[spur_bins]))]

    tiny = 1e-30
    out = dict(
        P=P, P_dbfs=10 * np.log10(P / p_fs + tiny), ks=ks, lobe=lobe,
        amp=np.sqrt(2 * p_sig),
        snr=10 * np.log10(p_sig / p_noise),
        sndr=10 * np.log10(p_sig / (p_noise + p_harm)),
        thd=10 * np.log10(max(p_harm, tiny) / p_sig),
        sfdr=10 * np.log10(P[ks] / p_spur), sfdr_bin=b_spur,   # peak bin vs peak bin
        harm=[(h, hb, 10 * np.log10(max(ph, tiny) / p_sig)) for h, hb, ph in harm],
        noise_floor_dbfs=10 * np.log10(p_noise / max(len(noise_bins), 1) / p_fs),
    )
    out["sig_dbfs"] = 10 * np.log10(p_sig / p_fs)
    out["enob"] = (out["sndr"] - 1.76) / 6.02
    out["enob_fs"] = (out["sndr"] - out["sig_dbfs"] - 1.76) / 6.02
    return out


def sine_fit4(t, y, f0, iters=10):
    """IEEE 1057 4-parameter sine fit. Returns (a, b, c, f, residual)."""
    w = 2 * np.pi * f0
    for _ in range(iters):
        D = np.column_stack([np.cos(w * t), np.sin(w * t), np.ones_like(t)])
        a, b, c = np.linalg.lstsq(D, y, rcond=None)[0]
        D4 = np.column_stack([D, t * (-a * np.sin(w * t) + b * np.cos(w * t))])
        a, b, c, dw = np.linalg.lstsq(D4, y, rcond=None)[0]
        w += dw
        if abs(dw) < 1e-12 * w:
            break
    D = np.column_stack([np.cos(w * t), np.sin(w * t), np.ones_like(t)])
    a, b, c = np.linalg.lstsq(D, y, rcond=None)[0]
    return a, b, c, w / (2 * np.pi), y - D @ np.array([a, b, c])


# ---------------------------------------------------------------------------
# Static analysis -- IEEE 1241 sine-wave histogram
# ---------------------------------------------------------------------------
def histogram_static(codes, nbits, vin_pk, lsb, h_expect=None):
    nc = 2 ** nbits
    h = np.bincount(codes, minlength=nc)[:nc].astype(float)
    ntot = h.sum()
    ch = np.cumsum(h)[:-1]                              # hits with code <= k-1, k=1..nc-1
    k = np.arange(1, nc)
    T = -vin_pk * np.cos(np.pi * ch / ntot)             # transition levels, V (differential)
    T_ideal = (k - nc / 2) * lsb
    valid = (h[0] > 0) and (h[-1] > 0)

    # best-fit (independent) line
    g = np.polyfit(k, T, 1)
    lsb_bf = g[0]
    inl_bf = (T - np.polyval(g, k)) / lsb_bf
    dnl = np.diff(T) / lsb_bf - 1                       # codes 1..nc-2
    # end-point line
    lsb_ep = (T[-1] - T[0]) / (nc - 2)
    inl_ep = (T - (T[0] + (k - 1) * lsb_ep)) / lsb_ep
    lo_hit, hi_hit = int(np.min(codes)), int(np.max(codes))
    missing = [int(i) for i in range(max(1, lo_hit), min(nc - 1, hi_hit + 1)) if h[i] == 0]
    # a zero-hit code is only a CONFIRMED missing code if >= 15 hits were expected
    # (Poisson P(0|15) = 3e-7); with fewer it may be counting noise (transient-noise runs)
    if h_expect is None:
        confirmed, suspect = missing, []
    else:
        confirmed = [i for i in missing if h_expect[i] >= 15]
        suspect = [i for i in missing if h_expect[i] < 15]

    return dict(
        h=h, T=T, T_ideal=T_ideal, k=k, valid=valid,
        dnl=dnl, inl_bf=inl_bf, inl_ep=inl_ep, missing=confirmed, missing_suspect=suspect,
        lsb_bf=lsb_bf, lsb_ep=lsb_ep,
        # SIGN CONVENTION (output-referred):  + gain  = codes span MORE than ideal
        #                                     + offset = ADC reads HIGH (transitions early)
        gain_err_bf=100 * (lsb / lsb_bf - 1), gain_err_ep=100 * (lsb / lsb_ep - 1),
        gain_err_bf_lsb=(lsb / lsb_bf - 1) * nc, gain_err_ep_lsb=(lsb / lsb_ep - 1) * nc,
        offset_bf=-(np.polyval(g, nc / 2) - 0.0) / lsb,   # best-fit line at mid-scale
        offset_ep=-(T[0] - T_ideal[0]) / lsb,              # first transition
        err_lsb=-(T - T_ideal) / lsb,                      # output-referred error per transition
        fit=g,
    )


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def analyse(csv_path, vin_pk_cfg):
    t_raw, c_raw, nbad = load_csv(csv_path)
    nc = 2 ** N_BITS
    lsb = 2 * (VREF_P - VREF_N) / nc                    # differential full scale / 2^N
    fs = FSAM or 1.0 / np.median(np.diff(t_raw))
    notes = []

    if c_raw.min() < 0 or c_raw.max() > nc - 1:
        sys.exit(f"ERROR: codes outside 0..{nc-1}; check N_BITS / logger alignment")

    # --- record selection -------------------------------------------------
    if len(c_raw) >= N_FFT:
        ndrop = len(c_raw) - N_FFT
        if ndrop < N_DROP:
            notes.append(f"only {ndrop} spare conversions (wanted N_DROP={N_DROP}); "
                         f"simulate N+{N_DROP} to discard more start-up samples")
        t, c = t_raw[-N_FFT:], c_raw[-N_FFT:]
    else:
        t, c = t_raw, c_raw
        notes.append(f"only {len(c_raw)} samples < N_FFT={N_FFT}: NON-coherent, window applied")
    n = len(c)
    dt = np.diff(t)
    jitter = np.max(np.abs(dt - 1 / fs)) * fs
    uniform = jitter < 0.01
    if not uniform:
        notes.append(f"time stamps not uniform (max deviation {100*jitter:.1f} % of Ts): "
                     "gaps/resets in the capture -> results unreliable")

    # --- coherence --------------------------------------------------------
    x = c - c.mean()
    P0 = np.abs(np.fft.rfft(x)) ** 2
    k0 = int(np.argmax(P0[1:])) + 1
    m_cyc = M_CYCLES or k0
    coherent = (n == N_FFT) and uniform and (np.gcd(m_cyc, n) == 1) and (k0 == m_cyc)
    if coherent:
        neigh = max(P0[k0 - 1], P0[k0 + 1] if k0 + 1 < len(P0) else 0)
        coherent = neigh < 1e-7 * P0[k0]
    if not coherent:
        notes.append("record is NOT coherent (non-integer cycles or gcd(M,N)!=1): "
                     "Blackman-Harris window used, histogram test degraded")
    if np.gcd(m_cyc, n) != 1:
        notes.append(f"M={m_cyc} shares a factor with N={n}: only N/gcd distinct phases "
                     "-> use an ODD M")
    fin = m_cyc * fs / n if coherent else k0 * fs / n

    # --- sine fit (unclipped samples) --------------------------------------
    ti = np.arange(n) / fs
    inner = (c > 0) & (c < nc - 1)
    if coherent:   # frequency is known exactly -> 3-parameter fit (IEEE 1241), no drift
        D = np.column_stack([np.cos(2*np.pi*fin*ti[inner]), np.sin(2*np.pi*fin*ti[inner]), np.ones(inner.sum())])
        a, b, dc = np.linalg.lstsq(D, c[inner].astype(float), rcond=None)[0]
        r = c[inner] - D @ np.array([a, b, dc])
        f_fit = fin
    else:
        a, b, dc, f_fit, r = sine_fit4(ti[inner], c[inner].astype(float), fin)
    amp_fit = np.hypot(a, b)
    theta = np.arctan2(b, a)
    sinad_fit = 10 * np.log10(amp_fit ** 2 / 2 / np.mean(r ** 2))

    vin_pk = vin_pk_cfg if vin_pk_cfg else amp_fit * lsb
    if not vin_pk_cfg:
        notes.append("VIN_PEAK_DIFF not set: input amplitude taken from the fit -> "
                     "absolute gain error cannot be measured (reported vs fit)")
    a_in = vin_pk / lsb                                   # input amplitude in LSB
    if vin_pk_cfg and abs(amp_fit / a_in - 1) > 0.01:
        notes.append(f"fitted amplitude {amp_fit*lsb:.4f} V differs from VIN_PEAK_DIFF={vin_pk_cfg} V by "
                     f"{100*(amp_fit/a_in-1):+.1f} %: either --vamp does not match the test bench, "
                     "or it is a real gain error (check the transfer-curve plot)")

    # --- ideal twin ---------------------------------------------------------
    x_id = nc / 2 + a_in * np.cos(2 * np.pi * f_fit * ti - theta)
    c_id = np.clip(np.floor(x_id), 0, nc - 1).astype(np.int64)
    diff = c - c_id
    match = dict(same=int(np.sum(diff == 0)), maxdiff=int(np.max(np.abs(diff))),
                 hist=dict(zip(*np.unique(diff, return_counts=True))))

    dyn = fft_analysis(c, N_BITS, coherent, N_HARM)
    dyn_id = fft_analysis(c_id, N_BITS, coherent, N_HARM)
    st_id = histogram_static(c_id, N_BITS, vin_pk, lsb)
    st = histogram_static(c, N_BITS, vin_pk, lsb, h_expect=st_id["h"])
    if st["missing_suspect"]:
        notes.append(f"codes {st['missing_suspect']} got 0 hits but only <15 were expected: "
                     "could be statistics (e.g. transient noise), not a true missing code. "
                     "Confirm with larger N or another noise seed.")
    hits_mid = st_id["h"][nc // 2]
    notes_dnl_stat = 1 / np.sqrt(max(hits_mid, 1))
    if not st["valid"]:
        notes.append("codes 0 and/or 2^N-1 never hit: sine does not reach full scale -> "
                     "histogram INL/DNL/gain/offset INVALID. Use VAMP >= full scale for the static run.")
    elif min(st["h"][0], st["h"][-1]) < 5:
        notes.append("end codes hit < 5 times: histogram end-point accuracy is poor; "
                     "raise VAMP by ~1 % for the static run")
    res_mid = 2 * np.pi * a_in / n                      # transition-level resolution at mid-scale

    # --- sine-fit offset / gain (independent cross-check) -------------------
    off_fit = (dc - (nc / 2 - 0.5))                      # floor quantiser mean = 2^(N-1) - 0.5
    gain_fit = 100 * (amp_fit / a_in - 1) if vin_pk_cfg else float("nan")

    # --- spec check ---------------------------------------------------------
    peak = lambda v: float(np.max(np.abs(v)))
    sv = st["valid"]
    checks = [
        ("ENOB", dyn["enob"] >= SPEC["enob_min"], f">= {SPEC['enob_min']} bit"),
        ("|DNL|", (peak(st["dnl"]) <= SPEC["dnl_max"]) if sv else None, f"<= {SPEC['dnl_max']} LSB"),
        ("|INL| best-fit", (peak(st["inl_bf"]) <= SPEC["inl_max"]) if sv else None, f"<= {SPEC['inl_max']} LSB"),
        ("missing codes", (len(st["missing"]) <= SPEC["missing_codes"]) if sv else None, f"<= {SPEC['missing_codes']}"),
    ]

    return dict(
        csv=Path(csv_path), n_raw=len(c_raw), nbad=nbad, t=t, c=c, ti=ti, n=n, fs=fs, fin=fin,
        f_fit=f_fit, m=m_cyc, coherent=coherent, uniform=uniform, lsb=lsb, nc=nc,
        vin_pk=vin_pk, vin_cfg=vin_pk_cfg, a_in=a_in, fit=(a, b, dc), amp_fit=amp_fit,
        sinad_fit=sinad_fit, off_fit=off_fit, gain_fit=gain_fit, c_id=c_id, match=match,
        dyn=dyn, dyn_id=dyn_id, st=st, st_id=st_id, res_mid=res_mid, notes=notes, dnl_stat=notes_dnl_stat,
        checks=checks, peak=peak,
    )


# ---------------------------------------------------------------------------
# Text report
# ---------------------------------------------------------------------------
def write_report(R):
    d, di, s, si, pk = R["dyn"], R["dyn_id"], R["st"], R["st_id"], R["peak"]
    L = []
    w = L.append
    bar = "=" * 74
    w(bar)
    w(f"  {N_BITS}-BIT SAR ADC BENCHMARK REPORT")
    w(bar)
    w(f"  File              : {R['csv'].name}")
    w(f"  Rows in file      : {R['n_raw']}  (non-numeric rows skipped: {R['nbad']})")
    w(f"  Record used       : last {R['n']} samples   coherent: {R['coherent']}   uniform: {R['uniform']}")
    w(f"  Fs                : {R['fs']:.3f} S/s")
    w(f"  Fin               : {R['fin']:.6f} Hz  (M = {R['m']} cycles, fitted {R['f_fit']:.6f} Hz)")
    w(f"  Full scale        : {2*(VREF_P-VREF_N):.3f} Vpp differential,  1 LSB = {R['lsb']*1e3:.4f} mV")
    w(f"  Input amplitude   : {R['vin_pk']:.4f} V diff peak = {R['a_in']:.3f} LSB "
      f"({20*np.log10(R['a_in']/(R['nc']/2)):+.2f} dBFS)  [{'test bench' if R['vin_cfg'] else 'from fit'}]")
    w("")
    if R["notes"]:
        w("  WARNINGS / NOTES")
        for nt in R["notes"]:
            w(f"   ! {nt}")
        w("")
    w("-" * 74)
    w(f"  {'DYNAMIC (FFT)':<34}{'DUT':>12}{'IDEAL TWIN':>14}{'THEORY':>12}")
    w("-" * 74)
    th_sndr = 6.02 * N_BITS + 1.76 + d["sig_dbfs"]
    rows = [
        ("Signal [dBFS]", d["sig_dbfs"], di["sig_dbfs"], None, ".2f"),
        ("SNR [dB]", d["snr"], di["snr"], None, ".2f"),
        ("SNDR / SINAD [dB]", d["sndr"], di["sndr"], th_sndr, ".2f"),
        ("ENOB [bit]", d["enob"], di["enob"], (th_sndr - 1.76) / 6.02, ".3f"),
        ("ENOB, full-scale referred [bit]", d["enob_fs"], di["enob_fs"], float(N_BITS), ".3f"),
        (f"THD H2..H{N_HARM} [dBc]", d["thd"], di["thd"], None, ".2f"),
        ("SFDR [dBc]", d["sfdr"], di["sfdr"], None, ".2f"),
        ("Noise floor [dBFS/bin]", d["noise_floor_dbfs"], di["noise_floor_dbfs"], None, ".1f"),
        ("SINAD, sine-fit cross-check [dB]", R["sinad_fit"], None, None, ".2f"),
    ]
    for name, v, vi, vt, f in rows:
        s1 = format(v, f)
        s2 = format(vi, f) if vi is not None else "-"
        s3 = format(vt, f) if vt is not None else "-"
        w(f"  {name:<34}{s1:>12}{s2:>14}{s3:>12}")
    w(f"  Largest spur: bin {d['sfdr_bin']} = {d['sfdr_bin']*R['fs']/R['n']:.2f} Hz")
    w("  Harmonics [dBc]  (h: DUT / twin)")
    w("   " + "   ".join(f"H{h}: {v:6.1f}/{vi:6.1f}" for (h, _, v), (_, _, vi) in zip(d["harm"][:4], di["harm"][:4])))
    w("   " + "   ".join(f"H{h}: {v:6.1f}/{vi:6.1f}" for (h, _, v), (_, _, vi) in zip(d["harm"][4:], di["harm"][4:])))
    w("")
    w("-" * 74)
    w(f"  {'STATIC (sine histogram, IEEE 1241)':<34}{'DUT':>18}{'IDEAL TWIN':>18}")
    w("-" * 74)
    if not s["valid"]:
        w("  !! INVALID: end codes not reached -- see notes. Values below are NOT meaningful.")
    rng = lambda v: f"{np.min(v):+.3f}/{np.max(v):+.3f}"
    srows = [
        ("DNL min/max [LSB]", rng(s["dnl"]), rng(si["dnl"])),
        ("INL best-fit min/max [LSB]", rng(s["inl_bf"]), rng(si["inl_bf"])),
        ("INL end-point min/max [LSB]", rng(s["inl_ep"]), rng(si["inl_ep"])),
        ("DNL rms [LSB]", f"{np.std(s['dnl']):.3f}", f"{np.std(si['dnl']):.3f}"),
        ("INL rms [LSB]", f"{np.std(s['inl_bf']):.3f}", f"{np.std(si['inl_bf']):.3f}"),
        ("Missing codes (confirmed)", str(s["missing"] or "none"), str(si["missing"] or "none")),
        ("Zero-hit codes (statistical?)", str(s["missing_suspect"] or "none"), "-"),
        ("Offset, best-fit @ mid [LSB] (+=high)", f"{s['offset_bf']:+.3f}", f"{si['offset_bf']:+.3f}"),
        ("Offset, first transition [LSB]", f"{s['offset_ep']:+.3f}", f"{si['offset_ep']:+.3f}"),
        ("Gain error, best-fit [%]", f"{s['gain_err_bf']:+.3f}", f"{si['gain_err_bf']:+.3f}"),
        ("Gain error, end-point [%]", f"{s['gain_err_ep']:+.3f}", f"{si['gain_err_ep']:+.3f}"),
        ("Gain error, end-point [LSB over FS]", f"{s['gain_err_ep_lsb']:+.3f}", f"{si['gain_err_ep_lsb']:+.3f}"),
    ]
    for name, v, vi in srows:
        w(f"  {name:<34}{v:>18}{vi:>18}")
    w(f"  Hits at code 0 / {R['nc']-1}: {int(s['h'][0])} / {int(s['h'][-1])}")
    w(f"  Transition-level resolution of this record at mid-scale: +/-{R['res_mid']/2:.2f} LSB")
    w("   -> DUT DNL/INL within the ideal-twin band are at the METHOD limit, not ADC error.")
    w(f"  If transient noise is ON: per-code DNL also scatters by ~+/-{R['dnl_stat']:.2f} LSB (1/sqrt(hits)),")
    w("   so compare several seeds / a larger N before calling a code bad.")
    w("")
    w("-" * 74)
    w("  CROSS-CHECKS")
    w("-" * 74)
    m = R["match"]
    w(f"  Codes identical to ideal twin : {m['same']}/{R['n']} ({100*m['same']/R['n']:.2f} %), max |diff| = {m['maxdiff']} LSB")
    w(f"     difference histogram       : " + ", ".join(f"{int(k):+d}: {v}" for k, v in m["hist"].items()))
    w(f"  Sine-fit offset               : {R['off_fit']:+.3f} LSB = {R['off_fit']*R['lsb']*1e3:+.2f} mV")
    gf = R["gain_fit"]
    w(f"  Sine-fit gain error           : " + (f"{gf:+.3f} %" if np.isfinite(gf) else "n/a (VIN_PEAK_DIFF not set)"))
    w("")
    w("-" * 74)
    w("  SPEC CHECK")
    w("-" * 74)
    for name, ok, lim in R["checks"]:
        w(f"  {name:<20}{'N/A' if ok is None else ('PASS' if ok else 'FAIL'):>6}   ({lim})")
    w("")
    w("  NOTE: a noise-free, mismatch-free post-layout run is expected to match the ideal")
    w("  twin. Silicon-representative numbers need transient noise + Monte Carlo runs.")
    w(bar)
    txt = "\n".join(L)
    out = R["csv"].with_name(R["csv"].stem + "_report.txt")
    out.write_text(txt + "\n", encoding="utf-8")

    sc = R["csv"].with_name(R["csv"].stem + "_static.csv")
    with open(sc, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["code", "hits", "hits_ideal", "T_k_V(code-1->code)", "T_k_ideal_V",
                     "DNL_LSB", "DNL_ideal", "INL_bestfit_LSB", "INL_endpoint_LSB", "INL_ideal"])
        for code in range(R["nc"]):
            if 1 <= code <= R["nc"] - 1:
                i = code - 1
                Tk, Ti = s["T"][i], s["T_ideal"][i]
                ib, ie, ii = s["inl_bf"][i], s["inl_ep"][i], si["inl_bf"][i]
            else:
                Tk = Ti = ib = ie = ii = ""
            if 1 <= code <= R["nc"] - 2:
                dn, dni = s["dnl"][code - 1], si["dnl"][code - 1]
            else:
                dn = dni = ""
            wr.writerow([code, int(s["h"][code]), int(si["h"][code]), Tk, Ti, dn, dni, ib, ie, ii])
    return txt, out, sc


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
BLUE, ORANGE, GRAY, INK, INK2, GREEN, RED = ("#2a78d6", "#eb6834", "#8a8984", "#0b0b0b",
                                             "#52514e", "#1f8f4e", "#d13b3b")


def make_figure(R, interactive):
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    plt.rcParams.update({
        "font.size": 8.5, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": INK2,
        "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": "#e6e5e0",
        "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "axes.titlesize": 9.5,
    })
    d, di, s, si, nc, lsb = R["dyn"], R["dyn_id"], R["st"], R["st_id"], R["nc"], R["lsb"]
    fig = plt.figure(figsize=(19, 11.5))
    title = (f"{N_BITS}-bit SAR ADC benchmark  |  {R['csv'].name}  |  Fs {R['fs']/1e3:.3f} kS/s, "
             f"Fin {R['fin']:.3f} Hz (M={R['m']}), N={R['n']}, Vin {R['vin_pk']:.3f} V diff pk")
    fig.suptitle(title, fontsize=11, color=INK)
    gs = GridSpec(3, 3, figure=fig, hspace=0.42, wspace=0.22, left=0.045, right=0.985, top=0.93, bottom=0.055)
    ax = {}
    hover = {}   # ax -> (x, y, label_fn)

    # 1 time domain
    a = ax["time"] = fig.add_subplot(gs[0, 0])
    tms = R["ti"] * 1e3
    a.plot(tms, R["c"], ".", ms=2.2, color=BLUE, label="DUT code")
    aa, bb, dc = R["fit"]
    tt = np.linspace(0, R["ti"][-1], 6000)
    a.plot(tt * 1e3, aa * np.cos(2*np.pi*R["f_fit"]*tt) + bb * np.sin(2*np.pi*R["f_fit"]*tt) + dc,
           color=GRAY, lw=1.0, label="4-param sine fit")
    a.set(xlabel="Time from record start [ms]", ylabel="Code", title="Output codes (whole record)")
    a.legend(frameon=False, loc="lower left", fontsize=7.5)
    hover[a] = (tms, R["c"].astype(float), lambda i, x, y: f"n={i}  t={x:.3f} ms  code={int(y)}  ideal={R['c_id'][i]}")

    # 2 spectrum
    a = ax["spec"] = fig.add_subplot(gs[0, 1])
    f = np.arange(len(d["P_dbfs"])) * R["fs"] / R["n"]
    a.plot(f, d["P_dbfs"], color=BLUE, lw=0.7, label="DUT")
    hb = [hb for _, hb, _ in d["harm"]]
    a.plot(f[hb], d["P_dbfs"][hb], "o", ms=4, mfc="none", color=ORANGE, label="H2..H%d" % N_HARM)
    spread = (f[hb].max() - f[hb].min()) > 0.08 * R["fs"] / 2   # label only if not bunched up
    for h, b_, _ in (d["harm"][:5] if spread else []):
        a.annotate(f"H{h}", (f[b_], d["P_dbfs"][b_]), textcoords="offset points", xytext=(0, 5),
                   fontsize=7, color=ORANGE, ha="center")
    a.axhline(d["noise_floor_dbfs"], color=GRAY, lw=0.8, ls="--", label=f"noise floor {d['noise_floor_dbfs']:.1f} dBFS/bin")
    a.set(xlabel="Frequency [Hz]", ylabel="Power [dBFS]", xlim=(0, R["fs"] / 2), ylim=(-140, 5),
          title=f"Spectrum  SNDR {d['sndr']:.2f} dB | SNR {d['snr']:.2f} | ENOB {d['enob']:.2f} | SFDR {d['sfdr']:.1f} dBc")
    a.legend(frameon=False, fontsize=7.5, loc="upper right")
    hover[a] = (f, d["P_dbfs"], lambda i, x, y: f"bin {i}  {x:.2f} Hz  {y:.1f} dBFS")

    # 3 harmonics
    a = ax["harm"] = fig.add_subplot(gs[0, 2])
    hh = np.array([h for h, _, _ in d["harm"]])
    hv = np.array([v for _, _, v in d["harm"]])
    hvi = np.array([v for _, _, v in di["harm"]])
    floor = -130
    wdt = 0.38
    a.bar(hh - wdt/2, np.maximum(hv, floor) - floor, wdt, bottom=floor, color=BLUE, label="DUT")
    a.bar(hh + wdt/2, np.maximum(hvi, floor) - floor, wdt, bottom=floor, color=GRAY, label="Ideal twin")
    a.set(xlabel="Harmonic", ylabel="Level [dBc]", xticks=hh, ylim=(floor, -30),
          title=f"Harmonic distortion  THD {d['thd']:.1f} dBc (twin {di['thd']:.1f})")
    a.legend(frameon=False, fontsize=7.5)
    hover[a] = (hh.astype(float), hv, lambda i, x, y: f"H{int(x)}: DUT {y:.1f} dBc, twin {hvi[i]:.1f} dBc")

    # 4 histogram
    a = ax["hist"] = fig.add_subplot(gs[1, 0])
    k = np.arange(nc)
    a.bar(k, s["h"], width=1.0, color=BLUE, label="DUT")
    a.step(k, si["h"], where="mid", color=INK2, lw=0.8, label="Ideal twin")
    top = np.percentile(s["h"][1:-1], 99) * 2.2
    a.set(xlabel="Code", ylabel="Hits", xlim=(-2, nc + 1), ylim=(0, max(top, 5)),
          title=f"Code histogram  (end codes: {int(s['h'][0])} / {int(s['h'][-1])} hits)")
    a.legend(frameon=False, fontsize=7.5, loc="upper center")
    hover[a] = (k.astype(float), s["h"], lambda i, x, y: f"code {i}: {int(y)} hits (twin {int(si['h'][i])})")

    # 5 DNL
    a = ax["dnl"] = fig.add_subplot(gs[1, 1])
    kd = np.arange(1, nc - 1)
    a.plot(kd, s["dnl"], color=BLUE, lw=1.4, label="DUT")
    a.plot(kd, si["dnl"], color=INK2, lw=0.7, ls=(0, (2, 1.5)), label="Ideal twin = method floor")
    for y in (-0.5, 0.5):
        a.axhline(y, color=RED, lw=0.8, ls="--")
    lim = max(0.6, 1.25 * R["peak"](s["dnl"]))
    a.set(xlabel="Code", ylabel="DNL [LSB]", xlim=(0, nc), ylim=(-lim, lim),
          title=f"DNL  {np.min(s['dnl']):+.3f} / {np.max(s['dnl']):+.3f} LSB"
                + ("" if s["valid"] else "  (INVALID)"))
    a.legend(frameon=False, fontsize=7.5, loc="lower right")
    hover[a] = (kd.astype(float), s["dnl"], lambda i, x, y: f"code {int(x)}: DNL {y:+.3f} (twin {si['dnl'][i]:+.3f})")

    # 6 INL
    a = ax["inl"] = fig.add_subplot(gs[1, 2])
    ki = np.arange(1, nc)
    a.plot(ki, s["inl_bf"], color=BLUE, lw=1.4, label="DUT, best-fit")
    a.plot(ki, s["inl_ep"], color=GREEN, lw=0.9, alpha=0.8, label="DUT, end-point")
    a.plot(ki, si["inl_bf"], color=INK2, lw=0.7, ls=(0, (2, 1.5)), label="Ideal twin = method floor")
    for y in (-0.5, 0.5):
        a.axhline(y, color=RED, lw=0.8, ls="--")
    lim = max(0.6, 1.25 * max(R["peak"](s["inl_bf"]), R["peak"](s["inl_ep"])))
    a.set(xlabel="Code (transition k-1 -> k)", ylabel="INL [LSB]", xlim=(0, nc), ylim=(-lim, lim),
          title=f"INL best-fit {np.min(s['inl_bf']):+.3f} / {np.max(s['inl_bf']):+.3f} LSB"
                + ("" if s["valid"] else "  (INVALID)"))
    a.legend(frameon=False, fontsize=7.5, loc="lower right")
    hover[a] = (ki.astype(float), s["inl_bf"],
                lambda i, x, y: f"T{int(x)}: INL bf {y:+.3f}, ep {s['inl_ep'][i]:+.3f} (twin {si['inl_bf'][i]:+.3f})")

    # 7 transfer curve (gain plot)
    a = ax["xfer"] = fig.add_subplot(gs[2, 0])
    Tm = s["T"] * 1e3
    a.step(Tm, s["k"], where="post", color=BLUE, lw=1.2, label="DUT (measured transitions)")
    vv = np.array([-R["vin_pk"], R["vin_pk"]]) * 1e3
    a.plot(vv, vv / (lsb * 1e3) + nc / 2, color=INK2, lw=0.8, ls="--", label="Ideal: code = Vin/LSB + 2^(N-1)")
    gfit = s["fit"]
    a.plot(np.polyval(gfit, [1, nc - 1]) * 1e3, [1, nc - 1], color=ORANGE, lw=1.0,
           label=f"Best-fit line: gain err {s['gain_err_bf']:+.3f} %, offset {s['offset_bf']:+.2f} LSB")
    a.set(xlabel="Differential input [mV]", ylabel="Output code",
          title="Static transfer curve (gain plot)")
    a.legend(frameon=False, fontsize=7.2, loc="upper left")
    hover[a] = (Tm, s["k"].astype(float), lambda i, x, y: f"T{int(y)} at {x:.2f} mV (ideal {s['T_ideal'][i]*1e3:.2f} mV)")

    # 8 transfer error: gain + offset + INL
    a = ax["gain"] = fig.add_subplot(gs[2, 1])
    a.plot(ki, s["err_lsb"], ".", ms=3, color=BLUE, label="DUT: (T_k,ideal - T_k)/LSB")
    a.plot(ki, si["err_lsb"], ".", ms=2, color=GRAY, label="Ideal twin")
    line = -(np.polyval(gfit, ki) - s["T_ideal"]) / lsb
    a.plot(ki, line, color=ORANGE, lw=1.2, label=f"offset + gain  (slope = {s['gain_err_bf']:+.3f} %)")
    a.axhline(0, color=INK2, lw=0.6)
    lim = max(1.0, 1.25 * R["peak"](s["err_lsb"]))
    a.set(xlabel="Code (transition k-1 -> k)", ylabel="Error [LSB]  (+ = reads high)", xlim=(0, nc), ylim=(-lim, lim),
          title=f"Gain / offset error  (end-point gain {s['gain_err_ep']:+.3f} %, first-transition offset {s['offset_ep']:+.2f} LSB)")
    a.legend(frameon=False, fontsize=7.2, loc="lower left")
    hover[a] = (ki.astype(float), s["err_lsb"], lambda i, x, y: f"T{int(x)}: error {y:+.3f} LSB (twin {si['err_lsb'][i]:+.3f})")

    # 9 summary table
    a = ax["tbl"] = fig.add_subplot(gs[2, 2])
    a.axis("off")
    pk = R["peak"]
    rows = [
        ["SNDR [dB]", f"{d['sndr']:.2f}", f"{di['sndr']:.2f}"],
        ["SNR [dB]", f"{d['snr']:.2f}", f"{di['snr']:.2f}"],
        ["ENOB [bit]", f"{d['enob']:.3f}", f"{di['enob']:.3f}"],
        ["THD [dBc]", f"{d['thd']:.1f}", f"{di['thd']:.1f}"],
        ["SFDR [dBc]", f"{d['sfdr']:.1f}", f"{di['sfdr']:.1f}"],
        ["|DNL| max [LSB]", f"{pk(s['dnl']):.3f}", f"{pk(si['dnl']):.3f}"],
        ["|INL| max [LSB]", f"{pk(s['inl_bf']):.3f}", f"{pk(si['inl_bf']):.3f}"],
        ["Missing codes", str(len(s["missing"])), str(len(si["missing"]))],
        ["Offset [LSB]", f"{s['offset_bf']:+.3f}", f"{si['offset_bf']:+.3f}"],
        ["Gain error [%]", f"{s['gain_err_bf']:+.3f}", f"{si['gain_err_bf']:+.3f}"],
        ["Codes = twin", f"{100*R['match']['same']/R['n']:.1f} %", "100 %"],
    ]
    tb = a.table(cellText=rows, colLabels=["Metric", "DUT", "Ideal twin"], cellLoc="center",
                 colWidths=[0.42, 0.29, 0.29], bbox=[0.0, 0.2, 1.0, 0.8])
    tb.auto_set_font_size(False)
    tb.set_fontsize(8.5)
    for j in range(3):
        tb[0, j].set_facecolor("#2a4f86")
        tb[0, j].set_text_props(color="white", fontweight="bold")
    allpass = all(ok is not False for _, ok, _ in R["checks"])
    verdict = "  ".join(f"{n}: {'N/A' if ok is None else ('PASS' if ok else 'FAIL')}" for n, ok, _ in R["checks"])
    a.text(0.5, 0.08, verdict, transform=a.transAxes, ha="center", fontsize=8,
           color="white", fontweight="bold",
           bbox=dict(boxstyle="round,pad=0.4", fc=GREEN if allpass else RED, ec="none"))
    if R["notes"]:
        a.text(0.5, -0.02, f"{len(R['notes'])} warning(s) - see report", transform=a.transAxes, ha="center",
               fontsize=8, color=RED)
    a.set_title("Summary (spec limits in SPEC dict)")

    out = R["csv"].with_name(R["csv"].stem + "_bench.png")
    fig.savefig(out, dpi=150)

    if interactive:
        _make_interactive(fig, ax, hover, title, out)
    return fig, out


def _make_interactive(fig, ax, hover, title, png_path):
    import matplotlib.pyplot as plt
    graphs = [a for key, a in ax.items() if key != "tbl"]
    tbl = ax["tbl"]
    pos0 = {a: a.get_position() for a in list(ax.values())}
    xl0 = {a: a.get_xlim() for a in graphs}
    yl0 = {a: a.get_ylim() for a in graphs}
    state = {"zoom": None}
    ann = {}
    for a in graphs:
        an = a.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#9a9a9a", alpha=0.95),
                        zorder=10)
        an.set_visible(False)
        mk, = a.plot([], [], "o", ms=6, mfc="none", mec=INK, zorder=11)
        ann[a] = (an, mk)
    hint = "click: expand | scroll: zoom X (left of axis: Y) | r: reset | s: save | hover: values"
    fig.suptitle(title + "\n" + hint, fontsize=10, color=INK)

    def on_move(ev):
        changed = False
        for a in graphs:
            an, mk = ann[a]
            if ev.inaxes is a and a in hover:
                x, y, fmt = hover[a]
                xl, yl = a.get_xlim(), a.get_ylim()
                sx = (x - ev.xdata) / (xl[1] - xl[0])
                sy = (y - ev.ydata) / (yl[1] - yl[0])
                i = int(np.nanargmin(sx ** 2 + 0.15 * sy ** 2))
                an.xy = (x[i], y[i])
                an.set_text(fmt(i, x[i], y[i]))
                # keep label inside the axes
                fx = (x[i] - xl[0]) / (xl[1] - xl[0])
                an.set_position((-10 if fx > 0.6 else 10, 10))
                an.set_ha("right" if fx > 0.6 else "left")
                an.set_visible(True)
                mk.set_data([x[i]], [y[i]])
                changed = True
            elif an.get_visible():
                an.set_visible(False)
                mk.set_data([], [])
                changed = True
        if changed:
            fig.canvas.draw_idle()

    def restore():
        for a, p in pos0.items():
            a.set_position(p)
            a.set_visible(True)
        state["zoom"] = None
        fig.canvas.draw_idle()

    def expand(a):
        for g in list(ax.values()):
            g.set_visible(g is a)
        a.set_position([0.06, 0.08, 0.9, 0.8])
        state["zoom"] = a
        fig.canvas.draw_idle()

    def on_click(ev):
        if ev.button != 1 or ev.inaxes not in graphs:
            return
        if fig.canvas.toolbar is not None and getattr(fig.canvas.toolbar, "mode", ""):
            return   # pan/zoom tool active
        if state["zoom"] is ev.inaxes:
            restore()
        else:
            expand(ev.inaxes)

    def target_for(ev):
        if ev.inaxes in graphs:
            return ev.inaxes, "x"
        for a in graphs:
            if not a.get_visible():
                continue
            bb = a.get_window_extent()
            if bb.x0 - 70 <= ev.x <= bb.x0 and bb.y0 <= ev.y <= bb.y1:
                return a, "y"
        return None, None

    def on_scroll(ev):
        a, axis = target_for(ev)
        if a is None:
            return
        k = 0.8 if ev.button == "down" else 1.25
        if axis == "x":
            lo, hi = a.get_xlim()
            c = ev.xdata
            o_lo, o_hi = xl0[a]
        else:
            lo, hi = a.get_ylim()
            bb = a.get_window_extent()
            c = lo + (ev.y - bb.y0) / (bb.y1 - bb.y0) * (hi - lo)
            o_lo, o_hi = yl0[a]
        span = (hi - lo) * k
        if span >= (o_hi - o_lo):
            nlo, nhi = o_lo, o_hi
        else:
            r = (c - lo) / (hi - lo)
            nlo = c - r * span
            nhi = nlo + span
            if nlo < o_lo:
                nlo, nhi = o_lo, o_lo + span
            if nhi > o_hi:
                nlo, nhi = o_hi - span, o_hi
        (a.set_xlim if axis == "x" else a.set_ylim)(nlo, nhi)
        fig.canvas.draw_idle()

    def on_key(ev):
        if ev.key == "escape" and state["zoom"] is not None:
            restore()
        elif ev.key == "r":
            a = ev.inaxes if ev.inaxes in graphs else state["zoom"]
            for g in ([a] if a else graphs):
                g.set_xlim(xl0[g])
                g.set_ylim(yl0[g])
            fig.canvas.draw_idle()
        elif ev.key == "s":
            name = png_path.with_name(png_path.stem + ("_" + [k for k, v in ax.items() if v is state["zoom"]][0]
                                                        if state["zoom"] else "_view") + ".png")
            fig.savefig(name, dpi=150)
            print(f"saved {name}")

    fig.canvas.mpl_connect("motion_notify_event", on_move)
    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("scroll_event", on_scroll)
    fig.canvas.mpl_connect("key_press_event", on_key)
    plt.show()


# ---------------------------------------------------------------------------
def main():
    global VIN_PEAK_DIFF, N_FFT, M_CYCLES, FSAM, N_BITS
    ap = argparse.ArgumentParser(description="SAR ADC benchmark (numpy + matplotlib only)")
    ap.add_argument("csv", nargs="?", default=CSV_FILE, help="Time,DecimalCode CSV")
    ap.add_argument("--vamp", type=float, default=VIN_PEAK_DIFF,
                    help="differential input peak in V (= VAMP); 0 = take from fit")
    ap.add_argument("--n", type=int, default=N_FFT, help="record length N")
    ap.add_argument("--m", type=int, default=M_CYCLES, help="input cycles M (default: detect)")
    ap.add_argument("--fs", type=float, default=FSAM, help="sample rate (default: from time stamps)")
    ap.add_argument("--bits", type=int, default=N_BITS)
    ap.add_argument("--no-show", action="store_true", help="save files only, no window")
    args = ap.parse_args()

    VIN_PEAK_DIFF = args.vamp if args.vamp else None
    N_FFT, M_CYCLES, FSAM, N_BITS = args.n, args.m, args.fs, args.bits
    interactive = _pick_backend(args.no_show)

    path = Path(args.csv) if args.csv else find_csv()
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    print(f"Analysing {path}")
    R = analyse(path, VIN_PEAK_DIFF)
    txt, rep, sc = write_report(R)
    print(txt)
    fig, png = make_figure(R, interactive=False)
    print(f"\nwrote {png}\nwrote {rep}\nwrote {sc}")
    if interactive:
        import matplotlib.pyplot as plt
        plt.close(fig)
        make_figure(R, interactive=True)
    elif not args.no_show:
        print("(no display/Tk available -> PNG only)")


if __name__ == "__main__":
    main()