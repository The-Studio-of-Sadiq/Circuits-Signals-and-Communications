"""Figures for Chapter 7 — Second-Order Circuits.

Run from the repository root:  python figures/scripts/ch07.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Wedge  # noqa: E402
from scipy.linalg import expm  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import COLORS, INK, new_fig, save  # noqa: E402

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

GREY = "#666666"


# ----------------------------------------------------------------------------- helpers
def drawing(ax, unit=2.0, fontsize=9):
    """A schemdraw Drawing that renders onto the matplotlib axis ax."""
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(unit=unit, fontsize=fontsize, lw=1.2, font="DejaVu Sans")
    return d


def finish(d, ax, pad=0.4, xlim=None, ylim=None):
    """Draw d on ax, then give ax equal aspect, no frame and limits around the drawing."""
    d.draw(show=False)
    bb = d.get_bbox()
    ax.set_xlim(*(xlim or (bb.xmin - pad, bb.xmax + pad)))
    ax.set_ylim(*(ylim or (bb.ymin - pad, bb.ymax + pad)))
    ax.set_aspect("equal")
    ax.axis("off")


# series RLC of Sections 7.4-7.6
L_S, C_S, V0 = 10e-3, 1e-6, 10.0
W0 = 1 / np.sqrt(L_S * C_S)  # 10 000 rad/s


def series_natural(R, t):
    """Capacitor voltage of the series RLC released with v_C = V0, i = 0 (exact, all three cases)."""
    a = R / (2 * L_S)
    if np.isclose(a, W0):
        return V0 * (1 + a * t) * np.exp(-a * t)
    if a > W0:
        r = np.sqrt(a * a - W0 * W0)
        s1, s2 = -a + r, -a - r
        A1 = -s2 * V0 / (s1 - s2)
        return A1 * np.exp(s1 * t) + (V0 - A1) * np.exp(s2 * t)
    wd = np.sqrt(W0 * W0 - a * a)
    return np.exp(-a * t) * (V0 * np.cos(wd * t) + a * V0 / wd * np.sin(wd * t))


# ----------------------------------------------------------------------------- Figure 7.1
def fig_7_1():
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.1))
    # series RLC
    ax = axs[0]
    d = drawing(ax, unit=2.0, fontsize=9)
    d += (src := elm.SourceV().up().length(3.2).label("$v_s(t)$", loc="top"))
    d += (sw := elm.Switch(action="close").right().length(1.6).label("$t$ = 0", loc="top"))
    d += (r := elm.Resistor().right().length(1.8).label("$R$", loc="top"))
    d += (ind := elm.Inductor2(loops=3).right().length(1.8).label("$L$", loc="top"))
    d += (cap := elm.Capacitor().down().length(3.2).label("$C$", loc="bottom"))
    d += (bot := elm.Line().left().length(5.2))
    d += elm.LoopCurrent([r, cap, bot, src], direction="cw", pad=0.9).label("$i(t)$")
    finish(d, ax, xlim=(-1.9, 7.2), ylim=(-1.7, 4.4))
    ax.text(4.9, 1.6, "+\n$v_C$\n−", ha="right", va="center", fontsize=9, color=COLORS[0], linespacing=1.3)
    ax.text(2.6, -0.5, "e.g. $R$ = 50–500 Ω, $L$ = 10 mH, $C$ = 1 µF", ha="center", va="top",
            fontsize=8, color=GREY)
    ax.set_title("(a) series RLC, voltage-source driven", fontsize=9.5, pad=2)
    # parallel RLC
    ax = axs[1]
    d = drawing(ax, unit=2.0, fontsize=9)
    H = 3.2
    d += elm.SourceI().up().length(H).label("$i_s(t)$", loc="top")
    d += elm.Line().right().length(1.8)
    d += (n1 := elm.Dot())
    d += elm.Line().right().length(1.6)
    d += (n2 := elm.Dot())
    d += elm.Line().right().length(1.6)
    d += elm.Resistor().at(n1.center).down().length(H).label("$R$", loc="bottom")
    d += elm.Dot()
    d += (w := elm.Line().at(n2.center).down().length(0.8))
    d += elm.CurrentLabelInline(direction="in", ofst=0.0).at(w).label("$i_L$", loc="bottom")
    d += elm.Inductor2(loops=3).down().length(H - 0.8).label("$L$", loc="bottom")
    d += elm.Dot()
    d += elm.Capacitor().at((5.0, H)).down().length(H).label("$C$", loc="bottom")
    d += elm.Line().left().length(5.0)
    d += elm.Ground().at((2.5, 0))
    finish(d, ax, xlim=(-1.9, 7.2), ylim=(-1.7, 4.4))
    ax.text(2.6, H + 0.2, "$v(t)$", ha="center", va="bottom", fontsize=9.5, color=COLORS[0])
    ax.text(2.6, -0.85, "e.g. $R$ = 10 kΩ, $L$ = 100 µH, $C$ = 10 nF", ha="center", va="top",
            fontsize=8, color=GREY)
    ax.set_title("(b) parallel RLC, current-source driven", fontsize=9.5, pad=2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.01, wspace=0.05)
    save(fig, "07", "fig-7-1-series-parallel-rlc")


# ----------------------------------------------------------------------------- Figure 7.2
def fig_7_2():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    k = 1e-3  # plot in units of 1000 1/s
    w0 = W0
    # underdamped region shading (inside the circle, left half-plane)
    ax.add_patch(Wedge((0, 0), w0 * k, 90, 270, fc=COLORS[5], alpha=0.12, ec="none"))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(w0 * k * np.cos(th), w0 * k * np.sin(th), color=GREY, ls="--", lw=0.9)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    # locus
    R = np.linspace(0, 500, 4001)
    a = R / (2 * L_S)
    cplx = a <= w0
    ac = a[cplx]
    wd = np.sqrt(w0 ** 2 - ac ** 2)
    for sgn in (1, -1):
        ax.plot(-ac * k, sgn * wd * k, color=COLORS[0], lw=2.2)
    ar = a[~cplx]
    rr = np.sqrt(ar ** 2 - w0 ** 2)
    ax.plot((-ar + rr) * k, 0 * ar, color=COLORS[1], lw=2.6)
    ax.plot((-ar - rr) * k, 0 * ar, color=COLORS[1], lw=2.6)
    # arrows showing increasing R
    for sgn in (1, -1):
        p0 = np.array([-np.sin(0.30) * w0 * k, sgn * np.cos(0.30) * w0 * k])
        p1 = np.array([-np.sin(0.42) * w0 * k, sgn * np.cos(0.42) * w0 * k])
        ax.annotate("", p1, p0, arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=12))
    ax.annotate("", (-5.0, 0), (-7.0, 0), arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.6, mutation_scale=12))
    ax.annotate("", (-30.0, 0), (-25.0, 0), arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.6, mutation_scale=12))
    # marked points
    pts = [((0, 10.0), "$R$ = 0: ±$j$10 000", (0.6, 10.6), "left"),
           ((-2.5, 9.682), "$R$ = 50 Ω, $\\zeta$ = 0.25\n−2500 ± $j$9682", (-15.5, 9.8), "left"),
           ((-10.0, 0), "$R$ = 200 Ω (critical)\ndouble root −10 000", (-21.5, 3.0), "left"),
           ((-2.087, 0), "$R$ = 500 Ω: −2087", (1.0, -2.6), "left"),
           ((-47.913, 0), "$R$ = 500 Ω: −47 913", (-49.5, -3.0), "left")]
    for (x, y), txt, (tx, ty), ha in pts:
        ax.plot(x, y, "o", color=INK, ms=5, zorder=6)
        if y > 0:
            ax.plot(x, -y, "o", color=INK, ms=5, zorder=6)
        ax.annotate(txt, (x, y), xytext=(tx, ty), fontsize=8, ha=ha, va="center", color=INK,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    # angle theta
    zeta = 0.25
    ang = np.degrees(np.arccos(zeta))
    ax.plot([0, -2.5], [0, 9.682], color=COLORS[2], lw=1.0)
    ax.add_patch(Arc((0, 0), 6, 6, theta1=180 - ang, theta2=180, color=COLORS[2], lw=1.0))
    ax.text(-3.6, 1.4, "$\\theta$", color=COLORS[2], fontsize=10, ha="center", va="center")
    ax.text(-11.0, -6.8, "$\\cos\\theta = \\zeta$,  radius $\\omega_0$ = 10 000 rad/s", color=COLORS[2], fontsize=8.5, ha="right")
    ax.text(-6.2, 5.6, "underdamped", color=COLORS[0], fontsize=8.5, ha="center", rotation=0)
    ax.text(-40, 1.2, "overdamped (real roots)", color=COLORS[1], fontsize=8.5, ha="center", va="bottom")
    ax.set_xlim(-50, 2)
    ax.set_ylim(-12, 12)
    ax.set_aspect("equal")
    ax.set_xticks([-50, -40, -30, -20, -10, 0])
    ax.set_yticks([-10, -5, 0, 5, 10])
    ax.set_xlabel("$\\sigma$ (×1000 s$^{-1}$)")
    ax.set_ylabel("$j\\omega$ (×1000 rad/s)")
    ax.set_title("Roots of $s^2 + (R/L)s + 1/(LC)$ = 0,  $L$ = 10 mH, $C$ = 1 µF", fontsize=9.5)
    save(fig, "07", "fig-7-2-root-locus-vs-r")


# ----------------------------------------------------------------------------- Figure 7.3
def fig_7_3():
    fig, ax = new_fig(6.4, 4.0)
    t = np.linspace(0, 3e-3, 6001)
    tm = t * 1e3
    cases = [(500, "$R$ = 500 Ω, overdamped ($\\zeta$ = 2.5)", COLORS[1], 2.23),
             (200, "$R$ = 200 Ω, critically damped ($\\zeta$ = 1)", COLORS[2], 0.66),
             (50, "$R$ = 50 Ω, underdamped ($\\zeta$ = 0.25)", COLORS[0], None)]
    for R, lab, col, tx in cases:
        ax.plot(tm, series_natural(R, t), color=col, label=lab)
        if tx:
            ax.plot(tx, 0.1, "o", color=col, ms=5, zorder=5)
    env = 10.33 * np.exp(-2500 * t)
    ax.plot(tm, env, color=COLORS[0], ls="--", lw=0.9)
    ax.plot(tm, -env, color=COLORS[0], ls="--", lw=0.9)
    ax.text(1.05, 1.75, "envelope ±10.33 $e^{-2500t}$", color=COLORS[0], fontsize=8, ha="left")
    ax.axhline(0.1, color=GREY, ls=":", lw=0.8)
    ax.axhline(-0.1, color=GREY, ls=":", lw=0.8)
    ax.axhline(0, color=GREY, lw=0.5)
    ax.annotate("0.1 V at 0.66 ms", (0.66, 0.1), xytext=(0.75, 3.6), fontsize=8, color=COLORS[2],
                arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    ax.annotate("0.1 V at 2.23 ms", (2.23, 0.1), xytext=(2.05, 2.6), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    ax.plot(0.3245, -4.44, "o", color=COLORS[0], ms=5, zorder=5)
    ax.annotate("first negative peak\n−4.44 V at 0.324 ms", (0.3245, -4.44), xytext=(1.12, -4.1), fontsize=8,
                color=COLORS[0], va="center", arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.annotate("", (0.649 + 0.3245, -5.6), (0.3245, -5.6),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[0], lw=0.8, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax.text(0.65, -5.45, "$T_d$ = 0.649 ms", fontsize=8, color=COLORS[0], ha="center", va="bottom")
    for tt in (0.3245, 0.3245 + 0.649):
        ax.plot([tt, tt], [-5.6, -0.9 if tt > 0.5 else -4.44], color=COLORS[0], ls=":", lw=0.7)
    ax.set_xlim(0, 3)
    ax.set_ylim(-6, 10.5)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("capacitor voltage $v_C$ (V)")
    ax.legend(loc="upper right", fontsize=8)
    ax.text(2.98, -0.35, "±0.1 V", fontsize=7.5, color=GREY, ha="right", va="top")
    save(fig, "07", "fig-7-3-three-damping-cases")


# ----------------------------------------------------------------------------- Figure 7.4
def _step(z, x):
    wd = np.sqrt(1 - z * z)
    return 1 - np.exp(-z * x) / wd * np.sin(wd * x + np.arccos(z))


def fig_7_4():
    fig, ax = new_fig(6.4, 4.0)
    x = np.linspace(0, 30, 3001)
    ax.axhspan(0.98, 1.02, color=COLORS[2], alpha=0.15, lw=0)
    ax.axhline(1.0, color=GREY, lw=0.6)
    z = 0.102
    wd = np.sqrt(1 - z * z)
    ax.plot(x, 1 + np.exp(-z * x) / wd, color=COLORS[0], ls="--", lw=0.8)
    ax.plot(x, 1 - np.exp(-z * x) / wd, color=COLORS[0], ls="--", lw=0.8)
    ax.plot(x, _step(0.7, x), color=COLORS[2], lw=1.5, label="$\\zeta$ = 0.7 (overshoot 4.6 %)")
    ax.plot(x, _step(0.40, x), color=COLORS[1], lw=1.5, label="$\\zeta$ = 0.40, 1 cm spring tip (26 %)")
    ax.plot(x, _step(z, x), color=COLORS[0], lw=2.0, label="$\\zeta$ = 0.102, 15 cm ground lead (72 %)")
    tp = np.pi / wd
    mp = 1 + np.exp(-np.pi * z / wd)
    ax.plot(tp, mp, "o", color=COLORS[0], ms=5, zorder=5)
    ax.annotate(f"peak {mp:.2f} at $\\omega_0 t_p$ = {tp:.2f}\novershoot $M_p$ = 72 %", (tp, mp),
                xytext=(5.0, 1.66), fontsize=8.5, color=COLORS[0], va="center",
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.annotate("", (tp, 0.05), (0, 0.05),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.8, mutation_scale=7, shrinkA=0, shrinkB=0))
    ax.text(tp / 2, 0.07, "$t_p$", fontsize=9, ha="center", va="bottom")
    ax.plot([tp, tp], [0.0, mp], color=GREY, ls=":", lw=0.8)
    from matplotlib.patches import Patch
    band = Patch(fc=COLORS[2], alpha=0.15, label="±2 % band (0.98–1.02)")
    ax.annotate("settling ($\\zeta$ = 0.102) at $\\omega_0 t_s \\approx 4/\\zeta$ = 39 (off scale)", (30, 0.93), xytext=(29.8, 0.65),
                fontsize=8, ha="right", va="center", color=COLORS[0],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=0.8, mutation_scale=8))
    ax.text(17.5, 1.38, "envelope $1 \\pm e^{-\\zeta\\omega_0 t}/\\sqrt{1-\\zeta^2}$", fontsize=8, color=COLORS[0])
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1.8)
    ax.set_xlabel("normalised time $\\omega_0 t$")
    ax.set_ylabel("normalised output $x(t)$")
    h, l = ax.get_legend_handles_labels()
    ax.legend(handles=h + [band], loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.06))
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.set_ylim(0, 1.8 * 3.3)
    ax2.set_ylabel("probe display for a 3.3 V edge (V)")
    ax2.set_yticks([0, 1, 2, 3.3, 4, 5])
    ax2.set_yticklabels(["0", "1", "2", "3.3", "4", "5"])
    save(fig, "07", "fig-7-4-step-response-metrics")


# ----------------------------------------------------------------------------- Figure 7.5
def fig_7_5():
    L, C, R, Vc0 = 100e-6, 10e-9, 10e3, 5.0
    A = np.array([[-1 / (R * C), -1 / C], [1 / L, 0.0]])  # state (v, i_L)
    t = np.linspace(0, 60e-6, 6001)
    dt = t[1] - t[0]
    Ad = expm(A * dt)
    X = np.zeros((2, t.size))
    X[:, 0] = [Vc0, 0.0]
    for n in range(1, t.size):
        X[:, n] = Ad @ X[:, n - 1]
    v, il = X
    wc = 0.5 * C * v ** 2 * 1e9
    wl = 0.5 * L * il ** 2 * 1e9
    tu = t * 1e6

    fig = plt.figure(figsize=(6.6, 4.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 2.6], hspace=0.12)
    av = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1], sharex=av)
    av.plot(tu, v, color=COLORS[3], lw=1.0)
    av.plot(tu, 5 * np.exp(-t / 200e-6), color=GREY, ls="--", lw=0.8)
    av.plot(tu, -5 * np.exp(-t / 200e-6), color=GREY, ls="--", lw=0.8)
    av.set_ylim(-5.5, 5.5)
    av.set_yticks([-5, 0, 5])
    av.set_ylabel("$v$ (V)")
    av.text(59.5, 5.6, "$v(t)$, 159 kHz; envelope $5e^{-t/200\\,\\mu s}$", fontsize=8, ha="right", va="bottom", color=GREY)
    plt.setp(av.get_xticklabels(), visible=False)

    ax.plot(tu, wc, color=COLORS[0], lw=1.0, label="$w_C = Cv^2/2$")
    ax.plot(tu, wl, color=COLORS[1], lw=1.0, label="$w_L = Li_L^2/2$")
    ax.plot(tu, wc + wl, color=INK, lw=2.0, label="total $w_C + w_L$")
    ax.plot(tu, 125 * np.exp(-t / 100e-6), color=GREY, ls=":", lw=1.2, label="$125\\,e^{-t/100\\,\\mu s}$ nJ")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 130)
    ax.set_xlabel("time (µs)")
    ax.set_ylabel("stored energy (nJ)")
    ax.set_ylim(0, 150)
    ax.legend(loc="upper right", fontsize=8, ncol=2, bbox_to_anchor=(1.0, 1.04),
              title="$w_C$, $w_L$ swap in antiphase at 318 kHz (2 × 159 kHz)", title_fontsize=8)
    ax.annotate("6.1 % of the stored energy\nlost per cycle ($\\approx 2\\pi/Q$, $Q$ = 100)",
                (12.6, 125 * np.exp(-0.126)), xytext=(2.0, 140), fontsize=8, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.1)
    save(fig, "07", "fig-7-5-energy-exchange")


if __name__ == "__main__":
    fig_7_1()
    fig_7_2()
    fig_7_3()
    fig_7_4()
    fig_7_5()
