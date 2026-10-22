"""Figures for Chapter 21 — DSP Fundamentals.

Run from the repository root:  python figures/scripts/ch21.py
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, FancyBboxPatch
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, box, save, COLORS, INK, GRID  # noqa: E402

CH = "21"
BLUE, RED, GREEN, PURPLE, ORANGE = COLORS[0], COLORS[1], COLORS[2], COLORS[3], COLORS[4]


def fig_21_1():
    """3-bit mid-tread quantizer: staircase and error."""
    D = 0.25
    x = np.linspace(-1.5, 1.5, 6001)
    q = np.clip(D * np.round(x / D), -1.0, 0.75)
    e = q - x
    lo, hi = -1.0 - D / 2, 0.75 + D / 2
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.35, 1]))
    for ax in (a1, a2):
        ax.axvspan(-1.5, lo, color=RED, alpha=0.10, lw=0)
        ax.axvspan(hi, 1.5, color=RED, alpha=0.10, lw=0)
        ax.axhline(0, color="0.5", lw=0.6)
        ax.axvline(0, color="0.5", lw=0.6)
    a1.plot(x, x, ls="--", color="0.5", lw=1.0, label="ideal $y = x$")
    a1.plot(x, q, color=BLUE, lw=1.8, label="quantizer output $Q(x)$")
    a1.set_ylim(-1.55, 1.55)
    a1.set_yticks(np.arange(-1, 0.76, 0.25))
    a1.set_yticklabels([f"{v:g}".replace("-", "−") for v in np.arange(-1, 0.76, 0.25)], fontsize=8)
    a1.set_ylabel("output level")
    a1.legend(loc="upper left", fontsize=8.5)
    a1.text(1.2, -0.6, "overload\n(clipping)", ha="center", fontsize=9, color=RED)
    a1.text(-1.32, 0.6, "overload\n(clipping)", ha="center", fontsize=9, color=RED)
    a1.text(0.06, 1.25, "8 levels, $\\Delta$ = 0.25\n(mid-tread: 0 is a level)", fontsize=8.5, va="center")
    a1.set_title("3-bit mid-tread quantizer, full scale $-1$ to $+1$", loc="left", fontsize=10)
    a2.plot(x, e, color=INK, lw=1.3)
    for yy in (D / 2, -D / 2):
        a2.axhline(yy, color=GREEN, ls=":", lw=1.0)
    a2.text(-0.95, 0.15, r"$+\Delta/2$ = 0.125", fontsize=8.5, color=GREEN, va="bottom")
    a2.text(-0.95, -0.15, r"$-\Delta/2$", fontsize=8.5, color=GREEN, va="top")
    a2.text(-0.1, 0.32, "granular noise", ha="center", fontsize=9, color=GREEN)
    a2.text(1.18, 0.42, "overload\nerror grows", ha="center", fontsize=8.5, color=RED)
    a2.text(-1.32, -0.42, "overload\nerror grows", ha="center", fontsize=8.5, color=RED)
    a2.set_ylim(-0.6, 0.6)
    a2.set_xlim(-1.5, 1.5)
    a2.set_ylabel("error $Q(x)-x$")
    a2.set_xlabel("input $x$ (full scale = $\\pm$1)")
    fig.tight_layout(h_pad=0.6)
    save(fig, CH, "fig-21-1-quantizer-staircase-error")


def _sqnr_sine(N, L):
    """SQNR (dB) of an N-bit quantizer (range +-1) for a sine at level L dBFS, including clipping."""
    D = 2.0 / 2 ** N
    A = 10 ** (L / 20)
    th = np.linspace(0, 2 * np.pi, 4001)[:-1]
    out = np.empty_like(A)
    for i, a in enumerate(A):
        s = a * np.sin(th)
        clip = np.clip(s, -1, 1) - s
        inside = np.mean(np.abs(s) < 1)
        out[i] = 10 * np.log10((a ** 2 / 2) / (D ** 2 / 12 * inside + np.mean(clip ** 2)))
    return out


def _sqnr_gauss(N, L):
    """SQNR (dB) for a Gaussian input of RMS level L dBFS (re full-scale sine RMS), including clipping."""
    D = 2.0 / 2 ** N
    s = 10 ** (L / 20) / np.sqrt(2)
    c = 1 / s
    pin = 2 * stats.norm.cdf(c) - 1
    ov = 2 * s ** 2 * ((1 + c ** 2) * stats.norm.sf(c) - c * stats.norm.pdf(c))
    return 10 * np.log10(s ** 2 / (D ** 2 / 12 * pin + ov))


def fig_21_2():
    """SQNR versus input level for 8, 12, 16 bits, sine and Gaussian inputs."""
    L = np.linspace(-100, 5, 1051)
    fig, ax = new_fig(6.4, 4.2)
    cols = {8: BLUE, 12: GREEN, 16: PURPLE}
    for N in (8, 12, 16):
        ys = _sqnr_sine(N, L)
        yg = _sqnr_gauss(N, L)
        ax.plot(L, ys, color=cols[N], lw=1.7, label=f"N = {N}, sine")
        ax.plot(L, yg, color=cols[N], lw=1.2, ls="--", label=f"N = {N}, Gaussian")
        pk = 6.02 * N + 1.76
        ax.plot(0, pk, "o", color=cols[N], ms=4.5)
        ax.text(-2, pk + 1.5, f"{pk:.1f} dB", ha="right", va="bottom", fontsize=8, color=cols[N])
        i = np.argmax(yg)
        ax.plot(L[i], yg[i], "v", color=cols[N], ms=5)
    ax.axvspan(0, 5, color=RED, alpha=0.10, lw=0)
    ax.text(2.5, 104, "overload", rotation=90, ha="center", va="top", fontsize=8.5, color=RED)
    ax.text(-60, 4, "granular region: slope 1 dB per dB", fontsize=8.5, ha="center", color="0.3")
    ax.annotate("", xy=(-40, 6.02 * 16 + 1.76 - 40), xytext=(-40, 6.02 * 12 + 1.76 - 40),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color="0.3", mutation_scale=8))
    ax.text(-39, 6.02 * 14 + 1.76 - 40, "24 dB = 4 bits\n(6 dB per bit)", fontsize=8, va="center", color="0.3")
    ax.text(-97, 103, "▼ Gaussian optimum (N = 8, 12, 16): 9.3, 11.3, 12.7 dB below\n   the full-scale-sine value, at −8.9, −11.0, −12.5 dBFS",
            fontsize=7.5, va="top", color="0.3")
    ax.set_xlim(-100, 5)
    ax.set_ylim(0, 105)
    ax.set_xlabel("input RMS level (dBFS, relative to a full-scale sine)")
    ax.set_ylabel("SQNR (dB)")
    ax.legend(loc="upper left", fontsize=7.5, ncol=2, bbox_to_anchor=(0.0, 0.88), columnspacing=1.0,
              handlelength=1.8)
    save(fig, CH, "fig-21-2-sqnr-versus-level")


def fig_21_3():
    """Generic DSP processing chain for a 48 kSa/s audio system, with latency budget."""
    fig, ax = schematic(6.8, 3.9, xlim=(0, 17.6), ylim=(-0.2, 9.6))
    blocks = [("Sensor", "micro-\nphone\n10 mV RMS"),
              ("Condition-\ning amp", "gain\n40 dB"),
              ("Anti-alias\nfilter", "3rd order\n50 kHz"),
              ("S/H +\nADC", "64× ΣΔ\n24-bit at\n48 kSa/s"),
              ("Processor", "64-tap FIR\n6.1 M\nMAC/s\n(stereo)"),
              ("DAC", "8× over-\nsampling\nZOH"),
              ("Recon-\nstruction\nfilter", "2nd order"),
              ("Power\namp", "drives\nloud-\nspeaker")]
    w, g, y0, h = 1.86, 0.32, 4.4, 3.6
    xs = [0.2 + i * (w + g) for i in range(len(blocks))]
    # digital domain
    xd0 = xs[3] + w * 0.55
    xd1 = xs[5] + w * 0.45
    ax.add_patch(Rectangle((xd0, y0 - 0.45), xd1 - xd0, h + 0.9, fill=False, ls="--", ec=BLUE, lw=1.2))
    ax.text((xd0 + xd1) / 2, y0 + h + 0.6, "digital domain", ha="center", va="bottom", fontsize=9, color=BLUE)
    ax.text(xs[1] + w / 2, y0 + h + 0.6, "analogue", ha="center", va="bottom", fontsize=9, color="0.4")
    ax.text(xs[7] - 0.2, y0 + h + 0.6, "analogue", ha="center", va="bottom", fontsize=9, color="0.4")
    for i, ((t, sub), x) in enumerate(zip(blocks, xs)):
        fc = "#E3EEF8" if 3 <= i <= 5 else "#F3F3F3"
        ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc=fc, ec=INK, lw=1.0))
        ax.text(x + w / 2, y0 + h - 0.15, t, ha="center", va="top", fontsize=7, weight="bold")
        ax.text(x + w / 2, y0 + 0.15, sub, ha="center", va="bottom", fontsize=7, color="0.2")
        if i < len(blocks) - 1:
            ax.annotate("", xy=(x + w + g, y0 + h / 2), xytext=(x + w, y0 + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=8,
                                        shrinkA=0, shrinkB=0))
    # latency timeline
    total = 0.4 + 2 * 10.7 + 0.4
    x0, x1 = 0.6, 16.6
    sc = (x1 - x0) / total
    yb, hb = 1.2, 0.8
    segs = [(0.4, "#C9A227", "ADC decimation\nfilter ≈ 0.4 ms"),
            (10.7, "#9CC3E4", "input block 512 samples = 10.7 ms"),
            (10.7, "#6FA8DC", "output block 512 samples = 10.7 ms"),
            (0.4, "#C9A227", "DAC interpolation\nfilter ≈ 0.4 ms")]
    xc = x0
    for i, (d, c, lab) in enumerate(segs):
        ax.add_patch(Rectangle((xc, yb), d * sc, hb, fc=c, ec=INK, lw=0.8))
        if d > 1:
            ax.text(xc + d * sc / 2, yb + hb / 2, lab, ha="center", va="center", fontsize=8)
        else:
            if i == 0:
                ax.annotate(lab, xy=(xc + d * sc / 2, yb), xytext=(xc + 0.1, yb - 1.25), fontsize=7.5,
                            ha="left", va="center",
                            arrowprops=dict(arrowstyle="-", lw=0.7, color="0.3"))
            else:
                ax.annotate(lab, xy=(xc + d * sc / 2, yb), xytext=(xc + d * sc - 0.1, yb - 1.25),
                            fontsize=7.5, ha="right", va="center",
                            arrowprops=dict(arrowstyle="-", lw=0.7, color="0.3"))
        xc += d * sc
    ax.text(x0, yb + hb + 0.25, "latency budget (block processing, double buffering)", fontsize=8.5,
            va="bottom")
    ax.text(x1, yb + hb + 0.25, f"total ≈ {total:.1f} ms", fontsize=8.5, va="bottom", ha="right",
            weight="bold")
    save(fig, CH, "fig-21-3-dsp-processing-chain")


def _cells(ax, x0, y0, n, cw, ch, fcs, texts=None, fs=8):
    for i in range(n):
        ax.add_patch(Rectangle((x0 + i * cw, y0), cw, ch, fc=fcs[i], ec=INK, lw=0.7))
        if texts is not None and texts[i] != "":
            ax.text(x0 + (i + 0.5) * cw, y0 + ch / 2, texts[i], ha="center", va="center", fontsize=fs)


def fig_21_4():
    """Bit layouts: Q15, 40-bit accumulator, IEEE 754 single."""
    fig, ax = schematic(6.8, 5.6, xlim=(0, 15.2), ylim=(0, 12.8))
    W = 13.6
    x0 = 0.8
    SIGN, INT, FRAC, EXP, GUARD = "#F4C7B8", "#E8E8E8", "#CFE2F3", "#D9EAD3", "#FFF2CC"
    # Q15
    y = 10.6
    ax.text(0.1, y + 1.45, "Q15 (16 bits)", fontsize=10, weight="bold", va="bottom")
    bits = "0101101010000010"
    cw = W / 16
    _cells(ax, x0, y, 16, cw, 0.8, [SIGN] + [FRAC] * 15, list(bits), fs=9)
    for i in range(16):
        ax.text(x0 + (i + 0.5) * cw, y + 0.95, str(15 - i), ha="center", va="bottom", fontsize=6.5, color="0.4")
        wl = "$-1$" if i == 0 else f"$2^{{-{i}}}$"
        ax.text(x0 + (i + 0.5) * cw, y - 0.12, wl, ha="center", va="top", fontsize=7)
    ax.plot([x0 + cw, x0 + cw], [y - 0.15, y + 0.95], color=RED, lw=2)
    ax.plot(x0 + cw, y - 0.05, "o", color=RED, ms=5)
    ax.text(x0 + cw + 0.1, y - 0.62, "binary point (after the sign bit); weights shown below each bit",
            color=RED, fontsize=7.5, va="top")
    ax.text(x0, y - 1.25,
            "example: 0.70709 → 0101 1010 1000 0010 = 23170 (0x5A82).   Range $-1$ to $1-2^{-15}$,  "
            "resolution $2^{-15}$ = 3.05×10$^{-5}$",
            fontsize=7.8, va="top")
    # accumulator
    y = 6.1
    ax.text(0.1, y + 1.45, "40-bit accumulator (Q8.31)", fontsize=10, weight="bold", va="bottom")
    cw = W / 40
    _cells(ax, x0, y, 40, cw, 0.8, [GUARD] * 8 + [SIGN] + [FRAC] * 31)
    for i, lab in ((0, "39"), (8, "31"), (39, "0")):
        ax.text(x0 + (i + 0.5) * cw, y + 0.95, lab, ha="center", va="bottom", fontsize=6.5, color="0.4")
    ax.plot([x0 + 9 * cw] * 2, [y - 0.15, y + 0.95], color=RED, lw=2)
    ax.plot(x0 + 9 * cw, y - 0.05, "o", color=RED, ms=5)
    for a, b, lab, xc in ((0, 8, "8 guard bits", 3.6), (8, 9, "sign", 8.9),
                          (9, 40, "31 fractional bits", 24.5)):
        ax.annotate("", xy=(x0 + a * cw, y - 0.3), xytext=(x0 + b * cw, y - 0.3),
                    arrowprops=dict(arrowstyle="|-|", lw=0.8, color="0.3", mutation_scale=3))
        ax.text(x0 + xc * cw, y - 0.42, lab, ha="center", va="top", fontsize=8)
    ax.text(x0 + 9 * cw + 0.1, y + 0.95, "binary point", color=RED, fontsize=7.5, va="bottom", ha="left")
    ax.text(x0, y - 1.05,
            "Range $\\pm$256 (up to 256 full-scale Q30 products summed without overflow),  "
            "resolution $2^{-31}$ = 4.66×10$^{-10}$",
            fontsize=7.8, va="top")
    # IEEE single
    y = 1.9
    ax.text(0.1, y + 1.45, "IEEE 754 single precision (32 bits)", fontsize=10, weight="bold", va="bottom")
    cw = W / 32
    bits = "0" + "01111111" + "0" * 23
    _cells(ax, x0, y, 32, cw, 0.8, [SIGN] + [EXP] * 8 + [FRAC] * 23, list(bits), fs=7.5)
    for i, lab in ((0, "31"), (1, "30"), (8, "23"), (9, "22"), (31, "0")):
        ax.text(x0 + (i + 0.5) * cw, y + 0.95, lab, ha="center", va="bottom", fontsize=6.5, color="0.4")
    for a, b, lab in ((0, 1, "s"), (1, 9, "exponent e\n(8 bits, bias 127)"),
                      (9, 32, "fraction f (23 bits), implicit leading 1")):
        ax.annotate("", xy=(x0 + a * cw, y - 0.3), xytext=(x0 + b * cw, y - 0.3),
                    arrowprops=dict(arrowstyle="|-|", lw=0.8, color="0.3", mutation_scale=3))
        ax.text(x0 + (a + b) / 2 * cw, y - 0.42, lab, ha="center", va="top", fontsize=8)
    ax.text(x0, y - 1.35,
            "value $(-1)^s$ × 1.f × $2^{e-127}$;  example 1.0 = 0 01111111 000…0.   "
            "Range 1.18×10$^{-38}$ to 3.40×10$^{38}$,  $\\varepsilon=2^{-23}$ = 1.19×10$^{-7}$",
            fontsize=7.8, va="top")
    save(fig, CH, "fig-21-4-number-formats")


def _adder(ax, x, y, r=0.3):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=4))
    ax.text(x, y, "+", ha="center", va="center", fontsize=12, zorder=5)


def _arr(ax, p0, p1):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1,
                                                      shrinkA=0, shrinkB=0, mutation_scale=10))


def _gain(ax, x, y, direction, label, s=0.6, off=(0, 0.45)):
    if direction == "right":
        pts = [(x - s / 2, y - s / 2), (x - s / 2, y + s / 2), (x + s / 2, y)]
    else:
        pts = [(x + s / 2, y - s / 2), (x + s / 2, y + s / 2), (x - s / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, fc="#EEF3F8", ec=INK, lw=1.1, zorder=4))
    ax.text(x + off[0], y + off[1], label, ha="center", va="bottom", fontsize=9)


def fig_21_5():
    """Linear noise model of a first-order recursive filter, with noise-gain inset."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.0, 0.47, 1.0, 0.53])
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")
    yt = 3.6
    ax.text(0.15, yt, "$x[n]$", va="center", fontsize=11)
    ax.plot([0.95, 1.95], [yt, yt], color=INK, lw=1.1)
    _gain(ax, 2.3, yt, "right", "$1-a$")
    _arr(ax, (2.6, yt), (4.2, yt))
    _adder(ax, 4.5, yt)
    _arr(ax, (4.8, yt), (6.9, yt))
    _adder(ax, 7.2, yt)
    ax.text(5.85, yt + 0.12, "exact sum", ha="center", va="bottom", fontsize=8, color="0.35")
    # error injection
    _arr(ax, (7.2, yt + 1.25), (7.2, yt + 0.3))
    ax.text(7.2, yt + 1.32, r"$e[n]$, variance $\Delta^2/12$", ha="center", va="bottom", fontsize=9, color=RED)
    ax.text(7.55, yt + 0.55, "rounding $Q$\nmodelled as\nadded noise", ha="left", va="center", fontsize=7.5,
            color=RED)
    _arr(ax, (7.5, yt), (10.6, yt))
    ax.plot(9.6, yt, "o", color=INK, ms=4.5, zorder=5)
    ax.text(10.7, yt, "$y[n]$", va="center", fontsize=11)
    # feedback path
    ax.plot([9.6, 9.6], [yt, 2.45], color=INK, lw=1.1)
    ax.add_patch(Rectangle((9.15, 1.55), 0.9, 0.9, fc="#EEF3F8", ec=INK, lw=1.1, zorder=4))
    ax.text(9.6, 2.0, "$z^{-1}$", ha="center", va="center", fontsize=11, zorder=5)
    ax.plot([9.6, 9.6, 7.3], [1.55, 0.9, 0.9], color=INK, lw=1.1)
    _gain(ax, 7.0, 0.9, "left", "$a$", off=(0, -0.85))
    ax.plot([6.7, 4.5], [0.9, 0.9], color=INK, lw=1.1)
    _arr(ax, (4.5, 0.9), (4.5, yt - 0.3))
    ax.text(4.35, 2.0, "$a\\,y[n-1]$", ha="right", va="center", fontsize=9)
    ax.text(9.75, 1.2, "$y[n-1]$", ha="left", va="center", fontsize=9)
    ax.text(10.4, 0.55, r"noise path: $g[n]=a^n u[n]$" + "\n" + r"noise gain $\sum g^2 = 1/(1-a^2)$",
            fontsize=8.5, va="center", color=RED)
    # inset plot
    a2 = fig.add_axes([0.14, 0.09, 0.62, 0.33])
    oma = np.logspace(np.log10(0.5), -3, 400)
    a = 1 - oma
    ng = 10 * np.log10(1 / (1 - a ** 2))
    a2.semilogx(oma, ng, color=BLUE, lw=1.6)
    a2.invert_xaxis()
    for av in (0.5, 0.9, 0.99, 0.999):
        v = 10 * np.log10(1 / (1 - av ** 2))
        a2.plot(1 - av, v, "o", color=RED if av > 0.5 else BLUE, ms=5)
        a2.annotate(f"a = {av}: {v:.1f} dB", xy=(1 - av, v), xytext=(6, -12 if av > 0.5 else 4),
                    textcoords="offset points", fontsize=8, ha="left")
    a2.set_xlabel("$1-a$ (log scale; poles approach $z$ = 1 to the right)")
    a2.set_ylabel("noise gain (dB)")
    a2.set_ylim(0, 30)
    a2.set_xlim(0.5, 0.0007)
    a2.grid(True, which="major", color=GRID, lw=0.6)
    save(fig, CH, "fig-21-5-roundoff-noise-model")


def fig_21_6():
    """Single-precision clock error versus double precision and an integer counter."""
    fs = 48000
    N = 600 * fs
    dt32 = np.float32(1 / fs)
    t32 = np.cumsum(np.full(N, dt32, np.float32), dtype=np.float32)
    real = np.arange(1, N + 1) / fs
    step = 480
    err32 = t32[::step].astype(np.float64) - real[::step]
    # double precision (sequential accumulation) and integer counter
    t64 = np.cumsum(np.full(N, 1 / fs))
    err64 = t64[::step] - real[::step]
    rr = real[::step]
    fig, ax = new_fig(6.4, 4.0)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.plot(rr, err32, color=RED, lw=1.8, label="float32 clock  t = t + 1/48000")
    ax.plot(rr, err64, color=BLUE, lw=1.4, label="float64 clock (−16 µs after 1 h)")
    ax.plot(rr, np.zeros_like(rr), color=GREEN, lw=1.2, ls="--", label="integer counter, t = n/fs (exact)")
    tf = np.argmax(t32 >= 512) / fs
    ax.plot(tf, 512 - tf, "o", color=RED, ms=5)
    ax.annotate(f"logged time reaches 512 s at {tf:.1f} s:\nclock frozen, error slope −1",
                xy=(tf, 512 - tf), xytext=(150, 40), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
    i256 = 256 * fs - 1
    ax.plot(256, t32[i256] - 256, "o", color=RED, ms=4)
    ax.annotate(f"−{256 - t32[i256]:.1f} s at 256 s", xy=(256, t32[i256] - 256), xytext=(150, -55),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
    for p in (32, 64, 128, 256):
        ib = np.argmax(t32 >= p)
        xb = (ib + 1) / fs
        yb = float(t32[ib]) - xb
        ax.plot(xb, yb, "s", color=INK, ms=3.5, zorder=5)
        ax.text(xb, yb - 4 if p != 64 else yb - 4, f"{p} s", ha="center", va="top", fontsize=7.5, color="0.3")
    ax.text(330, -58, "squares: logged time crosses\na power of two (float32 spacing\ndoubles, increment rounding changes)",
            fontsize=7.5, color="0.3", va="top")
    ax.text(5, 6, "small positive error\nbelow ≈ 30 s", fontsize=8, va="bottom", color="0.3")
    ax.set_xlim(0, 600)
    ax.set_ylim(-100, 50)
    ax.set_xlabel("real elapsed time (s)")
    ax.set_ylabel("logged time − real time (s)")
    ax.legend(loc="lower left", fontsize=8, bbox_to_anchor=(0.0, 0.08))
    save(fig, CH, "fig-21-6-float32-clock-error")


if __name__ == "__main__":
    fig_21_1()
    fig_21_2()
    fig_21_3()
    fig_21_4()
    fig_21_5()
    fig_21_6()
