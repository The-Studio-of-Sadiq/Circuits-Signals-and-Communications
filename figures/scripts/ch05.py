"""Figures for Chapter 5 — Capacitors and Inductors.

Run from the repository root:  python figures/scripts/ch05.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Ellipse, Circle, Wedge, FancyArrowPatch, Arc  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import COLORS, INK, new_fig, save  # noqa: E402

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

GREY = "#666666"
LIGHT = "#9A9A9A"


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


def harrow(ax, x0, y0, x1, y1, color=INK, lw=1.0, ms=9, style="-|>"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


# ----------------------------------------------------------------------------- Figure 5.1
def fig_5_1():
    fig, axs = plt.subplots(1, 3, figsize=(6.8, 3.0))
    for ax in axs:
        ax.set_aspect("equal")
        ax.axis("off")

    # (a) parallel-plate capacitor
    ax = axs[0]
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.75, 2.35)
    w, g, t = 3.0, 1.4, 0.16
    ax.add_patch(Rectangle((-w / 2, -g / 2), w, g, fc="#E8F1E4", ec="none"))
    ax.add_patch(Rectangle((-w / 2, g / 2), w, t, fc=COLORS[1], ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-w / 2, -g / 2 - t), w, t, fc=COLORS[0], ec=INK, lw=0.8))
    for x in np.linspace(-1.2, 1.2, 7):
        harrow(ax, x, g / 2 - 0.05, x, -g / 2 + 0.05, color=COLORS[2], lw=0.9, ms=7)
    # fringing at both edges
    for s in (-1, 1):
        th = np.linspace(-np.pi / 2, np.pi / 2, 40)
        r = g / 2
        for bulge, x0 in ((0.16, 0.0), (0.32, 0.08)):
            ax.plot(s * (w / 2 - x0) + s * bulge * np.cos(th), r * np.sin(th), color=COLORS[2], lw=0.8)
    ax.text(-0.15, 0.0, "$\\varepsilon_r$", fontsize=10, ha="right", va="center", color=INK,
            bbox=dict(fc="#E8F1E4", ec="none", pad=0.5))
    ax.text(0.15, 0.0, "$E$", fontsize=10, ha="left", va="center", color=COLORS[2],
            bbox=dict(fc="#E8F1E4", ec="none", pad=0.5))
    ax.text(0, g / 2 + t + 0.08, "$+q$   (area $A$)", ha="center", va="bottom", fontsize=9, color=COLORS[1])
    ax.text(0, -g / 2 - t - 0.08, "$-q$", ha="center", va="top", fontsize=9, color=COLORS[0])
    # terminals
    ax.plot([0, 0, 1.9], [g / 2 + t + 0.45, 1.75, 1.75], color=INK, lw=1.0)
    ax.plot([0, 0, 1.9], [-g / 2 - t - 0.45, -1.75, -1.75], color=INK, lw=1.0)
    ax.plot([0, 0], [g / 2 + t, g / 2 + t + 0.08], color=INK, lw=1.0)
    for y in (1.75, -1.75):
        ax.add_patch(Circle((1.95, y), 0.07, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.text(2.0, 0.0, "+\n$v$\n−", ha="center", va="center", fontsize=10, linespacing=1.6)
    # gap dimension
    harrow(ax, -1.95, g / 2, -1.95, -g / 2, style="<|-|>", lw=0.8, ms=6)
    ax.text(-2.05, 0, "$d$", ha="right", va="center", fontsize=10)
    ax.set_title("(a) parallel-plate capacitor", fontsize=9, pad=2)
    ax.text(0, -2.45, "$C = \\varepsilon_r\\varepsilon_0 A/d$", ha="center", fontsize=10)

    # (b) air-cored solenoid
    ax = axs[1]
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.75, 2.35)
    L, R = 2.6, 0.55
    # field lines: inside straight, outside closing
    a_out = 1.95
    for y in (-0.3, 0.0, 0.3):
        xe = a_out if y == 0 else L / 2 + 0.15
        ax.plot([-xe, xe], [y, y], color=COLORS[2], lw=0.9)
        harrow(ax, 0.2, y, 0.45, y, color=COLORS[2], ms=7, lw=0.9)
    for b in (1.05, 1.6):
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(a_out * np.cos(th), b * np.sin(th), color=COLORS[2], lw=0.8)
        harrow(ax, 0.05, b, -0.2, b, color=COLORS[2], ms=7, lw=0.8)
        harrow(ax, 0.05, -b, -0.2, -b, color=COLORS[2], ms=7, lw=0.8)
    # windings
    n = 13
    xs = np.linspace(-L / 2, L / 2, n)
    for x in xs:
        ax.add_patch(Arc((x, 0), 0.22, 2 * R, theta1=90, theta2=270, color=GREY, lw=0.8))
    for x0, x1 in zip(xs[:-1], xs[1:]):
        ax.plot([x0, x1], [R, -R], color=COLORS[1], lw=1.4)
    ax.plot([xs[0] - 0.6, xs[0]], [-R - 0.35, -R], color=COLORS[1], lw=1.4)
    ax.plot([xs[-1], xs[-1] + 0.6], [R, R + 0.35], color=COLORS[1], lw=1.4)
    harrow(ax, xs[0] - 0.6, -R - 0.35, xs[0] - 0.3, -R - 0.175, color=COLORS[1], ms=8)
    ax.text(xs[0] - 0.55, -R - 0.45, "$i$", fontsize=10, color=COLORS[1], va="top", ha="right")
    ax.text(0.2, 0.62, "$B$", fontsize=10, color=COLORS[2], ha="left", va="bottom",
            bbox=dict(fc="white", ec="none", pad=0.3))
    harrow(ax, -L / 2, -1.95, L / 2, -1.95, style="<|-|>", lw=0.8, ms=6)
    ax.text(0, -2.0, "$l$ = 50 mm", ha="center", va="top", fontsize=8.5)
    harrow(ax, L / 2 + 0.35, -R, L / 2 + 0.35, R, style="<|-|>", lw=0.8, ms=6)
    ax.text(L / 2 + 0.35, -R - 0.1, "⌀ 10 mm", ha="center", va="top", fontsize=8,
            bbox=dict(fc="white", ec="none", pad=0.4))
    ax.text(0, 2.05, "$N$ = 200 turns", ha="center", va="center", fontsize=8.5)
    ax.set_title("(b) air-cored solenoid", fontsize=9, pad=2)
    ax.text(0, -2.6, "$L = \\mu_0 N^2 A/l$ = 79 µH", ha="center", fontsize=10)

    # (c) ferrite toroid
    ax = axs[2]
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.75, 2.35)
    ro, ri = 1.55, 0.95
    ax.add_patch(Wedge((0, 0), ro, 0, 360, width=ro - ri, fc="#D9D2C5", ec=INK, lw=0.9))
    rm = (ro + ri) / 2
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(rm * np.cos(th), rm * np.sin(th), color=COLORS[2], lw=1.0, ls="--")
    harrow(ax, rm * np.cos(0.25 * np.pi), rm * np.sin(0.25 * np.pi), rm * np.cos(0.22 * np.pi + 0.15),
           rm * np.sin(0.22 * np.pi + 0.15), color=COLORS[2], ms=8)
    for k in range(20):
        a = np.pi * (1.05 + 0.9 * k / 19)  # winding on the lower-left sector
        ax.plot([(ri - 0.1) * np.cos(a), (ro + 0.1) * np.cos(a)],
                [(ri - 0.1) * np.sin(a), (ro + 0.1) * np.sin(a)], color=COLORS[1], lw=1.1)
    a0, a1 = np.pi * 1.05, np.pi * 1.95
    ax.plot([(ro + 0.1) * np.cos(a0), (ro + 0.45) * np.cos(a0)],
            [(ro + 0.1) * np.sin(a0), (ro + 0.45) * np.sin(a0)], color=COLORS[1], lw=1.1)
    ax.plot([(ro + 0.1) * np.cos(a1), (ro + 0.45) * np.cos(a1)],
            [(ro + 0.1) * np.sin(a1), (ro + 0.45) * np.sin(a1)], color=COLORS[1], lw=1.1)
    ax.text(0, -ro - 0.3, "$N$ = 20 turns", ha="center", va="top", fontsize=8.5, color=COLORS[1])
    ax.text(0, 0.18, "$l_e$ = 40 mm\n(dashed path)", ha="center", va="center", fontsize=8, color=COLORS[2])
    ax.text(0, ro + 0.12, "$A_e$ = 20 mm², $\\mu_r$ = 2000", ha="center", va="bottom", fontsize=8.5)
    ax.set_title("(c) ferrite toroid", fontsize=9, pad=2)
    ax.text(0, -2.6, "$L = \\mu_0\\mu_r N^2 A_e/l_e$ = 503 µH", ha="center", fontsize=10)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.02, wspace=0.04)
    save(fig, "05", "fig-5-1-capacitor-inductor-geometry")


# ----------------------------------------------------------------------------- Figure 5.2
def fig_5_2():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True)
    t = np.linspace(0, 8, 4001)  # microseconds
    # capacitor: triangle 0..2 V, period 4 us
    ph = np.mod(t, 4.0)
    v = np.where(ph < 2, ph, 4 - ph)
    i = np.where(ph < 2, 1.0, -1.0)  # C dv/dt = 1e-6 * 1e6 = 1 A
    a1.plot(t, v, color=COLORS[0], label="$v_C$ (V)")
    a1b = a1.twinx()
    a1b.spines["right"].set_visible(True)
    a1b.plot(t, i, color=COLORS[1], ls="--", label="$i_C$ (A)")
    a1.set_ylim(-0.3, 2.6)
    a1b.set_ylim(-1.6, 1.6)
    a1.set_ylabel("$v_C$ (V)", color=COLORS[0])
    a1b.set_ylabel("$i_C$ (A)", color=COLORS[1])
    a1.tick_params(axis="y", colors=COLORS[0])
    a1b.tick_params(axis="y", colors=COLORS[1])
    a1.set_title("Capacitor $C$ = 1 µF: triangular voltage → square current", fontsize=10, loc="left")
    a1.text(0.62, 0.45, "slope +1 V/µs", fontsize=8, color=INK, ha="left", va="center")
    a1.text(0.38, 0.15, "$i = C\\,dv/dt$ = +1 A", fontsize=8, color=INK, ha="left", va="center")
    a1.text(2.6, 1.78, "slope −1 V/µs", fontsize=8, color=INK, ha="left", va="center")
    a1.text(2.6, 1.5, "$i$ = −1 A", fontsize=8, color=INK, ha="left", va="center")

    # inductor: buck, 12 V -> 3.3 V, 500 kHz, L = 10 uH
    T, ton = 2.0, 0.55
    ph = np.mod(t, T)
    vl = np.where(ph < ton, 8.7, -3.3)
    rise = 8.7 / 10.0  # A/us
    fall = 3.3 / 10.0
    imin = 2.0 - 0.4785 / 2
    il = np.where(ph < ton, imin + rise * ph, imin + rise * ton - fall * (ph - ton))
    a2.plot(t, vl, color=COLORS[0], drawstyle="steps-post")
    a2b = a2.twinx()
    a2b.spines["right"].set_visible(True)
    a2b.plot(t, il, color=COLORS[1], ls="--")
    a2.set_ylim(-5, 11)
    a2b.set_ylim(1.4, 2.6)
    a2.set_ylabel("$v_L$ (V)", color=COLORS[0])
    a2b.set_ylabel("$i_L$ (A)", color=COLORS[1])
    a2.tick_params(axis="y", colors=COLORS[0])
    a2b.tick_params(axis="y", colors=COLORS[1])
    a2.axhline(0, color=GREY, lw=0.6)
    a2.set_title("Buck inductor $L$ = 10 µH, 500 kHz: square voltage → triangular current", fontsize=10, loc="left")
    a2.text(0.6, 9.2, "+8.7 V for 0.55 µs", fontsize=8, color=COLORS[0], va="center")
    a2.text(1.2, -4.2, "−3.3 V for 1.45 µs", fontsize=8, color=COLORS[0], va="center")
    a2b.text(2.9, 2.5, "$i_L$:  $di/dt = v/L$ = +0.87 A/µs (on),  −0.33 A/µs (off)", fontsize=8,
             color=COLORS[1], ha="left", va="center")
    # ripple bracket
    x0 = 7.8
    a2b.annotate("", (x0, imin), (x0, imin + 0.4785),
                 arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=0.8, mutation_scale=7, shrinkA=0, shrinkB=0))
    a2b.text(7.2, 1.66, "0.478 A p-p\nabout 2 A", fontsize=7.5, color=COLORS[1], ha="center", va="center")
    a2.set_xlim(0, 8)
    a2.set_xlabel("time $t$ (µs)")
    fig.tight_layout(h_pad=1.0)
    save(fig, "05", "fig-5-2-vi-waveforms-c-and-l")


# ----------------------------------------------------------------------------- Figure 5.3
def fig_5_3():
    fig = plt.figure(figsize=(6.8, 2.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.3)
    axc = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[0, 1])

    d = drawing(axc, unit=2.0, fontsize=8.5)
    d += elm.Capacitor().up().length(3).label("$C_1$\n10 µF\n10 V", loc="top")
    d += elm.Switch(action="close").right().length(1.8).label("S", loc="top")
    d += elm.Resistor().right().length(2.2).label("$R$", loc="top")
    d += elm.Capacitor().down().length(3).label("$C_2$\n10 µF\n0 V", loc="bottom")
    d += elm.Line().left().length(4.0)
    finish(d, axc, pad=0.3, xlim=(-2.3, 6.3), ylim=(-2.6, 4.2))
    axc.text(2.0, -0.4, "$R$: any value,\nincluding wiring", ha="center", va="top", fontsize=8.5, color=INK)
    axc.text(2.0, -1.6, "$q$ = 100 µC conserved", ha="center", va="top", fontsize=8.5, color=COLORS[0])

    x = np.linspace(0, 5, 400)
    v1 = 5 + 5 * np.exp(-x)
    v2 = 5 - 5 * np.exp(-x)
    W = 0.5 * 10e-6 * (v1 ** 2 + v2 ** 2) * 1e6  # uJ
    ax.plot(x, v1, color=COLORS[0], label="$v_1$")
    ax.plot(x, v2, color=COLORS[2], label="$v_2$")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("$t\\,/\\,[R\\,C_1C_2/(C_1+C_2)]$")
    ax.set_ylabel("capacitor voltage (V)")
    ax.text(0.5, 9.4, "$v_1$", color=COLORS[0], fontsize=10)
    ax.text(0.5, 1.0, "$v_2$", color=COLORS[2], fontsize=10)
    ax.text(3.6, 3.3, "$v_1$, $v_2$ → 5.0 V", color=INK, fontsize=9, ha="center")
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(x, W, color=COLORS[1], ls="--")
    ax2.fill_between(x, W, 500, color=COLORS[1], alpha=0.15, lw=0)
    ax2.axhline(500, color=COLORS[1], lw=0.6, ls=":")
    ax2.set_ylim(0, 525)
    ax2.set_ylabel("total stored energy (µJ)", color=COLORS[1])
    ax2.tick_params(axis="y", colors=COLORS[1])
    ax2.text(2.9, 390, "250 µJ dissipated in $R$", ha="center", va="center", fontsize=9, color=COLORS[1])
    ax2.annotate("$w$ → 250 µJ stored", (4.6, 252), xytext=(3.6, 110), ha="center", fontsize=9,
                 color=COLORS[1], arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.8, mutation_scale=8))
    ax2.annotate("$w$", (0.45, 351), xytext=(0.12, 280), color=COLORS[1], fontsize=10,
                 arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    fig.subplots_adjust(left=0.0, right=0.9, top=0.95, bottom=0.17)
    save(fig, "05", "fig-5-3-charge-sharing")


# ----------------------------------------------------------------------------- Figure 5.4
def _ic_panel(ax, mode):
    """mode: 'full', 'minus' (t = 0-), 'plus' (t = 0+)."""
    d = drawing(ax, unit=2.0, fontsize=8)
    H = 4.0
    grey = LIGHT if mode == "plus" else INK
    d += elm.SourceV().up().length(H).label("12 V", loc="top").color(grey)
    if mode == "plus":
        d += elm.Switch().right().length(2.0).label("S open", loc="top").color(grey)
    elif mode == "minus":
        d += elm.Line().right().length(2.0).label("S closed", loc="top")
    else:
        d += elm.Switch(action="open").right().length(2.0).label("S", loc="top")
    d += elm.Resistor().right().length(2.2).label("$R_1$ = 2 Ω", loc="top").color(grey)
    d += (na := elm.Dot())
    d += elm.Line().right().length(5.0)
    # R2 branch at x = 4.2
    d += elm.Resistor().at(na.center).down().length(H).label("$R_2$\n4 Ω", loc="bottom")
    d += elm.Dot()
    # L branch at x = 6.7
    d += elm.Line().at((6.7, H)).down().length(0.0)
    if mode == "full":
        d += elm.Inductor().at((6.7, H)).down().length(2.0).label("$L$\n10 mH", loc="bottom")
    elif mode == "minus":
        d += elm.Line().at((6.7, H)).down().length(2.0).color(COLORS[1]).label("short", loc="bottom", color=COLORS[1])
    else:
        d += elm.SourceI().at((6.7, H)).down().length(2.0).color(COLORS[1]).label("2.4 A", loc="bottom", color=COLORS[1])
    d += elm.Resistor().down().length(2.0).label("$R_3$\n2 Ω", loc="bottom")
    d += elm.Dot()
    # C branch at x = 9.2
    if mode == "full":
        d += elm.Capacitor().at((9.2, H)).down().length(2.0).label("$C$\n100 µF", loc="bottom")
    elif mode == "minus":
        d += elm.Gap().at((9.2, H)).down().length(2.0).label("open", loc="bottom", color=COLORS[1])
        ax.plot([9.2, 9.2], [H, H - 0.6], color=INK, lw=1.2)
        ax.plot([9.2, 9.2], [H - 1.4, H - 2.0], color=INK, lw=1.2)
        for yy in (H - 0.6, H - 1.4):
            ax.plot(9.2, yy, "o", ms=4, mfc="white", mec=INK, zorder=6)
    else:
        d += elm.SourceV().at((9.2, H)).down().length(2.0).reverse().color(COLORS[1]).label("4.8 V", loc="bottom", color=COLORS[1])
    d += elm.Resistor().at((9.2, H - 2.0)).down().length(2.0).label("$R_4$\n1 Ω", loc="bottom")
    d += elm.Line().at((9.2, 0)).left().length(9.2).color(INK)
    finish(d, ax, xlim=(-2.1, 11.2), ylim=(-2.6, 5.4))
    ax.text(4.2 + 0.1, H + 0.15, "$a$", fontsize=10, fontweight="bold", ha="left", va="bottom")
    if mode == "minus":
        ax.text(4.6, -0.5, "$v_a(0^-)$ = 4.8 V,  $i_L(0^-)$ = 2.4 A,\n$v_C(0^-)$ = 4.8 V",
                ha="center", va="top", fontsize=8.5, color=COLORS[0])
    elif mode == "plus":
        ax.text(4.6, -0.5, "$v_a(0^+)$ = 1.92 V,  $i_C(0^+)$ = −2.88 A,\n$v_L(0^+)$ = −2.88 V",
                ha="center", va="top", fontsize=8.5, color=COLORS[0])
        ax.text(6.0, 3.0, "+\n$v_L$\n−", ha="right", va="center", fontsize=8, color=COLORS[1], linespacing=0.9)
    else:
        ax.text(4.6, -0.5, "S closed for a long time,\nopens at $t$ = 0",
                ha="center", va="top", fontsize=8.5, color=GREY)


def fig_5_4():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.4))
    axs = axs.ravel()
    _ic_panel(axs[0], "full")
    axs[0].set_title("(a) circuit", fontsize=9.5, pad=2)
    _ic_panel(axs[1], "minus")
    axs[1].set_title("(b) $t = 0^-$: $L$ short, $C$ open", fontsize=9.5, pad=2)
    _ic_panel(axs[2], "plus")
    axs[2].set_title("(c) $t = 0^+$: $L$ → current source, $C$ → voltage source", fontsize=9.5, pad=2)
    ax = axs[3]
    ax.axis("off")
    ax.text(0.5, 0.55,
            "KCL at $a$ for $t = 0^+$ (currents leaving):\n\n"
            "$\\dfrac{v_a}{4} + 2.4 + \\dfrac{v_a - 4.8}{1} = 0$\n\n"
            "$v_a$ = 1.92 V  (jumps from 4.8 V)\n"
            "$i_C = (1.92 - 4.8)/1$ = −2.88 A\n"
            "$v_L = v_a - R_3 i_L$ = 1.92 − 4.8 = −2.88 V\n\n"
            "$dv_C/dt(0^+)$ = −28 800 V/s\n"
            "$di_L/dt(0^+)$ = −288 A/s",
            ha="center", va="center", fontsize=8.5, color=INK, transform=ax.transAxes, linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F4F4F4", ec=GREY, lw=0.6))
    fig.subplots_adjust(left=0.005, right=0.995, top=0.95, bottom=0.01, wspace=0.05, hspace=0.12)
    save(fig, "05", "fig-5-4-initial-conditions-circuit")


# ----------------------------------------------------------------------------- Figure 5.5
def _dot(ax, x, y):
    ax.plot(x, y, "o", color=INK, ms=4.5, zorder=6)


def _m_arrow(ax, x0, x1, y, text, rad=-0.45):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<|-|>", mutation_scale=8,
                                 connectionstyle=f"arc3,rad={rad}", color=COLORS[3], lw=0.9))
    ax.text((x0 + x1) / 2, y + 1.05, text, ha="center", va="bottom", fontsize=8, color=COLORS[3])


def fig_5_5():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.6))
    axs = axs.ravel()

    # (a) coupled pair with dots
    ax = axs[0]
    d = drawing(ax, unit=2.0, fontsize=8.5)
    X2 = 4.4
    d += elm.Dot(open=True).at((-1.4, 3))
    d += (w1 := elm.Line().right().length(1.4))
    d += elm.CurrentLabelInline(direction="in", ofst=0.2).at(w1).label("$i_1$", loc="top")
    d += (c1 := elm.Inductor2(loops=4).down().length(3))
    d += elm.Line().left().length(1.4)
    d += elm.Dot(open=True)
    d += elm.Dot(open=True).at((X2 + 1.4, 3))
    d += (w2 := elm.Line().left().length(1.4))
    d += elm.CurrentLabelInline(direction="in", ofst=0.2).at(w2).label("$i_2$", loc="top")
    d += (c2 := elm.Inductor2(loops=4).down().length(3).reverse().flip())
    d += elm.Line().right().length(1.4)
    d += elm.Dot(open=True)
    finish(d, ax, xlim=(-2.4, X2 + 2.4), ylim=(-1.1, 4.3))
    p1, p2 = c1.absanchors["istart"], c2.absanchors["istart"]
    _dot(ax, p1.x - 0.3, p1.y)
    _dot(ax, p2.x + 0.3, p2.y)
    ax.text(0.55, 1.5, "$L_1$\n2 mH", ha="left", va="center", fontsize=8.5)
    ax.text(X2 - 0.55, 1.5, "$L_2$\n8 mH", ha="right", va="center", fontsize=8.5)
    ax.text(-1.4, 1.5, "+\n$v_1$\n−", ha="center", va="center", fontsize=9, linespacing=1.4)
    ax.text(X2 + 1.4, 1.5, "+\n$v_2$\n−", ha="center", va="center", fontsize=9, linespacing=1.4)
    ax.add_patch(FancyArrowPatch((0.5, 2.55), (X2 - 0.5, 2.55), arrowstyle="<|-|>", mutation_scale=8,
                                 connectionstyle="arc3,rad=-0.25", color=COLORS[3], lw=0.9))
    ax.text(X2 / 2, -0.3, "$M$ = 3.6 mH,  $k$ = 0.9", ha="center", va="top", fontsize=8.5, color=COLORS[3])
    ax.set_title("(a) dot convention", fontsize=9.5, pad=2)

    # (b) series aiding and (c) series opposing, coils drawn horizontally
    for ax, aid in ((axs[1], True), (axs[2], False)):
        d = drawing(ax, unit=2.0, fontsize=8.5)
        d += elm.Dot(open=True).at((0, 0))
        d += (w := elm.Line().right().length(1.4))
        d += elm.CurrentLabelInline(direction="in", ofst=0.1).at(w).label("$i$", loc="bottom")
        d += (c1 := elm.Inductor2(loops=4).right().length(2.6).label("$L_1$ = 2 mH", loc="bottom"))
        d += elm.Line().right().length(1.2)
        d += (c2 := elm.Inductor2(loops=4).right().length(2.6).label("$L_2$ = 8 mH", loc="bottom"))
        d += elm.Line().right().length(1.4)
        d += elm.Dot(open=True)
        finish(d, ax, xlim=(-0.8, 9.9), ylim=(-2.6, 2.8))
        a1, a2s, a2e = c1.absanchors["istart"], c2.absanchors["istart"], c2.absanchors["iend"]
        _dot(ax, a1.x - 0.15, 0.6)
        if aid:
            _dot(ax, a2s.x - 0.15, 0.6)
        else:
            _dot(ax, a2e.x + 0.15, 0.6)
        _m_arrow(ax, c1.absanchors["center"].x, c2.absanchors["center"].x, 0.75, "$M$ = 3.6 mH")
        if aid:
            ax.text(4.55, -1.4, "current enters both dots\n$L_{aid} = L_1 + L_2 + 2M$ = 17.2 mH",
                    ha="center", va="top", fontsize=8.5, color=COLORS[0])
        else:
            ax.text(4.55, -1.4, "enters one dot, leaves the other\n$L_{opp} = L_1 + L_2 - 2M$ = 2.8 mH",
                    ha="center", va="top", fontsize=8.5, color=COLORS[0])
    axs[1].set_title("(b) series aiding", fontsize=9.5, pad=2)
    axs[2].set_title("(c) series opposing", fontsize=9.5, pad=2)

    # (d) T-equivalent
    ax = axs[3]
    d = drawing(ax, unit=2.0, fontsize=8.5)
    d += elm.Dot(open=True).at((0, 3))
    d += elm.Line().right().length(0.6)
    d += elm.Inductor2(loops=3).right().length(3.2).label("$L_1 - M$\n= −1.6 mH", loc="top")
    d += (nd := elm.Dot())
    d += elm.Inductor2(loops=3).right().length(3.2).label("$L_2 - M$\n= 4.4 mH", loc="top")
    d += elm.Line().right().length(0.6)
    d += elm.Dot(open=True)
    d += elm.Inductor2(loops=3).at(nd.center).down().length(3).label("$M$ = 3.6 mH", loc="bottom")
    d += elm.Dot()
    d += elm.Dot(open=True).at((0, 0))
    d += elm.Line().right().length(7.6)
    d += elm.Dot(open=True)
    finish(d, ax, xlim=(-0.8, 8.4), ylim=(-2.2, 5.3))
    ax.text(3.8, -0.35, "common terminal", ha="center", va="top", fontsize=8, color=GREY)
    ax.text(3.8, -1.0, "a negative arm is acceptable in a model\nthat is only equivalent at its terminals",
            ha="center", va="top", fontsize=8, color=COLORS[1])
    ax.set_title("(d) T-equivalent", fontsize=9.5, pad=2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01, wspace=0.08, hspace=0.12)
    save(fig, "05", "fig-5-5-coupled-coils-dot-t-equivalent")


# ----------------------------------------------------------------------------- Figure 5.6
def fig_5_6():
    fig = plt.figure(figsize=(6.8, 5.2))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 2.3], hspace=0.22, wspace=0.08)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    ax = fig.add_subplot(gs[1, :])

    # (a) capacitor model: ESR - ESL - (C || Rp)
    d = drawing(axa, unit=1.6, fontsize=8)
    d += elm.Dot(open=True).at((0, 0))
    d += elm.Resistor().right().length(2.0).label("ESR")
    d += elm.Inductor2(loops=3).right().length(2.0).label("ESL")
    d += (n1 := elm.Dot())
    d += elm.Capacitor().right().length(2.2).label("$C$")
    d += (n2 := elm.Dot())
    d += elm.Line().right().length(0.6)
    d += elm.Dot(open=True)
    d += elm.Line().at(n1.center).down().length(1.1)
    d += elm.Resistor().right().length(2.2).label("$R_p$", loc="bottom")
    d += elm.Line().up().length(1.1)
    finish(d, axa, xlim=(-0.4, 7.4), ylim=(-2.0, 1.2))
    axa.set_title("(a) capacitor model", fontsize=9.5, pad=2)

    # (b) inductor model: (DCR - L) || Cp || Rcore
    d = drawing(axb, unit=1.6, fontsize=8)
    d += elm.Dot(open=True).at((0, 0))
    d += elm.Line().right().length(0.6)
    d += (n1 := elm.Dot())
    d += elm.Resistor().right().length(2.0).label("DCR")
    d += elm.Inductor2(loops=3).right().length(2.0).label("$L$")
    d += (n2 := elm.Dot())
    d += elm.Line().right().length(0.6)
    d += elm.Dot(open=True)
    d += elm.Line().at(n1.center).down().length(0.9)
    d += elm.Capacitor().right().length(4.0).label("$C_p$", loc="bottom")
    d += elm.Line().up().length(0.9)
    d += elm.Line().at((0.6, -0.9)).down().length(1.1)
    d += elm.Resistor().right().length(4.0).label("$R_{core}$", loc="bottom")
    d += elm.Line().up().length(1.1)
    finish(d, axb, xlim=(-0.4, 5.6), ylim=(-3.0, 1.2))
    axb.set_title("(b) inductor model", fontsize=9.5, pad=2)

    # (c) impedance
    f = np.logspace(2, 8, 1200)
    w = 2 * np.pi * f
    caps = [("100 µF electrolytic (ESR 0.1 Ω, ESL 10 nH)", 100e-6, 0.1, 10e-9, COLORS[0]),
            ("100 nF MLCC (ESR 10 mΩ, ESL 0.5 nH)", 100e-9, 0.01, 0.5e-9, COLORS[1])]
    for lab, C, esr, esl, col in caps:
        Z = np.abs(esr + 1j * w * esl + 1 / (1j * w * C))
        ax.loglog(f, Z, color=col, lw=2.0, label=lab)
        ax.loglog(f, 1 / (w * C), color=col, lw=1.0, ls="--")
        fsr = 1 / (2 * np.pi * np.sqrt(esl * C))
        ax.plot(fsr, esr, "o", color=col, ms=6, zorder=5)
        ax.axvline(fsr, color=col, lw=0.6, ls=":")
    ax.annotate("$f_{SR}$ = 159 kHz\n|Z| ≈ ESR = 0.1 Ω", (1.59e5, 0.1), xytext=(1.3e3, 0.018), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.plot([1e2], [1 / (2 * np.pi * 1e2 * 100e-6)], "o", color=COLORS[0], ms=4, clip_on=False, zorder=5)
    ax.plot([1e3], [1 / (2 * np.pi * 1e3 * 100e-9)], "o", color=COLORS[1], ms=4, zorder=5)
    ax.plot([], [], color=GREY, lw=1.0, ls="--", label="ideal capacitor, $1/(\\omega C)$")
    ax.annotate("$f_{SR}$ = 22.5 MHz\n|Z| = 10 mΩ", (2.25e7, 0.01), xytext=(1.4e6, 0.0125), fontsize=8,
                color=COLORS[1], arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6), ha="left")
    ax.text(150, 22, "15.9 Ω", fontsize=8, color=COLORS[0])
    ax.text(1.3e3, 2.3e3, "1.59 kΩ at 1 kHz", fontsize=8, color=COLORS[1])
    ax.text(7e7, 8.5, "6.3 Ω", fontsize=8, color=COLORS[0], ha="right")
    ax.text(7e7, 0.40, "0.30 Ω", fontsize=8, color=COLORS[1], ha="right")
    ax.text(3e6, 2.5, "inductive:\n|Z| ≈ ω·ESL", fontsize=8, color=GREY, ha="center")
    ax.set_xlim(1e2, 1e8)
    ax.set_ylim(0.005, 2e4)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("impedance magnitude |Z| (Ω)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, which="major", color="#E6E6E6", lw=0.6)
    ax.set_title("(c) impedance of two practical capacitors", fontsize=9.5, loc="left", pad=3)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.96, bottom=0.08)
    save(fig, "05", "fig-5-6-practical-models-impedance")


if __name__ == "__main__":
    fig_5_1()
    fig_5_2()
    fig_5_3()
    fig_5_4()
    fig_5_5()
    fig_5_6()
