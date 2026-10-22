"""Figures for Chapter 24 — Advanced Signal Processing.

Run from the repository root:  python figures/scripts/ch24.py
"""
import sys
from pathlib import Path

import numpy as np
import scipy.signal as ss
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, GRID, box, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


# ----------------------------------------------------------------------------
# diagram helpers
# ----------------------------------------------------------------------------
def _ln(ax, pts, arrow=False, color=INK, lw=1.1, ls="-"):
    pts = np.asarray(pts, float)
    if arrow:
        if len(pts) > 2:
            ax.plot(pts[:-1, 0], pts[:-1, 1], color=color, lw=lw, ls=ls)
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0,
                                    mutation_scale=9, ls=ls))
    else:
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=ls)


def _sum(ax, x, y, r=0.22, signs=None, fs=8):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(x, y - 0.01, r"$\Sigma$", ha="center", va="center", fontsize=fs + 1, zorder=4)
    if signs:
        for (dx, dy, s) in signs:
            ax.text(x + dx, y + dy, s, ha="center", va="center", fontsize=fs + 1, zorder=4)


def _dot(ax, x, y, r=0.05):
    ax.add_patch(Circle((x, y), r, fc=INK, ec=INK, zorder=4))


def _down(ax, x, y, M, w=0.75, h=0.55, fs=9):
    """Down-sampler box with a down-arrow and factor."""
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, rf"$\downarrow {M}$", ha="center", va="center", fontsize=fs, zorder=4)


# ----------------------------------------------------------------------------
def _tri(w, edge):
    """Triangular baseband spectrum of unit height reaching `edge` (rad), periodic 2*pi."""
    wr = np.mod(w + np.pi, 2 * np.pi) - np.pi
    return np.clip(1 - np.abs(wr) / edge, 0, None)


def fig_24_1():
    """Spectra for decimation by 3 and interpolation by 3."""
    w = np.linspace(-np.pi, np.pi, 4001)
    M = 3
    fig, axs = plt.subplots(4, 1, figsize=(6.4, 6.6), sharex=True)

    # (a) input, triangle to 0.5 pi
    X = _tri(w, 0.5 * np.pi)
    ax = axs[0]
    ax.fill_between(w, X, color=COLORS[0], alpha=0.25, lw=0)
    ax.plot(w, X, color=COLORS[0])
    ax.plot([-np.pi, -np.pi / 3, -np.pi / 3, np.pi / 3, np.pi / 3, np.pi],
            [0, 0, 1.1, 1.1, 0, 0], color=INK, ls="--", lw=1.0)
    m = np.abs(w) > np.pi / 3
    ax.fill_between(w, X, where=m, color=COLORS[1], alpha=0.45, lw=0)
    ax.text(0.62 * np.pi, 0.75, "content above $\\pi/3$\nwould alias:\nremoved by the\ndecimation filter",
            fontsize=7.5, color=COLORS[1], va="center")
    ax.text(-np.pi / 3 - 0.08, 1.12, r"$H_d$, cutoff $\pi/3$", ha="right", va="bottom", fontsize=8)
    ax.set_title(r"(a) input $X(e^{j\omega})$, band edge $0.5\pi$", loc="left", fontsize=9.5)

    # (b) filtered and downsampled: (1/M) sum X_f((w - 2 pi k)/M)
    Xf = lambda v: _tri(v, 0.5 * np.pi) * (np.abs(np.mod(v + np.pi, 2 * np.pi) - np.pi) <= np.pi / 3)
    Yb = sum(Xf((w - 2 * np.pi * k) / M) for k in range(M)) / M
    Yalias = sum(_tri((w - 2 * np.pi * k) / M, 0.5 * np.pi) for k in range(M)) / M
    ax = axs[1]
    ax.plot(w, Yalias, color=COLORS[1], ls=":", lw=1.2, label="without filter (aliased)")
    ax.fill_between(w, Yb, color=COLORS[0], alpha=0.25, lw=0)
    ax.plot(w, Yb, color=COLORS[0], label="filtered, then $\\downarrow 3$")
    ax.legend(loc="upper right", fontsize=7.5, borderaxespad=0.1)
    ax.set_title(r"(b) after filtering and $\downarrow 3$: spectrum stretched by 3, height $\times 1/3$",
                 loc="left", fontsize=9.5)

    # (c) baseband to 0.8 pi before upsampling
    Xc = _tri(w, 0.8 * np.pi)
    ax = axs[2]
    ax.fill_between(w, Xc, color=COLORS[2], alpha=0.25, lw=0)
    ax.plot(w, Xc, color=COLORS[2])
    ax.set_title(r"(c) input to the interpolator, band edge $0.8\pi$", loc="left", fontsize=9.5)

    # (d) upsampled: X(e^{j 3 w})
    Xd = _tri(3 * w, 0.8 * np.pi)
    ax = axs[3]
    base = np.abs(w) <= np.pi / 3
    ax.fill_between(w, Xd, where=base, color=COLORS[2], alpha=0.25, lw=0)
    ax.fill_between(w, Xd, where=~base, color=COLORS[3], alpha=0.35, lw=0)
    ax.plot(w, Xd, color=COLORS[2])
    ax.plot([-np.pi, -np.pi / 3, -np.pi / 3, np.pi / 3, np.pi / 3, np.pi],
            [0, 0, 3, 3, 0, 0], color=INK, ls="--", lw=1.0)
    ax.text(np.pi / 3 + 0.06, 2.75, r"anti-imaging filter: cutoff $\pi/3$, gain 3", fontsize=8,
            va="center")
    for c in (-2 * np.pi / 3, 2 * np.pi / 3):
        ax.text(c, 1.12, "image", ha="center", va="bottom", fontsize=8, color=COLORS[3])
    ax.text(0, 1.12, r"$\pm0.27\pi$", ha="center", va="bottom", fontsize=8, color=COLORS[2])
    ax.set_title(r"(d) after $\uparrow 3$: baseband compressed by 3, images at $\pm 2\pi/3$",
                 loc="left", fontsize=9.5)

    for i, ax in enumerate(axs):
        ax.set_xlim(-np.pi, np.pi)
        ax.set_ylim(0, 3.4 if i == 3 else 1.45)
        ax.set_ylabel("|·|")
        ax.axhline(0, color=INK, lw=0.6)
    axs[1].set_ylim(0, 0.75)
    ticks = np.arange(-3, 4) * np.pi / 3
    axs[-1].set_xticks(ticks)
    axs[-1].set_xticklabels([r"$-\pi$", r"$-2\pi/3$", r"$-\pi/3$", "0", r"$\pi/3$", r"$2\pi/3$", r"$\pi$"])
    axs[-1].set_xlabel(r"Normalised frequency $\omega$ (rad/sample)")
    for ax in axs:
        ax.grid(axis="x", color=GRID, lw=0.6)
    fig.tight_layout(h_pad=0.5)
    save(fig, "24", "fig-24-1-decimation-interpolation-spectra")


# ----------------------------------------------------------------------------
def fig_24_2():
    """Direct-form vs polyphase decimator, plus the three-stage audio decimator."""
    fig, ax = schematic(6.8, 5.3, xlim=(0, 14), ylim=(0, 10.9))

    # ---- direct form
    y = 9.7
    ax.text(0.1, 10.6, "Direct form: filter at the input rate, then discard", fontsize=9.5,
            weight="bold", va="center")
    ax.text(0.2, y + 0.15, r"$x[n]$", fontsize=10, va="bottom")
    _ln(ax, [(0.2, y), (2.8, y)], arrow=True)
    box(ax, 2.8, y - 0.45, 2.6, 0.9, r"$H(z)$, $N$ taps", fontsize=9)
    _ln(ax, [(5.4, y), (6.6, y)], arrow=True)
    _down(ax, 7.0, y, "M")
    _ln(ax, [(7.375, y), (9.0, y)], arrow=True)
    ax.text(9.05, y, r"$y[m]$", fontsize=10, va="center")
    ax.text(4.1, y - 0.75, r"$N$ MACs per input sample  ($= NM$ per output sample)", fontsize=8.5,
            ha="center", va="top", color=COLORS[1])

    # ---- polyphase form
    ax.text(0.1, 7.75, "Polyphase form: commutator feeds M short sub-filters at the output rate",
            fontsize=9.5, weight="bold", va="center")
    ys = [6.9, 5.7, 3.9]
    labs = [r"$E_0(z)$", r"$E_1(z)$", r"$E_{M-1}(z)$"]
    xc, yc = 2.0, 5.7  # commutator pivot
    ax.text(0.2, yc + 0.15, r"$x[n]$", fontsize=10, va="bottom")
    _ln(ax, [(0.2, yc), (xc, yc)])
    _dot(ax, xc, yc, 0.07)
    xk = 3.4  # contacts
    for yy in ys:
        ax.add_patch(Circle((xk, yy), 0.07, fc="white", ec=INK, lw=1.0, zorder=4))
    _ln(ax, [(xc, yc), (xk - 0.08, ys[0] - 0.05)], lw=1.4)   # blade on E0 contact
    arc = FancyArrowPatch((2.7, 4.3), (2.7, 6.55), connectionstyle="arc3,rad=0.3",
                          arrowstyle="-|>", mutation_scale=9, lw=1.0, color=COLORS[0])
    ax.add_patch(arc)
    ax.text(1.0, 4.55, "commutator\n(counter-clockwise,\none sample per branch)", fontsize=7.5,
            color=COLORS[0], ha="center", va="center")
    ax.text(5.6, 4.85, r"$\vdots$", fontsize=12, ha="center", va="center")
    for yy, lab in zip(ys, labs):
        _ln(ax, [(xk + 0.07, yy), (4.2, yy)], arrow=True)
        box(ax, 4.2, yy - 0.38, 2.9, 0.76, lab + r", $N/M$ taps", fontsize=8.5)
    xs_ = 8.3
    _ln(ax, [(7.1, ys[0]), (xs_, ys[0]), (xs_, yc + 0.22)], arrow=True)
    _ln(ax, [(7.1, ys[2]), (xs_, ys[2]), (xs_, yc - 0.22)], arrow=True)
    _ln(ax, [(7.1, ys[1]), (xs_ - 0.22, ys[1])], arrow=True)
    _sum(ax, xs_, yc)
    _ln(ax, [(xs_ + 0.22, yc), (9.4, yc)], arrow=True)
    ax.text(9.45, yc, r"$y[m]$", fontsize=10, va="center")
    ax.text(11.6, 4.4, r"$N$ MACs per output" "\n" r"sample (factor $M$" "\n" r"saving); all sub-filters" "\n"
            r"run at $f_s/M$", fontsize=8.5, ha="center", va="center", color=COLORS[2])

    # ---- side note: three-stage audio decimator
    ax.plot([0.1, 13.9], [2.75, 2.75], color=GRID, lw=1.0)
    ax.text(0.1, 2.35, "Example: three-stage decimator of a 24-bit audio ADC", fontsize=9.5,
            weight="bold", va="center")
    yy = 0.9
    stages = ["CIC\nR = 16, N = 4", "FIR, 22 taps\n↓2", "FIR, 154 taps\n↓2"]
    rates = ["3.072 MHz", "192 kHz", "96 kHz", "48 kHz"]
    bx = [2.2, 5.9, 9.6]
    bw = 2.2
    edges = [0.1] + [b + bw for b in bx]
    for k, b in enumerate(bx):
        _ln(ax, [(edges[k] if k == 0 else bx[k - 1] + bw, yy), (b, yy)], arrow=True)
        box(ax, b, yy - 0.45, bw, 0.9, stages[k], fontsize=8)
    _ln(ax, [(bx[-1] + bw, yy), (13.6, yy)], arrow=True)
    mids = [(0.1 + bx[0]) / 2, (bx[0] + bw + bx[1]) / 2, (bx[1] + bw + bx[2]) / 2, (bx[2] + bw + 13.6) / 2]
    for m_, r_ in zip(mids, rates):
        ax.text(m_, yy + 0.12, r_, fontsize=8, ha="center", va="bottom")
    save(fig, "24", "fig-24-2-polyphase-decimator")


# ----------------------------------------------------------------------------
def _af_box(ax, x, y, w, h, text, fs=8):
    box(ax, x, y, w, h, "", fc="#E8F1E6", fontsize=fs)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=6,
            bbox=dict(fc="#E8F1E6", ec="none", alpha=0.85, pad=0.3))


def _panel(ax, x0, y0, title, kind):
    """Small configuration panel, local frame 6.6 x 3.3 with origin (x0, y0)."""
    X = lambda x: x0 + x
    Y = lambda y: y0 + y
    ax.add_patch(Rectangle((x0, y0), 6.6, 3.45, fc="none", ec="#BBBBBB", lw=0.8))
    ax.text(X(0.12), Y(3.22), title, fontsize=8.5, weight="bold", va="center")
    yb, yt = 1.05, 2.35          # bottom (filter) path and top (desired) path
    xs = 5.0                     # summing junction
    afx, afw = 2.75, 1.45
    _af_box(ax, X(afx), Y(yb - 0.38), afw, 0.76, "adaptive\nFIR", fs=7.5)
    _sum(ax, X(xs), Y(yb), r=0.2, fs=7)
    ax.text(X(xs - 0.36), Y(yb + 0.22), "−", fontsize=9, ha="center", va="center")
    ax.text(X(xs + 0.3), Y(yb + 0.42), "+", fontsize=8, ha="center", va="center")
    _ln(ax, [(X(afx + afw), Y(yb)), (X(xs - 0.2), Y(yb))], arrow=True)
    ax.text(X(4.45), Y(yb - 0.08), r"$y$", fontsize=8, va="top", ha="center")
    _ln(ax, [(X(xs), Y(yt)), (X(xs), Y(yb + 0.2))], arrow=True)
    _ln(ax, [(X(xs + 0.2), Y(yb)), (X(6.45), Y(yb))], arrow=True)
    # error feedback to the adaptive filter
    _dot(ax, X(5.75), Y(yb))
    _ln(ax, [(X(5.75), Y(yb)), (X(5.75), Y(0.25)), (X(afx + 0.1), Y(0.25))])
    _ln(ax, [(X(afx + 0.1), Y(0.25)), (X(afx + afw - 0.1), Y(yb + 0.55))], arrow=True, color=COLORS[1])
    out_lab = {"a": r"$e$", "b": r"$e$", "c": r"$e$", "d": r"$e\approx s$"}[kind]
    ax.text(X(6.45), Y(yb + 0.1), out_lab, fontsize=8, ha="right", va="bottom")
    if kind == "a":
        ax.text(X(0.1), Y(yb + 0.08), r"$x[n]$", fontsize=8, va="bottom")
        _dot(ax, X(1.0), Y(yb))
        _ln(ax, [(X(0.1), Y(yb)), (X(afx), Y(yb))], arrow=True)
        _ln(ax, [(X(1.0), Y(yb)), (X(1.0), Y(yt)), (X(2.4), Y(yt))], arrow=True)
        box(ax, X(2.4), Y(yt - 0.38), 2.15, 0.76, "unknown plant\n(echo path)", fontsize=7.5)
        _ln(ax, [(X(4.55), Y(yt)), (X(xs), Y(yt))])
        ax.text(X(xs + 0.08), Y(yt - 0.35), r"$d$", fontsize=8, va="center")
    elif kind == "b":
        ax.text(X(0.1), Y(yt + 0.08), r"$s[n]$", fontsize=8, va="bottom")
        _dot(ax, X(0.75), Y(yt))
        _ln(ax, [(X(0.1), Y(yt)), (X(2.6), Y(yt))], arrow=True)
        box(ax, X(2.6), Y(yt - 0.32), 1.0, 0.64, r"$z^{-\Delta}$", fontsize=8)
        _ln(ax, [(X(3.6), Y(yt)), (X(xs), Y(yt))])
        ax.text(X(3.75), Y(yt + 0.08), "delayed training", fontsize=7, va="bottom")
        ax.text(X(xs + 0.08), Y(yt - 0.35), r"$d$", fontsize=8, va="center")
        _ln(ax, [(X(0.75), Y(yt)), (X(0.75), Y(yb)), (X(1.05), Y(yb))], arrow=True)
        box(ax, X(1.05), Y(yb - 0.32), 1.2, 0.64, "channel", fontsize=7.5)
        _ln(ax, [(X(2.25), Y(yb)), (X(afx), Y(yb))], arrow=True)
        ax.text(X(2.5), Y(yb + 0.08), r"$x$", fontsize=8, va="bottom", ha="center")
    elif kind == "c":
        ax.text(X(0.1), Y(yt + 0.08), r"$s[n]$", fontsize=8, va="bottom")
        _dot(ax, X(0.75), Y(yt))
        _ln(ax, [(X(0.1), Y(yt)), (X(xs), Y(yt))])
        ax.text(X(xs + 0.08), Y(yt - 0.35), r"$d$", fontsize=8, va="center")
        _ln(ax, [(X(0.75), Y(yt)), (X(0.75), Y(yb)), (X(1.05), Y(yb))], arrow=True)
        box(ax, X(1.05), Y(yb - 0.32), 1.1, 0.64, r"$z^{-D}$", fontsize=8)
        _ln(ax, [(X(2.15), Y(yb)), (X(afx), Y(yb))], arrow=True)
        ax.text(X(2.45), Y(yb + 0.08), r"$x$", fontsize=8, va="bottom", ha="center")
    elif kind == "d":
        ax.text(X(0.1), Y(yt + 0.08), r"primary $s+n_0$", fontsize=8, va="bottom")
        _ln(ax, [(X(0.1), Y(yt)), (X(xs), Y(yt))])
        ax.text(X(xs + 0.08), Y(yt - 0.35), r"$d$", fontsize=8, va="center")
        ax.text(X(0.1), Y(yb + 0.08), r"reference $n_1$", fontsize=8, va="bottom")
        _ln(ax, [(X(0.1), Y(yb)), (X(afx), Y(yb))], arrow=True)
        ax.text(X(2.45), Y(yb - 0.08), r"$x$", fontsize=8, va="top", ha="center")


def fig_24_3():
    """Generic adaptive filter and its four standard configurations."""
    fig, ax = schematic(6.8, 5.6, xlim=(0, 13.6), ylim=(0, 11.2))
    # top panels
    _panel(ax, 0.1, 7.65, "(a) System identification", "a")
    _panel(ax, 6.9, 7.65, "(b) Inverse modelling (equalisation)", "b")
    _panel(ax, 0.1, 0.1, "(c) Prediction  ($e$ = prediction error)", "c")
    _panel(ax, 6.9, 0.1, "(d) Interference cancelling", "d")

    # centre: generic adaptive filter
    yc = 5.35
    ax.text(6.8, 7.15, "Generic adaptive filter", fontsize=9.5, weight="bold", ha="center")
    ax.text(2.0, yc + 0.12, r"$x[n]$", fontsize=10, va="bottom")
    _ln(ax, [(2.0, yc), (4.6, yc)], arrow=True)
    _af_box(ax, 4.6, yc - 0.6, 3.0, 1.2, "adaptive FIR filter\n" r"$\mathbf{w}[n]$", fs=9)
    _ln(ax, [(7.6, yc), (9.18, yc)], arrow=True)
    ax.text(8.35, yc + 0.1, r"$y[n]$", fontsize=10, va="bottom", ha="center")
    _sum(ax, 9.45, yc, r=0.27)
    ax.text(9.0, yc - 0.32, "−", fontsize=11, ha="center", va="center")
    ax.text(9.75, yc + 0.5, "+", fontsize=11, ha="center", va="center")
    _ln(ax, [(9.45, 6.75), (9.45, yc + 0.27)], arrow=True)
    ax.text(9.6, 6.6, r"$d[n]$", fontsize=10, va="center")
    _ln(ax, [(9.72, yc), (12.2, yc)], arrow=True)
    ax.text(12.25, yc, r"$e[n]=d[n]-y[n]$", fontsize=9, va="center", ha="left")
    ax.text(12.25, yc, "", fontsize=9)
    _dot(ax, 10.6, yc)
    _ln(ax, [(10.6, yc), (10.6, 4.05), (4.2, 4.05)])
    _ln(ax, [(4.2, 4.05), (7.9, 6.25)], arrow=True, color=COLORS[1], lw=1.3)
    ax.text(3.0, 4.1, "LMS update", fontsize=9, color=COLORS[1], ha="center", va="center")
    ax.set_xlim(0, 13.6)
    save(fig, "24", "fig-24-3-adaptive-filter-configurations")


# ----------------------------------------------------------------------------
def fig_24_4():
    """LMS mains canceller: weight convergence and equivalent notch."""
    fs = 500.0
    f0 = 50.0
    w0 = 2 * np.pi * f0 / fs
    n = np.arange(int(2.0 * fs) + 1)
    x1, x2 = np.cos(w0 * n), np.sin(w0 * n)
    rng = np.random.default_rng(24)
    A, ph = 1.0, 0.7
    hum = A * np.cos(w0 * n + ph)
    ecg = 0.05 * rng.standard_normal(n.size)     # broadband "ECG + noise" component
    d = hum + ecg
    wopt = np.array([A * np.cos(ph), -A * np.sin(ph)])

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.8, 4.0))
    for mu, c in [(0.01, COLORS[0]), (0.005, COLORS[2])]:
        wv = np.zeros(2)
        err = np.empty(n.size)
        for k in range(n.size):
            err[k] = np.linalg.norm(wv - wopt) / np.linalg.norm(wopt)
            xv = np.array([x1[k], x2[k]])
            e = d[k] - wv @ xv
            wv = wv + mu * e * xv
        tau = 1 / (mu * 0.5) / fs
        ax.plot(n / fs, err, color=c, lw=1.4, label=rf"$\mu$ = {mu}, simulated")
        ax.plot(n / fs, np.exp(-n / fs / tau), color=c, ls="--", lw=1.0,
                label=rf"$e^{{-t/{tau:.1f}\,\mathrm{{s}}}}$")
    ax.axhline(np.exp(-1), color="#999999", lw=0.6, ls=":")
    ax.text(1.98, np.exp(-1) + 0.02, "0.37", fontsize=8, ha="right", va="bottom", color="#666666")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"Normalised weight error $\|\mathbf{w}-\mathbf{w}_o\|/\|\mathbf{w}_o\|$")
    ax.legend(fontsize=7.5, loc="upper right")
    ax.set_title("Convergence ($f_s$ = 500 Hz)", fontsize=9.5)

    f = np.linspace(45, 55, 20001)
    for mu, c in [(0.01, COLORS[0]), (0.005, COLORS[2])]:
        b = [1, -2 * np.cos(w0), 1]
        a = [1, -2 * (1 - mu / 2) * np.cos(w0), 1 - mu]
        _, H = ss.freqz(b, a, worN=2 * np.pi * f / fs)
        G = 20 * np.log10(np.abs(H) + 1e-12)
        idx = np.where(G < -3.0103)[0]
        bw = f[idx[-1]] - f[idx[0]]
        ax2.plot(f, G, color=c, lw=1.4, label=rf"LMS $\mu$={mu}: {bw:.2f} Hz")
    # fixed notch of Chapter 23 (fs = 1 kHz, r = 0.99)
    w0b, r = 2 * np.pi * 50 / 1000, 0.99
    _, H = ss.freqz([1, -2 * np.cos(w0b), 1], [1, -2 * r * np.cos(w0b), r * r], worN=2 * np.pi * f / 1000)
    G = 20 * np.log10(np.abs(H) + 1e-12)
    idx = np.where(G < -3.0103)[0]
    bw = f[idx[-1]] - f[idx[0]]
    ax2.plot(f, G, color=INK, ls="--", lw=1.1, label=f"fixed, r=0.99: {bw:.1f} Hz")
    ax2.axhline(-3, color="#999999", lw=0.6, ls=":")
    ax2.text(54.9, -3.6, "−3 dB", fontsize=7.5, color="#666666", va="top", ha="right")
    ax2.set_xlim(45, 55)
    ax2.set_ylim(-40, 1)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Gain (dB)")
    ax2.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.2), handlelength=1.6)
    ax2.set_title("Equivalent notch (3 dB widths)", fontsize=9.5)
    fig.tight_layout(w_pad=1.5)
    save(fig, "24", "fig-24-4-lms-mains-canceller")


# ----------------------------------------------------------------------------
def _resonator(fc, bw, fs):
    r = np.exp(-np.pi * bw / fs)
    th = 2 * np.pi * fc / fs
    a = [1, -2 * r * np.cos(th), r * r]
    g = np.sum(a)  # unit DC gain
    return [g], a


def fig_24_5():
    """Narrowband vs wideband spectrograms of a synthetic voiced sound plus a chirp."""
    fs = 16000
    T = 0.5
    t = np.arange(int(T * fs)) / fs
    # 120 Hz glottal pulse train (pulse positions rounded to the nearest sample)
    pulses = np.zeros_like(t)
    tp = np.arange(0, T, 1 / 120)
    pulses[np.round(tp * fs).astype(int)[np.round(tp * fs).astype(int) < t.size]] = 1.0
    v = pulses
    for fc, bw in [(700, 90), (1200, 110)]:
        b, a = _resonator(fc, bw, fs)
        v = ss.lfilter(b, a, v)
    v = v / np.max(np.abs(v))
    # linear chirp 2 -> 3.5 kHz between 0.2 and 0.4 s
    ch = np.zeros_like(t)
    m = (t >= 0.2) & (t < 0.4)
    tc = t[m] - 0.2
    ch[m] = 0.08 * np.sin(2 * np.pi * (2000 * tc + 0.5 * (1500 / 0.2) * tc ** 2)) * np.hanning(m.sum()) ** 0.2
    x = v + ch + 1e-5 * np.random.default_rng(5).standard_normal(t.size)

    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.6), sharey=True)
    cfgs = [(400, 160, "25 ms Hann window, hop 10 ms", "3 dB resolution 57.6 Hz"),
            (80, 16, "5 ms Hann window, hop 1 ms", "3 dB resolution 288 Hz")]
    for ax, (L, hop, tt, res) in zip(axs, cfgs):
        f, tt_, S = ss.spectrogram(x, fs=fs, window="hann", nperseg=L, noverlap=L - hop,
                                   nfft=max(1024, L), mode="psd", scaling="spectrum")
        SdB = 10 * np.log10(S / S.max() + 1e-20)
        im = ax.pcolormesh(tt_, f / 1e3, SdB, vmin=-60, vmax=0, cmap="magma", shading="auto",
                           rasterized=True)
        ax.set_xlim(0, 0.5)
        ax.set_ylim(0, 4)
        ax.set_xlabel("Time (s)")
        ax.set_title(tt, fontsize=9)
        ax.text(0.015, 3.85, res, color="white", fontsize=8, va="top",
                bbox=dict(fc="black", alpha=0.45, ec="none", pad=1.5))
    axs[0].set_ylabel("Frequency (kHz)")
    axs[0].text(0.015, 3.55, "harmonics every 120 Hz", color="white", fontsize=7.5, va="top")
    axs[1].text(0.015, 3.55, "pulses every 8.3 ms", color="white", fontsize=7.5, va="top")
    for ax in axs:
        ax.text(0.36, 2.4, "chirp", color="white", fontsize=7.5, ha="center")
    cb = fig.colorbar(im, ax=axs, fraction=0.035, pad=0.02)
    cb.set_label("Level (dB re max)")
    save(fig, "24", "fig-24-5-spectrogram-window-tradeoff")


# ----------------------------------------------------------------------------
def fig_24_6():
    """Three-level DWT filter bank and octave-band tiling at fs = 360 Hz."""
    fig, ax = schematic(6.8, 5.2, xlim=(0, 14), ylim=(0, 10.7))

    def split(x, y, dy, label_hi, label_lo, rate):
        """One two-channel analysis stage starting at node (x, y)."""
        _dot(ax, x, y)
        yh, yl = y + dy, y - dy
        _ln(ax, [(x, y), (x, yh), (x + 0.4, yh)], arrow=True)
        _ln(ax, [(x, y), (x, yl), (x + 0.4, yl)], arrow=True)
        box(ax, x + 0.4, yh - 0.3, 0.75, 0.6, r"$g$", fc="#FCEBD9", fontsize=9)
        box(ax, x + 0.4, yl - 0.3, 0.75, 0.6, r"$h$", fc="#E8F1E6", fontsize=9)
        for yy in (yh, yl):
            _ln(ax, [(x + 1.15, yy), (x + 1.45, yy)], arrow=True)
            _down(ax, x + 1.8, yy, 2, w=0.7, h=0.5)
        _ln(ax, [(x + 2.15, yh), (x + 2.55, yh)], arrow=True)
        ax.text(x + 2.6, yh, label_hi, fontsize=8.5, va="center")
        return x + 2.15, yl

    ax.text(0.1, 10.35, "Mallat's algorithm: iterated two-channel filter bank", fontsize=9.5,
            weight="bold", va="center")
    ax.text(0.1, 7.7, r"$x[n]$", fontsize=9, va="bottom")
    ax.text(0.1, 7.5, "360 Hz", fontsize=8, va="top")
    _ln(ax, [(0.1, 7.6), (1.3, 7.6)])
    x, y = split(1.3, 7.6, 1.4, r"$d_1$: 90–180 Hz  (at 180 Hz)", None, None)
    _ln(ax, [(x, y), (x + 0.4, y)])
    x, y = split(x + 0.4, y, 0.8, r"$d_2$: 45–90 Hz  (at 90 Hz)", None, None)
    _ln(ax, [(x, y), (x + 0.4, y)])
    x, y = split(x + 0.4, y, 0.6, r"$d_3$: 22.5–45 Hz  (45 Hz)", None, None)
    _ln(ax, [(x, y), (x + 0.4, y)], arrow=True)
    ax.text(x + 0.45, y, r"$a_3$: 0–22.5 Hz  (45 Hz)", fontsize=8.5, va="center")
    ax.text(0.1, 5.4, r"$g$: highpass,  $h$: lowpass", fontsize=8, color="#555555")

    # tiling
    x0, x1 = 1.6, 13.4
    sc = (x1 - x0) / 180.0
    ya, yb = 2.75, 0.75
    ax.text(0.1, 3.95, "Frequency-axis tiling", fontsize=9.5, weight="bold", va="center")
    bands = [("$a_3$", 0, 22.5, COLORS[0]), ("$d_3$", 22.5, 45, COLORS[2]), ("$d_2$", 45, 90, COLORS[4]),
             ("$d_1$", 90, 180, COLORS[1])]
    for lab, f1, f2, c in bands:
        ax.add_patch(Rectangle((x0 + f1 * sc, ya), (f2 - f1) * sc, 0.75, fc=c, alpha=0.35, ec=INK, lw=0.8))
        ax.text(x0 + (f1 + f2) / 2 * sc, ya + 0.375, lab, fontsize=9, ha="center", va="center")
    ax.text(x0 - 0.15, ya + 0.375, "DWT\n(octave)", fontsize=8, ha="right", va="center")
    for k in range(8):
        ax.add_patch(Rectangle((x0 + k * 22.5 * sc, yb), 22.5 * sc, 0.75, fc="#DDDDDD", ec=INK, lw=0.8))
    ax.text(x0 + 11.25 * sc * 15, yb + 0.375, "", fontsize=8)
    ax.text(x0 - 0.15, yb + 0.375, "STFT\n(uniform)", fontsize=8, ha="right", va="center")
    ax.text(x0 + 90 * sc, yb + 0.375, "eight equal 22.5 Hz bins", fontsize=8, ha="center", va="center",
            bbox=dict(fc="#DDDDDD", ec="none", pad=0.5))
    # axis
    yax = 0.45
    _ln(ax, [(x0, yax), (x1 + 0.2, yax)], arrow=True)
    for fv in (0, 22.5, 45, 90, 180):
        ax.plot([x0 + fv * sc] * 2, [yax - 0.08, yax + 0.08], color=INK, lw=1)
        ax.text(x0 + fv * sc, yax - 0.15, f"{fv:g}", fontsize=8, ha="center", va="top")
    ax.text(x1 + 0.35, yax + 0.05, "Hz", fontsize=8, ha="left", va="top")
    save(fig, "24", "fig-24-6-dwt-filter-bank")


if __name__ == "__main__":
    fig_24_1()
    fig_24_2()
    fig_24_3()
    fig_24_4()
    fig_24_5()
    fig_24_6()
