"""Figures for Chapter 26 — Analog Communication. Run from the repository root: python figures/scripts/ch26.py"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from scipy.special import jv
import schemdraw
import schemdraw.elements as elm

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

schemdraw.use("matplotlib")
CH = "26"


# ----------------------------------------------------------------------------- Figure 26.1
def fig_26_1():
    """Conventional AM waveforms for mu = 0.5, 1.0, 1.5 with dashed envelopes."""
    Ac, fc, fm = 10.0, 20e3, 1e3
    t = np.linspace(0, 2e-3, 8001)
    tm = t * 1e3
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 5.6), sharex=True)
    for ax, mu, tag in zip(axes, [0.5, 1.0, 1.5], "abc"):
        a = Ac * (1 + mu * np.cos(2 * np.pi * fm * t))
        s = a * np.cos(2 * np.pi * fc * t)
        ax.plot(tm, s, color=COLORS[0], lw=0.8)
        env = np.abs(a)
        ax.plot(tm, env, "--", color=COLORS[1], lw=1.4)
        ax.plot(tm, -env, "--", color=COLORS[1], lw=1.4)
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_ylim(-25, 25)
        ax.set_yticks([-20, -10, 0, 10, 20])
        ax.set_ylabel("s(t) (V)")
        title = f"({tag})  $\\mu$ = {mu}"
        if mu == 1.5:
            title += "   —   overmodulation: envelope no longer follows m(t)"
        ax.set_title(title, loc="left", fontsize=10)
        ap = dict(arrowstyle="-|>", color=INK, lw=0.8)
        if mu == 0.5:
            ax.annotate("$A_{max}$ = 15 V", xy=(1.0, 15), xytext=(1.12, 20.5), fontsize=9, arrowprops=ap)
            ax.annotate("$A_{min}$ = 5 V", xy=(0.5, 5.3), xytext=(0.5, 13), ha="center", fontsize=9, arrowprops=ap)
        if mu == 1.0:
            ax.annotate("envelope\ntouches zero", xy=(0.5, 0.6), xytext=(0.5, 9), ha="center",
                        fontsize=9, arrowprops=ap)
        if mu == 1.5:
            t0 = np.arccos(-1 / 1.5) / (2 * np.pi)  # ms, where 1 + 1.5 cos = 0
            ax.annotate("envelope folds at zero:\ncarrier phase reversal", xy=(t0, 0.3), xytext=(0.5, 12),
                        ha="center", fontsize=8.5, arrowprops=ap)
    axes[-1].set_xlabel("time t (ms)")
    axes[-1].set_xlim(0, 2)
    fig.tight_layout(h_pad=0.6)
    save(fig, CH, "fig-26-1-am-waveforms")


# ----------------------------------------------------------------------------- Figure 26.2
def fig_26_2():
    """Spectra of message, AM, DSB-SC, SSB-USB and VSB on a 100 kHz carrier."""
    f1, W, fc = 0.3, 3.4, 100.0
    h_lo, h_hi = 1.0, 0.45  # message spectrum: higher at low audio frequencies

    def msg(f):
        f = np.asarray(f, float)
        out = h_lo + (h_hi - h_lo) * (f - f1) / (W - f1)
        return np.where((f >= f1) & (f <= W), out, 0.0)

    f = np.linspace(85, 115, 60001)
    usb = msg(f - fc)
    lsb = msg(fc - f)
    fv = 1.5  # half-width of VSB filter skirt (kHz)
    x = np.clip((f - fc) / fv, -1, 1)
    Hv = 0.5 * (1 + np.sin(np.pi * x / 2))  # odd-symmetric about fc: H(fc+d)+H(fc-d)=1

    fig, axes = plt.subplots(5, 1, figsize=(6.4, 6.6),
                             gridspec_kw=dict(height_ratios=[1, 1, 1, 1, 1.15]))
    # baseband
    ax = axes[0]
    fb = np.linspace(0, 5, 2001)
    ax.fill_between(fb, msg(fb), color=COLORS[0], alpha=0.35, lw=0)
    ax.plot(fb, msg(fb), color=COLORS[0])
    ax.set_xlim(0, 5)
    ax.set_xticks([0, 0.3, 1, 2, 3, 3.4, 4, 5])
    ax.set_xticklabels(["0", "0.3", "1", "2", "3", "3.4", "4", "5"])
    ax.set_title("(a) message m(t): speech 0.3–3.4 kHz", loc="left", fontsize=10)
    ax.text(3.6, 0.55, "W = 3.4 kHz", fontsize=9)
    ax.set_xlabel("baseband frequency f (kHz)", fontsize=9, labelpad=1)

    def band(ax, y, color=COLORS[0]):
        ax.fill_between(f, y, color=color, alpha=0.35, lw=0)
        ax.plot(f, y, color=color, lw=1.2)

    def bw_arrow(ax, x0, x1, y, text):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=8, shrinkA=0, shrinkB=0))
        ax.text(x1 + 0.3, y, text, ha="left", va="center", fontsize=8.5)

    # AM
    ax = axes[1]
    band(ax, usb + lsb)
    ax.annotate("", xy=(fc, 1.7), xytext=(fc, 0), arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.6))
    ax.text(fc - 0.25, 1.6, "carrier", ha="right", color=COLORS[1], fontsize=8.5)
    bw_arrow(ax, fc - W, fc + W, 1.2, "$B_T$ = 2W = 6.8 kHz")
    ax.set_title("(b) conventional AM", loc="left", fontsize=10)
    ax.text(fc - 2.2, 0.15, "LSB", ha="center", fontsize=8.5)
    ax.text(fc + 2.2, 0.15, "USB", ha="center", fontsize=8.5)
    # DSB-SC
    ax = axes[2]
    band(ax, usb + lsb)
    bw_arrow(ax, fc - W, fc + W, 1.2, "$B_T$ = 2W = 6.8 kHz")
    ax.axvline(fc, color=INK, lw=0.6, ls=":")
    ax.set_title("(c) DSB-SC (no carrier line)", loc="left", fontsize=10)
    # SSB
    ax = axes[3]
    band(ax, usb)
    ax.axvline(fc, color=INK, lw=0.6, ls=":")
    bw_arrow(ax, fc, fc + W, 1.2, "$B_T$ = W = 3.4 kHz")
    ax.set_title("(d) SSB, upper sideband", loc="left", fontsize=10)
    # VSB
    ax = axes[4]
    band(ax, (usb + lsb) * Hv)
    ax.plot(f, 1.25 * Hv, "--", color=COLORS[1], lw=1.2)
    ax.text(fc + 4.6, 0.85, "VSB filter H(f) (dashed)", color=COLORS[1], fontsize=8.5)
    ax.text(fc - 4.3, 0.95, "skirt odd-symmetric\nabout $f_c$: H = ½ at 100 kHz", fontsize=8, ha="center")
    ax.axvline(fc, color=INK, lw=0.6, ls=":")
    ax.set_title("(e) VSB: upper sideband + vestige of lower", loc="left", fontsize=10)
    bw_arrow(ax, fc - fv, fc + W, 1.6, "$B_T$ ≈ W + vestige")
    ax.set_xlabel("frequency f (kHz)")
    for ax in axes[1:]:
        ax.set_xlim(90, 110)
        ax.set_xticks([90, 96.6, 100, 103.4, 110])
        ax.set_xticklabels(["90", "96.6", "100", "103.4", "110"])
    for ax in axes:
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_ylim(0, 1.95)
    axes[0].set_ylim(0, 1.3)
    for ax in axes:
        ax.tick_params(labelbottom=True, labelsize=8.5)
    fig.tight_layout(h_pad=0.25)
    save(fig, CH, "fig-26-2-amplitude-modulation-spectra")


# ----------------------------------------------------------------------------- Figure 26.3
def fig_26_3():
    """Bessel line spectra of tone FM for beta = 0.5, 2.405, 5 with the Carson band."""
    n = np.arange(-9, 10)
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 5.6), sharex=True)
    for ax, beta, tag in zip(axes, [0.5, 2.405, 5.0], "abc"):
        a = np.abs(jv(n, beta))
        a[np.abs(a) < 1e-12] = 0
        half = beta + 1
        ax.axvspan(-half, half, color=COLORS[5], alpha=0.18, lw=0)
        ml, sl, bl = ax.stem(n, a, basefmt=" ")
        plt.setp(sl, color=COLORS[0], lw=1.6)
        plt.setp(ml, color=COLORS[0], markersize=4)
        ax.axhline(0, color=INK, lw=0.6)
        ax.set_ylim(0, 1.08)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylabel("$|J_n(\\beta)|$")
        ax.set_title(f"({tag})  $\\beta$ = {beta}", loc="left", fontsize=10)
        lab = f"Carson bandwidth\n$2(\\beta+1)f_m$ = {2*half:.2f} $f_m$"
        if beta < 1:
            ax.text(half + 0.2, 0.98, lab, ha="left", va="top", fontsize=8.5, color="#2B6C8F")
        else:
            ax.text(0, 0.98, lab, ha="center", va="top", fontsize=8.5, color="#2B6C8F")
        for k in range(0, 9):
            v = abs(jv(k, beta))
            if v >= 0.03 and (beta != 5.0 or k in (0, 4)):
                ax.text(k, v + 0.03, f"{v:.3f}", ha="center", fontsize=7.5)
        if beta == 2.405:
            ax.text(0, 0.11, "carrier null", ha="center", fontsize=8.5, color=COLORS[1])
            ax.plot([0], [0], "x", color=COLORS[1], ms=7, mew=1.6)
        if beta == 5.0:
            ax.text(-8.8, 0.62, "power spread over\n$\\approx\\pm\\Delta f$ = ±5$f_m$", fontsize=8.5)
    axes[-1].set_xlim(-9.6, 9.6)
    axes[-1].set_xticks(range(-9, 10))
    axes[-1].set_xlabel("$(f-f_c)/f_m$")
    fig.tight_layout(h_pad=0.5)
    save(fig, CH, "fig-26-3-fm-bessel-spectra")


# ----------------------------------------------------------------------------- Figure 26.4
def _detector(vin, dt, rc):
    """Ideal-diode peak detector: charges instantly, discharges through RC."""
    out = np.empty_like(vin)
    v = 0.0
    k = np.exp(-dt / rc)
    for i, x in enumerate(vin):
        v *= k
        if x > v:
            v = x
        out[i] = v
    return out


def fig_26_4():
    """Envelope detector circuit and waveforms: ripple (RC = 10 us) and diagonal clipping (RC = 100 us)."""
    fc, fm, mu, Ac = 1e6, 5e3, 0.8, 1.0
    dt = 5e-9
    t = np.arange(0, 0.4e-3, dt)
    env = Ac * (1 + mu * np.cos(2 * np.pi * fm * t))
    vin = env * np.cos(2 * np.pi * fc * t)
    o10 = _detector(vin, dt, 10e-6)
    o100 = _detector(vin, dt, 100e-6)
    tm = t * 1e3

    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(4, 2, width_ratios=[1.35, 1.0], height_ratios=[1.75, 1, 1, 1],
                          wspace=0.05, hspace=0.6)
    axc = fig.add_subplot(gs[0, 0])
    d = schemdraw.Drawing(canvas=axc, show=False)
    d.config(unit=2.0, fontsize=8, lw=1.1, font="DejaVu Sans")
    d += (src := elm.SourceSin().up().length(3).label(["AM in", "1 MHz"], loc="top", ofst=0.2))
    d += elm.Diode().right().length(2.4).label("D (1N34A)", loc="top")
    d += (n1 := elm.Dot())
    d += elm.Line().right().length(2.2)
    d += (n2 := elm.Dot())
    d += elm.Capacitor().right().length(2.4).label("1 µF", loc="top")
    d += elm.Line().right().length(0.6)
    d += elm.Resistor().down().length(3).label(["$R_L$", "load"], loc="bottom", ofst=0.2)
    d += elm.Line().left().tox(src.start)
    d += elm.Resistor().at(n1.center).down().length(3).label(["R", "10 kΩ"], loc="bottom", ofst=0.2)
    d += elm.Capacitor().at(n2.center).down().length(3).label(["C", "1 nF"], loc="bottom", ofst=0.2)
    d += elm.Ground().at(src.start)
    d += elm.Label().at((n1.center[0] + 1.1, n1.center[1] + 0.45)).label("$v_o$", fontsize=9)
    d.draw(show=False)
    bb = d.get_bbox()
    axc.set_xlim(bb.xmin - 0.2, bb.xmax + 0.2)
    axc.set_ylim(bb.ymin - 0.2, bb.ymax + 0.2)
    axc.set_aspect("equal")
    axc.axis("off")
    axn = fig.add_subplot(gs[0, 1])
    axn.axis("off")
    axn.text(0.02, 0.85, "RC = 10 kΩ × 1 nF = 10 µs\n= 10 carrier periods", fontsize=8.5, va="top",
             transform=axn.transAxes)
    axn.text(0.02, 0.42, "no diagonal clipping if\n$RC\\leq\\sqrt{1-\\mu^2}/(2\\pi W\\mu)$ = 23.9 µs\n"
             "($\\mu$ = 0.8, W = 5 kHz)", fontsize=8.5, va="top", transform=axn.transAxes)

    ax1 = fig.add_subplot(gs[1, :])
    ax1.fill_between(tm[::20], -env[::20], env[::20], color=COLORS[0], alpha=0.35, lw=0)
    ax1.plot(tm, env, "--", color=COLORS[1], lw=1.2)
    ax1.plot(tm, -env, "--", color=COLORS[1], lw=1.2)
    ax1.set_title("(a) AM input: 1 MHz carrier (shaded band), $\\mu$ = 0.8, 5 kHz tone", loc="left", fontsize=9)
    ax1.set_ylim(-2, 2)
    ax1.set_ylabel("$v_{in}$ (V)")

    ax2 = fig.add_subplot(gs[2, :], sharex=ax1)
    ax2.plot(tm, env, "--", color=COLORS[1], lw=1.0, label="envelope")
    ax2.plot(tm, o10, color=COLORS[0], lw=1.2, label="$v_o$")
    ax2.set_title("(b) RC = 10 µs: follows envelope", loc="left", fontsize=9)
    ax2.set_ylim(0, 2)
    ax2.set_ylabel("$v_o$ (V)")
    # zoom inset showing carrier ripple
    ins = ax2.inset_axes([0.665, 0.47, 0.17, 0.48])
    sel = (t >= 0.100e-3) & (t <= 0.106e-3)
    ins.plot((t[sel] - 0.100e-3) * 1e6, env[sel], "--", color=COLORS[1], lw=0.9)
    ins.plot((t[sel] - 0.100e-3) * 1e6, o10[sel], color=COLORS[0], lw=1.1)
    lo, hi = o10[sel].min(), o10[sel].max()
    ins.set_ylim(lo - 0.15, hi + 0.08)
    ins.set_xlim(0, 6)
    ins.set_xticks([])
    ins.set_yticks([])
    ins.set_ylim(lo - 0.06, hi + 0.06)
    ins.set_title("6 µs zoom: sawtooth ripple", fontsize=7, pad=2)
    for sp in ["top", "right"]:
        ins.spines[sp].set_visible(True)

    ax3 = fig.add_subplot(gs[3, :], sharex=ax1)
    ax3.plot(tm, env, "--", color=COLORS[1], lw=1.0)
    ax3.plot(tm, o100, color=COLORS[0], lw=1.2)
    ax3.set_title("(c) RC = 100 µs: cannot follow the falling envelope", loc="left", fontsize=9)
    ax3.set_ylim(0, 2)
    ax3.set_ylabel("$v_o$ (V)")
    ax3.set_xlabel("time (ms)")
    ax3.set_xlim(0, 0.4)
    ax3.annotate("diagonal clipping", xy=(0.135, 0.85), xytext=(0.215, 1.55), fontsize=8.5,
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    for a in (ax1, ax2):
        a.tick_params(labelbottom=False)
    save(fig, CH, "fig-26-4-envelope-detector")


# ----------------------------------------------------------------------------- Figure 26.5
def fig_26_5():
    """Superheterodyne AM receiver at 1000 kHz with spectrum strip showing the image."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.0, 0.33, 1.0, 0.67])
    ax.set_xlim(0, 17)
    ax.set_ylim(0.4, 8.6)
    ax.set_aspect("equal")
    ax.axis("off")
    yt, yb, h = 7.0, 2.5, 1.3
    fs = 7.6
    # antenna
    ax.plot([0.55, 0.55], [yt, yt + 1.1], color=INK, lw=1.2)
    ax.plot([0.2, 0.55, 0.9], [yt + 1.4, yt + 1.1, yt + 1.4], color=INK, lw=1.2)
    ax.plot([0.55, 0.55], [yt + 1.1, yt + 1.4], color=INK, lw=1.2)
    ax.plot([0.55, 1.1], [yt, yt], color=INK, lw=1.1)
    box(ax, 1.1, yt - h / 2, 2.8, h, "RF preselector\n(tuned, Q = 50)", fontsize=fs)
    box(ax, 4.6, yt - h / 2, 2.0, h, "RF\namplifier", fontsize=fs)
    mx, r = 7.75, 0.45
    ax.add_patch(Circle((mx, yt), r, fc="white", ec=INK, lw=1.1))
    ax.plot([mx - r * 0.7, mx + r * 0.7], [yt - r * 0.7, yt + r * 0.7], color=INK, lw=1.1)
    ax.plot([mx - r * 0.7, mx + r * 0.7], [yt + r * 0.7, yt - r * 0.7], color=INK, lw=1.1)
    ax.text(mx, yt + r + 0.15, "mixer", ha="center", fontsize=fs)
    box(ax, 9.0, yt - h / 2, 3.3, h, "IF filter 455 kHz\n10 kHz BW (ceramic)", fontsize=fs)
    box(ax, 13.1, yt - h / 2, 2.6, h, "IF amplifier\nwith AGC", fontsize=fs)
    arrow(ax, 3.9, yt, 4.6, yt)
    arrow(ax, 6.6, yt, mx - r, yt)
    arrow(ax, mx + r, yt, 9.0, yt)
    arrow(ax, 12.3, yt, 13.1, yt)
    ax.text(4.25, yt + 0.85, "1000\nkHz", ha="center", fontsize=7, color=COLORS[0])
    ax.text(8.6, yt + 0.85, "455\nkHz", ha="center", fontsize=7, color=COLORS[0])
    # LO
    box(ax, 6.35, 4.2, 2.8, 1.15, "LO 1455 kHz\n(ganged with\npreselector)", fontsize=7.2, fc="#FFF4E0")
    arrow(ax, mx, 5.35, mx, yt - r)
    ax.plot([2.5, 2.5], [yt - h / 2, 4.78], color=COLORS[1], lw=0.9, ls=(0, (4, 3)))
    ax.plot([2.5, 6.35], [4.78, 4.78], color=COLORS[1], lw=0.9, ls=(0, (4, 3)))
    ax.text(3.0, 4.9, "gang", fontsize=7, color=COLORS[1])
    # second row, right to left
    box(ax, 13.1, yb - h / 2, 2.6, h, "Envelope\ndetector", fontsize=fs)
    box(ax, 9.0, yb - h / 2, 2.6, h, "Audio\namplifier", fontsize=fs)
    arrow(ax, 14.4, yt - h / 2, 14.4, yb + h / 2)
    ax.text(14.55, 4.75, "455 kHz", fontsize=7, color=COLORS[0])
    arrow(ax, 13.1, yb, 11.6, yb)
    ax.text(12.35, yb + 0.15, "audio", ha="center", fontsize=7, color=COLORS[0])
    # loudspeaker
    sx = 7.2
    arrow(ax, 9.0, yb, sx + 0.45, yb)
    ax.add_patch(Polygon([[sx + 0.45, yb - 0.25], [sx + 0.45, yb + 0.25], [sx + 0.15, yb + 0.25], [sx + 0.15, yb - 0.25]],
                         closed=True, fc="white", ec=INK, lw=1.1))
    ax.add_patch(Polygon([[sx + 0.15, yb - 0.25], [sx + 0.15, yb + 0.25], [sx - 0.35, yb + 0.6], [sx - 0.35, yb - 0.6]],
                         closed=True, fc="white", ec=INK, lw=1.1))
    ax.text(sx, yb - 0.95, "loudspeaker", ha="center", fontsize=fs)
    # AGC paths
    agc = dict(color=COLORS[2], lw=1.1)
    ax.plot([15.7, 16.4, 16.4], [yb - 0.3, yb - 0.3, yt - 0.3], **agc)
    arrow(ax, 16.4, yt - 0.3, 15.7, yt - 0.3, color=COLORS[2])
    ax.plot([14.4, 14.4, 5.6], [yb - h / 2, 1.0, 1.0], **agc)
    ax.plot([5.6, 5.6], [1.0, yt - h / 2 - 0.0], **agc)
    arrow(ax, 5.6, 5.6, 5.6, yt - h / 2, color=COLORS[2])
    ax.text(10.0, 0.6, "AGC (detected carrier level)", ha="center", fontsize=7.5, color=COLORS[2])
    ax.text(16.5, 4.75, "AGC", fontsize=7.5, color=COLORS[2], rotation=90, va="center")

    # spectrum strip
    axs = fig.add_axes([0.08, 0.07, 0.88, 0.22])
    f = np.linspace(1, 2200, 4000)
    fr, Q = 1000.0, 50.0
    rho = f / fr - fr / f
    HdB = -10 * np.log10(1 + (Q * rho) ** 2)
    axs.plot(f, HdB, color=COLORS[0], lw=1.4)
    axs.text(1070, -8, "preselector response", color=COLORS[0], fontsize=8)
    lines = [(455, "IF 455", COLORS[4]), (1000, "wanted\n1000", COLORS[2]),
             (1455, "LO 1455", COLORS[1]), (1910, "image\n1910", COLORS[3])]
    for fx, lab, c in lines:
        axs.axvline(fx, color=c, lw=1.4, ls="--" if fx in (455, 1455) else "-")
        if fx == 1910:
            axs.text(fx - 18, -47, lab, color=c, fontsize=8, va="bottom", ha="right")
        else:
            axs.text(fx + 18, -47, lab, color=c, fontsize=8, va="bottom")
    ai = -10 * np.log10(1 + (Q * (1.91 - 1 / 1.91)) ** 2)
    axs.plot([1910], [ai], "o", color=COLORS[3], ms=4)
    axs.annotate(f"{ai:.1f} dB at image", xy=(1910, ai), xytext=(1530, -22), fontsize=8,
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    axs.set_xlim(0, 2200)
    axs.set_ylim(-50, 3)
    axs.set_yticks([0, -20, -40])
    axs.set_xlabel("frequency (kHz)")
    axs.set_ylabel("|H| (dB)")
    save(fig, CH, "fig-26-5-superheterodyne-receiver")


# ----------------------------------------------------------------------------- Figure 26.6
def fig_26_6():
    """Output SNR versus gamma for baseband/DSB/SSB, AM (mu=1) and FM (beta=2, 5) with threshold."""
    gdB = np.linspace(0, 50, 2001)
    g = 10 ** (gdB / 10)

    def fm(beta, I=1.0):
        cnr = g / (2 * (beta + 1))  # carrier-to-noise ratio in the Carson bandwidth
        click = (12 * beta / np.pi) * g * np.exp(-cnr)  # Rice click-noise term
        supp = (1 - np.exp(-cnr)) ** 2  # signal suppression below threshold
        return 10 * np.log10(1.5 * beta ** 2 * g * supp / (1 / I + click))

    gth_am = 20.0  # ~13 dB
    am = 10 * np.log10((g / 3) / (1 + gth_am / g))
    I75 = 10 ** (13.2 / 10)
    fig, ax = new_fig(6.4, 4.4)
    ax.plot(gdB, gdB, color=INK, lw=1.6, label="baseband, DSB-SC, SSB")
    ax.plot(gdB, am, color=COLORS[1], label="AM, envelope, $\\mu$ = 1 (−4.8 dB)")
    ax.plot(gdB, fm(2), color=COLORS[0], label="FM, $\\beta$ = 2 (+7.8 dB)")
    ax.plot(gdB, fm(5), color=COLORS[2], label="FM, $\\beta$ = 5 (+15.7 dB)")
    ax.plot(gdB, fm(5, I75), ":", color=COLORS[2], lw=2.0, label="FM, $\\beta$ = 5, 75 µs de-emphasis (+13.2 dB)")
    for x, c, lab in [(13.0, COLORS[1], "AM\nthreshold"), (17.8, COLORS[0], "17.8"), (20.8, COLORS[2], "20.8")]:
        ax.axvline(x, color=c, lw=0.7, ls=(0, (2, 3)))
    ax.text(17.6, 1.2, "FM thresholds\n17.8 / 20.8 dB", fontsize=8, ha="center")
    ax.text(12.8, 22, "AM knee\n≈13 dB", fontsize=8, ha="right", color=COLORS[1])
    xg = 38.2
    ax.axvline(xg, color="#888888", lw=0.8, ls="--")
    for y, c, t in [(33.5, COLORS[1], "33.5 dB (AM)"), (54.0, COLORS[2], "54.0 dB (FM)"),
                    (67.2, COLORS[2], "67.2 dB (FM + de-emph.)")]:
        ax.plot([xg], [y], "o", color=c, ms=5, zorder=5)
        if y == 54.0:
            ax.text(xg - 0.8, y + 1.2, t, fontsize=8, color=c, ha="right")
        else:
            ax.text(xg + 0.8, y - 2.8, t, fontsize=8, color=c)
    ax.text(xg + 0.4, 3.5, "γ = 38.2 dB\n(worked example)", fontsize=8, color="#555555")
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 70)
    ax.set_xlabel("baseband reference SNR  γ = $S_R/(N_0W)$  (dB)")
    ax.set_ylabel("output SNR (dB)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, lw=0.5)
    save(fig, CH, "fig-26-6-analog-noise-performance")


if __name__ == "__main__":
    fig_26_1()
    fig_26_2()
    fig_26_3()
    fig_26_4()
    fig_26_5()
    fig_26_6()
