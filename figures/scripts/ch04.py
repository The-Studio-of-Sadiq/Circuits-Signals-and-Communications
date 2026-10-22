"""Figures for Chapter 4 — Network Theorems.

Run from the repository root:  python figures/scripts/ch04.py
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
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


# ----------------------------------------------------------------------------- Figure 4.1
def _charging_panel(ax, alt=True, batt=True, title="", node_note="", il_label="$I_L$"):
    d = drawing(ax, unit=2.0, fontsize=8.5)
    if alt:
        d += elm.SourceV().up().length(3).label("14.4 V", loc="top")
    else:
        d += elm.Line().up().length(3).color(COLORS[1]).label("short", loc="top", color=COLORS[1])
    d += (w1 := elm.Line().right().length(1.3))
    if alt and batt:
        d += elm.CurrentLabelInline(direction="in", ofst=0.3).at(w1).label("$I_{alt}$", loc="top")
    d += elm.Resistor().right().length(2.0).label("0.05 Ω")
    d += elm.Line().right().length(0.7)
    d += elm.Dot()
    d.push()
    d += (load := elm.Resistor().down().length(3).label("0.5 Ω", loc="top"))
    d += elm.CurrentLabel(top=True, ofst=0.3, length=1.0).at(load).label(il_label)
    d += elm.Dot()
    d.pop()
    d += elm.Line().right().length(0.7)
    d += elm.Resistor().right().length(2.0).label("0.02 Ω")
    d += (w2 := elm.Line().right().length(1.3))
    if batt:
        if alt:
            d += elm.CurrentLabelInline(direction="in", ofst=0.3).at(w2).label("$I_{batt}$", loc="bottom")
        d += elm.SourceV().down().length(3).reverse().label("12.6 V", loc="bottom")
    else:
        d += elm.Line().down().length(3).color(COLORS[1]).label("short", loc="bottom", color=COLORS[1])
    d += elm.Line().left().length(8.0)
    finish(d, ax, xlim=(-2.0, 10.3), ylim=(-1.1, 3.9))
    ax.set_title(title, fontsize=9.5, pad=2)
    if node_note:
        ax.text(4.0, -0.4, node_note, ha="center", va="top", fontsize=8.5, color=COLORS[0])


def fig_4_1():
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.0))
    axs = axs.ravel()
    _charging_panel(axs[0], True, True, "(a) alternator and battery",
                    "$v_L$ = 12.75 V,  $I_L$ = 25.5 A")
    _charging_panel(axs[1], True, False, "(b) alternator alone (battery source shorted)",
                    "$v_L'$ = 4.00 V,  $I_L'$ = 8.0 A", il_label="$I_L'$")
    _charging_panel(axs[2], False, True, "(c) battery alone (alternator source shorted)",
                    "$v_L''$ = 8.75 V,  $I_L''$ = 17.5 A", il_label="$I_L''$")
    ax = axs[3]
    ax.axis("off")
    ax.text(0.5, 0.5, "Superposition:\n\n$v_L = v_L' + v_L''$\n= 4.00 + 8.75 = 12.75 V\n\n"
            "$I_L = I_L' + I_L''$\n= 8.0 + 17.5 = 25.5 A",
            ha="center", va="center", fontsize=10, color=INK, transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.6", fc="#F4F4F4", ec=GREY, lw=0.6))
    fig.subplots_adjust(left=0.005, right=0.995, top=0.94, bottom=0.01, wspace=0.04, hspace=0.18)
    save(fig, "04", "fig-4-1-superposition-alternator-battery")


# ----------------------------------------------------------------------------- Figure 4.2
def fig_4_2():
    fig = plt.figure(figsize=(6.8, 3.9))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 2.1], wspace=0.25, hspace=0.25)
    ax_th = fig.add_subplot(gs[0, 0])
    ax_no = fig.add_subplot(gs[1, 0])
    ax = fig.add_subplot(gs[:, 1])

    # Thevenin equivalent
    d = drawing(ax_th, unit=1.6, fontsize=8.5)
    d += elm.SourceV().up().length(2.4).label("12 V", loc="top")
    d += elm.Resistor().right().length(2.2).label("4 Ω")
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Gap().down().length(2.4)
    d += elm.Dot(open=True).label("b", loc="right")
    d += elm.Line().left().length(2.2)
    finish(d, ax_th, pad=0.3)
    ax_th.set_title("Thévenin", fontsize=9, pad=1)

    # Norton equivalent
    d = drawing(ax_no, unit=1.6, fontsize=8.5)
    d += elm.SourceI().up().length(2.4).label("3 A", loc="top")
    d += elm.Line().right().length(1.3)
    d.push()
    d += elm.Resistor().down().length(2.4).label("4 Ω", loc="bottom")
    d.pop()
    d += elm.Line().right().length(1.0)
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Gap().down().length(2.4)
    d += elm.Dot(open=True).label("b", loc="right")
    d += elm.Line().left().length(2.3)
    finish(d, ax_no, pad=0.3)
    ax_no.set_title("Norton", fontsize=9, pad=1)

    # Main plot
    i = np.linspace(0, 3.0, 200)
    ax.plot(i, 12 - 4 * i, color=COLORS[0], lw=2.2)
    ax.add_patch(Rectangle((0, 0), 1.5, 6.0, fc=COLORS[4], alpha=0.22, ec="none"))
    ax.text(0.75, 3.0, "$P$ = 9 W", ha="center", va="center", fontsize=9.5, color=INK)
    ii = np.linspace(0, 3.5, 50)
    for RL, col, op, lab_xy in [(1, COLORS[2], (2.4, 2.4), (2.85, 3.85)),
                                (4, COLORS[1], (1.5, 6.0), (2.95, 10.6)),
                                (16, COLORS[3], (0.6, 9.6), (0.92, 13.0))]:
        ax.plot(ii, RL * ii, color=col, lw=1.2, ls="--")
        ax.plot(*op, "o", color=col, ms=6, zorder=5)
        ax.text(*lab_xy, f"$R_L$ = {RL} Ω", color=col, fontsize=8.5,
                ha="left" if RL != 16 else "left", va="center")
    ax.annotate("(2.4 A, 2.4 V)", (2.4, 2.4), xytext=(2.55, 1.1), fontsize=8, color=COLORS[2],
                arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    ax.annotate("(1.5 A, 6 V)", (1.5, 6.0), xytext=(1.75, 7.6), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    ax.annotate("(0.6 A, 9.6 V)", (0.6, 9.6), xytext=(1.0, 10.6), fontsize=8, color=COLORS[3],
                arrowprops=dict(arrowstyle="-", color=COLORS[3], lw=0.6))
    ax.plot(0, 12, "s", color=COLORS[0], ms=5)
    ax.plot(3, 0, "s", color=COLORS[0], ms=5)
    ax.text(0.06, 12.35, "$v_{oc}$ = 12 V", fontsize=9, color=COLORS[0], va="bottom")
    ax.text(3.02, 0.35, "$i_{sc}$ = 3 A", fontsize=9, color=COLORS[0], ha="left", va="bottom")
    ax.text(2.25, 6.0, "source line\n$v = 12 - 4i$\nslope $-R_{Th}$ = −4 Ω", fontsize=8.5,
            color=COLORS[0], ha="left", va="center")
    ax.set_xlim(0, 3.5)
    ax.set_ylim(0, 13.5)
    ax.set_xlabel("terminal current $i$ (A)")
    ax.set_ylabel("terminal voltage $v$ (V)")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.13)
    save(fig, "04", "fig-4-2-thevenin-norton-iv-line")


# ----------------------------------------------------------------------------- Figure 4.3
def fig_4_3():
    fig = plt.figure(figsize=(6.8, 3.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.08)
    axb = fig.add_subplot(gs[0, 0])
    axt = fig.add_subplot(gs[0, 1])

    # Bridge
    d = drawing(axb, unit=2.0, fontsize=8.5)
    d += elm.SourceV().up().length(5).label("E\n5.000 V", loc="top")
    d += elm.Line().right().length(3.6)
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().length(2.5).label("R = 350 Ω", loc="top")
    d += (A := elm.Dot())
    d += elm.ResistorVar().down().length(2.5).label("$R_g$ = 350.70 Ω\n(active gauge)", loc="top")
    d += elm.Dot()
    d.pop()
    d += elm.Line().right().length(3.6)
    d += elm.Resistor().down().length(2.5).label("350 Ω", loc="bottom")
    d += (B := elm.Dot())
    d += elm.Resistor().down().length(2.5).label("350 Ω", loc="bottom")
    d += elm.Line().left().length(7.2)
    d += elm.Resistor().at(A.center).to(B.center).color(COLORS[0]).label("$R_m$", color=COLORS[0])
    finish(d, axb, pad=0.3)
    axb.text(3.6 + 0.15, 2.5 + 0.2, "A", ha="left", va="bottom", fontsize=9, fontweight="bold")
    axb.text(7.2 - 0.15, 2.5 + 0.2, "B", ha="right", va="bottom", fontsize=9, fontweight="bold")
    axb.text(5.4, 2.0, "instrument\ninput", ha="center", va="top", fontsize=8, color=COLORS[0])
    axb.set_title("(a) quarter bridge", fontsize=9.5, pad=2)

    # Thevenin equivalent
    d = drawing(axt, unit=2.0, fontsize=8.5)
    d += elm.SourceV().up().length(3).label("$V_{Th}$\n2.498 mV", loc="top")
    d += elm.Resistor().right().length(3).label("$R_{Th}$ = 350.17 Ω")
    d += elm.Dot()
    d += elm.Resistor().down().length(3).color(COLORS[0]).label("$R_m$", loc="bottom", color=COLORS[0])
    d += elm.Dot()
    d += elm.Line().left().length(3)
    finish(d, axt, pad=0.3, ylim=(-3.3, 3.8))
    axt.text(2.55, 1.5, "+\n$v_m$\n−", ha="right", va="center", fontsize=9, color=COLORS[0], linespacing=1.1)
    axt.set_title("(b) Thévenin equivalent at A–B", fontsize=9.5, pad=2)
    rows = [("$R_m$", "$v_m$", "error"), ("10 kΩ", "2.413 mV", "−3.4 %"), ("1 MΩ", "2.4966 mV", "−0.035 %")]
    xs = [-0.6, 1.5, 3.6]
    for r, row in enumerate(rows):
        for c, txt in enumerate(row):
            axt.text(xs[c], -1.1 - 0.62 * r, txt, ha="center", va="center", fontsize=8.5,
                     fontweight="bold" if r == 0 else "normal", color=INK)
    axt.plot([-1.4, 4.5], [-1.42, -1.42], color=GREY, lw=0.6)
    axt.text(1.5, -3.15, "$v_m = V_{Th}\\,R_m/(R_m+R_{Th})$", ha="center", fontsize=8.5, color=GREY)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.02)
    save(fig, "04", "fig-4-3-strain-bridge-thevenin")


# ----------------------------------------------------------------------------- Figure 4.4
def fig_4_4():
    fig, ax = new_fig(6.4, 3.9)
    x = np.logspace(-1, 1, 400)
    p = 4 * x / (1 + x) ** 2
    eta = 100 * x / (1 + x)
    l1, = ax.plot(x, p, color=COLORS[0], lw=2.0, label="$P_L/P_{max} = 4x/(1+x)^2$")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 10)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("load ratio $x = R_L/R_{Th}$")
    ax.set_ylabel("$P_L/P_{max}$", color=COLORS[0])
    ax.tick_params(axis="y", colors=COLORS[0])
    ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    l2, = ax2.plot(x, eta, color=COLORS[1], lw=2.0, ls="--", label="$\\eta = 100\\,x/(1+x)$ %")
    ax2.set_ylim(0, 112)
    ax2.set_ylabel("efficiency $\\eta$ (%)", color=COLORS[1])
    ax2.tick_params(axis="y", colors=COLORS[1])
    ax.axvline(1, color=INK, ls=":", lw=1.2)
    ax.text(1.06, 0.36, "matched:\n$P = P_{max}$, $\\eta$ = 50 %", fontsize=8.5, va="center")
    for xx in (0.5, 2):
        ax.plot(xx, 8 / 9, "o", color=COLORS[0], ms=5)
    ax.annotate("0.889 at $x$ = 0.5", (0.5, 0.889), xytext=(0.13, 0.80), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.annotate("0.889 at $x$ = 2", (2, 0.889), xytext=(2.6, 0.97), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.plot(1, 1, "o", color=COLORS[0], ms=5)
    # regimes
    ax.annotate("RF links, antennas,\nenergy harvesting\n(operate near $x$ = 1)", xy=(0.9, 0.975),
                xytext=(0.12, 0.45), fontsize=8, color=INK, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=9))
    ax.annotate("power systems,\naudio amplifiers\n(operate at $x \\gg 1$)", xy=(8.0, 0.87),
                xytext=(2.6, 0.16), fontsize=8, color=INK, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=9))
    ax.legend(handles=[l1, l2], loc="upper left", fontsize=8.5, bbox_to_anchor=(0.0, 1.12), ncol=2)
    save(fig, "04", "fig-4-4-max-power-efficiency")


# ----------------------------------------------------------------------------- Figure 4.5
def _recip_panel(ax, src_at_1=True):
    d = drawing(ax, unit=2.0, fontsize=8)
    h = 3.0
    # ground rail and left element
    d += elm.Line().at((-2.9, 0)).right().length(2.9 + 8.9)
    left_el = (elm.SourceV().label("10 V", loc="top") if src_at_1
               else elm.MeterA().color(COLORS[1]))
    d += left_el.at((-2.9, 0)).up().length(h)
    d += elm.Line().right().length(2.9)
    d += (n1 := elm.Dot())
    d += elm.Resistor().right().length(3).label("1 k", loc="bottom")
    d += (n3 := elm.Dot())
    d += elm.Resistor().right().length(3).label("3 k", loc="bottom")
    d += (n2 := elm.Dot())
    d += elm.Line().right().length(2.9)
    right_el = (elm.MeterA().color(COLORS[1]) if src_at_1
                else elm.SourceV().reverse().label("10 V", loc="bottom"))
    d += right_el.down().length(h)
    # shunt resistors
    d += elm.Resistor().at(n1.center).down().length(h).label("2 k", loc="bottom")
    d += elm.Dot()
    d += elm.Resistor().at(n3.center).down().length(h).label("4 k", loc="bottom")
    d += elm.Dot()
    # 5 k over the top
    d += elm.Line().at(n1.center).up().length(1.4)
    d += elm.Resistor().right().length(6).label("5 k")
    d += elm.Line().down().length(1.4)
    d += elm.Ground().at((3.0, 0))
    finish(d, ax, xlim=(-4.4, 10.4), ylim=(-1.6, 5.4))
    ax.text(8.9 if src_at_1 else -2.9, h + 0.55, "4.105 mA", ha="center", va="center", fontsize=8.5,
            color=COLORS[1], fontweight="bold")
    v3 = "6.316 V" if src_at_1 else "2.105 V"
    ax.text(3.0, h + 0.75, f"$v_3$ = {v3}", fontsize=8.5, color=COLORS[0], ha="center", va="center")
    for xn, lab, ha in [(0.0, "1", "right"), (3.0, "3", "left"), (6.0, "2", "left")]:
        ax.text(xn + (0.15 if ha == "left" else -0.15), h + 0.12, lab, fontsize=9, fontweight="bold",
                ha=ha, va="bottom")


def fig_4_5():
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 2.9))
    _recip_panel(axs[0], True)
    _recip_panel(axs[1], False)
    axs[0].set_title("(a) source at port 1, ammeter at port 2", fontsize=9, pad=2)
    axs[1].set_title("(b) source at port 2, ammeter at port 1", fontsize=9, pad=2)
    for ax in axs:
        ax.text(3.0, -1.35, "transfer resistance 10 V / 4.105 mA = 2.436 kΩ", ha="center",
                fontsize=8.5, color=INK, bbox=dict(boxstyle="round,pad=0.25", fc="#F4F4F4", ec=GREY, lw=0.5))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.02, wspace=0.06)
    save(fig, "04", "fig-4-5-reciprocity-swap")


# ----------------------------------------------------------------------------- Figure 4.6
def fig_4_6():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    d = drawing(ax, unit=2.0, fontsize=8.5)
    H = 6.0
    xs = [0, 5.0, 10.0, 15.0]
    d += elm.Line().at((0, H)).right().length(15.0)
    d += elm.Line().at((0, 0)).right().length(15.0)
    data = [("A", "54.0 V", "0.10 Ω", "15.5 A"), ("B", "53.2 V", "0.08 Ω", "9.4 A"),
            ("C", "52.6 V", "0.12 Ω", "1.3 A")]
    for x, (nm, V, R, I) in zip(xs[:3], data):
        d += elm.Dot().at((x, 0))
        d += elm.SourceV().at((x, 0)).up().length(3.0).label(V, loc="top")
        d += (r := elm.Resistor().up().length(3.0).label(R, loc="top"))
        d += elm.CurrentLabel(top=False, ofst=0.3, length=1.2).at(r).label(I, color=COLORS[1]).color(COLORS[1])
        d += elm.Dot()
        ax.text(x, -0.65, f"string {nm}", ha="center", va="center", fontsize=9, fontweight="bold")
    d += elm.Dot().at((15.0, H))
    d += (rl := elm.Resistor().at((15.0, H)).down().length(H).label("2.0 Ω", loc="bottom"))
    d += elm.CurrentLabel(top=False, ofst=0.3, length=1.2).at(rl).label("26.2 A", color=COLORS[1]).color(COLORS[1])
    ax.text(15.0, -0.65, "load", ha="center", va="center", fontsize=9, fontweight="bold")
    finish(d, ax, xlim=(-2.6, 18.2), ylim=(-4.6, 7.3))
    ax.text(7.5, H + 0.35, "bus  $V$ = 52.45 V", ha="center", va="bottom", fontsize=10, color=COLORS[0])
    ax.text(7.5, -1.55, r"Millman:  $V = \Sigma G_kV_k / \Sigma G_k$ = 1643.3 / 31.33 = 52.45 V",
            ha="center", va="center", fontsize=9, color=INK)
    ax.text(7.5, -3.3, "No load (2.0 Ω removed):  bus 53.30 V\n"
            "A delivers 7.0 A,  B absorbs 1.2 A,  C absorbs 5.8 A  (circulating currents)",
            ha="center", va="center", fontsize=8.5, color=INK, linespacing=1.4,
            bbox=dict(boxstyle="round,pad=0.45", fc="#FFF6E5", ec=COLORS[4], lw=0.9))
    save(fig, "04", "fig-4-6-millman-battery-strings")


if __name__ == "__main__":
    fig_4_1()
    fig_4_2()
    fig_4_3()
    fig_4_4()
    fig_4_5()
    fig_4_6()
