"""Figures for Chapter 13 — Network Frequency Response.

Run from the repository root:  python figures/scripts/ch13.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")

ASYM = "#555555"


def db(h):
    return 20 * np.log10(np.abs(h))


def _bode_axes(w=6.4, h=5.0, ratio=(1.2, 1)):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(w, h), sharex=True,
                                 gridspec_kw=dict(height_ratios=ratio, hspace=0.12))
    for a in (a1, a2):
        a.grid(True, which="both", lw=0.4)
    return fig, a1, a2


# ---------------------------------------------------------------- 13.1
def fig_13_1():
    """Bode plot of the RC low-pass, R = 1.6 kOhm, C = 10 nF."""
    R, C = 1.6e3, 10e-9
    fc = 1 / (2 * np.pi * R * C)
    f = np.logspace(2, 6, 2000)
    H = 1 / (1 + 1j * f / fc)
    fig, a1, a2 = _bode_axes()
    a1.semilogx(f, db(H), color=COLORS[0], label="exact")
    asym = np.where(f < fc, 0, -20 * np.log10(f / fc))
    a1.semilogx(f, asym, "--", color=ASYM, lw=1.2, label="asymptotes")
    a1.axvline(fc, color="#999999", lw=0.7)
    a1.plot([fc], [-3.01], "o", color=COLORS[0], ms=5)
    a1.annotate("−3.01 dB at corner", (fc, -3.01), xytext=(1.2e3, -14), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    for fx in (20e3, 100e3):
        v = db(1 / (1 + 1j * fx / fc))
        a1.plot([fx], [v], "o", color=COLORS[1], ms=5, zorder=5)
        a1.annotate(f"{fx/1e3:.0f} kHz: {v:.1f} dB".replace("-", "−"), (fx, v), xytext=(fx * 1.35, v + 5),
                    fontsize=8.5, color=COLORS[1],
                    arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    a1.text(fc * 1.08, -36, "$f_c$ = 9.95 kHz", fontsize=8.5, color="#444444")
    a1.text(2.4e5, -32, "−20 dB/decade", fontsize=8.5, color=ASYM, ha="right")
    a1.set_ylim(-40, 5)
    a1.set_ylabel("magnitude (dB)")
    a1.legend(loc="lower left", fontsize=8.5)
    ph = -np.degrees(np.arctan(f / fc))
    a2.semilogx(f, ph, color=COLORS[0], label="exact")
    pa = np.where(f < fc / 10, 0, np.where(f > fc * 10, -90, -45 * (np.log10(f / fc) + 1)))
    a2.semilogx(f, pa, "--", color=ASYM, lw=1.2, label="straight-line approximation")
    a2.axvline(fc, color="#999999", lw=0.7)
    a2.plot([fc], [-45], "o", color=COLORS[0], ms=5)
    a2.annotate("−45° at $f_c$", (fc, -45), xytext=(1.6e3, -62), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    p20 = -np.degrees(np.arctan(20e3 / fc))
    a2.plot([20e3], [p20], "o", color=COLORS[1], ms=5, zorder=5)
    a2.annotate(f"20 kHz: {p20:.1f}°".replace("-", "−"), (20e3, p20), xytext=(5e4, -45), fontsize=8.5,
                color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    a2.text(fc / 10, 3, "995 Hz", fontsize=8, ha="center", va="bottom", color=ASYM)
    a2.text(fc * 10 * 1.15, -83, "99.5 kHz", fontsize=8, ha="left", va="bottom", color=ASYM)
    a2.set_ylim(-95, 10)
    a2.set_yticks([0, -15, -30, -45, -60, -75, -90])
    a2.set_ylabel("phase (degrees)")
    a2.set_xlabel("frequency (Hz)")
    a2.set_xlim(100, 1e6)
    a2.legend(loc="lower left", fontsize=8.5)
    save(fig, "13", "fig-13-1-rc-lowpass-bode")


# ---------------------------------------------------------------- 13.2
def fig_13_2():
    """Pole-zero map of 10(s+2)/(s^2+2s+101) with the vectors to j10, plus magnitude inset."""
    fig = plt.figure(figsize=(6.6, 4.6))
    ax = fig.add_axes([0.08, 0.10, 0.36, 0.86])
    z = -2 + 0j
    p1, p2 = -1 + 10j, -1 - 10j
    s0 = 10j
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.plot([z.real], [z.imag], "o", ms=9, mfc="white", mec=COLORS[2], mew=2, zorder=5)
    for p in (p1, p2):
        ax.plot([p.real], [p.imag], "x", ms=10, mew=2.2, color=COLORS[1], zorder=5)
    ax.plot([0], [10], "o", ms=6, color=INK, zorder=6)
    ax.text(0.15, 10.3, "$s=j10$", fontsize=9, va="bottom")
    cols = [COLORS[2], COLORS[1], COLORS[3]]
    for (src, c) in zip((z, p1, p2), cols):
        ax.annotate("", xy=(0, 10), xytext=(src.real, src.imag),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.4, mutation_scale=11,
                                    shrinkA=4, shrinkB=3))
    # length / angle labels
    ax.text(-1.55, 4.4, "10.20\n∠78.7°", color=COLORS[2], fontsize=8.5, ha="right")
    ax.text(-0.5, 10.55, "1.00\n∠0°", color=COLORS[1], fontsize=8.5, ha="center", va="bottom")
    ax.text(-0.75, -4.0, "20.02\n∠87.1°", color=COLORS[3], fontsize=8.5, ha="right")
    # angle arcs
    ax.add_patch(Arc((-2, 0), 1.6, 1.6, theta1=0, theta2=78.7, color=COLORS[2], lw=0.9))
    ax.add_patch(Arc((-1, -10), 1.6, 1.6, theta1=0, theta2=87.1, color=COLORS[3], lw=0.9))
    ax.plot([-2, -1.0], [0, 0], color=COLORS[2], lw=0.6, ls=":")
    ax.plot([-1, 0.2], [-10, -10], color=COLORS[3], lw=0.6, ls=":")
    ax.text(-2.05, -0.5, "zero −2", fontsize=8.5, color=COLORS[2], ha="center", va="top")
    ax.text(-1.25, 8.7, "pole\n−1 + j10", fontsize=8.5, color=COLORS[1], ha="right", va="top")
    ax.text(-1.25, -10.6, "pole −1 − j10", fontsize=8.5, color=COLORS[1], ha="center", va="top")
    ax.set_xlim(-4, 1)
    ax.set_ylim(-12, 12)
    ax.set_xlabel("real part σ (rad/s)")
    ax.set_ylabel("imaginary part ω (rad/s)")
    ax.set_xticks([-4, -3, -2, -1, 0, 1])
    ax.set_yticks(range(-12, 13, 4))
    ax.grid(True, lw=0.4)
    # magnitude panel
    b = fig.add_axes([0.58, 0.40, 0.40, 0.50])
    w = np.logspace(-1, 2, 2000)
    s = 1j * w
    H = 10 * (s + 2) / (s ** 2 + 2 * s + 101)
    b.semilogx(w, db(H), color=COLORS[0])
    b.plot([0.1], [db(10 * 2 / 101)], "o", color=COLORS[0], ms=4)
    b.text(0.13, -11.5, "DC: −14.1 dB", fontsize=8.5)
    b.plot([10], [db(10 * (10j + 2) / (-100 + 20j + 101))], "o", color=COLORS[1], ms=5)
    b.text(13, 13.5, "+14.1 dB\nat 10 rad/s", fontsize=8.5, color=COLORS[1], va="top")
    b.set_xlim(0.1, 100)
    b.set_ylim(-30, 20)
    b.set_xlabel("ω (rad/s)")
    b.set_ylabel("|H(jω)| (dB)")
    b.grid(True, which="both", lw=0.4)
    b.set_title("magnitude response", fontsize=9.5)
    fig.text(0.58, 0.20, "$|H(j10)|=\\dfrac{10\\times10.20}{1.00\\times20.02}=5.09$\n\n"
             "$\\angle H(j10)=78.7^\\circ-0^\\circ-87.1^\\circ=-8.4^\\circ$", fontsize=9, va="center")
    save(fig, "13", "fig-13-2-pole-zero-vectors")


# ---------------------------------------------------------------- 13.3
def fig_13_3():
    """ECG front end: 0.5 Hz high-pass, 150 Hz low-pass, gain 1000; corrected 0.05 Hz corner."""
    f = np.logspace(-2, 4, 3000)
    f2 = 150.0

    def H(f1):
        return 1000 * (1j * f / f1) / (1 + 1j * f / f1) / (1 + 1j * f / f2)

    Ha, Hb = H(0.5), H(0.05)
    fig, a1, a2 = _bode_axes(6.4, 5.4)
    a1.axvspan(0.05, 1, color=COLORS[4], alpha=0.15, lw=0)
    a1.text(0.22, 2, "ST segment and\nT-wave content", ha="center", va="bottom", fontsize=8.5, color="#8A5A00")
    a1.semilogx(f, db(Ha), color=COLORS[0], label="$f_1$ = 0.5 Hz (as designed)")
    a1.semilogx(f, db(Hb), "--", color=COLORS[2], lw=1.5, label="$f_1$ = 0.05 Hz (corrected)")
    asym = np.where(f < 0.5, 60 + 20 * np.log10(f / 0.5), np.where(f > f2, 60 - 20 * np.log10(f / f2), 60))
    a1.semilogx(f, asym, ":", color=ASYM, lw=1.2, label="asymptotes ($f_1$ = 0.5 Hz)")
    for fx in (0.5, 150):
        a1.plot([fx], [57.0], "o", color=COLORS[0], ms=5, zorder=5)
    a1.text(0.5 * 1.15, 54, "0.5 Hz\n57.0 dB", fontsize=8, va="top")
    a1.text(150 * 1.15, 54, "150 Hz\n57.0 dB", fontsize=8, va="top")
    a1.axvline(50, color=COLORS[1], ls=":", lw=1.2)
    a1.text(50 * 0.85, 12, "50 Hz\nmains", fontsize=8, color=COLORS[1], ha="right")
    a1.annotate("+20 dB/decade", (0.02, 32), xytext=(0.011, 15), fontsize=8, color=ASYM,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=ASYM))
    a1.text(1.5e3, 50, "−20 dB/decade", fontsize=8, color=ASYM)
    a1.set_ylim(0, 70)
    a1.set_ylabel("magnitude (dB)")
    a1.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.0))
    pa = np.degrees(np.angle(Ha))
    pb = np.degrees(np.angle(Hb))
    a2.axvspan(0.05, 1, color=COLORS[4], alpha=0.15, lw=0)
    a2.semilogx(f, pa, color=COLORS[0])
    a2.semilogx(f, pb, "--", color=COLORS[2], lw=1.5)
    a2.axvline(50, color=COLORS[1], ls=":", lw=1.2)
    a2.axhline(0, color="#999999", lw=0.7)
    pts = [(0.05, "+84.3° at 0.05 Hz", (0.011, 15)), (0.5, "+44.8° at 0.5 Hz", (1.2, 55)),
           (np.sqrt(0.5 * 150), "0° at 8.66 Hz", (12, 30)), (150, "−44.8° at 150 Hz", (400, -25))]
    for fx, lab, xy in pts:
        v = np.degrees(np.angle(1000 * (1j * fx / 0.5) / (1 + 1j * fx / 0.5) / (1 + 1j * fx / f2)))
        a2.plot([fx], [v], "o", color=COLORS[0], ms=5, zorder=5)
        a2.annotate(lab, (fx, v), xytext=xy, fontsize=8,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    a2.set_ylim(-95, 95)
    a2.set_yticks([-90, -45, 0, 45, 90])
    a2.set_ylabel("phase (degrees)")
    a2.set_xlabel("frequency (Hz)")
    a2.set_xlim(0.01, 1e4)
    save(fig, "13", "fig-13-3-ecg-bandpass-bode")


# ---------------------------------------------------------------- 13.4
def fig_13_4():
    """Normalised series-RLC band-pass for Q = 5, 20, 100 at 1 MHz."""
    f0 = 1e6
    f = np.linspace(0.9e6, 1.1e6, 4001)
    u = f / f0 - f0 / f
    fig, a1, a2 = _bode_axes(6.4, 5.2)
    for Q, c, ls in ((5, COLORS[2], "-"), (20, COLORS[0], "-"), (100, COLORS[1], "-")):
        H = 1 / (1 + 1j * Q * u)
        a1.plot(f / 1e6, db(H), color=c, ls=ls, label=f"Q = {Q}  (B = {f0/Q/1e3:.0f} kHz)")
        a2.plot(f / 1e6, np.degrees(np.angle(H)), color=c, ls=ls)
    a1.axhline(-3.01, color="#888888", lw=0.8, ls="--")
    a1.text(1.098, -2.6, "half-power (−3 dB)", fontsize=8, ha="right", va="bottom", color="#555555")
    Q = 100
    f1 = f0 * (np.sqrt(1 + 1 / (4 * Q * Q)) - 1 / (2 * Q))
    f2 = f0 * (np.sqrt(1 + 1 / (4 * Q * Q)) + 1 / (2 * Q))
    for fx in (f1, f2):
        a1.plot([fx / 1e6], [-3.01], "o", color=COLORS[1], ms=4.5, zorder=5)
    a1.annotate("", xy=(f1 / 1e6, -3.01), xytext=(0.95, -32),
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    a1.annotate("", xy=(f2 / 1e6, -3.01), xytext=(1.05, -32),
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    a1.text(0.95, -32.5, f"$f_1$ = {f1/1e3:.1f} kHz", fontsize=8, color=COLORS[1], ha="center",
            va="top")
    a1.text(1.05, -32.5, f"$f_2$ = {f2/1e3:.1f} kHz", fontsize=8, color=COLORS[1], ha="center",
            va="top")
    a1.text(1.0, -35.5, "Q = 100:  B = $f_2-f_1$ = 10 kHz = $f_0/Q$", fontsize=8, color=COLORS[1],
            ha="center", va="top")
    fa = 1.009e6
    va = db(1 / (1 + 1j * Q * (fa / f0 - f0 / fa)))
    a1.plot([fa / 1e6], [va], "s", color=COLORS[1], ms=5, zorder=5)
    a1.annotate(f"1.009 MHz (adjacent channel): {va:.1f} dB".replace("-", "−"), (fa / 1e6, va),
                xytext=(1.032, -14), fontsize=7.5, color=COLORS[1], va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    a1.set_ylim(-40, 1)
    a1.set_ylabel("magnitude (dB)")
    a1.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=8, handlelength=1.5,
              columnspacing=1.2)
    for fx, v in ((f1, 45), (f2, -45)):
        a2.plot([fx / 1e6], [v], "o", color=COLORS[1], ms=4.5, zorder=5)
    a2.annotate("+45° at $f_1$", (f1 / 1e6, 45), xytext=(0.93, 62), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    a2.annotate("−45° at $f_2$", (f2 / 1e6, -45), xytext=(1.035, -65), fontsize=8,
                color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    a2.axhline(0, color="#999999", lw=0.7)
    a2.set_ylim(-95, 95)
    a2.set_yticks([-90, -45, 0, 45, 90])
    a2.set_ylabel("phase (degrees)")
    a2.set_xlabel("frequency (MHz)")
    a2.set_xlim(0.9, 1.1)
    save(fig, "13", "fig-13-4-rlc-resonance-curves")


# ---------------------------------------------------------------- 13.5
def fig_13_5():
    """Third-order Butterworth LC ladder at 10 MHz, 50 ohm, and Butterworth responses."""
    fig = plt.figure(figsize=(6.8, 3.6))
    ax = fig.add_axes([0.0, 0.08, 0.46, 0.84])
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=9, unit=2.0, lw=1.3)
        elm.SourceSin().up(3).at((0, 0))
        elm.Resistor().right(2.2).label("$R_s$ = 50 Ω", loc="top")
        elm.Dot()
        d.push()
        elm.Capacitor().down(3).label("$C_1$" + chr(10) + "318 pF", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Inductor2().right(2.6).label("$L_2$ = 1.59 µH", loc="top")
        elm.Dot()
        d.push()
        elm.Capacitor().down(3).label("$C_3$" + chr(10) + "318 pF", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Line().right(1.8)
        elm.Dot(open=True)
        elm.Resistor().down(3).label("$R_L$" + chr(10) + "50 Ω", loc="bottom")
        elm.Dot(open=True)
        elm.Line().left(6.6)
        elm.Label().at((6.6, 3.55)).label("$V_{out}$", fontsize=9.5)
        elm.Label().at((-0.8, 1.5)).label("$V_s$", fontsize=9.5, halign="right")
        elm.Label().at((3.4, -0.9)).label("3rd-order Butterworth, $f_c$ = 10 MHz", fontsize=9)
    d.draw(show=False)
    b = fig.add_axes([0.58, 0.16, 0.40, 0.76])
    f = np.logspace(6, 8, 1000)
    for n, c in ((1, COLORS[2]), (3, COLORS[0]), (5, COLORS[1])):
        b.semilogx(f / 1e6, -10 * np.log10(1 + (f / 1e7) ** (2 * n)), color=c, label=f"n = {n}")
    b.axhline(-3.01, color="#888888", lw=0.7, ls="--")
    b.axvline(10, color="#888888", lw=0.7, ls="--")
    b.text(1.1, -1.5, "−3 dB at 10 MHz", fontsize=8, va="top")
    for n, c, xy in ((1, COLORS[2], (1.3, -9)), (3, COLORS[0], (5.0, -36))):
        v = -10 * np.log10(1 + 3.0 ** (2 * n))
        b.plot([30], [v], "o", color=c, ms=5, zorder=5)
        b.annotate(f"{v:.1f} dB at 30 MHz".replace("-", "−"), (30, v), xytext=xy, fontsize=8, color=c,
                   arrowprops=dict(arrowstyle="-", lw=0.7, color=c))
    b.set_xlim(1, 100)
    b.set_ylim(-70, 2)
    b.set_xlabel("frequency (MHz)")
    b.set_ylabel("magnitude (dB, re matched load)")
    b.grid(True, which="both", lw=0.4)
    b.legend(loc="lower left", fontsize=8.5)
    save(fig, "13", "fig-13-5-butterworth-ladder")


# ---------------------------------------------------------------- 13.6
def fig_13_6():
    """Three-pole loop gain L = 4/(1 + j w/w1)^3 with margins, closed-loop inset."""
    x = np.logspace(-2, 2, 4000)
    L = 4 / (1 + 1j * x) ** 3
    mag = db(L)
    ph = -3 * np.degrees(np.arctan(x))
    xgc = np.sqrt(4 ** (2 / 3) - 1)
    xpc = np.sqrt(3)
    pgc = -3 * np.degrees(np.arctan(xgc))
    fig, a1, a2 = _bode_axes(6.4, 5.4)
    a1.semilogx(x, mag, color=COLORS[0])
    a1.axhline(0, color=INK, lw=0.8)
    a1.axvline(xgc, color=COLORS[2], lw=0.8, ls="--")
    a1.axvline(xpc, color=COLORS[1], lw=0.8, ls="--")
    a1.plot([xgc], [0], "o", color=COLORS[2], ms=5, zorder=5)
    a1.text(xgc / 1.12, -6, f"gain crossover\nat {xgc:.3f}", fontsize=8, color=COLORS[2], ha="right",
            va="top")
    a1.plot([xpc], [-6.02], "o", color=COLORS[1], ms=5, zorder=5)
    a1.annotate("", xy=(xpc, -6.02), xytext=(xpc, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.2, mutation_scale=9,
                                shrinkA=0, shrinkB=0))
    a1.text(2.3, 4.0, "GM = 6.0 dB", fontsize=8.5, color=COLORS[1], va="center")
    a1.text(2.3, -3.5, "|L| = −6.0 dB at 1.732", fontsize=8, color=COLORS[1], va="center")
    a1.text(0.012, -12, "$L=\\dfrac{4}{(1+j\\omega/\\omega_1)^3}$", fontsize=10, va="center")
    a1.set_ylim(-80, 20)
    a1.set_ylabel("|L| (dB)")
    # inset: closed-loop response
    ins = a1.inset_axes([0.07, 0.08, 0.36, 0.42])
    T = L / (1 + L)
    ins.semilogx(x, db(T) - db(0.8), color=COLORS[3], lw=1.3)
    k = np.argmax(np.abs(T))
    ins.plot([x[k]], [db(T[k]) - db(0.8)], "o", color=COLORS[3], ms=4)
    ins.text(x[k] * 1.35, db(T[k]) - db(0.8), f"+{db(T[k]) - db(0.8):.1f} dB\nat {x[k]:.2f}",
             fontsize=7, color=COLORS[3], va="center")
    ins.set_xlim(0.1, 10)
    ins.set_ylim(-25, 15)
    ins.tick_params(labelsize=7)
    ins.set_title("closed loop |L/(1+L)|, re DC gain 0.8", fontsize=7)
    ins.set_xlabel("ω/ω₁", fontsize=7, labelpad=1)
    ins.set_ylabel("dB", fontsize=7, labelpad=1)
    ins.grid(True, which="both", lw=0.3)
    ins.set_facecolor("white")
    a2.semilogx(x, ph, color=COLORS[0])
    a2.axhline(-180, color=INK, lw=0.8)
    a2.axvline(xgc, color=COLORS[2], lw=0.8, ls="--")
    a2.axvline(xpc, color=COLORS[1], lw=0.8, ls="--")
    a2.plot([xgc], [pgc], "o", color=COLORS[2], ms=5, zorder=5)
    a2.annotate("", xy=(xgc, pgc), xytext=(xgc, -180),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[2], lw=1.2, mutation_scale=9,
                                shrinkA=0, shrinkB=0))
    a2.text(xgc / 1.12, -166, f"PM = {180 + pgc:.1f}°", fontsize=8.5, color=COLORS[2], ha="right")
    a2.text(xgc / 1.12, -192, f"phase at gain crossover\n{pgc:.1f}° at {xgc:.3f}".replace("-", "−"), fontsize=8, color=COLORS[2], ha="right", va="top")
    a2.plot([xpc], [-180], "o", color=COLORS[1], ms=5, zorder=5)
    a2.text(xpc * 1.15, -195, "phase crossover 1.732", fontsize=8, color=COLORS[1], va="top")
    a2.set_ylim(-270, 0)
    a2.set_yticks([0, -45, -90, -135, -180, -225, -270])
    a2.set_ylabel("∠L (degrees)")
    a2.set_xlabel("normalised frequency ω/ω₁")
    a2.set_xlim(0.01, 100)
    save(fig, "13", "fig-13-6-three-pole-loop-margins")


if __name__ == "__main__":
    fig_13_1()
    fig_13_2()
    fig_13_3()
    fig_13_4()
    fig_13_5()
    fig_13_6()
