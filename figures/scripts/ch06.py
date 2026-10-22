"""Figures for Chapter 6 — First-Order Circuits.

Run from the repository root:  python figures/scripts/ch06.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, FancyArrowPatch  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import COLORS, INK, new_fig, save  # noqa: E402

schemdraw.use("matplotlib")
warnings.filterwarnings("ignore", message=".*non-interactive.*")

GREY = "#666666"
LIGHTGREY = "#BBBBBB"


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


def note_box(ax, x, y, text, fontsize=8.5, **kw):
    ax.text(x, y, text, fontsize=fontsize, color=INK, linespacing=1.35,
            bbox=dict(boxstyle="round,pad=0.4", fc="#F4F4F4", ec=GREY, lw=0.6), **kw)


# ----------------------------------------------------------------------------- Figure 6.1
def fig_6_1():
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.3))
    # (a) RC
    ax = axs[0]
    d = drawing(ax, unit=2.0, fontsize=9)
    d += elm.SourceV().up().length(3).label("$V_{Th}$", loc="top")
    d += elm.Switch(action="close").right().length(1.8).label("S\n$t$ = 0", loc="top")
    d += elm.Resistor().right().length(1.6).label("$R_{Th}$", loc="top")
    d += (w := elm.Line().right().length(0.9))
    d += elm.CurrentLabelInline(direction="in", ofst=0.0).at(w).label("$i$", loc="top")
    d += elm.Capacitor().down().length(3).label("$C$", loc="bottom")
    d += elm.Line().left().length(4.3)
    finish(d, ax, xlim=(-1.9, 6.3), ylim=(-2.9, 4.75))
    ax.text(3.75, 1.5, "+\n$v_C$\n−", ha="right", va="center", fontsize=9, color=COLORS[0], linespacing=1.3)
    note_box(ax, 2.0, -0.55, "Example: 12 V with divider $R_1$ = 6 kΩ,\n$R_2$ = 3 kΩ; $C$ = 2 µF across $R_2$\n"
             "→ $V_{Th}$ = 4 V, $R_{Th}$ = 2 kΩ\n→ $\\tau = R_{Th}C$ = 4 ms", ha="center", va="top")
    ax.set_title("(a) RC: source switched onto a capacitor", fontsize=9.5, pad=2)
    # (b) RL
    ax = axs[1]
    d = drawing(ax, unit=2.0, fontsize=9)
    d += elm.SourceV().up().length(3).label("$V_{Th}$", loc="top")
    d += elm.Switch(action="close").right().length(1.8).label("S\n$t$ = 0", loc="top")
    d += elm.Resistor().right().length(2.2).label("$R_{Th}$", loc="top")
    d += (w := elm.Line().down().length(0.8))
    d += elm.CurrentLabelInline(direction="in", ofst=0.0).at(w).label("$i_L$", loc="bottom")
    d += elm.Inductor2(loops=4).down().length(2.2).label("$L$", loc="bottom")
    d += elm.Line().left().length(4.0)
    finish(d, ax, xlim=(-1.9, 6.3), ylim=(-2.9, 4.75))
    ax.text(5.0, 1.2, "+\n$v_L$\n−", ha="left", va="center", fontsize=9, color=COLORS[0], linespacing=1.3)
    note_box(ax, 2.0, -0.55, "Example: relay coil $L$ = 0.2 H,\n$R$ = 40 Ω, 24 V supply\n"
             "→ $\\tau = L/R$ = 5 ms\n→ $I_{final}$ = 24/40 = 0.6 A", ha="center", va="top")
    ax.set_title("(b) RL: source switched onto an inductor", fontsize=9.5, pad=2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.01, wspace=0.06)
    save(fig, "06", "fig-6-1-rc-rl-switched-circuits")


# ----------------------------------------------------------------------------- Figure 6.2
def fig_6_2():
    fig, ax = new_fig(6.4, 4.0)
    x = np.linspace(0, 5, 500)
    ax.plot(x, np.exp(-x), color=COLORS[0], label="natural decay $e^{-t/\\tau}$")
    ax.plot(x, 1 - np.exp(-x), color=COLORS[1], ls="--", label="step rise $1 - e^{-t/\\tau}$")
    ax.plot([0, 1], [1, 0], color=COLORS[0], lw=0.9, ls="-.")
    ax.annotate("initial tangent of the decay\nreaches 0 at $t = \\tau$", (0.85, 0.15), xytext=(2.3, 0.33),
                fontsize=8, color=COLORS[0], ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    labs = {1: ("0.368", "0.632"), 2: ("0.135", "0.865"), 3: ("0.050", "0.950"),
            4: ("0.018", "0.982"), 5: ("0.0067", "0.9933")}
    for n, (dl, rl) in labs.items():
        yd, yr = np.exp(-n), 1 - np.exp(-n)
        ax.plot(n, yd, "o", color=COLORS[0], ms=5, zorder=5)
        ax.plot(n, yr, "s", color=COLORS[1], ms=5, zorder=5)
        ha = "left" if n < 5 else "right"
        dx = 0.08 if n < 5 else -0.08
        ax.text(n + dx, yd + 0.035, dl, fontsize=8, color=COLORS[0], ha=ha, va="bottom")
        ax.text(n + dx, yr - 0.035, rl, fontsize=8, color=COLORS[1], ha=ha, va="top")
    # 10-90 % rise time
    t10, t90 = np.log(1 / 0.9), np.log(10)
    ax.plot([0, t10], [0.1, 0.1], color=GREY, ls=":", lw=1.0)
    ax.plot([0, t90], [0.9, 0.9], color=GREY, ls=":", lw=1.0)
    ax.plot([t10, t10], [0.1, 1.0], color=GREY, ls=":", lw=1.0)
    ax.plot([t90, t90], [0.9, 1.0], color=GREY, ls=":", lw=1.0)
    ax.annotate("", (t90, 0.985), (t10, 0.985),
                arrowprops=dict(arrowstyle="<|-|>", color=GREY, lw=0.9, mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text((t10 + t90) / 2, 1.0, "10–90 % rise time $t_r$ = 2.20$\\tau$", fontsize=8.5, color=INK,
            ha="center", va="bottom")
    ax.text(-0.04, 0.1, "0.1", fontsize=8, color=GREY, ha="right", va="center")
    ax.text(-0.04, 0.9, "0.9", fontsize=8, color=GREY, ha="right", va="center")
    # half-value time
    th = np.log(2)
    ax.plot([th, th], [0, 0.5], color=COLORS[2], ls=":", lw=1.1)
    ax.plot(th, 0.5, "o", color=COLORS[2], ms=5, zorder=6)
    ax.annotate("half-value time $t$ = 0.693$\\tau$", (th, 0.5), xytext=(1.5, 0.5), fontsize=8,
                color=COLORS[2], va="center", arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    ax.set_xlim(0, 5.2)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("normalised time $t/\\tau$")
    ax.set_ylabel("normalised value")
    ax.legend(loc="center right", fontsize=8.5, bbox_to_anchor=(1.0, 0.62))
    save(fig, "06", "fig-6-2-normalised-exponentials")


# ----------------------------------------------------------------------------- Figure 6.3
def _schmitt(ax, x, y, s=0.9):
    ax.add_patch(Polygon([[x, y - s / 2], [x, y + s / 2], [x + s * 0.9, y]], closed=True,
                         fc="white", ec=INK, lw=1.2, zorder=4))
    # hysteresis glyph
    a = s * 0.12
    cx, cy = x + s * 0.32, y
    ax.plot([cx - a, cx + a * 0.4, cx + a * 0.4, cx + a], [cy - a, cy - a, cy + a, cy + a], color=INK, lw=0.8, zorder=5)
    ax.plot([cx - a, cx - a * 0.4, cx - a * 0.4, cx + a], [cy - a, cy - a, cy + a, cy + a], color=INK, lw=0.8, zorder=5)


def fig_6_3():
    fig, ax = new_fig(6.4, 4.0)
    t = np.linspace(0, 500, 1000)
    tau = 100.0
    v = 3.3 * (1 - np.exp(-t / tau))
    tf, ts = tau * 0.95 * 0.8, tau * 1.05 * 1.2
    ax.plot(t, 3.3 * (1 - np.exp(-t / tf)), color=COLORS[0], lw=1.0, alpha=0.45)
    ax.plot(t, 3.3 * (1 - np.exp(-t / ts)), color=COLORS[0], lw=1.0, alpha=0.45)
    ax.plot(t, v, color=COLORS[0], lw=2.0, label="$v = 3.3(1 - e^{-t/100\\,\\mathrm{ms}})$")
    ax.axhline(2.31, color=COLORS[1], ls="--", lw=1.2)
    ax.text(498, 2.36, "threshold $0.7V_{DD}$ = 2.31 V", color=COLORS[1], fontsize=8.5, ha="right", va="bottom")
    ax.axhline(3.3, color=GREY, ls=":", lw=0.8)
    ax.text(498, 3.33, "$V_{DD}$ = 3.3 V", color=GREY, fontsize=8, ha="right", va="bottom")
    for tc, lab, dy in [(91.5, "91.5 ms\nfast corner\n(R −5 %, C −20 %)", 0.0), (120.4, "120.4 ms\nnominal", 0.0),
                        (151.7, "151.7 ms\nslow corner\n(R +5 %, C +20 %)", 0.0)]:
        ax.plot([tc, tc], [0, 2.31], color=COLORS[1], lw=0.9, ls=":")
        ax.plot(tc, 2.31, "o", color=COLORS[1], ms=4.5, zorder=5)
    ax.text(88, 0.08, "91.5 ms\nfast\n(R −5 %,\nC −20 %)", fontsize=7.5, color=COLORS[1], ha="right", va="bottom")
    ax.text(122.5, 0.08, "120.4\nms", fontsize=7.5, color=COLORS[1], ha="left", va="bottom")
    ax.text(154, 0.08, "151.7 ms\nslow\n(R +5 %,\nC +20 %)", fontsize=7.5, color=COLORS[1], ha="left", va="bottom")
    # time constant
    ax.plot(100, 3.3 * (1 - np.exp(-1)), "s", color=COLORS[2], ms=5, zorder=6)
    ax.annotate("$\\tau$ = 100 ms:\n63.2 % → 2.09 V", (100, 2.086), xytext=(170, 1.35), fontsize=8.5,
                color=COLORS[2], arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 3.6)
    ax.set_xlabel("time after power-up (ms)")
    ax.set_ylabel("RESET pin voltage (V)")
    ax.legend(loc="upper left", fontsize=8.5, bbox_to_anchor=(0.0, 1.07), ncol=1)
    # inset circuit
    ins = ax.inset_axes([0.47, 0.04, 0.52, 0.5])
    d = drawing(ins, unit=1.5, fontsize=8)
    d += elm.Vdd().label("3.3 V")
    d += elm.Resistor().down().length(2.2).label("R\n100 kΩ", loc="top")
    d += (n := elm.Dot())
    d += elm.Capacitor().down().length(2.2).label("C\n1 µF", loc="top")
    d += elm.Ground()
    d += elm.Line().at(n.center).right().length(1.6)
    finish(d, ins, xlim=(-2.6, 4.6), ylim=(-5.5, 1.2))
    ins.text(0.25, -2.0, "RESET", fontsize=8, ha="left", va="bottom", color=INK)
    _schmitt(ins, 1.6, -2.2, s=1.3)
    ins.text(2.95, -2.2, "MCU\nSchmitt\ninput", fontsize=7.5, ha="left", va="center", color=INK)
    save(fig, "06", "fig-6-3-power-on-reset")


# ----------------------------------------------------------------------------- Figure 6.4
def fig_6_4():
    fig = plt.figure(figsize=(6.8, 4.8))
    gs = fig.add_gridspec(2, 2, width_ratios=[0.95, 1.6], hspace=0.12, wspace=0.28)
    axs = fig.add_subplot(gs[:, 0])
    a1 = fig.add_subplot(gs[0, 1])
    a2 = fig.add_subplot(gs[1, 1], sharex=a1)

    # schematic
    d = drawing(axs, unit=1.6, fontsize=8)
    X = 4.6
    d += elm.Vdd().at((X, 7.5)).label("+24 V")
    d += elm.Line().at((X, 7.5)).down().length(0.6)
    d += (top := elm.Dot())
    d += elm.Inductor2(loops=4).down().length(1.9).label("$L$\n0.2 H", loc="bottom")
    d += elm.Resistor().down().length(1.9).label("$R$\n40 Ω", loc="bottom")
    d += (dn := elm.Dot())
    d += elm.Line().down().length(0.4)
    d += (q := elm.NFet().right().anchor("drain").label("switch", loc="right", ofst=(0.2, -0.9)))
    d += elm.Ground().at(q.source)
    # suppressor branches between top (6.9) and dn
    ytop, ybot = top.center.y, dn.center.y
    xs = [3.2, 1.7, 0.2]
    d += elm.Line().at(top.center).left().length(X - xs[2])
    d += elm.Line().at(dn.center).left().length(X - xs[2])
    for xx in xs:
        d += elm.Dot().at((xx, ytop))
        d += elm.Dot().at((xx, ybot))
    d += elm.Line().at((xs[0], ybot)).up().length(0.6)
    d += elm.Diode().up().length(ytop - ybot - 1.2).label("(i)", loc="top")
    d += elm.Line().up().length(0.6)
    d += elm.Diode().at((xs[1], ybot)).up().length((ytop - ybot) / 2).label("(ii)", loc="top")
    d += elm.Zener().up().reverse().length((ytop - ybot) / 2).label("24 V", loc="top")
    d += elm.Line().at((xs[2], ybot)).up().length(0.6)
    d += elm.Resistor().up().length(ytop - ybot - 1.2).label("(iii)\n200 Ω", loc="top")
    d += elm.Line().up().length(0.6)
    finish(d, axs, xlim=(-1.7, 6.9), ylim=(-0.6, 9.0))
    axs.text(2.4, ybot - 2.9, "one suppressor fitted:\n(i) diode, (ii) diode + 24 V Zener,\n(iii) 200 Ω resistor",
             fontsize=7.5, ha="center", va="top", color=GREY)
    axs.text(X + 0.15, ybot + 0.1, "$v_{sw}$", fontsize=8.5, ha="left", va="bottom", color=COLORS[0])

    # coil current and switch voltage
    t = np.linspace(-0.5, 10, 2101)
    tm = t * 1e-3
    tau = 5e-3
    I0, R, L = 0.6, 40.0, 0.2
    i_d = np.where(t < 0, I0, (I0 + 0.7 / R) * np.exp(-tm / tau) - 0.7 / R)
    i_z = np.where(t < 0, I0, np.maximum((I0 + 24.7 / R) * np.exp(-tm / tau) - 24.7 / R, 0))
    tau_r = L / (R + 200)
    i_r = np.where(t < 0, I0, I0 * np.exp(-tm / tau_r))
    v_d = np.where(t < 0, 0.0, 24.7)
    v_z = np.where(t < 0, 0.0, np.where(i_z > 0, 48.7, 24.0))
    v_r = np.where(t < 0, 0.0, 24 + 200 * i_r)
    curves = [("(i) diode", i_d, v_d, COLORS[0], 6.52), ("(ii) diode + Zener", i_z, v_z, COLORS[1], 2.31),
              ("(iii) 200 Ω", i_r, v_r, COLORS[2], 1.16)]
    for lab, ii, vv, col, tr in curves:
        a1.plot(t, ii, color=col, label=lab)
        a1.plot(tr, 0.15, "o", color=col, ms=5, zorder=5)
        a2.plot(t, vv, color=col, label=lab)
    a1.axhline(0.15, color=GREY, ls="--", lw=0.9)
    a1.text(3.65, 0.137, "armature releases", fontsize=8, color=GREY, ha="left", va="top")
    a1.annotate("1.16 ms", (1.16, 0.15), xytext=(0.45, 0.04), fontsize=8, color=COLORS[2],
                arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    a1.annotate("2.31 ms", (2.31, 0.15), xytext=(2.5, 0.27), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    a1.annotate("6.52 ms", (6.52, 0.15), xytext=(6.7, 0.25), fontsize=8, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    a1.annotate("zero at 3.39 ms", (3.39, 0.0), xytext=(4.3, 0.035), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    a1.set_ylim(0, 0.68)
    a1.set_ylabel("coil current (A)")
    a1.legend(loc="upper right", fontsize=8)
    plt.setp(a1.get_xticklabels(), visible=False)
    a1.axvline(0, color=GREY, lw=0.6)
    a1.text(0.1, 0.62, "switch off at $t$ = 0", fontsize=8, color=GREY, ha="left")

    a2.text(9.9, 26.5, "(i) 24.7 V", fontsize=8, color=COLORS[0], ha="right", va="bottom")
    a2.text(1.6, 51, "(ii) 48.7 V until $i$ = 0", fontsize=8, color=COLORS[1], ha="left", va="bottom")
    a2.text(9.9, 18.5, "(ii) back to 24 V", fontsize=8, color=COLORS[1], ha="right", va="top")
    a2.text(0.35, 140, "(iii) 144 V, decays to 24 V\n($\\tau$ = 0.83 ms)", fontsize=8, color=COLORS[2],
            ha="left", va="top")
    a2.axvline(0, color=GREY, lw=0.6)
    a2.set_ylim(0, 155)
    a2.set_xlim(-0.5, 10)
    a2.set_ylabel("switch voltage $v_{sw}$ (V)")
    a2.set_xlabel("time after turn-off (ms)")
    fig.subplots_adjust(left=0.01, right=0.98, top=0.97, bottom=0.1)
    save(fig, "06", "fig-6-4-relay-turn-off-suppression")


# ----------------------------------------------------------------------------- Figure 6.5
def _sq_response(tau, x):
    """Steady-state RC output (0-1 V, 50 % square, period 1) at normalised times x."""
    a = np.exp(-0.5 / tau)
    vmax = (1 - a) / (1 - a * a)
    vmin = vmax * a
    ph = np.mod(x, 1.0)
    v = np.where(ph < 0.5, 1 - (1 - vmin) * np.exp(-ph / tau), vmax * np.exp(-(ph - 0.5) / tau))
    return v, vmax, vmin


def fig_6_5():
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(3, 2, width_ratios=[2.3, 1.0], hspace=0.18, wspace=0.62)
    x = np.linspace(0, 3, 3001)
    sq = (np.mod(x, 1.0) < 0.5).astype(float)
    axes = []
    for k, (tr, tag) in enumerate([(0.1, "(a) $\\tau$ = 0.1$T$"), (1.0, "(b) $\\tau$ = $T$"),
                                   (10.0, "(c) $\\tau$ = 10$T$")]):
        ax = fig.add_subplot(gs[k, 0], sharex=axes[0] if axes else None)
        axes.append(ax)
        ax.plot(x, sq, color=LIGHTGREY, lw=1.4, drawstyle="steps-post")
        v, vmax, vmin = _sq_response(tr, x)
        ax.plot(x, v, color=COLORS[0], lw=1.8)
        ax.axhline(vmax, color=COLORS[1], lw=0.7, ls=":")
        ax.axhline(vmin, color=COLORS[1], lw=0.7, ls=":")
        ax.set_ylim(-0.05, 1.12)
        ax.set_yticks([0, 0.5, 1])
        ax.set_ylabel("V")
        ax.text(0.01, 1.11, tag, transform=ax.transData, fontsize=9, va="top", ha="left",
                bbox=dict(fc="white", ec="none", pad=0.5))
        lab = f"max {vmax:.3f}\nmin {vmin:.3f}"
        ax.text(3.04, 0.5, lab, fontsize=8, color=COLORS[1], ha="left", va="center")
        if k < 2:
            plt.setp(ax.get_xticklabels(), visible=False)
    axes[1].text(1.25, 0.2, "shark-fin", fontsize=8, color=COLORS[0])
    axes[2].text(1.05, 0.2, "small triangular ripple, 0.025 V p-p", fontsize=8, color=COLORS[0],
                 bbox=dict(fc="white", ec="none", pad=0.6))
    axes[-1].set_xlim(0, 3)
    axes[-1].set_xlabel("$t/T$  (periodic steady state; grey: 0–1 V input square wave)")

    # PWM DAC panel
    ax = fig.add_subplot(gs[:, 1])
    T = 50.0  # us
    tau = 1000.0
    a = np.exp(-25.0 / tau)
    vmax = 3.3 * (1 - a) / (1 - a * a)
    vmin = vmax * a
    tt = np.linspace(0, 150, 1501)
    ph = np.mod(tt, T)
    vv = np.where(ph < 25, 3.3 - (3.3 - vmin) * np.exp(-ph / tau), vmax * np.exp(-(ph - 25) / tau))
    ax.plot(tt, vv * 1e3, color=COLORS[0], lw=1.8)
    ax.axhline(vmax * 1e3, color=COLORS[1], ls=":", lw=0.8)
    ax.axhline(vmin * 1e3, color=COLORS[1], ls=":", lw=0.8)
    ax.axhline(1650, color=GREY, ls="--", lw=0.6)
    ax.set_ylim(1620, 1682)
    ax.set_xlim(0, 150)
    ax.set_xticks([0, 50, 100, 150])
    ax.set_xlabel("time (µs)")
    ax.set_ylabel("output (mV)")
    ax.text(75, 1674, "1.671 V", fontsize=8, color=COLORS[1], ha="center", va="bottom")
    ax.text(75, 1626, "1.629 V", fontsize=8, color=COLORS[1], ha="center", va="top")
    ax.set_title("PWM DAC: 3.3 V, 20 kHz,\n$D$ = 0.5, $\\tau$ = 1 ms\nripple 41.2 mV p-p\n(dashed: 1.65 V average)", fontsize=8.5)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.09)
    save(fig, "06", "fig-6-5-square-wave-response")


# ----------------------------------------------------------------------------- Figure 6.6
def _ecg_beat(t):
    """Schematic ECG complex (mV) centred at t = 0: P, QRS and T waves."""
    g = lambda mu, s, a: a * np.exp(-0.5 * ((t - mu) / s) ** 2)  # noqa: E731
    return g(-0.2, 0.025, 0.15) + g(-0.03, 0.008, -0.1) + g(0.0, 0.012, 1.0) + g(0.03, 0.008, -0.25) + g(0.25, 0.05, 0.3)


def fig_6_6():
    fig = plt.figure(figsize=(6.8, 5.2))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.45, 1.2, 1.5], hspace=0.55, wspace=0.3)
    ai = fig.add_subplot(gs[0, 0])
    aa = fig.add_subplot(gs[1, 0], sharex=ai)
    ab = fig.add_subplot(gs[0:2, 1])
    ac = fig.add_subplot(gs[2, :])

    # (a) input
    x = np.linspace(-0.5, 5, 1101)
    ai.plot(x, (x >= 0).astype(float), color=COLORS[1], ls="--", lw=1.2, drawstyle="steps-post")
    ai.annotate("", (0, 1.35), (0, 0), arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=10,
                                                         shrinkA=0, shrinkB=0))
    ai.text(0.12, 1.3, "$\\delta(t)$", color=COLORS[0], fontsize=9, va="top")
    ai.text(4.9, 1.05, "$u(t)$", color=COLORS[1], fontsize=9, ha="right", va="bottom")
    ai.set_ylim(0, 1.5)
    ai.set_yticks([0, 1])
    ai.set_ylabel("input", fontsize=8.5)
    plt.setp(ai.get_xticklabels(), visible=False)
    ai.set_title("(a) RC low-pass, $\\tau$ = 1", fontsize=9.5, loc="left", pad=3)
    s = np.where(x >= 0, 1 - np.exp(-x), 0)
    h = np.where(x >= 0, np.exp(-x), 0)
    aa.plot(x, s, color=COLORS[1], ls="--", label="step response $s(t) = 1 - e^{-t/\\tau}$")
    aa.plot(x, h, color=COLORS[0], label="impulse response $h(t) = (1/\\tau)e^{-t/\\tau}$")
    aa.set_xlim(-0.5, 5)
    aa.set_ylim(0, 1.15)
    aa.set_xlabel("$t/\\tau$")
    aa.set_ylabel("output")
    aa.text(2.3, 0.25, "$h = ds/dt$", fontsize=8.5, color=COLORS[0])
    aa.text(1.4, 0.9, "$s(t)$", fontsize=9, color=COLORS[1])
    aa.text(0.5, 0.85, "$h(t)$", fontsize=9, color=COLORS[0])

    # (b) charge-sensitive detector
    tb = np.linspace(-5, 50, 1101)
    vb = np.where(tb >= 0, 100 * np.exp(-tb / 10), 0)
    ab.plot(tb, vb, color=COLORS[0])
    ab.axvline(0, color=GREY, lw=0.6)
    ab.set_xlim(-5, 50)
    ab.set_ylim(0, 115)
    ab.set_xlabel("time (µs)")
    ab.set_ylabel("node voltage (mV)")
    ab.set_title("(b) 1 pC into 10 pF ∥ 1 MΩ", fontsize=9.5, loc="left", pad=3)
    ab.text(1.5, 103, "jump $Q/C$ = 100 mV", fontsize=8.5, color=COLORS[0], va="center")
    ab.plot(10, 100 * np.exp(-1), "o", color=COLORS[0], ms=4.5)
    ab.text(12, 40, "$\\tau = RC$ = 10 µs\n(36.8 mV)", fontsize=8.5, color=COLORS[0], va="bottom")

    # (c) ECG baseline recovery
    tc = np.linspace(0, 20, 40001)
    for tau, col, lab, tx in [(3.18, COLORS[1], "0.05 Hz corner, $\\tau$ = 3.18 s", 18.2),
                              (0.318, COLORS[0], "0.5 Hz corner, $\\tau$ = 0.318 s", 1.82)]:
        base = 300 * np.exp(-tc / tau)
        if tau < 1:
            beats = sum(_ecg_beat(tc - tb0) for tb0 in np.arange(0.4, 20, 0.8))
            y = base + beats
            y = np.where(y > 0.1, y, np.nan)
            ac.semilogy(tc, y, color=col, lw=1.2, label=lab + " (with 1 mV ECG)")
        else:
            ac.semilogy(tc, base, color=col, lw=1.8, label=lab)
        ac.plot(tx, 1.0, "o", color=col, ms=6, zorder=5)
    ac.axhline(1.0, color=GREY, ls="--", lw=0.9)
    ac.text(10.0, 1.12, "1 mV (size of the ECG)", fontsize=8, color=GREY, ha="center", va="bottom")
    ac.annotate("1.82 s", (1.82, 1.0), xytext=(2.6, 9), fontsize=8.5, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ac.annotate("18.2 s", (18.2, 1.0), xytext=(16.4, 5), fontsize=8.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    ac.set_xlim(0, 20)
    ac.set_ylim(0.1, 500)
    ac.set_yticks([0.1, 1, 10, 100])
    ac.set_yticklabels(["0.1", "1", "10", "100"])
    ac.set_xticks(range(0, 21, 2))
    ac.set_xlabel("time after a 300 mV electrode-offset step (s)")
    ac.set_ylabel("output (mV)")
    ac.legend(loc="upper right", fontsize=8)
    ac.set_title("(c) AC-coupled ECG amplifier: baseline recovery", fontsize=9.5, loc="left", pad=3)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.08)
    save(fig, "06", "fig-6-6-step-impulse-ecg-baseline")


if __name__ == "__main__":
    fig_6_1()
    fig_6_2()
    fig_6_3()
    fig_6_4()
    fig_6_5()
    fig_6_6()
