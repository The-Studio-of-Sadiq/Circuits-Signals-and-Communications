"""Figures for Chapter 15 — Signal Fundamentals.

Run from the repository root:  python figures/scripts/ch15.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset  # noqa: E402

CH = "15"


def _stem(ax, n, x, color=COLORS[0], ms=3.5, lw=1.0, base=True, label=None):
    """Plain stem plot with small markers."""
    ml, sl, bl = ax.stem(n, x, linefmt="-", markerfmt="o", basefmt=" ", label=label)
    plt.setp(sl, color=color, lw=lw)
    plt.setp(ml, color=color, ms=ms)
    if base:
        ax.axhline(0, color=INK, lw=0.6)
    return ml


def busbar(t):
    """Busbar voltage (V) with harmonics and a capacitor-switching transient at 25 ms."""
    v = (325 * np.sin(2 * np.pi * 50 * t) + 16.3 * np.sin(2 * np.pi * 250 * t)
         + 9.8 * np.sin(2 * np.pi * 350 * t))
    t0 = 25e-3
    tr = 200 * np.exp(-(t - t0) / 4e-3) * np.cos(2 * np.pi * 650 * (t - t0))
    return v + np.where(t >= t0, tr, 0.0)


def fig_15_1():
    t = np.linspace(0, 60e-3, 12001)
    v = busbar(t)
    fs = 2000.0
    n = np.arange(0, 121)
    vn = busbar(n / fs)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1, 1.45]))
    a1.plot(t * 1e3, v, color=COLORS[0], lw=1.3)
    a1.axhline(0, color=INK, lw=0.6)
    a1.axvline(25, color="0.5", ls=":", lw=0.9)
    ipk = np.argmax(v)
    a1.annotate(f"peak {v[ipk]:.0f} V ≈ {v[ipk] / 325:.2f} p.u.", xy=(t[ipk] * 1e3, v[ipk]),
                xytext=(33, 520), fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8, color=INK))
    a1.text(25.4, -560, "capacitor switched\nat t = 25 ms", fontsize=8.5, va="bottom")
    a1.set_ylim(-650, 650)
    a1.set_ylabel("v(t) (V)")
    a1.set_title("Continuous time: 325 V peak, 50 Hz + 5 % 5th + 3 % 7th, 650 Hz transient", fontsize=9.5)

    ml = _stem(a2, n / fs * 1e3, vn, ms=2.4, lw=0.8)
    a2.plot(t * 1e3, v, color="0.75", lw=0.6, zorder=0)
    a2.set_ylim(-600, 1350)
    a2.set_yticks([-500, -250, 0, 250, 500])
    a2.set_ylabel("x[n] = v(nT$_s$) (V)")
    a2.set_xlabel("t (ms)")
    a2.set_xlim(0, 60)
    a2.set_title("Discrete time: sampled at f$_s$ = 2 kHz (T$_s$ = 0.5 ms)", fontsize=9.5)
    sec = a2.secondary_xaxis("top", functions=(lambda x: x * fs / 1e3, lambda m: m * 1e3 / fs))
    sec.set_xlabel("sample index n", fontsize=9, labelpad=2)
    sec.set_xticks(np.arange(0, 121, 20))
    sec.tick_params(labelsize=8)

    ax_in = inset_axes(a2, width="44%", height="36%", loc="upper right", borderpad=0.3)
    sel = (n >= 46) & (n <= 64)
    _stem(ax_in, n[sel], vn[sel], ms=2.6, lw=0.8)
    tt = np.linspace(46 / fs, 64 / fs, 800)
    ax_in.plot(tt * fs, busbar(tt), color="0.7", lw=0.6, zorder=0)
    ax_in.set_xlim(45.5, 64.5)
    ax_in.set_xticks([50, 55, 60])
    ax_in.tick_params(labelsize=7)
    ax_in.set_yticks([0, 400])
    ax_in.text(0.98, 0.95, "zoom: n = 46 … 64", transform=ax_in.transAxes, ha="right", va="top",
               fontsize=7.5)
    ax_in.set_ylim(-450, 650)
    from matplotlib.patches import Rectangle
    a2.add_patch(Rectangle((23, -450), 9, 1050, fill=False, ec="0.4", lw=0.7, ls="--"))
    a2.annotate("", xy=(0.56, 0.62), xycoords="axes fraction", xytext=(31, 600), textcoords="data",
                arrowprops=dict(arrowstyle="->", lw=0.7, color="0.4"))
    for s in ("top", "right"):
        ax_in.spines[s].set_visible(True)
    fig.subplots_adjust(hspace=0.45, left=0.12, right=0.97, top=0.94, bottom=0.09)
    save(fig, CH, "fig-15-1-ct-and-dt-power-quality")


def fig_15_2():
    n = np.arange(0, 61)
    t = np.linspace(0, 60, 2000)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.8), sharex=True)

    a1.plot(t, np.cos(0.3 * np.pi * t), ":", color="0.45", lw=1.0)
    _stem(a1, n, np.cos(0.3 * np.pi * n), ms=3)
    for k in range(3):
        x0, x1 = 20 * k, 20 * (k + 1)
        y = 1.32
        a1.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="|-|", lw=0.9, color=COLORS[1], mutation_scale=4))
        a1.text((x0 + x1) / 2, y + 0.05, "N = 20 (3 cycles)", ha="center", va="bottom",
                fontsize=8, color=COLORS[1])
    a1.set_ylim(-1.2, 1.6)
    a1.set_yticks([-1, 0, 1])
    a1.set_ylabel(r"$\cos(0.3\pi n)$")
    a1.set_title(r"$\Omega_0/2\pi = 3/20$: periodic, N = 20", fontsize=9.5, loc="left")

    a2.plot(t, np.cos(0.3 * t), ":", color="0.45", lw=1.0)
    _stem(a2, n, np.cos(0.3 * n), ms=3, color=COLORS[2])
    for k in (0, 21, 42):
        a2.plot([k], [np.cos(0.3 * k)], "s", ms=7, mfc="none", mec=COLORS[1], mew=1.2)
    vals = ", ".join(f"{np.cos(0.3 * k):.5f}" for k in (0, 21, 42))
    a2.text(30, 1.66, f"n = 0, 21, 42: {vals} — close, never equal; values drift\n"
            r"(envelope period $2\pi/0.3$ = 20.94 samples; $\Omega_0/2\pi$ irrational)",
            ha="center", va="top", fontsize=8, color=COLORS[1])
    a2.set_ylim(-1.2, 1.7)
    a2.set_yticks([-1, 0, 1])
    a2.set_ylabel(r"$\cos(0.3 n)$")
    a2.set_xlabel("n")
    a2.set_xlim(-1, 61)
    a2.set_title(r"$\Omega_0/2\pi = 0.3/2\pi$: not periodic", fontsize=9.5, loc="left")
    fig.tight_layout()
    save(fig, CH, "fig-15-2-discrete-sinusoid-periodicity")


def fig_15_3():
    t_neg = np.linspace(-4, 0, 400, endpoint=False)
    t_pos = np.linspace(0, 4, 400)
    fig, axs = plt.subplots(3, 1, figsize=(6.4, 5.0), sharex=True)
    specs = [
        (np.zeros_like(t_neg), np.exp(-t_pos), r"$x(t)=e^{-t}u(t)$", "E = 0.5"),
        (0.5 * np.exp(t_neg), 0.5 * np.exp(-t_pos), r"$x_e(t)=\frac{1}{2}e^{-|t|}$", "E = 0.25"),
        (-0.5 * np.exp(t_neg), 0.5 * np.exp(-t_pos), r"$x_o(t)=\frac{1}{2}\,\mathrm{sgn}(t)\,e^{-|t|}$",
         "E = 0.25"),
    ]
    for ax, (yn, yp, lab, en), c in zip(axs, specs, COLORS):
        ax.plot(t_neg, yn, color=c)
        ax.plot(t_pos, yp, color=c)
        ax.plot([0, 0], [yn[-1], yp[0]], ":", color=c, lw=1.0)
        ax.axhline(0, color=INK, lw=0.6)
        ax.axvline(0, color="0.6", lw=0.6)
        ax.set_ylim(-0.6, 1.1)
        ax.set_yticks([-0.5, 0, 0.5, 1])
        ax.text(-3.9, 0.95, lab, fontsize=10, va="top")
        ax.text(3.9, 0.95, en, fontsize=9.5, va="top", ha="right",
                bbox=dict(fc="white", ec="0.7", lw=0.6, boxstyle="round,pad=0.25"))
    axs[-1].set_xlabel("t (s)")
    axs[-1].set_xlim(-4, 4)
    axs[1].set_ylabel("amplitude")
    fig.tight_layout()
    save(fig, CH, "fig-15-3-even-odd-decomposition")


def fig_15_4():
    fig, axs = plt.subplots(2, 4, figsize=(6.8, 4.4))
    t = np.linspace(-1, 4, 2001)
    u = (t >= 0).astype(float)
    # (a) step
    ax = axs[0, 0]
    ax.plot(t[t < 0], 0 * t[t < 0], color=COLORS[0])
    ax.plot(t[t >= 0], u[t >= 0], color=COLORS[0])
    ax.plot([0, 0], [0, 1], ":", color=COLORS[0], lw=1)
    ax.set_title("(a) u(t)", fontsize=9.5)
    ax.set_ylim(-0.3, 1.4)
    # (b) pulses converging to delta
    ax = axs[0, 1]
    for w, c in zip([1, 0.5, 0.25], COLORS[:3]):
        ax.plot([-1, 0, 0, w, w, 4], [0, 0, 1 / w, 1 / w, 0, 0], color=c, lw=1.2,
                label=f"width {w:g}, height {1 / w:g}")
    ax.annotate("", xy=(0, 5.4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=INK, mutation_scale=10))
    ax.text(0.35, 5.2, r"$\delta(t)$, area 1", fontsize=8.5)
    ax.text(1.3, 3.3, "w = 1, ½, ¼\nh = 1, 2, 4\n(area 1)", fontsize=7.5, color="0.3")
    ax.set_title(r"(b) pulses $\rightarrow\delta(t)$", fontsize=9.5)
    ax.set_ylim(-0.3, 6)
    # (c) ramp
    ax = axs[0, 2]
    ax.plot(t, t * u, color=COLORS[0])
    ax.set_title("(c) t u(t)", fontsize=9.5)
    ax.set_ylim(-0.3, 4.2)
    # (d) damped sinusoid
    ax = axs[0, 3]
    env = np.exp(-0.5 * t) * u
    ax.plot(t, env * np.cos(2 * np.pi * t), color=COLORS[0], lw=1.3)
    ax.plot(t[t >= 0], env[t >= 0], "--", color=COLORS[1], lw=1)
    ax.plot(t[t >= 0], -env[t >= 0], "--", color=COLORS[1], lw=1)
    ax.set_title(r"(d) $e^{-0.5t}\cos 2\pi t\,u(t)$", fontsize=9.5)
    ax.set_ylim(-1.1, 1.2)
    for ax in axs[0]:
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_xlim(-1, 4)
        ax.set_xticks([0, 2, 4])
        ax.set_xlabel("t (s)", fontsize=9, labelpad=1)

    n = np.arange(-5, 21)
    un = (n >= 0).astype(float)
    ax = axs[1, 0]
    _stem(ax, n, un, ms=2.4, lw=0.8)
    ax.set_title("(e) u[n]", fontsize=9.5)
    ax.set_ylim(-0.3, 1.4)
    ax = axs[1, 1]
    _stem(ax, n, (n == 0).astype(float), ms=2.4, lw=0.8)
    ax.set_title(r"(f) $\delta[n]$", fontsize=9.5)
    ax.set_ylim(-0.3, 1.4)
    ax = axs[1, 2]
    _stem(ax, n, n * un, ms=2.4, lw=0.8)
    ax.set_title("(g) n u[n]", fontsize=9.5)
    ax.set_ylim(-1, 21)
    ax = axs[1, 3]
    _stem(ax, n, 0.9 ** np.maximum(n, 0) * un, ms=2.4, lw=0.8, label=r"$0.9^n u[n]$")
    _stem(ax, n + 0.25, (-0.8) ** np.maximum(n, 0) * un, color=COLORS[1], ms=2.4, lw=0.8,
          label=r"$(-0.8)^n u[n]$")
    ax.set_title(r"(h) $a^n u[n]$", fontsize=9.5)
    ax.set_ylim(-1.1, 1.6)
    ax.legend(fontsize=7, loc="upper right", handlelength=1, borderpad=0.1, labelspacing=0.2)
    for ax in axs[1]:
        ax.set_xlim(-5.5, 20.5)
        ax.set_xticks([0, 10, 20])
        ax.set_xlabel("n", fontsize=9, labelpad=1)
    for ax in axs.flat:
        ax.tick_params(labelsize=8)
    fig.text(0.005, 0.74, "continuous time", rotation=90, va="center", fontsize=9, color="0.35")
    fig.text(0.005, 0.27, "discrete time", rotation=90, va="center", fontsize=9, color="0.35")
    fig.tight_layout(rect=(0.02, 0, 1, 1), w_pad=0.6, h_pad=1.0)
    save(fig, CH, "fig-15-4-elementary-signals")


def _pulse(tau):
    """x(tau): 1 on [0, 2], linear fall to 0 at 3."""
    return np.clip(np.where(tau < 0, 0, np.where(tau <= 2, 1, 3 - tau)), 0, 1)


def fig_15_5():
    t = np.linspace(-4, 7, 4401)
    rows = [
        ("x(t)", _pulse(t), [0, 2, 3], False),
        ("x(t − 3)", _pulse(t - 3), [3, 5, 6], False),
        ("x(2t)", _pulse(2 * t), [0, 1, 1.5], False),
        ("x(2t − 3)", _pulse(2 * t - 3), [1.5, 2.5, 3], True),
        ("x(−t)", _pulse(-t), [-3, -2, 0], False),
    ]
    fig, axs = plt.subplots(5, 1, figsize=(6.4, 5.2), sharex=True)
    for ax, (lab, y, bps, hl) in zip(axs, rows):
        c = COLORS[1] if hl else COLORS[0]
        ax.fill_between(t, y, color=c, alpha=0.18 if hl else 0.10, lw=0)
        ax.plot(t, y, color=c, lw=2.2 if hl else 1.6)
        for b in bps:
            ax.axvline(b, color="0.55", ls=":", lw=0.9)
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_ylim(0, 1.3)
        ax.set_yticks([0, 1])
        ax.text(-3.9, 0.95, lab, fontsize=10, va="top", color=c,
                fontweight="bold" if hl else "normal")
        right = bps[-1] < 4
        ax.text(6.95 if right else -3.9, 0.5,
                "breakpoints " + ", ".join(f"{b:g}" for b in bps) + " s",
                fontsize=8, ha="right" if right else "left", va="top", color="0.35")
    axs[3].text(-3.9, 0.55, "correct result:\nshift by 3, then scale by 2", fontsize=8.5,
                color=COLORS[1], va="top", ha="left")
    axs[-1].set_xlabel("t (s)")
    axs[-1].set_xlim(-4, 7)
    axs[-1].set_xticks(range(-4, 8))
    fig.tight_layout(h_pad=0.4)
    save(fig, CH, "fig-15-5-shift-scale-pulse")


def fig_15_6():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 5.0))
    # (a) addition
    ax = axs[0, 0]
    t = np.linspace(0, 40e-3, 4001)
    v1 = 325 * np.sin(2 * np.pi * 50 * t)
    v5 = 16.3 * np.sin(2 * np.pi * 250 * t)
    ax.plot(t * 1e3, v1, color=COLORS[0], lw=1.0, label="325 sin(2π·50t)")
    ax.plot(t * 1e3, v5, color=COLORS[2], lw=1.0, label="16.3 sin(2π·250t)")
    ax.plot(t * 1e3, v1 + v5, color=COLORS[1], lw=1.6, label="sum")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("V")
    ax.set_ylim(-420, 520)
    ax.set_title("(a) addition", fontsize=9.5)
    ax.legend(fontsize=7, loc="upper center", ncol=3, handlelength=1.2, columnspacing=0.7)
    # (b) AM
    ax = axs[0, 1]
    t = np.linspace(0, 4e-3, 8001)
    m = 1 + 0.5 * np.cos(2 * np.pi * 1e3 * t)
    car = np.cos(2 * np.pi * 20e3 * t)
    ax.plot(t * 1e3, m * car, color=COLORS[0], lw=0.7, label="AM product")
    ax.plot(t * 1e3, m, "--", color=COLORS[1], lw=1.3, label="1 + 0.5 cos(2π·1 kHz t)")
    ax.plot(t * 1e3, -m, "--", color=COLORS[1], lw=1.3)
    ax.plot(t * 1e3, -2.25 + 0.3 * car, color="0.45", lw=0.6)
    ax.text(2.0, -2.62, "carrier 20 kHz (×0.3, offset)", fontsize=7.5, ha="center", va="top",
            color="0.35")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("amplitude")
    ax.set_ylim(-3.0, 2.3)
    ax.set_yticks([-1, 0, 1])
    ax.set_title("(b) multiplication (AM, 20 kHz carrier)", fontsize=9.5)
    ax.legend(fontsize=7, loc="upper center", ncol=2, handlelength=1.2, columnspacing=0.7)
    # (c) differentiation
    ax = axs[1, 0]
    t = np.linspace(-1, 3, 4001)
    edge = np.clip(t, 0, 1)
    der = ((t >= 0) & (t < 1)).astype(float)
    ax.plot(t, edge, color=COLORS[0], label="edge x(t), t$_r$ = 1 ns")
    ax.plot(t, der, color=COLORS[1], lw=1.4, ls="--", label="dx/dt (per ns)")
    ax.set_xlabel("t (ns)")
    ax.set_ylabel("x(t);  dx/dt (ns$^{-1}$)")
    ax.set_ylim(-0.1, 1.45)
    ax.set_title("(c) differentiation", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper right")
    # (d) running sum
    ax = axs[1, 1]
    n = np.arange(-2, 11)
    x = ((n >= 0) & (n <= 4)).astype(float)
    y = np.cumsum(x)
    _stem(ax, n - 0.12, x, ms=3, label="x[n]")
    _stem(ax, n + 0.12, y, color=COLORS[1], ms=3, label=r"$\sum_{k\leq n} x[k]$")
    ax.set_xlabel("n")
    ax.set_ylim(-0.2, 6.4)
    ax.set_title("(d) running sum", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper left")
    for ax in axs.flat:
        ax.tick_params(labelsize=8)
    fig.tight_layout()
    save(fig, CH, "fig-15-6-signal-operations")


if __name__ == "__main__":
    fig_15_1()
    fig_15_2()
    fig_15_3()
    fig_15_4()
    fig_15_5()
    fig_15_6()
