"""Figures for Chapter 19 — Sampling and Reconstruction.

Run from the repository root:  python figures/scripts/ch19.py
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, save, COLORS, INK, GRID  # noqa: E402

CH = "19"
RED = "#D55E00"


def _tri(f, fc, B, h=1.0):
    """Triangle spectrum of half-width B and height h centred on fc."""
    return h * np.clip(1 - np.abs(f - fc) / B, 0, None)


def fig_19_1():
    """Baseband spectrum and its replicas for adequate and inadequate sampling."""
    f = np.linspace(-3, 3, 6001)
    B = 0.8
    fig, axs = plt.subplots(3, 1, figsize=(6.4, 5.0), sharex=True)

    # (a) baseband
    ax = axs[0]
    ax.fill_between(f, _tri(f, 0, B), color=COLORS[0], alpha=0.25, lw=0)
    ax.plot(f, _tri(f, 0, B), color=COLORS[0])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "1"])
    ax.set_ylabel("$|X(f)|$")
    ax.annotate("", xy=(B, 0.5), xytext=(0, 0.5),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=9))
    ax.text(B / 2, 0.56, "$B$ = 0.8 kHz", ha="center", va="bottom", fontsize=9)
    ax.set_title("(a) band-limited signal", loc="left", fontsize=10)

    # (b) fs = 2 kHz
    ax = axs[1]
    fs = 2.0
    for k in range(-2, 3):
        y = _tri(f, k * fs, B)
        ax.fill_between(f, y, color=COLORS[0], alpha=0.25 if k == 0 else 0.12, lw=0)
        ax.plot(f, y, color=COLORS[0], lw=1.6 if k == 0 else 1.2)
    ax.plot([-1, -1, 1, 1], [0, 1.18, 1.18, 0], ls="--", color=INK, lw=1.1)
    ax.text(0, 1.26, "ideal LPF, gain $T$, cut-off $f_s/2$ = 1 kHz", fontsize=8.5, ha="center", va="center")

    ax.text(-1.2, 0.35, "gap", ha="center", fontsize=8, color="0.35")
    ax.text(1.2, 0.35, "gap", ha="center", fontsize=8, color="0.35")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "$1/T$"])
    ax.set_ylabel("$|X_s(f)|$")
    ax.set_title("(b) $f_s$ = 2 kHz > 2$B$: replicas separate", loc="left", fontsize=10)

    # (c) fs = 1.2 kHz
    ax = axs[2]
    fs = 1.2
    tot = np.zeros_like(f)
    reps = []
    for k in range(-3, 4):
        y = _tri(f, k * fs, B)
        reps.append(y)
        tot += y
        ax.plot(f, y, color=COLORS[0], lw=0.9, alpha=0.8)
    reps = np.array(reps)
    overlap = (reps > 0).sum(axis=0) > 1
    ax.fill_between(f, tot, where=overlap, color=RED, alpha=0.35, lw=0)
    ax.plot(f, tot, color=INK, lw=1.4)
    ax.plot([0.6, 0.6], [0, 1.15], color=RED, ls="--", lw=1.0)
    ax.plot([-0.6, -0.6], [0, 1.15], color=RED, ls="--", lw=1.0)
    ax.text(0.0, 1.26, r"$\pm f_s/2$ = $\pm$0.6 kHz", color=RED, fontsize=8.5, ha="center", va="center")
    ax.text(-2.95, 1.26, "black: sum of replicas", fontsize=8, color=INK, va="center")
    for c in (-2.4, -1.2, 1.2, 2.4):
        ax.text(c, 1.05, f"{c:g}", ha="center", fontsize=7.5, color=COLORS[0])
    ax.annotate("aliasing (overlap)", xy=(1.65, 0.3), xytext=(2.1, 1.26), fontsize=9, color=RED,
                ha="center", va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9, mutation_scale=9))
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["0", "$1/T$"])
    ax.set_ylabel("$|X_s(f)|$")
    ax.set_ylim(0, 1.35)

    ax.set_title("(c) $f_s$ = 1.2 kHz < 2$B$: replicas overlap", loc="left", fontsize=10)
    ax.set_xlabel("frequency $f$ (kHz)")
    for ax in axs:
        ax.set_xlim(-3, 3)
        ax.set_xticks(np.arange(-3, 3.1, 1.0))
        ax.tick_params(axis="x", labelsize=8)
    for ax in axs[:2]:
        ax.set_ylim(0, 1.35)
    fig.tight_layout(h_pad=0.6)
    save(fig, CH, "fig-19-1-sampled-spectrum-replicas")


def fig_19_2():
    """Folding of mains harmonics at 1600 Sa/s."""
    fs = 1600.0
    fig, ax = new_fig(6.4, 3.9)
    f = np.linspace(0, 1700, 3401)
    fa = np.abs(f - fs * np.round(f / fs))
    ax.plot(f, fa, color=INK, lw=1.4)
    ax.axvline(800, color="0.4", ls="--", lw=1)
    ax.axvline(1600, color="0.4", ls="--", lw=1)
    ax.text(810, 420, "$f_s/2$ = 800 Hz", fontsize=8.5, color="0.3", rotation=90, va="center")
    ax.text(1590, 420, "$f_s$ = 1600 Hz", fontsize=8.5, color="0.3", rotation=90, va="center", ha="right")
    harm = {1: COLORS[2], 5: COLORS[2], 7: COLORS[2], 11: COLORS[2], 13: COLORS[2], 15: COLORS[2],
            17: RED, 19: RED, 31: COLORS[3], 33: COLORS[3]}
    for h, c in harm.items():
        fh = 50 * h
        a = abs(fh - fs * round(fh / fs))
        ax.plot(fh, a, "o", color=c, ms=6, zorder=5)
        ax.plot([fh, fh], [0, a], color=c, lw=0.6, ls=":")
    # arrows for 17th and 19th
    for h, lab in ((17, "17th → 750 Hz (read as 15th)"), (19, "19th → 650 Hz (read as 13th)")):
        fh = 50 * h
        a = abs(fh - fs)
        ax.annotate("", xy=(752, a), xytext=(fh - 4, a),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0, mutation_scale=9))
    ax.plot(750, 750, "o", mfc="white", mec=RED, ms=8, zorder=4)
    ax.plot(650, 650, "o", mfc="white", mec=RED, ms=8, zorder=4)
    ax.text(1010, 735, "17th reported as 15th", color=RED, fontsize=9, va="center")
    ax.text(1010, 640, "19th lands on 13th", color=RED, fontsize=9, va="center")
    ax.annotate("31st, 33rd → 50 Hz\n(added to fundamental)", xy=(1560, 55), xytext=(1150, 230),
                fontsize=9, color=COLORS[3], ha="center",
                arrowprops=dict(arrowstyle="-|>", color=COLORS[3], lw=0.9, mutation_scale=9))
    ax.text(300, 120, "first Nyquist zone:\nreported correctly", fontsize=8.5, color=COLORS[2], ha="center")
    ax.set_xlim(0, 1700)
    ax.set_ylim(0, 820)
    ax.set_xlabel("true frequency (Hz)")
    ax.set_ylabel("apparent frequency (Hz)")
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600])
    sec = ax.secondary_xaxis("top")
    orders = [1, 5, 7, 11, 13, 15, 17, 19, 31, 33]
    sec.set_xticks([50 * h for h in orders])
    sec.set_xticklabels([str(h) for h in orders], fontsize=8)
    sec.set_xlabel("harmonic order", fontsize=9)
    save(fig, CH, "fig-19-2-harmonic-folding")


def fig_19_3():
    """Natural versus flat-top sampling of a 300 Hz sine."""
    f0, fs = 300.0, 4000.0
    T = 1 / fs
    tau = 0.25 * T
    t = np.linspace(0, 5e-3, 20001)
    x = np.sin(2 * np.pi * f0 * t)
    phase = np.mod(t, T)
    gate = phase < tau
    nat = np.where(gate, x, 0.0)
    held = np.sin(2 * np.pi * f0 * (t - phase))
    flat = np.where(gate, held, 0.0)
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True)
    for ax, y, lab, kind in ((axs[0], nat, "natural sampling: tops follow the signal", "nat"),
                             (axs[1], flat, "flat-top sampling: tops held at the start value", "flat")):
        ax.plot(t * 1e3, x, color="0.65", lw=0.9)
        ax.fill_between(t * 1e3, y, color=COLORS[0], alpha=0.35, lw=0, step=None)
        ax.plot(t * 1e3, y, color=COLORS[0], lw=0.8)
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_ylim(-1.2, 1.2)
        ax.set_xlim(0, 5)
        ax.set_ylabel("amplitude")
        ax.set_title(lab, loc="left", fontsize=10)
        # inset zoom on the pulse at 0.75 ms
        t0 = 3 * T
        ins = ax.inset_axes([0.73, 0.06, 0.25, 0.34])
        tz = np.linspace(t0 - 0.2 * T, t0 + 1.2 * tau, 800)
        ph = np.mod(tz - 1e-12, T)
        g = (tz >= t0) & (tz < t0 + tau)
        xz = np.sin(2 * np.pi * f0 * tz)
        yz = np.where(g, xz if kind == "nat" else np.sin(2 * np.pi * f0 * t0), 0.0)
        ins.plot(tz * 1e6, xz, color="0.6", lw=0.9)
        ins.fill_between(tz * 1e6, yz, color=COLORS[0], alpha=0.35, lw=0)
        ins.plot(tz * 1e6, yz, color=COLORS[0], lw=1.2)
        lo, hi = np.sin(2 * np.pi * f0 * t0), np.sin(2 * np.pi * f0 * (t0 + tau))
        ins.set_ylim(lo - 0.12, hi + 0.06)
        ins.set_xlim(tz[0] * 1e6, tz[-1] * 1e6)
        ins.set_yticks([])
        ins.set_xticks([])
        ins.set_title("zoom: pulse at 0.75 ms, 62.5 µs wide", fontsize=7, pad=2)
        for s in ins.spines.values():
            s.set_visible(True)
            s.set_color("0.5")
        ax.add_patch(Rectangle((t0 * 1e3 - 0.03, lo - 0.1), tau * 1e3 + 0.06, hi - lo + 0.18,
                               fill=False, ec="0.35", lw=0.8))
    axs[1].set_xlabel("time (ms)")
    axs[0].text(0.02, 0.06, r"$f_0$ = 300 Hz, $f_s$ = 4 kHz, $\tau$ = 0.25$T$ = 62.5 µs",
                transform=axs[0].transAxes, fontsize=8.5)
    fig.tight_layout(h_pad=0.8)
    save(fig, CH, "fig-19-3-natural-flat-top-sampling")


def fig_19_4():
    """Sinc interpolation of eight samples."""
    def xs(t):
        return 0.8 * np.sin(2 * np.pi * 0.15 * t) + 0.3 * np.cos(2 * np.pi * 0.35 * t)
    n = np.arange(8)
    xn = xs(n)
    t = np.linspace(-2, 10, 2401)
    fig, ax = new_fig(6.4, 3.8)
    cmap = plt.get_cmap("viridis")
    tot = np.zeros_like(t)
    for i, (k, v) in enumerate(zip(n, xn)):
        p = v * np.sinc(t - k)
        tot += p
        ax.plot(t, p, color=cmap(i / 7.5), lw=0.9, alpha=0.85)
    ax.plot(t, tot, color=INK, lw=2.2, label=r"$\sum_n x[n]\,\mathrm{sinc}((t-nT)/T)$")
    ml, sl, bl = ax.stem(n, xn, basefmt=" ")
    plt.setp(sl, color=INK, lw=1.0)
    plt.setp(ml, color=INK, ms=6, zorder=6)
    ax.axhline(0, color=INK, lw=0.6)
    for k in n:
        ax.axvline(k, color=GRID, lw=0.6, zorder=0)
    ax.set_xlim(-2, 10)
    ax.set_ylim(-1, 1.5)
    ax.set_xlabel("time $t/T$")
    ax.set_ylabel("amplitude")
    ax.legend(loc="upper right", fontsize=9)
    ax.annotate("each sinc is zero at all\nother sample instants", xy=(8, 0.0), xytext=(6.6, -0.78),
                fontsize=8.5, ha="left",
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
    ax.text(-1.9, 1.38, "thin curves: one sinc per sample, scaled by $x[n]$", fontsize=8.5, color="0.3")
    save(fig, CH, "fig-19-4-sinc-interpolation")


def fig_19_5():
    """Zero-order-hold staircase and sinc droop."""
    fs, f0 = 20e3, 2e3
    T = 1 / fs
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1.05, 1]))
    t = np.linspace(0, 1e-3, 4001)
    a1.plot(t * 1e3, np.sin(2 * np.pi * f0 * t), color="0.6", lw=1.0, label="input, 2 kHz")
    tn = np.arange(0, 1e-3 + T / 2, T)
    a1.step(tn * 1e3, np.sin(2 * np.pi * f0 * tn), where="post", color=INK, lw=1.4, label="ZOH output")
    a1.plot(t * 1e3, np.sin(2 * np.pi * f0 * (t - T / 2)), color=COLORS[0], ls="--", lw=1.1,
            label="input delayed $T/2$ = 25 µs")
    a1.set_xlim(0, 1)
    a1.set_ylim(-1.25, 1.6)
    a1.set_xlabel("time (ms)")
    a1.set_ylabel("amplitude")
    a1.legend(loc="upper center", fontsize=7.5, ncol=2, handlelength=1.6, columnspacing=0.8)
    a1.set_title("(a) staircase at $f_s$ = 20 kSa/s", loc="left", fontsize=10)

    u = np.linspace(1e-4, 3, 3000)
    m = 20 * np.log10(np.abs(np.sinc(u)) + 1e-12)
    a2.axvspan(0, 0.4535, color=COLORS[2], alpha=0.15, lw=0)
    a2.plot(u, m, color=INK, lw=1.4)
    a2.plot(0.5, 20 * np.log10(2 / np.pi), "o", color=COLORS[1], ms=5)
    a2.annotate("$f_s/2$: −3.92 dB", xy=(0.5, -3.92), xytext=(1.05, -6.5), fontsize=8.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.8, mutation_scale=8))
    v = 20 * np.log10(np.sinc(0.4535))
    a2.plot(0.4535, v, "s", color=COLORS[2], ms=4.5)
    a2.annotate("CD audio,\n20 kHz at\n44.1 kSa/s:\n−3.17 dB", xy=(0.4535, v), xytext=(0.04, -32),
                fontsize=8.5, color=COLORS[2],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=0.8, mutation_scale=8))
    for k in (1, 2, 3):
        a2.text(k - 0.04, -38.5, "null", ha="right", va="bottom", fontsize=7.5, color="0.4")
    a2.set_xlim(0, 3)
    a2.set_ylim(-40, 1)
    a2.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
    a2.set_xlabel("normalised frequency $f/f_s$")
    a2.set_ylabel(r"$20\log_{10}|\mathrm{sinc}(f/f_s)|$ (dB)")
    a2.set_title("(b) ZOH magnitude response", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.2)
    save(fig, CH, "fig-19-5-zoh-staircase-droop")


def fig_19_6():
    """Anti-aliasing specification for an ECG front end at 500 Sa/s."""
    fp, fs, fc = 150.0, 500.0, 150.0
    fstop = fs - fp
    f = np.logspace(1, np.log10(2000), 1000)
    fig, ax = new_fig(6.4, 4.0)
    ax.add_patch(Rectangle((10, -80), fp - 10, 80, color=COLORS[2], alpha=0.12, lw=0))
    ax.text(38, -76, "passband to $f_p$ = 150 Hz", fontsize=8.5, color=COLORS[2], ha="center")
    ax.add_patch(Rectangle((fstop, -40), 2000 - fstop, 40, color=COLORS[1], alpha=0.15, lw=0,
                           hatch="///", ec=COLORS[1]))
    ax.text(840, -6, "forbidden zone\n(above $-$40 dB\nbeyond $f_s-f_p$)", fontsize=8.5, color=COLORS[1],
            ha="center", va="top")
    for order, c in ((2, COLORS[0]), (4, COLORS[4]), (6, COLORS[3])):
        m = -10 * np.log10(1 + (f / fc) ** (2 * order))
        ax.semilogx(f, m, color=c, lw=1.6, label=f"Butterworth, n = {order}")
    a6 = -10 * np.log10(1 + (fstop / fc) ** 12)
    ax.plot(fstop, a6, "o", color=COLORS[3], ms=5, zorder=5)
    ax.annotate(f"n = 6: {a6:.1f} dB at 350 Hz\n(meets spec)", xy=(fstop, a6), xytext=(13, -47),
                fontsize=8.5, color=COLORS[3],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[3], lw=0.8, mutation_scale=8))
    ax.axvline(250, color="0.35", ls="--", lw=1)
    ax.axvline(fstop, color="0.35", ls="--", lw=1)
    ax.text(245, -79, "$f_s/2$ = 250 Hz", rotation=90, ha="right", va="bottom", fontsize=8.5, color="0.3")
    ax.text(345, -79, "$f_s-f_p$ = 350 Hz", rotation=90, ha="right", va="bottom", fontsize=8.5, color="0.3")
    ax.axhline(-3, color="0.6", lw=0.6, ls=":")
    ax.set_xlim(10, 2000)
    ax.set_ylim(-80, 3)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("magnitude (dB)")
    ax.legend(loc="lower left", fontsize=8.5, bbox_to_anchor=(0.0, 0.07))
    # inset: folding of 350 Hz onto 150 Hz
    ins = ax.inset_axes([0.05, 0.6, 0.33, 0.2])
    ins.set_xlim(0, 520)
    ins.set_ylim(-0.6, 1.0)
    ins.plot([0, 500], [0, 0], color=INK, lw=0.8)
    for x0, lab in ((0, "0"), (150, "150"), (250, "250"), (350, "350"), (500, "500")):
        ins.plot([x0, x0], [-0.06, 0.06], color=INK, lw=0.8)
        ins.text(x0, -0.15, lab, ha="center", va="top", fontsize=6.5)
    ins.annotate("", xy=(150, 0.08), xytext=(350, 0.08),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.0, mutation_scale=8,
                                 connectionstyle="arc3,rad=0.6"))
    ins.text(250, 0.78, "350 Hz folds to 150 Hz", ha="center", fontsize=7, color=COLORS[1])
    ins.axis("off")
    save(fig, CH, "fig-19-6-anti-aliasing-specification")


if __name__ == "__main__":
    fig_19_1()
    fig_19_2()
    fig_19_3()
    fig_19_4()
    fig_19_5()
    fig_19_6()
