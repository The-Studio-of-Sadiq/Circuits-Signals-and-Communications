"""Figures for Chapter 25 — Communication System Fundamentals.

Run from the repository root:  python figures/scripts/ch25.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special
from matplotlib.patches import Circle, Polygon, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import COLORS, INK, GRID, box, new_fig, save, schematic  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402


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


def _circ(ax, x, y, sym, r=0.26, fs=10):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(x, y - 0.02, sym, ha="center", va="center", fontsize=fs, zorder=4)


def _dot(ax, x, y, r=0.05):
    ax.add_patch(Circle((x, y), r, fc=INK, ec=INK, zorder=4))


def _amp(ax, x0, x1, y, h=0.45, right=True, fc="#FCEBD9"):
    pts = [(x0, y - h), (x0, y + h), (x1, y)] if right else [(x1, y - h), (x1, y + h), (x0, y)]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=1.0, zorder=3))


def _antenna(ax, x, y, s=0.35):
    """Antenna symbol whose feed point is (x, y)."""
    _ln(ax, [(x, y), (x, y + 2 * s)])
    _ln(ax, [(x - s, y + 2.6 * s), (x, y + 2 * s), (x + s, y + 2.6 * s)])
    _ln(ax, [(x, y + 2 * s), (x, y + 2.7 * s)])


def _bracket(ax, x0, x1, y, text, h=0.2):
    ax.plot([x0, x0, x1, x1], [y + h, y, y, y + h], color="#555555", lw=1.0, ls="--")
    ax.text((x0 + x1) / 2, y - 0.12, text, ha="center", va="top", fontsize=8, color="#555555",
            style="italic")


# ----------------------------------------------------------------------------
def fig_25_1():
    """Generic communication-system model."""
    fig, ax = schematic(6.8, 2.2, xlim=(0, 27.2), ylim=(-0.6, 8.2))
    ax.set_position([0, 0, 1, 1])
    fs = 7.5
    yb, hb = 2.0, 3.0
    yc = yb + hb / 2
    box(ax, 0.2, yb, 3.2, hb, "Information\nsource", fontsize=fs)
    box(ax, 4.8, yb, 4.0, hb, "Transmitter\n(source coder,\nchannel coder,\nmodulator, PA)", fontsize=fs)
    box(ax, 10.2, yb, 4.6, hb, "", fc="#F2F2F2")
    box(ax, 19.0, yb, 3.4, hb, "Receiver\n(LNA,\ndemodulator,\ndetector,\ndecoder)", fontsize=fs)
    box(ax, 23.8, yb, 3.2, hb, "Destination", fontsize=fs)
    ax.text(11.75, yc, "Channel\n" r"$h(t)$:" "\nattenuation,\ndistortion,\ndelay",
            ha="center", va="center", fontsize=fs)
    xs = 13.9
    _circ(ax, xs, yc, "+", r=0.38, fs=11)
    _ln(ax, [(13.3, yc), (xs - 0.38, yc)], arrow=True)
    _ln(ax, [(12.9, 6.9), (xs - 0.27, yc + 0.28)], arrow=True)
    _ln(ax, [(14.9, 6.9), (xs + 0.27, yc + 0.28)], arrow=True)
    ax.text(12.8, 7.0, r"noise $n(t)$", ha="right", va="bottom", fontsize=8)
    ax.text(15.0, 7.0, r"interference $i(t)$", ha="left", va="bottom", fontsize=8)
    _ln(ax, [(3.4, yc), (4.8, yc)], arrow=True)
    ax.text(4.1, yc + 0.15, r"$m(t)$", ha="center", va="bottom", fontsize=8.5)
    _ln(ax, [(8.8, yc), (10.2, yc)], arrow=True)
    ax.text(9.5, yc + 0.15, r"$s(t)$", ha="center", va="bottom", fontsize=8.5)
    _ln(ax, [(xs + 0.38, yc), (19.0, yc)], arrow=True)
    ax.text(16.65, yc + 0.15, r"$r(t)=h(t)\ast s(t)$" "\n" r"$+\,n(t)+i(t)$", ha="center", va="bottom",
            fontsize=8)
    _ln(ax, [(22.4, yc), (23.8, yc)], arrow=True)
    ax.text(23.1, yc + 0.15, r"$\hat m(t)$", ha="center", va="bottom", fontsize=8.5)
    _bracket(ax, 4.8, 8.8, 1.5, "designed by\nthe engineer")
    _bracket(ax, 19.0, 22.4, 1.5, "designed by\nthe engineer")
    _bracket(ax, 10.2, 14.8, 1.5, "given by physics\nand regulation")
    save(fig, "25", "fig-25-1-communication-system-model")


# ----------------------------------------------------------------------------
def fig_25_2():
    """Digital transmitter and receiver with I/Q stages."""
    fig, ax = schematic(6.8, 4.6, xlim=(0, 17.2), ylim=(0.0, 11.6))
    ax.set_position([0, 0, 1, 1])
    fs = 7

    def blk(x, y, w, t, h=1.0, fc="#EEF3F8"):
        box(ax, x, y - h / 2, w, h, t, fontsize=fs, fc=fc)

    # ---------------- transmitter ----------------
    ax.text(0.1, 11.3, "Transmitter", fontsize=9.5, weight="bold", va="center")
    yI, yQ = 10.0, 6.8
    ym = (yI + yQ) / 2
    blk(0.1, ym, 1.4, "Source\ncoder")
    _ln(ax, [(1.5, ym), (1.8, ym)], arrow=True)
    blk(1.8, ym, 1.4, "Channel\ncoder")
    _ln(ax, [(3.2, ym), (3.5, ym)], arrow=True)
    blk(3.5, ym, 1.4, "Symbol\nmapper")
    _ln(ax, [(4.9, ym), (5.2, ym)])
    _dot(ax, 5.2, ym)
    for y, lab in [(yI, "I"), (yQ, "Q")]:
        _ln(ax, [(5.2, ym), (5.2, y), (5.55, y)], arrow=True)
        blk(5.55, y, 1.8, "Pulse-\nshaping filter", h=1.1)
        _ln(ax, [(7.35, y), (8.04, y)], arrow=True)
        ax.text(7.7, y + 0.1, lab, fontsize=8, va="bottom", ha="center", color=COLORS[0])
        _circ(ax, 8.3, y, r"$\times$")
    blk(7.5, ym, 1.6, "Carrier\noscillator", h=0.8, fc="#F5F0E1")
    _ln(ax, [(8.3, ym + 0.4), (8.3, yI - 0.26)], arrow=True)
    _ln(ax, [(8.3, ym - 0.4), (8.3, yQ + 0.26)], arrow=True)
    ax.text(8.42, yI - 0.75, r"$\cos 2\pi f_c t$", fontsize=7.5, va="center")
    ax.text(8.42, yQ + 0.75, r"$-\sin 2\pi f_c t$", fontsize=7.5, va="center")
    _ln(ax, [(8.56, yI), (10.4, yI), (10.4, ym + 0.26)], arrow=True)
    _ln(ax, [(8.56, yQ), (10.4, yQ), (10.4, ym - 0.26)], arrow=True)
    _circ(ax, 10.4, ym, "+")
    _ln(ax, [(10.66, ym), (11.0, ym)], arrow=True)
    blk(11.0, ym, 1.6, "Band-pass\nfilter")
    _ln(ax, [(12.6, ym), (12.9, ym)], arrow=True)
    _amp(ax, 12.9, 13.9, ym)
    ax.text(13.25, ym - 0.6, "PA", fontsize=7.5, ha="center", va="top")
    _ln(ax, [(13.9, ym), (15.0, ym)])
    _antenna(ax, 15.0, ym)
    ax.text(14.45, ym - 0.15, "+23 dBm", fontsize=7.5, ha="center", va="top", color=COLORS[1])

    _ln(ax, [(15.5, ym + 0.5), (15.5, 4.1)], arrow=True, ls="--", color="#777777")
    ax.text(15.65, 6.2, "radio\nchannel", fontsize=7.5, color="#555555", va="center")

    # ---------------- receiver ----------------
    ax.text(0.1, 5.75, "Receiver", fontsize=9.5, weight="bold", va="center")
    yI, yQ = 4.6, 1.3
    ym = (yI + yQ) / 2
    _antenna(ax, 15.0, ym)
    ax.text(14.6, ym + 1.05, "−90 dBm", fontsize=7.5, ha="right", va="center", color=COLORS[1])
    _ln(ax, [(15.0, ym), (14.7, ym)], arrow=True)
    blk(13.1, ym, 1.6, "Preselector\nBPF")
    _ln(ax, [(13.1, ym), (12.8, ym)], arrow=True)
    _amp(ax, 11.9, 12.8, ym, right=False)
    ax.text(12.35, ym - 0.6, "LNA\n$G$ = 15 dB", fontsize=7.5, ha="center", va="top")
    _ln(ax, [(11.9, ym), (11.5, ym)])
    _dot(ax, 11.5, ym)
    for y, lab in [(yI, "I"), (yQ, "Q")]:
        _ln(ax, [(11.5, ym), (11.5, y), (10.06, y)], arrow=True)
        _circ(ax, 9.8, y, r"$\times$")
        ax.text(10.8, y + 0.1, lab, fontsize=8, va="bottom", ha="center", color=COLORS[0])
    blk(8.5, ym, 2.6, "Local oscillator /\ncarrier recovery", h=0.9, fc="#F5F0E1")
    _ln(ax, [(9.8, ym + 0.45), (9.8, yI - 0.26)], arrow=True)
    _ln(ax, [(9.8, ym - 0.45), (9.8, yQ + 0.26)], arrow=True)
    ax.text(9.9, yI - 0.75, r"$\cos$", fontsize=7.5, va="center")
    ax.text(9.9, yQ + 0.75, r"$-\sin$", fontsize=7.5, va="center")
    for y in (yI, yQ):
        _ln(ax, [(9.54, y), (8.8, y)], arrow=True)
        blk(7.3, y, 1.5, "Matched\nfilter")
        _ln(ax, [(7.3, y), (7.0, y)], arrow=True)
    box(ax, 5.5, yQ - 0.5, 1.5, yI - yQ + 1.0, "Sampler\n(timing\nrecovery)", fontsize=fs)
    _ln(ax, [(5.5, ym), (5.2, ym)], arrow=True)
    blk(3.8, ym, 1.4, "Detector")
    _ln(ax, [(3.8, ym), (3.45, ym)], arrow=True)
    blk(1.95, ym, 1.5, "Channel\ndecoder")
    _ln(ax, [(1.95, ym), (1.6, ym)], arrow=True)
    blk(0.1, ym, 1.5, "Source\ndecoder")
    save(fig, "25", "fig-25-2-transmitter-receiver-architecture")


# ----------------------------------------------------------------------------
def fig_25_3():
    """Channel impairments on a 1 Mb/s NRZ pattern."""
    bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])
    dt = 0.002  # microseconds
    t = np.arange(0, 10, dt)
    s = np.where(bits[np.minimum((t // 1).astype(int), 9)] == 1, 1.0, -1.0)
    rng = np.random.default_rng(253)

    fig, axs = plt.subplots(4, 1, figsize=(6.4, 6.0), sharex=True)
    # (a) attenuation
    ax = axs[0]
    ax.plot(t, s, color="#AAAAAA", lw=1.0, label="transmitted")
    ax.plot(t, 0.3 * s, color=INK, lw=1.5, label="received, ×0.3")
    ax.set_title("(a) attenuation", loc="left", fontsize=9.5)
    # (b) noise, 0.1 V rms sampled every 20 ns (50 MHz noise bandwidth)
    ax = axs[1]
    tn = np.arange(0, 10, 0.02)
    sn = np.interp(tn, t, 0.3 * s) + 0.1 * rng.standard_normal(tn.size)
    ax.plot(tn, sn, color=INK, lw=0.9, label="0.3 V signal + 0.1 V rms noise")
    ax.plot(t, 0.3 * s, color=COLORS[0], lw=1.0, ls="--", label="noise-free")
    ax.set_title("(b) additive Gaussian noise", loc="left", fontsize=9.5)
    # (c) first-order low-pass, 300 kHz
    ax = axs[2]
    fc = 0.3  # MHz
    a = np.exp(-2 * np.pi * fc * dt)
    y = np.empty_like(s)
    acc = -1.0
    for k, v in enumerate(s):
        acc = a * acc + (1 - a) * v
        y[k] = acc
    ax.plot(t, s, color="#AAAAAA", lw=1.0, label="transmitted")
    ax.plot(t, y, color=INK, lw=1.5, label="first-order low-pass, $f_{3dB}$ = 300 kHz")
    ax.set_title("(c) band-limiting: intersymbol interference", loc="left", fontsize=9.5)
    # (d) echo
    ax = axs[3]
    td = 0.4
    s_d = np.interp(t - td, t, s, left=-1.0)
    ax.plot(t, s, color="#AAAAAA", lw=1.0, label="direct path")
    ax.plot(t, s + 0.5 * s_d, color=INK, lw=1.5, label="direct + 0.5 × echo delayed 0.4 µs")
    ax.set_title("(d) two-path echo", loc="left", fontsize=9.5)

    lims = [(-1.3, 1.9), (-0.75, 1.05), (-1.3, 1.9), (-1.8, 2.7)]
    for ax, lim in zip(axs, lims):
        ax.set_ylim(*lim)
        ax.set_ylabel("V")
        ax.axhline(0, color=GRID, lw=0.6, zorder=0)
        for k in range(1, 10):
            ax.axvline(k, color=GRID, lw=0.5, zorder=0)
        ax.legend(loc="upper right", fontsize=7, ncol=2, borderaxespad=0.1, handlelength=1.5,
                  frameon=True, facecolor="white", edgecolor="white", framealpha=0.9)
    for k, b in enumerate(bits):
        axs[0].text(k + 0.5, 1.02, str(b), ha="center", va="bottom", fontsize=8, color="#555555",
                    transform=axs[0].get_xaxis_transform())
    axs[0].set_title("(a) attenuation", loc="left", fontsize=9.5, pad=12)
    axs[-1].set_xlim(0, 10)
    axs[-1].set_xlabel("Time (µs)")
    fig.tight_layout(h_pad=0.4)
    save(fig, "25", "fig-25-3-channel-impairments")


# ----------------------------------------------------------------------------
def _sky_noise_dB(f_ghz):
    """Typical sky noise (galactic + CMB + atmosphere at 30 deg elevation), dB above kT0."""
    fz = np.array([0.5, 1, 2, 5, 10, 15, 18, 20, 22.2, 24, 27, 30, 35, 40, 45, 50, 53, 55, 57, 60,
                   63, 65, 67, 70, 75, 80, 90, 100])
    Az = np.array([0.035, 0.035, 0.037, 0.042, 0.055, 0.09, 0.16, 0.25, 0.40, 0.32, 0.22, 0.20,
                   0.22, 0.28, 0.45, 1.2, 4.0, 12, 60, 150, 60, 12, 3.0, 1.0, 0.55, 0.42, 0.40, 0.50])
    # slant-path attenuation (dB) at 30 deg elevation = 2 x zenith value
    A = 2.0 * 10 ** np.interp(np.log10(f_ghz), np.log10(fz), np.log10(Az))
    L = 10 ** (-A / 10)
    Tgal = 290 * 10 ** ((52 - 23 * np.log10(f_ghz * 1e3)) / 10)
    T = (Tgal + 2.7) * L + 270 * (1 - L)
    return 10 * np.log10(T / 290)


def fig_25_4():
    """External noise relative to kT0B versus frequency."""
    fig, ax = new_fig(6.6, 4.3)
    f_atm = np.logspace(np.log10(0.1), np.log10(40), 300)
    pts_f = np.log10([0.1, 0.3, 1, 3, 10, 20, 30, 40])
    pts_v = [83, 79, 70, 55, 32, 18, 10, 4]
    atm = np.interp(np.log10(f_atm), pts_f, pts_v)
    f_mm = np.logspace(np.log10(0.3), np.log10(250), 300)
    mm = 76.8 - 27.7 * np.log10(f_mm)
    f_gal = np.logspace(1, 3.3, 300)
    gal = 52 - 23 * np.log10(f_gal)
    f_sky = np.logspace(np.log10(0.6), 2, 600)  # GHz
    sky = _sky_noise_dB(f_sky)

    ax.axvspan(1e3, 1e4, color=COLORS[5], alpha=0.12, lw=0)
    ax.text(3.2e3, 30, "quiet\nwindow", ha="center", va="center", fontsize=8.5, color="#2C6E91")
    ax.plot(f_atm, atm, color=COLORS[0], label="atmospheric (lightning), typical")
    ax.plot(f_mm, mm, color=COLORS[1], label="man-made, business area (P.372)")
    ax.plot(f_gal, gal, color=COLORS[2], label="galactic (P.372)")
    ax.plot(f_sky * 1e3, sky, color=COLORS[3],
            label="quiet sky + O$_2$/H$_2$O (30° elevation)")
    ax.annotate("H$_2$O\n22 GHz", xy=(22.2e3, _sky_noise_dB(np.array([22.2]))[0]),
                xytext=(9e3, 2), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[3]))
    ax.annotate("O$_2$\n60 GHz", xy=(60e3, -0.4), xytext=(30e3, 12), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[3]))
    # receiver noise for comparison: Te/T0 = F - 1
    for nf, lab, c in [(1.0, "satellite LNA, NF 1 dB ($T_e$ = 75 K)", "#555555"),
                       (7.0, "low-cost receiver, NF 7 dB ($T_e$ = 1160 K)", "#555555")]:
        y = 10 * np.log10(10 ** (nf / 10) - 1)
        ax.axhline(y, color=c, ls="--", lw=1.0)
        ax.text(0.12, y + 0.8 if nf > 5 else y - 0.8, lab, fontsize=7.5, color=c, va="bottom" if nf > 5 else "top")
    ax.axhline(0, color=INK, lw=0.6)
    ax.text(0.12, 0.8, "0 dB = 290 K", fontsize=7.5, va="bottom", color="#444444")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 1e5)
    ax.set_ylim(-20, 90)
    ticks = [0.1, 1, 10, 100, 1e3, 1e4, 1e5]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["100 kHz", "1 MHz", "10 MHz", "100 MHz", "1 GHz", "10 GHz", "100 GHz"])
    ax.set_xlabel("Frequency")
    ax.set_ylabel(r"Noise above $kT_0$, $F_a$ (dB)")
    ax.legend(loc="upper right", fontsize=7.5)
    ax.grid(True, which="major", color=GRID, lw=0.5)
    save(fig, "25", "fig-25-4-noise-sources-vs-frequency")


# ----------------------------------------------------------------------------
def _contain(frac):
    g = lambda B: 2 * integrate.quad(lambda x: np.sinc(x) ** 2, 0, B / 2, limit=2000)[0] - frac
    return optimize.brentq(g, 0.1, 60)


def fig_25_5():
    """Bandwidth definitions on the rectangular-pulse BPSK PSD (Rb = 1 Mb/s)."""
    f = np.linspace(-5, 5, 20001)
    S = np.sinc(f) ** 2
    SdB = 10 * np.log10(np.maximum(S, 1e-12))
    b3 = 2 * optimize.brentq(lambda x: np.sinc(x) ** 2 - 0.5, 0.1, 0.9)
    b90, b99 = _contain(0.90), _contain(0.99)

    fig, ax = new_fig(6.6, 4.2)
    ax.plot(f, SdB, color=COLORS[0], lw=1.5)
    ax.fill_between(f, SdB, -60, color=COLORS[0], alpha=0.08, lw=0)
    # mask
    ax.plot([-5, -3, -3], [-40, -40, 0], color=COLORS[1], ls="--", lw=1.2)
    ax.plot([5, 3, 3], [-40, -40, 0], color=COLORS[1], ls="--", lw=1.2)
    ax.text(4.0, -41, "mask −40 dB\nbeyond ±3 MHz", fontsize=7.5, color=COLORS[1], ha="center", va="top")
    ax.text(-4.0, -41, "sinc$^2$ sidelobes\nexceed the mask", fontsize=7.5, color=COLORS[1],
            ha="center", va="top")

    def harrow(y, half, label, color=INK, off=False):
        if off:
            ax.annotate("", xy=(5, y), xytext=(-5, y),
                        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=1.0, mutation_scale=8))
        else:
            ax.annotate("", xy=(half, y), xytext=(-half, y),
                        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=1.0, mutation_scale=8,
                                        shrinkA=0, shrinkB=0))
        ax.text(max(half, 0.6) + 0.15 if not off else 0, y + (0.2 if off else 0), label, fontsize=8,
                va="center" if not off else "bottom", ha="left" if not off else "center", color=color,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.8))

    harrow(-3.0, b3 / 2, f"3 dB: {b3:.3f} MHz")
    harrow(-8, 0.5, "noise-equivalent: 1 MHz", color=COLORS[2])
    harrow(-13, b90 / 2, f"90 % containment: {b90:.2f} MHz", color=COLORS[3])
    harrow(-30, 1.0, "null-to-null: 2 MHz")
    ax.plot([-1, -1], [-30, -50], color="#999999", lw=0.6, ls=":")
    ax.plot([1, 1], [-30, -50], color="#999999", lw=0.6, ls=":")
    harrow(-49.0, 5, f"← 99 % containment: {b99:.1f} MHz (extends off the plot) →", color=COLORS[4], off=True)
    # noise-equivalent rectangle
    ax.plot([-0.5, -0.5, 0.5, 0.5], [-60, 0, 0, -60], color=COLORS[2], lw=0.9, ls=":")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-50, 2)
    ax.set_xlabel(r"$f-f_c$ (MHz)")
    ax.set_ylabel("Normalised PSD (dB)")
    ax.set_title(r"BPSK, rectangular pulses, $T_b$ = 1 µs: $S(f)=\mathrm{sinc}^2((f-f_c)T_b)$",
                 fontsize=9.5)
    save(fig, "25", "fig-25-5-bandwidth-definitions")


# ----------------------------------------------------------------------------
def _Q(x):
    return 0.5 * special.erfc(x / np.sqrt(2))


def _ebn0_for(pb_fun, target=1e-6):
    return 10 * np.log10(optimize.brentq(lambda g: pb_fun(g) - target, 1e-2, 1e4))


def _pb_mpsk(M):
    k = np.log2(M)
    if M <= 4:
        return lambda g: _Q(np.sqrt(2 * g))
    return lambda g: (2 / k) * _Q(np.sqrt(2 * k * g) * np.sin(np.pi / M))


def _pb_mqam(M):
    k = np.log2(M)
    return lambda g: (4 / k) * (1 - 1 / np.sqrt(M)) * _Q(np.sqrt(3 * k * g / (M - 1)))


def _pb_fsk(M):
    k = np.log2(M)

    def pb(g):
        a = np.sqrt(2 * k * g)
        y = np.linspace(a - 10, a + 10, 4001)
        pc = np.trapezoid(np.exp(-(y - a) ** 2 / 2) / np.sqrt(2 * np.pi) *
                          (1 - _Q(y)) ** (M - 1), y)
        return (M / 2 / (M - 1)) * (1 - pc)
    return pb


def fig_25_6():
    """Shannon bound on spectral efficiency vs Eb/N0 with uncoded schemes at BER 1e-6."""
    eta = np.logspace(-1.3, 1.0, 400)
    eb = 10 * np.log10((2 ** eta - 1) / eta)
    fig, ax = new_fig(6.6, 4.4)
    lim = 10 * np.log10(np.log(2))
    ax.fill_betweenx(eta, -2, eb, color="#DDDDDD", alpha=0.7, lw=0)
    ax.plot(eb, eta, color=INK, lw=1.8, label=r"Shannon bound $E_b/N_0=(2^\eta-1)/\eta$")
    ax.axvline(lim, color=INK, ls="--", lw=1.0)
    ax.text(lim + 0.25, 0.115, f"Shannon limit\nln 2 = {lim:.2f} dB", fontsize=8, va="bottom")
    ax.text(-1.6, 3.0, "unattainable", fontsize=9, rotation=90, va="center", color="#555555")

    pts = [("BPSK", 2, "psk"), ("QPSK", 4, "psk"), ("8-PSK", 8, "psk"), ("16-QAM", 16, "qam"),
           ("64-QAM", 64, "qam"), ("256-QAM", 256, "qam")]
    for lab, M, kind in pts:
        x = _ebn0_for(_pb_mpsk(M) if kind == "psk" else _pb_mqam(M))
        y = np.log2(M)
        ax.plot(x, y, "o" if kind == "psk" else "s", color=COLORS[0] if kind == "psk" else COLORS[1],
                ms=6, zorder=5)
        ax.text(x + 0.5, y, f"{lab} ({x:.1f} dB)", fontsize=8, va="center")
    fx, fy = [], []
    for M in (8, 16, 32, 64, 128):
        x = _ebn0_for(_pb_fsk(M))
        fx.append(x)
        fy.append(2 * np.log2(M) / M)
    ax.plot(fx, fy, "^-", color=COLORS[2], ms=6, lw=0.8, zorder=5)
    for x, y, M in zip(fx, fy, (8, 16, 32, 64, 128)):
        ax.text(x + 0.4, y, f"{M}-FSK", fontsize=7.5, va="center", color=COLORS[2])
    ax.axhline(1, color="#999999", lw=0.6, ls=":")
    ax.text(29.5, 1.12, "bandwidth-limited region", ha="right", va="bottom", fontsize=8.5,
            style="italic")
    ax.text(29.5, 0.9, "power-limited region", ha="right", va="top", fontsize=8.5, style="italic")
    ax.set_yscale("log")
    ax.set_xlim(-2, 30)
    ax.set_ylim(0.1, 10)
    ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])
    ax.set_xlabel(r"$E_b/N_0$ (dB)")
    ax.set_ylabel(r"Spectral efficiency $\eta=R/B$ (b/s/Hz)")
    from matplotlib.lines import Line2D
    hd = [Line2D([], [], color=INK, lw=1.8, label="Shannon bound"),
          Line2D([], [], ls="none", marker="o", color=COLORS[0], label=r"M-PSK, $\eta=\log_2 M$"),
          Line2D([], [], ls="none", marker="s", color=COLORS[1], label=r"M-QAM, $\eta=\log_2 M$"),
          Line2D([], [], ls="-", lw=0.8, marker="^", color=COLORS[2],
                 label=r"coherent orthogonal M-FSK, $\eta=2\log_2 M/M$")]
    ax.legend(handles=hd, loc="lower right", fontsize=7.5, title="uncoded, BER = $10^{-6}$",
              title_fontsize=7.5)
    ax.grid(True, which="major", color=GRID, lw=0.5)
    save(fig, "25", "fig-25-6-shannon-bound")


if __name__ == "__main__":
    fig_25_1()
    fig_25_2()
    fig_25_3()
    fig_25_4()
    fig_25_5()
    fig_25_6()
