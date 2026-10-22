"""Figures for Chapter 23 — Digital Filters.

Run from the repository root:  python figures/scripts/ch23.py
"""
import sys
from pathlib import Path

import numpy as np
import scipy.signal as ss
from matplotlib.patches import Circle, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, GRID, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


# ----------------------------------------------------------------------------
# small drawing helpers for signal-flow diagrams
# ----------------------------------------------------------------------------
def _line(ax, pts, arrow_end=False, color=INK, lw=1.1):
    pts = np.asarray(pts, float)
    if arrow_end and len(pts) >= 2:
        ax.plot(pts[:-1, 0], pts[:-1, 1], color=color, lw=lw, solid_capstyle="butt")
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0,
                                    mutation_scale=9))
    else:
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, solid_capstyle="butt")


def _adder(ax, x, y, r=0.2):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(x, y - 0.01, "+", ha="center", va="center", fontsize=10, zorder=4)


def _node(ax, x, y):
    ax.add_patch(Circle((x, y), 0.06, fc=INK, ec=INK, zorder=4))


def _delay(ax, x, y, w=0.7, h=0.5, label=r"$z^{-1}$"):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#EEF3F8", ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=9, zorder=4)


def _gain(ax, x, y, label, direction="down", s=0.32, label_side="right"):
    """Triangle multiplier centred at (x, y) pointing in `direction`."""
    if direction == "down":
        pts = [(x - s, y + s * 0.8), (x + s, y + s * 0.8), (x, y - s * 0.8)]
    elif direction == "right":
        pts = [(x - s * 0.8, y + s), (x - s * 0.8, y - s), (x + s * 0.8, y)]
    else:  # left
        pts = [(x + s * 0.8, y + s), (x + s * 0.8, y - s), (x - s * 0.8, y)]
    ax.add_patch(Polygon(pts, closed=True, fc="#FCEBD9", ec=INK, lw=1.0, zorder=3))
    off = {"right": (s + 0.08, 0, "left", "center"), "left": (-s - 0.08, 0, "right", "center"),
           "above": (0, s + 0.1, "center", "bottom"), "below": (0, -s - 0.1, "center", "top")}[label_side]
    ax.text(x + off[0], y + off[1], label, ha=off[2], va=off[3], fontsize=9, zorder=4)


# ----------------------------------------------------------------------------
def fig_23_1():
    """FIR tapped delay line (left) and transposed direct form II biquad (right)."""
    fig, ax = schematic(6.8, 3.3, xlim=(-0.2, 14.4), ylim=(-0.5, 6.4))

    # ---------------- FIR direct form ----------------
    ax.text(3.2, 6.15, "FIR direct form (M = 4)", ha="center", va="center", fontsize=10, weight="bold")
    yx, yg, ya = 4.9, 3.3, 1.6
    xs = [0.9, 2.3, 3.7, 5.1, 6.5]
    ax.text(-0.15, yx + 0.25, r"$x[n]$", ha="left", va="bottom", fontsize=10)
    _line(ax, [(-0.15, yx), (xs[0], yx)])
    for i in range(4):
        xm = (xs[i] + xs[i + 1]) / 2
        _line(ax, [(xs[i], yx), (xm - 0.35, yx)], arrow_end=True)
        _delay(ax, xm, yx)
        _line(ax, [(xm + 0.35, yx), (xs[i + 1], yx)])
    for i, x in enumerate(xs):
        _node(ax, x, yx)
        _line(ax, [(x, yx), (x, yg + 0.26)], arrow_end=True)
        _gain(ax, x, yg, rf"$b_{i}$", "down", label_side="right")
        if i == 0:
            _line(ax, [(x, yg - 0.26), (x, ya)])
        else:
            _line(ax, [(x, yg - 0.26), (x, ya + 0.2)], arrow_end=True)
            _adder(ax, x, ya)
    # accumulation chain
    _line(ax, [(xs[0], ya), (xs[1] - 0.2, ya)], arrow_end=True)
    for i in range(1, 4):
        _line(ax, [(xs[i] + 0.2, ya), (xs[i + 1] - 0.2, ya)], arrow_end=True)
    _line(ax, [(xs[4] + 0.2, ya), (7.25, ya)], arrow_end=True)
    ax.text(7.25, ya - 0.2, r"$y[n]$", ha="right", va="top", fontsize=10)
    ax.text(3.7, 0.35, "5 multiplies, 4 delays,\n4 additions per output sample",
            ha="center", va="center", fontsize=8.5, color="#444444")

    # ---------------- Transposed direct form II biquad ----------------
    ax.plot([7.55, 7.55], [-0.3, 6.3], color=GRID, lw=1.0)
    ax.text(11.0, 6.15, "IIR biquad, transposed direct form II", ha="center", va="center",
            fontsize=10, weight="bold")
    xin, xa, xout = 8.3, 11.0, 13.4
    y0, y1, y2 = 5.0, 3.1, 1.2
    # input bus
    ax.text(7.75, y0 + 0.25, r"$x[n]$", ha="left", va="bottom", fontsize=10)
    _line(ax, [(7.75, y0), (xin, y0)])
    _line(ax, [(xin, y0), (xin, y2)])
    for y, lab in [(y0, r"$b_0$"), (y1, r"$b_1$"), (y2, r"$b_2$")]:
        _node(ax, xin, y)
        _line(ax, [(xin, y), (9.25, y)])
        _gain(ax, 9.5, y, lab, "right", s=0.28, label_side="above")
        _line(ax, [(9.75, y), (xa - 0.2, y)], arrow_end=True)
        _adder(ax, xa, y)
    # delays between adders (upwards)
    for ylo, yhi, st in [(y1, y0, r"$s_1$"), (y2, y1, r"$s_2$")]:
        ym = (ylo + yhi) / 2
        _line(ax, [(xa, ylo + 0.2), (xa, ym - 0.25)])
        _delay(ax, xa, ym)
        _line(ax, [(xa, ym + 0.25), (xa, yhi - 0.2)], arrow_end=True)
        ax.text(xa - 0.42, ym, st, ha="right", va="center", fontsize=10, color=COLORS[0])
    # output bus
    _line(ax, [(xa + 0.2, y0), (14.3, y0)], arrow_end=True)
    ax.text(14.3, y0 + 0.2, r"$y[n]$", ha="right", va="bottom", fontsize=10)
    _node(ax, xout, y0)
    _line(ax, [(xout, y0), (xout, y2)])
    for y, lab in [(y1, r"$-a_1$"), (y2, r"$-a_2$")]:
        _node(ax, xout, y)
        _line(ax, [(xout, y), (12.45, y)])
        _gain(ax, 12.2, y, lab, "left", s=0.28, label_side="above")
        _line(ax, [(11.95, y), (xa + 0.2, y)], arrow_end=True)
    ax.text(11.0, 0.05, "5 multiplies, 2 state variables\n($s_1$, $s_2$) per biquad",
            ha="center", va="center", fontsize=8.5, color="#444444")
    save(fig, "23", "fig-23-1-fir-and-biquad-structures")


# ----------------------------------------------------------------------------
def fig_23_2():
    """ECG lowpass tolerance scheme and the 187-tap Kaiser FIR."""
    fs = 1000.0
    h = ss.firwin(187, 50.0, window=("kaiser", 5.65), fs=fs)
    f, H = ss.freqz(h, worN=2 ** 15, fs=fs)
    G = 20 * np.log10(np.maximum(np.abs(H), 1e-12))

    fig, ax = new_fig(6.4, 3.9)
    red = "#F4C7C3"
    ax.add_patch(Rectangle((0, 0.1), 40, 5, fc=red, ec="none"))
    ax.add_patch(Rectangle((0, -120), 40, 119.9, fc=red, ec="none"))
    ax.add_patch(Rectangle((60, -60), 90, 70, fc=red, ec="none"))
    ax.plot(f, G, color=COLORS[0], lw=1.4, label="187-tap Kaiser FIR, β = 5.65, cutoff 50 Hz")
    ax.set_xlim(0, 150)
    ax.set_ylim(-100, 5)
    ax.set_xlabel("Frequency (Hz)   [$f_s$ = 1 kHz]")
    ax.set_ylabel("Gain (dB)")
    ax.axvline(40, color=INK, lw=0.6, ls=":")
    ax.axvline(60, color=INK, lw=0.6, ls=":")
    ax.annotate("", xy=(60, -94), xytext=(40, -94),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=8))
    ax.text(50, -92.5, "transition\n40–60 Hz", ha="center", va="bottom", fontsize=8.5)
    ax.text(20, -84, "forbidden:\ngain below −0.1 dB", ha="center", va="center", fontsize=8.5, color="#8B1A1A")
    ax.text(105, -45, "forbidden: gain above −60 dB", ha="center", va="center", fontsize=8.5, color="#8B1A1A")
    ax.text(20, 1.0, "forbidden above +0.1 dB", ha="center", va="bottom", fontsize=7.5, color="#8B1A1A")
    ax.legend(loc="upper right", fontsize=8.5, frameon=True, facecolor="white", edgecolor="white")
    stop_pk = G[f >= 60].max()
    ax.text(62, stop_pk + 1.5, f"stopband peak {stop_pk:.1f} dB", ha="left", va="bottom", fontsize=8)

    # inset: passband ripple
    ins = ax.inset_axes([0.08, 0.34, 0.19, 0.28])
    m = f <= 45
    ins.plot(f[m], G[m], color=COLORS[0], lw=1.1)
    ins.axhspan(0.1, 1, color=red)
    ins.axhspan(-1, -0.1, color=red)
    ins.set_xlim(0, 45)
    ins.set_ylim(-0.015, 0.015)
    ins.axvline(40, color=INK, lw=0.6, ls=":")
    ins.set_yticks([-0.01, 0, 0.01])
    ins.set_xticks([0, 20])
    ins.tick_params(labelsize=7)
    ins.set_title("passband (dB)", fontsize=7.5, pad=2)
    for s in ("top", "right"):
        ins.spines[s].set_visible(True)
    save(fig, "23", "fig-23-2-lowpass-specification")


# ----------------------------------------------------------------------------
def fig_23_3():
    """Bilinear-transform frequency warping at fs = 8 kHz."""
    fs = 8000.0
    fa = np.linspace(0, 10000, 1001)
    fd = fs / np.pi * np.arctan(np.pi * fa / fs)
    fig, ax = new_fig(6.4, 3.8)
    ax.plot(fa / 1e3, fd / 1e3, color=COLORS[0], label=r"$f=(f_s/\pi)\,\arctan(\pi f_a/f_s)$")
    ax.plot(fa / 1e3, fa / 1e3, color=INK, ls="--", lw=1.0, label="identity $f=f_a$ (no warping)")
    ax.axhline(4, color="#888888", lw=0.8, ls=":")
    ax.text(9.9, 4.03, "$f_s/2$ = 4 kHz", ha="right", va="bottom", fontsize=8.5, color="#555555")
    fpw = fs / np.pi * np.tan(np.pi * 1000 / fs)
    fnw = fs / np.pi * np.arctan(np.pi * 1000 / fs)
    ax.plot([fpw / 1e3], [1.0], "o", color=COLORS[1], ms=6, zorder=5)
    ax.plot([1.0], [fnw / 1e3], "s", color=COLORS[2], ms=6, zorder=5)
    ax.annotate(f"pre-warped: $f_a$ = {fpw:.1f} Hz → $f$ = 1000 Hz",
                xy=(fpw / 1e3, 1.0), xytext=(2.6, 1.35), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.8))
    ax.annotate(f"not pre-warped: $f_a$ = 1000 Hz → $f$ = {fnw:.1f} Hz",
                xy=(1.0, fnw / 1e3), xytext=(2.6, 0.55), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.set_xlabel(r"Analog frequency $f_a=\Omega/2\pi$ (kHz)")
    ax.set_ylabel("Digital frequency $f$ (kHz)")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.93), fontsize=8.5)
    save(fig, "23", "fig-23-3-bilinear-warping")


# ----------------------------------------------------------------------------
def _sos_group_delay(sos, f, fs):
    gd = np.zeros_like(f)
    for s in sos:
        _, g = ss.group_delay((s[:3], s[3:]), w=f, fs=fs)
        gd += g
    return gd


def fig_23_4():
    """Butterworth / Chebyshev I / Chebyshev II / elliptic designs for the same spec."""
    fs = 8000.0
    fp, fst, rp, rs = 1000.0, 1500.0, 1.0, 60.0
    designs = []
    n, wn = ss.buttord(fp, fst, rp, rs, fs=fs)
    designs.append((f"Butterworth, order {n}", ss.butter(n, wn, fs=fs, output="sos")))
    n, wn = ss.cheb1ord(fp, fst, rp, rs, fs=fs)
    designs.append((f"Chebyshev I, order {n}", ss.cheby1(n, rp, wn, fs=fs, output="sos")))
    n, wn = ss.cheb2ord(fp, fst, rp, rs, fs=fs)
    designs.append((f"Chebyshev II, order {n}", ss.cheby2(n, rs, wn, fs=fs, output="sos")))
    n, wn = ss.ellipord(fp, fst, rp, rs, fs=fs)
    designs.append((f"Elliptic, order {n}", ss.ellip(n, rp, rs, wn, fs=fs, output="sos")))

    f = np.linspace(0, 4000, 4001)
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 5.0), gridspec_kw=dict(height_ratios=[2.2, 1]))
    red = "#F4C7C3"
    red = "#FBE1DE"
    ax.add_patch(Rectangle((0, -1), 1000, -100, fc=red, ec="none"))
    ax.add_patch(Rectangle((0, 0), 1000, 5, fc=red, ec="none"))
    ax.add_patch(Rectangle((1500, -60), 2500, 70, fc=red, ec="none"))
    for (lab, sos), c in zip(designs, COLORS):
        _, H = ss.sosfreqz(sos, worN=f, fs=fs)
        ax.plot(f / 1e3, 20 * np.log10(np.maximum(abs(H), 1e-9)), color=c, lw=1.4, label=lab)
    ax.set_xlim(0, 4)
    ax.set_ylim(-90, 2)
    ax.set_ylabel("Gain (dB)")
    ax.set_xlabel("Frequency (kHz)   [$f_s$ = 8 kHz]")
    ax.legend(loc="upper right", fontsize=8.5, frameon=True, facecolor="white", edgecolor="white")
    ax.text(0.5, -45, "passband 0–1 kHz\nwithin −1 dB", ha="center", va="center", fontsize=8.5)
    ax.text(2.75, -66, "stopband ≥ 1.5 kHz: below −60 dB", ha="center", va="top", fontsize=8.5)

    # group delay
    fg = np.linspace(1, 1200, 1200)
    sos_e = designs[3][1]
    gd_e = _sos_group_delay(sos_e, fg, fs)
    taps = 36
    hfir = ss.remez(taps, [0, fp, fst, fs / 2], [1, 0], weight=[1, 57.5], fs=fs)
    _, gd_f = ss.group_delay((hfir, [1.0]), w=fg, fs=fs)
    ax2.plot(fg / 1e3, gd_e, color=COLORS[3], lw=1.4, label=designs[3][0])
    ax2.plot(fg / 1e3, gd_f, color=INK, lw=1.4, ls="--", label=f"Parks–McClellan FIR, {taps} taps")
    ax2.axvline(1.0, color="#888888", lw=0.6, ls=":")
    ax2.set_xlim(0, 1.2)
    ax2.set_ylim(0, 45)
    ax2.set_xlabel("Frequency (kHz)")
    ax2.set_ylabel("Group delay\n(samples)")
    gmin, gmax = gd_e[fg <= 1000].min(), gd_e[fg <= 1000].max()
    ax2.text(0.02, gmin + 2.0, f"{gmin:.1f}", fontsize=8, color=COLORS[3], va="bottom")
    ax2.text(0.985, gmax, f"{gmax:.0f} at 1 kHz", fontsize=8, color=COLORS[3], ha="right", va="center")
    ax2.legend(loc="upper left", fontsize=8.5)
    fig.tight_layout(h_pad=0.8)
    save(fig, "23", "fig-23-4-iir-prototype-comparison")


# ----------------------------------------------------------------------------
def fig_23_5():
    """Zoomed z-plane: 50 Hz notch roots with quantised coefficients."""
    fs = 1000.0
    w0, r = 0.1 * np.pi, 0.99
    b = np.array([1, -2 * np.cos(w0), 1])
    a = np.array([1, -2 * r * np.cos(w0), r * r])

    fig, ax = new_fig(6.4, 5.6)
    ax.set_aspect("equal")
    # 8-bit representable pole grid
    q8 = 2.0 ** -6
    pts = []
    for k in range(100, 128):
        for mm in range(55, 65):
            p = np.roots([1, -k * q8, mm * q8])
            for z in p:
                if z.imag > 0:
                    pts.append(z)
    pts = np.array(pts)
    ax.plot(pts.real, pts.imag, ".", color="#BBBBBB", ms=6, zorder=1)
    # unit circle arc and radius-0.99 arc
    th = np.linspace(0.25, 0.40, 400)
    ax.plot(np.cos(th), np.sin(th), color=INK, lw=1.0)
    ax.text(np.cos(0.322) + 0.0012, np.sin(0.322) + 0.0004, "|z| = 1", fontsize=8, rotation=-71,
            ha="left", va="center")
    # rays at 50 Hz
    ax.plot([0.93, 0.96 * 1.0], [0.93 * np.tan(w0), 0.96 * np.tan(w0)], color="#AAAAAA", lw=0.6, ls=":")
    ax.text(0.9305, 0.93 * np.tan(w0) + 0.0006, "50 Hz", fontsize=7.5, color="#777777")

    styles = {None: ("ideal (16-bit coincident)", "o", "none", INK, 10),
              12: ("12-bit", "^", COLORS[0], COLORS[0], 7),
              8: ("8-bit", "s", COLORS[1], COLORS[1], 7)}
    for B in (None, 12, 8):
        if B is None:
            bq, aq = b, a
        else:
            q = 2.0 ** -(B - 2)
            bq, aq = np.round(b / q) * q, np.round(a / q) * q
        z = [x for x in np.roots(bq) if x.imag > 0][0]
        p = [x for x in np.roots(aq) if x.imag > 0][0]
        lab, mk, fc, ec, ms = styles[B]
        ax.plot([z.real], [z.imag], marker=mk, mfc="none" if B is None else "white", mec=ec, ms=ms,
                mew=1.4, ls="none", zorder=5, label=lab)
        ax.plot([p.real], [p.imag], marker="x" if B is None else mk, color=ec, mfc=fc, mec=ec,
                ms=ms, mew=1.4, ls="none", zorder=5)
        fz = np.angle(z) * fs / (2 * np.pi)
        fpz = np.angle(p) * fs / (2 * np.pi)
        if B is None:
            ax.annotate(f"ideal zero 50.00 Hz\n(16-bit: {50.003:.3f} Hz)", xy=(z.real, z.imag),
                        xytext=(0.9535, 0.3175), fontsize=8,
                        arrowprops=dict(arrowstyle="-", lw=0.6))
            ax.annotate(f"ideal pole, r = 0.990\n50.00 Hz", xy=(p.real, p.imag),
                        xytext=(0.9305, 0.2952), fontsize=8,
                        arrowprops=dict(arrowstyle="-", lw=0.6))
        elif B == 12:
            ax.annotate(f"12-bit zero {fz:.2f} Hz", xy=(z.real, z.imag), xytext=(0.9555, 0.3115),
                        fontsize=8, color=ec, arrowprops=dict(arrowstyle="-", lw=0.6, color=ec))
            ax.annotate(f"12-bit pole {fpz:.2f} Hz,\nr = {abs(p):.4f}", xy=(p.real, p.imag),
                        xytext=(0.9305, 0.3170), fontsize=8, color=ec,
                        arrowprops=dict(arrowstyle="-", lw=0.6, color=ec))
        else:
            ax.annotate(f"8-bit zero {fz:.2f} Hz", xy=(z.real, z.imag), xytext=(0.9545, 0.2945),
                        fontsize=8, color=ec, arrowprops=dict(arrowstyle="-", lw=0.6, color=ec))
            ax.annotate(f"8-bit pole {fpz:.2f} Hz,\nr = {abs(p):.4f}", xy=(p.real, p.imag),
                        xytext=(0.9440, 0.2912), fontsize=8, color=ec,
                        arrowprops=dict(arrowstyle="-", lw=0.6, color=ec))
    ax.set_xlim(0.93, 0.96)
    ax.set_ylim(0.29, 0.33)
    ax.set_xlabel("Re $z$")
    ax.set_ylabel("Im $z$")
    from matplotlib.lines import Line2D
    kz = np.arange(118, 125)
    zc = kz * q8 / 2
    ax.plot(zc, np.sqrt(1 - zc ** 2), "D", color="#BBBBBB", ms=4, zorder=2)
    hd = [Line2D([], [], ls="none", marker=".", color="#BBBBBB", ms=6, label="representable 8-bit poles"),
          Line2D([], [], ls="none", marker="D", color="#BBBBBB", ms=4, label="representable 8-bit zeros"),
          Line2D([], [], ls="none", marker="o", mfc="none", mec=INK, ms=9, mew=1.4, label="ideal zero (16-bit coincident)"),
          Line2D([], [], ls="none", marker="x", color=INK, ms=9, mew=1.4, label="ideal pole (16-bit coincident)"),
          Line2D([], [], ls="none", marker="^", mfc="white", mec=COLORS[0], ms=7, mew=1.4, label="12-bit zero"),
          Line2D([], [], ls="none", marker="^", color=COLORS[0], ms=7, label="12-bit pole"),
          Line2D([], [], ls="none", marker="s", mfc="white", mec=COLORS[1], ms=7, mew=1.4, label="8-bit zero"),
          Line2D([], [], ls="none", marker="s", color=COLORS[1], ms=7, label="8-bit pole")]
    ax.legend(handles=hd, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8)
    save(fig, "23", "fig-23-5-notch-quantisation-poles")


if __name__ == "__main__":
    fig_23_1()
    fig_23_2()
    fig_23_3()
    fig_23_4()
    fig_23_5()
