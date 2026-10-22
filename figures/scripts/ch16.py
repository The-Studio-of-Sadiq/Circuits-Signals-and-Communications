"""Figures for Chapter 16 — System Fundamentals.

Run from the repository root:  python figures/scripts/ch16.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Polygon, FancyBboxPatch  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")
CH = "16"
CT_C = COLORS[0]   # continuous-time signal colour
DT_C = COLORS[1]   # discrete-time signal colour


# ----------------------------------------------------------------- helpers
def adder(ax, x, y, r=0.28, signs=None, fs=8):
    """Summing junction (circle with Sigma). signs: dict position->sign text, e.g. {'w': '+'}."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, r"$\Sigma$", ha="center", va="center", fontsize=fs, zorder=4)
    off = {"w": (-r - 0.2, r + 0.1), "s": (r + 0.2, -r - 0.15), "n": (r * 0.6, r + 0.12),
           "e": (r + 0.12, r * 0.55)}
    for k, v in (signs or {}).items():
        dx, dy = off[k]
        ax.text(x + dx, y + dy, v, ha="center", va="center", fontsize=fs + 1, zorder=4)


def gain(ax, x, y, w=0.9, h=0.7, text="", fs=8, right=True, fc="#FFF4E0"):
    """Triangular gain block with its left (or right) base at x, centred vertically on y."""
    if right:
        pts = [(x, y - h / 2), (x, y + h / 2), (x + w, y)]
        tx = x + w * 0.36
    else:
        pts = [(x + w, y - h / 2), (x + w, y + h / 2), (x, y)]
        tx = x + w * 0.64
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=1.0, zorder=3))
    ax.text(tx, y, text, ha="center", va="center", fontsize=fs, zorder=4)


def line(ax, xs, ys, color=INK, lw=1.1, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", **kw)


def dot(ax, x, y, color=INK):
    ax.plot([x], [y], "o", ms=3.2, color=color, zorder=5)


# ----------------------------------------------------------------- figures
def fig_16_1():
    fig, ax = schematic(6.8, 4.6, xlim=(0, 17), ylim=(0, 11.5))
    # generic operator
    box(ax, 6.9, 9.6, 3.2, 1.2, r"$\mathcal{T}\{\cdot\}$", fc="#E8E8E8", fontsize=12)
    arrow(ax, 4.6, 10.2, 6.9, 10.2)
    arrow(ax, 10.1, 10.2, 12.4, 10.2)
    ax.text(4.5, 10.2, "x", ha="right", va="center", fontsize=11)
    ax.text(12.5, 10.2, "y", ha="left", va="center", fontsize=11)
    ax.text(8.5, 9.15, r"$y=\mathcal{T}\{x\}$: the whole input signal maps to the whole output",
            ha="center", va="top", fontsize=9, style="italic")
    ax.plot([0.3, 16.7], [8.35, 8.35], color="0.7", lw=0.6, ls="--")

    # Row 1: continuous time
    yc = 7.0
    ax.text(0.2, yc + 0.95, "continuous-time", fontsize=8.5, color="0.35")
    box(ax, 5.6, yc - 0.65, 5.8, 1.3, "RC low-pass, τ = 1 ms\nR = 10 kΩ, C = 100 nF", fontsize=8.5)
    arrow(ax, 2.6, yc, 5.6, yc, color=CT_C)
    arrow(ax, 11.4, yc, 14.4, yc, color=CT_C)
    ax.text(2.5, yc, "x(t)\nelectrode\nvoltage", ha="right", va="center", fontsize=8.5)
    ax.text(14.5, yc, "y(t)", ha="left", va="center", fontsize=9.5)

    # Row 2: discrete time
    yd = 4.6
    ax.text(0.2, yd + 0.95, "discrete-time", fontsize=8.5, color="0.35")
    box(ax, 5.6, yd - 0.65, 5.8, 1.3, "10-point moving average\n$f_s$ = 500 Hz", fontsize=8.5)
    arrow(ax, 2.6, yd, 5.6, yd, color=DT_C, ls="--")
    arrow(ax, 11.4, yd, 14.4, yd, color=DT_C, ls="--")
    ax.text(2.5, yd, "x[n]", ha="right", va="center", fontsize=9.5)
    ax.text(14.5, yd, "y[n]", ha="left", va="center", fontsize=9.5)

    # Row 3: mixed chain
    ym = 1.9
    ax.text(0.2, ym + 0.95, "mixed (sampled-data)", fontsize=8.5, color="0.35")
    labels = ["anti-alias\nfilter", "ADC\n$f_s$ = 500 Hz", "digital\nfilter", "DAC"]
    xs = [2.0, 5.6, 9.2, 12.8]
    w = 2.4
    for x0, lab in zip(xs, labels):
        box(ax, x0, ym - 0.65, w, 1.3, lab, fontsize=8.5)
    arrow(ax, 1.0, ym, xs[0], ym, color=CT_C)
    ax.text(0.95, ym, "x(t)", ha="right", va="center", fontsize=9.5)
    arrow(ax, xs[0] + w, ym, xs[1], ym, color=CT_C)
    arrow(ax, xs[1] + w, ym, xs[2], ym, color=DT_C, ls="--")
    arrow(ax, xs[2] + w, ym, xs[3], ym, color=DT_C, ls="--")
    arrow(ax, xs[3] + w, ym, 16.2, ym, color=CT_C)
    ax.text(16.25, ym, "y(t)", ha="left", va="center", fontsize=9.5)

    # legend
    ax.plot([3.5, 4.5], [0.25, 0.25], color=CT_C, lw=1.4)
    ax.text(4.65, 0.25, "continuous-time signal", va="center", fontsize=8.5, color=CT_C)
    ax.plot([9.5, 10.5], [0.25, 0.25], color=DT_C, lw=1.4, ls="--")
    ax.text(10.65, 0.25, "discrete-time signal (sequence)", va="center", fontsize=8.5, color=DT_C)
    save(fig, CH, "fig-16-1-system-block-examples")


def fig_16_2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.6), gridspec_kw=dict(width_ratios=[1, 1.05]))
    x = np.linspace(-0.3, 0.3, 301)
    a1.plot(x, 10 * x, "--", color="0.5", lw=1.2, label="linear: y = 10x")
    a1.plot(x, 10 * x + 0.5 * x ** 2, color=COLORS[0], label="y = 10x + 0.5x²")
    a1.axhline(0, color=INK, lw=0.5)
    a1.axvline(0, color=INK, lw=0.5)
    a1.set_xlabel("input x (V)")
    a1.set_ylabel("output y (V)")
    a1.set_title("Static characteristic", fontsize=10)
    a1.legend(fontsize=8, loc="upper left")
    ins = a1.inset_axes([0.58, 0.08, 0.38, 0.34])
    xi = np.linspace(0.15, 0.3, 50)
    ins.plot(xi, 10 * xi, "--", color="0.5", lw=1)
    ins.plot(xi, 10 * xi + 0.5 * xi ** 2, color=COLORS[0], lw=1.3)
    ins.set_xlim(0.25, 0.3)
    ins.set_ylim(2.45, 3.1)
    ins.tick_params(labelsize=6.5)
    ins.set_title("zoom", fontsize=7, pad=1)

    f = np.array([0, 1, 2])
    amp = np.array([0.5 * 0.5 * 0.2 ** 2, 10 * 0.2, 0.5 * 0.5 * 0.2 ** 2])
    db = 20 * np.log10(amp)
    base = -60
    a2.bar(f, db - base, bottom=base, width=0.18, color=[COLORS[1], COLORS[0], COLORS[1]])
    for fi, di, ai in zip(f, db, amp):
        a2.text(fi, di + 1.2, f"{ai:g} V\n({di:+.0f} dBV)".replace("-", "−") + "", ha="center", va="bottom", fontsize=8)
    a2.set_ylim(-60, 18)
    a2.set_yticks(range(-60, 11, 10))
    a2.set_xlim(-0.5, 2.7)
    a2.set_xticks([0, 1, 2])
    a2.set_xticklabels(["0 (DC)", "1", "2"])
    a2.set_xlabel("frequency (kHz)")
    a2.set_ylabel("output amplitude (dBV)")
    a2.set_title("Output spectrum, x = 0.2 cos(2π·1000 t)", fontsize=10)
    a2.annotate("", xy=(2.5, db[2]), xytext=(2.5, db[1]),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=8))
    a2.plot([1.1, 2.55], [db[1]] * 2, ":", color="0.5", lw=0.8)
    a2.text(2.42, (db[1] + db[2]) / 2, "HD2 = 0.5 %\n= −46 dB", ha="right", va="center", fontsize=8.5)
    fig.tight_layout(w_pad=1.5)
    save(fig, CH, "fig-16-2-quadratic-nonlinearity")


def fig_16_3():
    t = np.linspace(0, 1.2e-6, 6001)
    tus = t * 1e6
    x = ((t >= 0) & (t < 0.2e-6)).astype(float)
    xd = ((t >= 0.5e-6) & (t < 0.7e-6)).astype(float)
    lo = np.cos(2 * np.pi * 1e6 * t)
    y_del = xd * lo
    y_shift = xd * np.cos(2 * np.pi * 1e6 * (t - 0.5e-6))
    fig, axs = plt.subplots(3, 1, figsize=(6.4, 4.8), sharex=True)
    axs[0].plot(tus, x, color=COLORS[0], label="x(t)")
    axs[0].plot(tus, xd, "--", color=COLORS[1], label="x(t − 0.5 µs)")
    axs[0].legend(fontsize=8, loc="upper right", ncol=2)
    axs[0].set_title("Input pulse and delayed copy", fontsize=9.5, loc="left")
    axs[1].plot(tus, lo, ":", color="0.65", lw=0.9, label="carrier cos(2π·10⁶ t)")
    axs[1].plot(tus, y_del, color=COLORS[1])
    axs[1].set_title(r"Response to the delayed input: $x(t-0.5\,\mu s)\cos(2\pi 10^6 t)$",
                     fontsize=9.5, loc="left")
    axs[1].legend(fontsize=8, loc="lower left")
    axs[2].plot(tus, y_shift, color=COLORS[0])
    axs[2].set_title(r"Original response shifted by 0.5 µs: $y(t-0.5\,\mu s)$", fontsize=9.5, loc="left")
    for ax in axs:
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_ylim(-1.2, 1.25)
        ax.set_yticks([-1, 0, 1])
        ax.set_ylabel("V")
        ax.axvline(0.5, color="0.6", lw=0.6, ls=":")
    axs[1].plot([0.5], [-1], "o", ms=5, color=COLORS[1])
    axs[2].plot([0.5], [1], "o", ms=5, color=COLORS[0])
    axs[1].annotate("starts at −1 V", xy=(0.5, -1), xytext=(0.78, -0.75), fontsize=8.5,
                    color=COLORS[1], arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=0.8))
    axs[2].annotate("starts at +1 V:\nsign differs, so the\nmixer is time-varying",
                    xy=(0.5, 1), xytext=(0.8, 0.05), fontsize=8.5, color=COLORS[0],
                    arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=0.8))
    axs[2].set_xlabel("t (µs)")
    axs[2].set_xlim(0, 1.2)
    fig.tight_layout(h_pad=0.6)
    save(fig, CH, "fig-16-3-mixer-time-variance")


def fig_16_4():
    t = np.linspace(0, 10, 1001)
    fig, ax = new_fig(6.4, 3.8)
    ax.plot(t, np.ones_like(t), ":", color="0.35", lw=1.4, label="input: 1 mV constant offset")
    ax.plot(t, 1 - np.exp(-t / 1.0), color=COLORS[0],
            label="A: RC low-pass, τ = 1 s (mV) — stable")
    ax.plot(t, t, color=COLORS[1], label="B: ideal integrator (mV·s) — unstable")
    ax.plot(t, 3 * (1 - np.exp(-t / 3.0)), color=COLORS[2],
            label="C: leaky integrator, τ = 3 s (mV·s) — leaky (stable)")
    ax.text(8.6, 9.7, "grows without bound", ha="right", va="top", fontsize=8.5, color=COLORS[1])
    ax.text(9.9, 3.15, "settles at 3 mV·s", ha="right", va="bottom", fontsize=8.5, color=COLORS[2])
    ax.text(9.9, 1.12, "settles at 1 mV", ha="right", va="bottom", fontsize=8.5, color=COLORS[0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("output (mV or mV·s, per curve)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, lw=0.5)
    save(fig, CH, "fig-16-4-stable-vs-unstable")


def _rc_circuit(ax, x0, y0):
    """Draw the RC low-pass with schemdraw onto ax, lower-left corner at (x0, y0)."""
    d = schemdraw.Drawing(canvas=ax, show=False, unit=2.6, fontsize=8.5, lw=1.1)
    d.move(x0, y0)
    src = d.add(elm.SourceV().up())
    d.add(elm.Resistor().right().label("R = 10 kΩ", ofst=0.12))
    top = d.here
    d.add(elm.Line().right(3.4))
    t_out = d.add(elm.Dot(open=True))
    d.add(elm.Capacitor().down().at(top).label("C =\n100 nF", loc="bottom", ofst=0.15))
    bot = d.here
    d.add(elm.Line().left().tox(src.start))
    d.add(elm.Line().right(3.4).at(bot))
    d.add(elm.Dot(open=True))
    d.draw(show=False)
    xs, ys = src.center
    ax.text(xs - 0.75, ys, "x(t)", ha="right", va="center", fontsize=9)
    xo = t_out.center[0] + 0.3
    ax.text(xo, ys + 0.75, "+", ha="left", va="center", fontsize=9)
    ax.text(xo, ys, "y(t)", ha="left", va="center", fontsize=9)
    ax.text(xo, ys - 0.75, "−", ha="left", va="center", fontsize=9)
    return d


def fig_16_5():
    fig, ax = schematic(6.8, 4.9, xlim=(0, 20), ylim=(0, 14.3))
    _rc_circuit(ax, 7.4, 5.3)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(10.6, 4.8, "RC low-pass, τ = RC = 1 ms", ha="center", va="center", fontsize=8.5,
            style="italic")

    def panel(x, y, w, h, title):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.2",
                                    fc="#F5F8FB", ec="0.55", lw=0.8))
        ax.text(x + 0.2, y + h - 0.2, title, ha="left", va="top", fontsize=8, fontweight="bold")

    # (1) differential equation
    panel(0.1, 10.1, 5.9, 4.1, "(1) Differential eq.")
    ax.text(3.05, 11.9, r"$\tau\,\dfrac{dy}{dt}+y=x$", ha="center", va="center", fontsize=12)
    ax.text(3.0, 10.6, "τ = 1 ms", ha="center", va="center", fontsize=8.5)

    # (2) block diagram
    panel(6.2, 10.1, 7.4, 4.1, "(2) Block diagram")
    yb = 12.2
    ax.text(6.45, yb, "x", va="center", fontsize=9)
    arrow(ax, 6.85, yb, 7.6, yb)
    adder(ax, 7.92, yb, r=0.32, signs={"w": "+", "s": "−"})
    arrow(ax, 8.24, yb, 8.7, yb)
    box(ax, 8.7, yb - 0.45, 1.2, 0.9, "1/τ", fontsize=8.5, fc="#FFF4E0")
    arrow(ax, 9.9, yb, 10.4, yb)
    box(ax, 10.4, yb - 0.45, 1.0, 0.9, r"$\int$", fontsize=11, fc="white")
    arrow(ax, 11.4, yb, 13.0, yb)
    ax.text(13.05, yb, "y", va="center", fontsize=9)
    dot(ax, 12.3, yb)
    line(ax, [12.3, 12.3, 7.92], [yb, 10.75, 10.75])
    arrow(ax, 7.92, 10.75, 7.92, yb - 0.32)
    ax.text(10.1, 10.85, "feedback −1", fontsize=7.5, ha="center", va="bottom", color="0.3")

    # (3) state space
    panel(13.9, 10.1, 6.0, 4.1, "(3) State space")
    ax.text(16.9, 12.75, r"$\dot q = A q + B x$", ha="center", va="center", fontsize=9.5)
    ax.text(16.9, 12.05, r"$y = C q + D x$", ha="center", va="center", fontsize=9.5)
    ax.text(16.9, 10.95, "A = −1000 s⁻¹, B = 1000 s⁻¹\nC = 1, D = 0", ha="center", va="center",
            fontsize=8)

    # (4) impulse response
    panel(0.1, 0.1, 7.2, 4.4, "(4) Impulse response")
    axh = ax.inset_axes([1.65, 1.15, 5.3, 2.5], transform=ax.transData)
    th = np.linspace(0, 5, 400)
    axh.plot(th, 1000 * np.exp(-th), color=COLORS[0], lw=1.4)
    axh.set_xlim(0, 5)
    axh.set_ylim(0, 1100)
    axh.set_yticks([0, 500, 1000])
    axh.set_facecolor("none")
    axh.set_xlabel("t (ms)", fontsize=7.5, labelpad=1)
    axh.set_ylabel("h (s⁻¹)", fontsize=7.5, labelpad=1)
    axh.tick_params(labelsize=7, pad=1)
    axh.text(1.3, 750, r"$h(t)=1000\,e^{-1000t}$", fontsize=8.5)

    # (5) difference equation
    panel(7.7, 0.1, 12.2, 4.4, "(5) Exact sampled model, T = 0.1 ms")
    ax.text(13.8, 3.45, "y[n] = 0.9048 y[n−1] + 0.0952 x[n−1]", ha="center", va="center",
            fontsize=8.5)
    yb = 2.3
    ax.text(7.95, yb, "x[n]", va="center", fontsize=8.5)
    arrow(ax, 9.05, yb, 9.5, yb)
    box(ax, 9.5, yb - 0.4, 1.1, 0.8, r"$z^{-1}$", fontsize=9, fc="white")
    arrow(ax, 10.6, yb, 11.0, yb)
    box(ax, 11.0, yb - 0.4, 1.7, 0.8, "×0.0952", fontsize=8, fc="#FFF4E0")
    arrow(ax, 12.7, yb, 13.48, yb)
    adder(ax, 13.8, yb, r=0.32, signs={"w": "+", "s": "+"})
    arrow(ax, 14.12, yb, 18.5, yb)
    ax.text(18.6, yb, "y[n]", va="center", fontsize=8.5)
    dot(ax, 17.6, yb)
    line(ax, [17.6, 17.6], [yb, 0.95])
    arrow(ax, 17.6, 0.95, 17.0, 0.95)
    box(ax, 15.9, 0.55, 1.1, 0.8, r"$z^{-1}$", fontsize=9, fc="white")
    arrow(ax, 15.9, 0.95, 15.6, 0.95)
    box(ax, 13.9, 0.55, 1.7, 0.8, "×0.9048", fontsize=8, fc="#FFF4E0")
    line(ax, [13.9, 13.8], [0.95, 0.95])
    arrow(ax, 13.8, 0.95, 13.8, yb - 0.32)

    # derivation arrows from the circuit
    pairs = [((7.9, 9.0), (3.0, 10.1)), ((12.9, 9.3), (12.2, 10.1)), ((15.2, 8.9), (16.9, 10.1)),
             ((7.6, 6.0), (3.7, 4.5)), ((15.6, 5.8), (16.6, 4.5))]
    for (x0, y0), (x1, y1) in pairs:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="0.5", lw=0.9, ls="--",
                                    mutation_scale=9, shrinkA=0, shrinkB=2))
    save(fig, CH, "fig-16-5-rc-five-representations")


if __name__ == "__main__":
    fig_16_1()
    fig_16_2()
    fig_16_3()
    fig_16_4()
    fig_16_5()
