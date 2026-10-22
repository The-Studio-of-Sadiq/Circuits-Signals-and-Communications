"""Figures for Chapter 17 — Linear Time-Invariant Systems.

Run from the repository root:  python figures/scripts/ch17.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402

CH = "17"


def _stem(ax, n, x, color=COLORS[0], ms=3.5, lw=1.2, label=None):
    ml, sl, bl = ax.stem(n, x, linefmt="-", markerfmt="o", basefmt=" ", label=label)
    plt.setp(sl, color=color, lw=lw)
    plt.setp(ml, color=color, ms=ms)
    ax.axhline(0, color=INK, lw=0.6)
    return ml


def adder(ax, x, y, r=0.3, signs=None, fs=9):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, r"$\Sigma$", ha="center", va="center", fontsize=fs, zorder=4)
    off = {"w": (-r - 0.22, r + 0.12), "s": (r + 0.22, -r - 0.18), "n": (r + 0.22, r + 0.18)}
    for k, v in (signs or {}).items():
        dx, dy = off[k]
        ax.text(x + dx, y + dy, v, ha="center", va="center", fontsize=fs + 1, zorder=4)


def line(ax, xs, ys, lw=1.1):
    ax.plot(xs, ys, color=INK, lw=lw, solid_capstyle="butt")


def dot(ax, x, y):
    ax.plot([x], [y], "o", ms=3.2, color=INK, zorder=5)


# ------------------------------------------------------------------ 17.1
def fig_17_1():
    x = np.array([1, 2, 3])
    h = np.array([1, 0.5, 0.25])
    n = np.arange(0, 7)
    fig, axs = plt.subplots(4, 2, figsize=(6.6, 5.6), sharex=True, sharey=True)
    for k in range(3):
        comp = np.zeros(7)
        comp[k] = x[k]
        resp = np.zeros(7)
        resp[k:k + 3] = x[k] * h
        c = COLORS[k]
        _stem(axs[k, 0], n, comp, color=c)
        _stem(axs[k, 1], n, resp, color=c)
        lab_in = [r"$1\,\delta[n]$", r"$2\,\delta[n-1]$", r"$3\,\delta[n-2]$"][k]
        lab_out = [r"$1\,h[n]$", r"$2\,h[n-1]$", r"$3\,h[n-2]$"][k]
        axs[k, 0].text(6.3, 3.9, lab_in, ha="right", va="top", fontsize=10, color=c)
        axs[k, 1].text(6.3, 3.9, lab_out, ha="right", va="top", fontsize=10, color=c)
        for i in range(k, k + 3):
            axs[k, 1].text(i, resp[i] + 0.2, f"{resp[i]:g}", ha="center", va="bottom", fontsize=7.5,
                           color=c)
        axs[k, 1].annotate("", xy=(-0.25, 1.8), xytext=(-0.9, 1.8), xycoords="data",
                           annotation_clip=False)
    # bottom row: the sums
    xs = np.zeros(7)
    xs[:3] = x
    _stem(axs[3, 0], n, xs, color=INK)
    axs[3, 0].text(6.3, 3.9, r"$x[n]=\sum_k x[k]\,\delta[n-k]$", ha="right", va="top", fontsize=10)
    y = np.convolve(x, h)
    ax = axs[3, 1]
    bottom = np.zeros(7)
    for k in range(3):
        resp = np.zeros(7)
        resp[k:k + 3] = x[k] * h
        for i in range(7):
            if resp[i] > 0:
                ax.plot([i, i], [bottom[i], bottom[i] + resp[i]], color=COLORS[k], lw=4,
                        solid_capstyle="butt")
        bottom += resp
    ax.plot(np.arange(5), y, "o", color=INK, ms=4, zorder=5)
    ax.axhline(0, color=INK, lw=0.6)
    for i, v in enumerate(y):
        ax.text(i + 0.18, v + 0.05, f"{v:g}", ha="left", va="bottom", fontsize=8)
    ax.text(6.3, 3.9, r"$y[n]=\sum_k x[k]\,h[n-k]$", ha="right", va="top", fontsize=10)
    for a in axs.flat:
        a.set_ylim(0, 4.5)
        a.set_xlim(-0.5, 6.5)
        a.set_yticks([0, 2, 4])
    for a in axs[3]:
        a.set_xlabel("n")
    axs[0, 0].set_title("input pieces", fontsize=10)
    axs[0, 1].set_title("responses, h[n] = {1, 0.5, 0.25}", fontsize=10)
    fig.supylabel("amplitude", fontsize=10, x=0.01)
    fig.tight_layout(rect=(0.02, 0, 1, 1), h_pad=0.4)
    save(fig, CH, "fig-17-1-impulse-decomposition")


# ------------------------------------------------------------------ 17.2
def fig_17_2():
    tau = 1.0  # ms
    lam = np.linspace(-2, 5, 2801)
    xl = np.where((lam >= 0) & (lam <= 2), 5.0, 0.0)

    def y_of(t):
        t = np.asarray(t, dtype=float)
        return np.where(t < 0, 0, np.where(t <= 2, 5 * (1 - np.exp(-t / tau)),
                                           5 * (1 - np.exp(-2 / tau)) * np.exp(-(t - 2) / tau)))

    fig = plt.figure(figsize=(6.6, 6.0))
    gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1.35], hspace=0.55)
    scale = 5.0 / 1000.0  # plot h on the voltage axis: 1000 s^-1 -> 5
    for i, t in enumerate([1, 2, 3]):
        ax = fig.add_subplot(gs[i])
        h = np.where(lam <= t, 1000 * np.exp(-(t - lam) / tau), 0.0)
        ov = (lam >= 0) & (lam <= min(t, 2)) & (lam <= t)
        ax.fill_between(lam, 0, h * scale, where=ov, color=COLORS[1], alpha=0.25, lw=0,
                        label="overlap (product area)")
        ax.plot(lam, xl, color=COLORS[0], label=r"$x(\lambda)$ (V)")
        ax.plot(lam, h * scale, color=COLORS[1], lw=1.5, label=r"$h(t-\lambda)$ (s$^{-1}$, right)")
        ax.axvline(t, color="0.5", ls=":", lw=0.9)
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_xlim(-2, 5)
        ax.set_ylim(0, 6.2)
        ax.set_yticks([0, 5])
        ax.set_ylabel("V", fontsize=9)
        sec = ax.secondary_yaxis("right", functions=(lambda v: v / scale, lambda v: v * scale))
        sec.set_yticks([0, 1000])
        sec.tick_params(labelsize=8, colors=COLORS[1])
        ax.text(-1.9, 5.9, f"t = {t} ms", fontsize=9.5, va="top", fontweight="bold")
        ax.text(4.9, 5.9, f"y({t} ms) = {float(y_of(t)):.2f} V", fontsize=9, va="top", ha="right")
        if i == 0:
            ax.legend(fontsize=7.5, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.45),
                      handlelength=1.5, columnspacing=1.0)
        ax.set_xlabel(r"$\lambda$ (ms)", fontsize=9, labelpad=0)
        ax.tick_params(labelsize=8)
    ax = fig.add_subplot(gs[3])
    tt = np.linspace(0, 6, 1201)
    ax.plot(tt, y_of(tt), color=COLORS[2], lw=2)
    ax.plot(tt, np.where((tt >= 0) & (tt <= 2), 5, 0), ":", color=COLORS[0], lw=1)
    for t in (1, 2, 3):
        v = float(y_of(t))
        ax.plot(t, v, "o", color=INK, ms=5, zorder=5)
        if t == 1:
            ax.text(t + 0.12, v - 0.25, f"{v:.2f} V", fontsize=8.5, va="top")
        else:
            ax.text(t + 0.1, v + 0.15, f"{v:.2f} V", fontsize=8.5, va="bottom")
    ax.text(1.0, 5.1, "input x(t), 5 V for 0–2 ms", fontsize=8, color=COLORS[0], ha="center",
            va="bottom")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 5.6)
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("y(t) (V)")
    ax.text(5.95, 5.4, r"output $y(t)=\int x(\lambda)\,h(t-\lambda)\,d\lambda$", ha="right", va="top",
            fontsize=9)
    save(fig, CH, "fig-17-2-graphical-convolution-rc")


# ------------------------------------------------------------------ 17.3
def fig_17_3():
    L, C = 10e-3, 1e-6
    w0 = 1 / np.sqrt(L * C)
    t = np.linspace(0, 2e-3, 4001)
    fig, ax = new_fig(6.4, 3.9)
    ax.axhspan(0.98, 1.02, color="0.85", lw=0)
    ax.axhline(1.0, color="0.4", ls="--", lw=0.9)
    for R, c in [(50, COLORS[1]), (141, COLORS[0]), (200, COLORS[2])]:
        z = R / 2 * np.sqrt(C / L)
        _, y = signal.step(([w0 ** 2], [1, 2 * z * w0, w0 ** 2]), T=t)
        os_ = (y.max() - 1) * 100
        lab = f"R = {R} Ω, ζ = {z:.3g}" + (f", overshoot {os_:.1f} %" if os_ > 0.05 else ", no overshoot")
        ax.plot(t * 1e3, y, color=c, label=lab)
        if R == 50:
            i = np.argmax(y)
            ax.plot(t[i] * 1e3, y[i], "o", color=c, ms=5)
            ax.annotate(f"peak {y[i]:.3f} V at {t[i] * 1e3:.3f} ms", xy=(t[i] * 1e3, y[i]),
                        xytext=(0.45, 1.43), fontsize=8.5, color=c,
                        arrowprops=dict(arrowstyle="->", color=c, lw=0.8))
            env = np.exp(-z * w0 * t)
            ax.plot(t * 1e3, 1 + env, ":", color=c, lw=1.1)
            ax.plot(t * 1e3, 1 - env, ":", color=c, lw=1.1)
            ax.text(0.8, 1 + np.exp(-z * w0 * 0.8e-3) + 0.03, r"$1\pm e^{-2500t}$", fontsize=8.5,
                    color=c)
    ax.text(1.98, 0.955, "±2 % band", ha="right", va="top", fontsize=8, color="0.35")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.5)
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("output $v_C$ (V)")
    ax.legend(fontsize=8, loc="lower right", bbox_to_anchor=(1.0, 0.08))
    ax.set_title("Unit step response, L = 10 mH, C = 1 µF", fontsize=10)
    save(fig, CH, "fig-17-3-rlc-step-response")


# ------------------------------------------------------------------ 17.4
def fig_17_4():
    fig = plt.figure(figsize=(6.8, 4.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.15], hspace=0.75, wspace=0.12)
    axd = fig.add_subplot(gs[:, 0])
    axd.set_xlim(0, 7)
    axd.set_ylim(0, 6)
    axd.set_aspect("equal")
    axd.axis("off")
    yb = 4.0
    axd.text(0.0, yb, "x[n]", va="center", fontsize=10)
    arrow(axd, 0.85, yb, 1.4, yb)
    box(axd, 1.4, yb - 0.4, 1.2, 0.8, "×0.1", fontsize=9, fc="#FFF4E0")
    arrow(axd, 2.6, yb, 3.2, yb)
    adder(axd, 3.5, yb, signs={"w": "+", "s": "+"})
    arrow(axd, 3.8, yb, 6.0, yb)
    axd.text(6.05, yb, "y[n]", va="center", fontsize=10)
    dot(axd, 5.3, yb)
    line(axd, [5.3, 5.3], [yb, 3.05])
    box(axd, 4.7, 2.25, 1.2, 0.8, r"$z^{-1}$", fontsize=10, fc="white")
    line(axd, [5.3, 5.3], [2.25, 1.4])
    arrow(axd, 5.3, 1.4, 4.7, 1.4)
    box(axd, 3.5, 1.0, 1.2, 0.8, "×0.9", fontsize=9, fc="#FFF4E0")
    line(axd, [3.5, 3.5], [1.4, 1.4])
    axd.plot([3.5, 3.5], [1.4, 1.4])
    arrow(axd, 3.5, 1.8, 3.5, yb - 0.3)
    axd.text(5.95, 2.65, "y[n−1]", va="center", fontsize=8.5, ha="left", color="0.3")
    axd.text(3.5, 5.3, "y[n] = 0.9 y[n−1] + 0.1 x[n]", ha="center", fontsize=9.5)
    axd.text(3.5, 0.35, "exponential smoother, a = 0.9", ha="center", fontsize=8.5, style="italic",
             color="0.35")

    n = np.arange(0, 41)
    fs = 10.0
    ax1 = fig.add_subplot(gs[0, 1])
    _stem(ax1, n, 0.1 * 0.9 ** n, ms=2.4, lw=0.9)
    ax1.set_ylim(0, 0.115)
    ax1.set_xlim(-1, 41)
    ax1.set_ylabel("h[n]")
    ax1.set_xlabel("n", labelpad=1)
    ax1.text(40, 0.105, r"$h[n]=0.1\,(0.9)^n$", ha="right", va="top", fontsize=9.5)
    ax2 = fig.add_subplot(gs[1, 1])
    s = 1 - 0.9 ** (n + 1)
    _stem(ax2, n, s, ms=2.4, lw=0.9, color=COLORS[2])
    ax2.axhline(0.95, color=COLORS[1], ls="--", lw=1)
    ax2.plot(28, s[28], "o", ms=6, mfc="none", mec=COLORS[1], mew=1.3)
    ax2.annotate(f"n = 28: {s[28]:.3f}", xy=(28, s[28]), xytext=(14, 0.62), fontsize=8.5, bbox=dict(fc="white", ec="none", pad=1),
                 color=COLORS[1], arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=0.8))
    ax2.text(0.5, 0.97, "0.95", fontsize=8, color=COLORS[1], va="bottom")
    ax2.set_ylim(0, 1.1)
    ax2.set_xlim(-1, 41)
    ax2.set_xlabel("n", labelpad=1)
    ax2.set_ylabel("s[n]")
    ax2.text(40, 0.25, r"$s[n]=1-0.9^{\,n+1}$", ha="right", fontsize=9.5,
             bbox=dict(fc="white", ec="none", pad=1))
    for ax in (ax1, ax2):
        sec = ax.secondary_xaxis("top", functions=(lambda v: v / fs, lambda v: v * fs))
        sec.set_xticks([0, 1, 2, 3, 4])
        sec.tick_params(labelsize=7.5, pad=1)
        sec.set_xlabel("t (s) at $f_s$ = 10 Hz", fontsize=8, labelpad=2)
        ax.tick_params(labelsize=8)
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.spines["right"].set_visible(True)
        ax.spines["left"].set_visible(False)
    save(fig, CH, "fig-17-4-exponential-smoother")


# ------------------------------------------------------------------ 17.5
def fig_17_5():
    tau = 1e-3
    w = 2 * np.pi * 100
    t = np.linspace(0, 20e-3, 4001)
    Hm = 1 / np.sqrt(1 + (w * tau) ** 2)
    ph = -np.arctan(w * tau)
    A = 10 * Hm
    yf = A * np.cos(w * t + ph)
    yn = -A * np.cos(ph) * np.exp(-t / tau)
    fig, ax = new_fig(6.4, 3.9)
    ax.plot(t * 1e3, 10 * np.cos(w * t), ":", color="0.4", lw=1.3, label="input 10 cos(2π·100t) V")
    ax.plot(t * 1e3, yf, "--", color=COLORS[0], lw=1.4,
            label=f"forced {A:.2f} cos(2π·100t − {np.degrees(-ph):.1f}°)")
    ax.plot(t * 1e3, yn, "-.", color=COLORS[1], lw=1.4,
            label=f"natural −{A * np.cos(ph):.2f} e$^{{-t/1\\,ms}}$")
    ax.plot(t * 1e3, yf + yn, color=COLORS[2], lw=2.4, label="total response", zorder=4)
    ax.axhline(0, color=INK, lw=0.5)
    ax.axvline(5, color="0.6", lw=0.7, ls=":")
    ax.text(5.15, 8.8, "5τ = 5 ms", fontsize=8.5, color="0.35", va="bottom")
    ax.annotate("starts at 0 V", xy=(0, 0), xytext=(0.6, -9.6), fontsize=8.5,
                color=COLORS[2], arrowprops=dict(arrowstyle="->", color=COLORS[2], lw=0.8))
    ax.set_xlim(0, 20)
    ax.set_ylim(-10, 10)
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("voltage (V)")
    ax.legend(fontsize=7.8, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.2),
              columnspacing=1.0, handlelength=2.2)
    save(fig, CH, "fig-17-5-rc-switch-on-transient")


# ------------------------------------------------------------------ 17.6
def fig_17_6():
    fig, ax = schematic(6.4, 5.0, xlim=(0, 15.2), ylim=(0, 12.5))
    bw, bh = 1.6, 1.0
    # row 1: series
    y = 11.0
    ax.text(0.1, y + 1.0, "Series (cascade)", fontsize=9, fontweight="bold")
    ax.text(0.2, y, "x", va="center", fontsize=10)
    arrow(ax, 0.6, y, 1.4, y)
    box(ax, 1.4, y - bh / 2, bw, bh, r"$h_1$", fontsize=11)
    arrow(ax, 3.0, y, 3.8, y)
    box(ax, 3.8, y - bh / 2, bw, bh, r"$h_2$", fontsize=11)
    arrow(ax, 5.4, y, 6.3, y)
    ax.text(6.4, y, "y", va="center", fontsize=10)
    ax.text(7.6, y, "≡", va="center", ha="center", fontsize=16)
    arrow(ax, 8.6, y, 9.4, y)
    box(ax, 9.4, y - 0.6, 4.2, 1.2, r"$h_1 * h_2$" + "\n" + r"($H_1H_2$)", fontsize=10, fc="#E8F2E8")
    arrow(ax, 13.6, y, 14.4, y)
    ax.text(8.5, y, "x", va="center", ha="right", fontsize=10)
    ax.text(14.5, y, "y", va="center", fontsize=10)

    # row 2: parallel
    y = 7.0
    ax.text(0.1, y + 2.0, "Parallel", fontsize=9, fontweight="bold")
    ax.text(0.2, y, "x", va="center", fontsize=10)
    line(ax, [0.6, 1.3], [y, y])
    dot(ax, 1.3, y)
    line(ax, [1.3, 1.3], [y - 1.0, y + 1.0])
    arrow(ax, 1.3, y + 1.0, 2.2, y + 1.0)
    arrow(ax, 1.3, y - 1.0, 2.2, y - 1.0)
    box(ax, 2.2, y + 1.0 - bh / 2, bw, bh, r"$h_1$", fontsize=11)
    box(ax, 2.2, y - 1.0 - bh / 2, bw, bh, r"$h_2$", fontsize=11)
    line(ax, [3.8, 4.7], [y + 1.0, y + 1.0])
    line(ax, [3.8, 4.7], [y - 1.0, y - 1.0])
    arrow(ax, 4.7, y + 1.0, 4.7, y + 0.3)
    arrow(ax, 4.7, y - 1.0, 4.7, y - 0.3)
    adder(ax, 4.7, y, signs={"n": "+", "s": "+"})
    arrow(ax, 5.0, y, 6.3, y)
    ax.text(6.4, y, "y", va="center", fontsize=10)
    ax.text(7.6, y, "≡", va="center", ha="center", fontsize=16)
    arrow(ax, 8.6, y, 9.4, y)
    box(ax, 9.4, y - 0.6, 4.2, 1.2, r"$h_1 + h_2$" + "\n" + r"($H_1+H_2$)", fontsize=10, fc="#E8F2E8")
    arrow(ax, 13.6, y, 14.4, y)
    ax.text(8.5, y, "x", va="center", ha="right", fontsize=10)
    ax.text(14.5, y, "y", va="center", fontsize=10)

    # row 3: negative feedback
    y = 3.0
    ax.text(0.1, y + 1.4, "Negative feedback", fontsize=9, fontweight="bold")
    ax.text(0.2, y, "x", va="center", fontsize=10)
    arrow(ax, 0.6, y, 1.2, y)
    adder(ax, 1.5, y, signs={"w": "+", "s": "−"})
    arrow(ax, 1.8, y, 2.6, y)
    box(ax, 2.6, y - bh / 2, bw, bh, "G", fontsize=11)
    arrow(ax, 4.2, y, 6.3, y)
    ax.text(6.4, y, "y", va="center", fontsize=10)
    dot(ax, 5.4, y)
    line(ax, [5.4, 5.4], [y, y - 1.6])
    arrow(ax, 5.4, y - 1.6, 4.2, y - 1.6)
    box(ax, 2.6, y - 1.6 - bh / 2, bw, bh, "β", fontsize=11)
    line(ax, [2.6, 1.5], [y - 1.6, y - 1.6])
    arrow(ax, 1.5, y - 1.6, 1.5, y - 0.3)
    ax.text(7.6, y, "≡", va="center", ha="center", fontsize=16)
    arrow(ax, 8.6, y, 9.4, y)
    box(ax, 9.4, y - 0.8, 4.2, 1.6, r"$\dfrac{G}{1+G\beta}$", fontsize=11, fc="#E8F2E8")
    arrow(ax, 13.6, y, 14.4, y)
    ax.text(8.5, y, "x", va="center", ha="right", fontsize=10)
    ax.text(14.5, y, "y", va="center", fontsize=10)
    ax.text(11.5, 1.3, "G = 1000, β = 0.01:\nclosed-loop gain = 1000/11 = 90.9",
            ha="center", va="top", fontsize=9, color=COLORS[0])
    ax.plot([0.1, 15.1], [8.95 + 0.6, 8.95 + 0.6], color="0.8", lw=0.6, ls="--")
    ax.plot([0.1, 15.1], [4.95, 4.95], color="0.8", lw=0.6, ls="--")
    save(fig, CH, "fig-17-6-interconnections")


if __name__ == "__main__":
    fig_17_1()
    fig_17_2()
    fig_17_3()
    fig_17_4()
    fig_17_5()
    fig_17_6()
