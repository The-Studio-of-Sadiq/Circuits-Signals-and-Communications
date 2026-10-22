"""Figures for Chapter 1 — Electrical Quantities and Circuit Models.

Run from the repository root:  python figures/scripts/ch01.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")
BLUE, RED, GREEN = COLORS[0], COLORS[1], COLORS[2]


def _sd(ax, fontsize=9, unit=2.5):
    d = schemdraw.Drawing(canvas=ax, show=False)
    d.config(fontsize=fontsize, unit=unit, lw=1.2)
    return d


def _finish(d, ax, xlim=None, ylim=None, pad=0.4):
    d.draw(show=False)
    bb = d.get_bbox()
    ax.set_xlim(*(xlim or (bb.xmin - pad, bb.xmax + pad)))
    ax.set_ylim(*(ylim or (bb.ymin - pad, bb.ymax + pad)))
    ax.set_aspect("equal")
    ax.axis("off")


# ---------------------------------------------------------------- Figure 1.1
def fig_1_1():
    fig, ax = schematic(6.6, 5.0, xlim=(0, 13.2), ylim=(-0.7, 9.2))

    def element(x0, title, entering):
        cx = x0 + 3.0
        ax.text(cx, 8.85, title, ha="center", va="center", fontsize=10, weight="bold")
        # terminals and leads
        ax.plot([cx, cx], [7.6, 6.5], color=INK, lw=1.4)
        ax.plot([cx, cx], [4.5, 3.6], color=INK, lw=1.4)
        ax.add_patch(Rectangle((cx - 0.6, 4.5), 1.2, 2.0, fc="#EEF3F8", ec=INK, lw=1.4))
        for y, lab in ((7.6, "a"), (3.6, "b")):
            ax.plot(cx, y, "o", ms=6, mfc="white", mec=INK, mew=1.3)
            ax.text(cx - 0.35, y, lab, ha="right", va="center", fontsize=10, style="italic")
        ax.text(cx + 1.0, 6.25, "+", ha="center", va="center", fontsize=14, color=RED)
        ax.text(cx + 1.0, 4.75, "−", ha="center", va="center", fontsize=14, color=RED)
        ax.text(cx + 1.25, 5.5, r"$v$", ha="left", va="center", fontsize=12, color=RED)
        # current arrow alongside upper lead
        if entering:
            arrow(ax, cx - 0.55, 7.5, cx - 0.55, 6.7, color=BLUE)
        else:
            arrow(ax, cx - 0.55, 6.7, cx - 0.55, 7.5, color=BLUE)
        ax.text(cx - 0.75, 7.1, r"$i$", ha="right", va="center", fontsize=12, color=BLUE)
        txt = r"$p_{\mathrm{absorbed}} = v\,i$" if entering else r"$p_{\mathrm{absorbed}} = -v\,i$"
        ax.text(cx, 3.05, txt, ha="center", va="center", fontsize=11)
        sub = "(current reference enters +)" if entering else "(current reference leaves +)"
        ax.text(cx, 8.3, sub, ha="center", va="center", fontsize=8.5, color="#555555")

    element(0.5, "Passive sign convention", True)
    element(6.7, "Current leaving +", False)
    ax.plot([6.6, 6.6], [3.4, 9.0], color="#BBBBBB", lw=0.8, ls=":")

    cases = [
        ("Car battery, charging",
         "14.2 V, i = +8 A entering +\n" r"$p = 14.2\times8 = +113.6$ W" "\nabsorbs 113.6 W"),
        ("Car battery, cranking",
         "11.4 V, 150 A leaving +\n" r"(i = −150 A): $p = -1710$ W" "\ndelivers 1.71 kW"),
        ("Resistor, reversed ref.",
         "5 V, i = −2 mA entering +\n" r"$p = 5\times(-2\ \mathrm{mA}) = -10$ mW" "\n"
         "actual 2 mA flows the other\nway: using the actual\ndirection, p = +10 mW"),
    ]
    for k, (head, body) in enumerate(cases):
        x = 0.15 + k * 4.35
        box(ax, x, -0.6, 4.15, 3.0, fc="#F6F6F6")
        ax.text(x + 2.075, 2.1, head, ha="center", va="center", fontsize=8.6, weight="bold")
        ax.text(x + 2.075, 0.75, body, ha="center", va="center", fontsize=7.8, linespacing=1.35)
    save(fig, "01", "fig-1-1-passive-sign-convention")


# ---------------------------------------------------------------- Figure 1.2
def fig_1_2():
    Vs, Rs, RL = 1.5, 0.15, 2.0
    Isc = Vs / Rs
    iop = Vs / (Rs + RL)
    vop = iop * RL
    fig, ax = new_fig(6.4, 4.0)
    ax.axvspan(1.25, 1.5, color=BLUE, alpha=0.08, lw=0)
    ax.text(1.375, 7.6, "nearly ideal\nvoltage source\nwhen $R_{load}\\gg R_s$",
            ha="center", va="center", fontsize=8.2, color=BLUE)
    ax.axvline(Vs, color=COLORS[3], lw=1.6, ls="--")
    ax.text(Vs + 0.02, 5.2, "ideal voltage\nsource 1.5 V", ha="left", va="center", fontsize=8.5,
            color=COLORS[3])
    ax.axhline(Isc, color=COLORS[4], lw=1.6, ls="--")
    ax.text(0.55, Isc + 0.25, "ideal current source 10 A", ha="left", va="bottom", fontsize=8.5,
            color="#A06A00")
    v = np.linspace(0, Vs, 50)
    ax.plot(v, (Vs - v) / Rs, color=BLUE, lw=2)
    ax.annotate("practical source:\n" r"1.5 V, $R_s=0.15\ \Omega$", xy=(0.75, 5.0),
                xytext=(0.33, 3.2), ha="center", va="center", fontsize=8.5, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
    vl = np.linspace(0, 1.8, 50)
    ax.plot(vl, vl / RL, color=RED, lw=1.8)
    ax.text(0.45, 0.45 / RL + 0.3, r"load line $i=v\,/\,2\ \Omega$", ha="center",
            va="bottom", fontsize=8.5, color=RED)
    ax.plot(vop, iop, "o", color=INK, ms=6, zorder=5)
    ax.annotate(f"operating point\n({vop:.3f} V, {iop:.3f} A)", xy=(vop, iop), xytext=(1.05, 2.3),
                fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.plot(Vs, 0, "s", color=BLUE, ms=6, clip_on=False, zorder=5)
    ax.annotate("open-circuit\nvoltage 1.5 V", xy=(Vs, 0), xytext=(1.66, 2.6), ha="center",
                fontsize=8.2, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.plot(0, Isc, "s", color=BLUE, ms=6, clip_on=False, zorder=5)
    ax.annotate("short-circuit\ncurrent 10 A", xy=(0, Isc), xytext=(0.22, 8.4), ha="center",
                fontsize=8.2, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.set_xlim(0, 1.8)
    ax.set_ylim(0, 11)
    ax.set_xlabel("terminal voltage $v$ (V)")
    ax.set_ylabel("delivered current $i$ (A)")
    ax.grid(True, lw=0.5)
    save(fig, "01", "fig-1-2-source-iv-characteristics")


# ---------------------------------------------------------------- Figure 1.3
def fig_1_3():
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    d = _sd(ax, fontsize=9, unit=2.0)
    with d:
        kinds = [("VCVS", "v", "V", r"$v_o=\mu\,v_x$"),
                 ("CCVS", "i", "V", r"$v_o=r_m\,i_x$"),
                 ("VCCS", "v", "I", r"$i_o=g_m\,v_x$"),
                 ("CCCS", "i", "I", r"$i_o=\beta\,i_x$")]
        y0 = 7.0
        for k, (name, ctrl, out, rel) in enumerate(kinds):
            x = k * 4.0
            # controlling branch
            if ctrl == "v":
                elm.Dot(open=True).at((x, y0 + 2.0))
                elm.Dot(open=True).at((x, y0))
                elm.Label().at((x + 0.35, y0 + 1.0)).label(r"$v_x$", fontsize=10, color=RED)
                elm.Label().at((x + 0.35, y0 + 1.6)).label("+", fontsize=11, color=RED)
                elm.Label().at((x + 0.35, y0 + 0.4)).label("−", fontsize=11, color=RED)
            else:
                elm.Line().at((x, y0)).to((x, y0 + 2.0))
                elm.Dot(open=True).at((x, y0 + 2.0))
                elm.Dot(open=True).at((x, y0))
                elm.Arrow().at((x - 0.35, y0 + 0.6)).to((x - 0.35, y0 + 1.4)).color(BLUE)
                elm.Label().at((x - 0.45, y0 + 1.0)).label(r"$i_x$", fontsize=10, halign="right",
                                                           color=BLUE)
            if out == "V":
                elm.SourceControlledV().at((x + 1.6, y0)).up().length(2.0)
            else:
                elm.SourceControlledI().at((x + 1.6, y0)).up().length(2.0)
            elm.Label().at((x + 0.8, y0 - 0.6)).label(f"{name}", fontsize=9.5)
            elm.Label().at((x + 0.8, y0 - 1.25)).label(rel, fontsize=10)
        # hybrid-pi amplifier
        yb = 0.0
        vs = elm.SourceSin().at((0.5, yb)).up().length(3.0).label(r"$v_s$", loc="bot")
        elm.Resistor().at(vs.end).right().length(3.0).label(r"$R_s = 1\ \mathrm{k\Omega}$")
        b = elm.Dot().label("b", loc="top")
        rpi = elm.Resistor().at(b.end).down().length(3.0).label(
            r"$r_\pi=2.585\ \mathrm{k\Omega}$", loc="bot", ofst=0.15)
        elm.Label().at((3.15, 2.45)).label("+", fontsize=11, color=RED)
        elm.Label().at((3.15, 0.55)).label("−", fontsize=11, color=RED)
        elm.Label().at((3.0, 1.5)).label(r"$v_\pi$", fontsize=10, color=RED, halign="right")
        elm.Line().at((0.5, yb)).to((14.0, yb))
        elm.Ground().at((7.5, yb))
        elm.Label().at((8.0, -0.45)).label("e", fontsize=9.5)
        elm.SourceControlledI().at((7.5, 3.0)).down().length(3.0).label(
            [r"$g_m v_\pi$", r"$g_m=38.7$ mS"], loc="bot", ofst=0.15)
        elm.Line().at((7.5, 3.0)).to((14.0, 3.0))
        elm.Dot().at((7.5, 3.0)).label("c", loc="top")
        elm.Resistor().at((11.0, 3.0)).down().length(3.0).label([r"$R_C$", r"4.7 k$\Omega$"],
                                                                 loc="bot", ofst=0.15)
        elm.Dot().at((11.0, 3.0))
        elm.Dot().at((11.0, 0.0))
        elm.Resistor().at((14.0, 3.0)).down().length(3.0).label([r"$R_L$", r"10 k$\Omega$"],
                                                                 loc="bot", ofst=0.15)
        elm.Dot().at((14.0, 3.0))
        elm.Dot().at((14.0, 0.0))
        elm.Line().at((14.0, 3.0)).to((16.0, 3.0))
        elm.Line().at((14.0, 0.0)).to((16.0, 0.0))
        elm.Dot(open=True).at((16.0, 3.0))
        elm.Dot(open=True).at((16.0, 0.0))
        elm.Label().at((16.0, 2.4)).label("+", fontsize=11, color=RED)
        elm.Label().at((16.0, 0.6)).label("−", fontsize=11, color=RED)
        elm.Label().at((16.0, 1.5)).label(r"$v_o$", fontsize=11, color=RED)
    _finish(d, ax, xlim=(-1.6, 16.8), ylim=(-1.4, 10.4))
    ax.text(-1.5, 10.35, "(a) the four dependent sources", fontsize=9.5, weight="bold", va="top")
    ax.text(-1.5, 4.55, "(b) hybrid-π small-signal model of a common-emitter stage",
            fontsize=9.5, weight="bold", va="top")
    ax.plot([-1.5, 16.7], [4.95, 4.95], color="#BBBBBB", lw=0.8, ls=":")
    save(fig, "01", "fig-1-3-dependent-sources")


# ---------------------------------------------------------------- Figure 1.4
def fig_1_4():
    c = 3e8
    f = np.logspace(1, 11, 200)
    fig, ax = new_fig(6.6, 4.6)
    l_fs = c / f / 10
    l_fr4 = 0.48 * c / f / 10
    ymin, ymax = 1e-4, 1e7
    ax.fill_between(f, ymin, l_fr4, color=GREEN, alpha=0.10, lw=0)
    ax.fill_between(f, l_fs, ymax, color=RED, alpha=0.07, lw=0)
    ax.loglog(f, l_fs, color=BLUE, lw=2, label=r"$\lambda/10$ in free space ($c$)")
    ax.loglog(f, l_fr4, color=RED, lw=2, ls="--", label=r"$\lambda/10$ on FR-4 stripline ($0.48c$)")
    bands = [("chip die", 1e-3, 1e-2), ("PCB trace", 1e-2, 0.3), ("equipment cable", 1, 10),
             ("building wiring", 10, 100), ("300 km transmission line", 2.9e5, 3.1e5),
             ("1000 km HVDC link", 0.97e6, 1.03e6)]
    for k, (name, lo, hi) in enumerate(bands):
        if hi / lo < 1.2:
            ax.axhline(np.sqrt(lo * hi), color="#777777", lw=1.0, ls=":")
        else:
            ax.axhspan(lo, hi, color="#7A7A7A" if k % 2 else "#B0B0B0", alpha=0.18, lw=0)
            for yy in (lo, hi):
                ax.axhline(yy, color="#999999", lw=0.5)
        ax.text(1.4e11, np.sqrt(lo * hi), name, ha="left", va="center", fontsize=8.2,
                color="#444444")
    pts = [(50, 300e3, "50 Hz, 300 km line\n" r"($\lambda/20$)", (1.2e2, 12)),
           (1e9, 0.10, "1 GHz, 10 cm trace\n" r"($\lambda/1.5$ on FR-4)", (2e6, 2e-3)),
           (2.4e9, 0.03, "2.4 GHz antenna feed", (1.5e7, 1.6e-4))]
    for fx, lx, txt, xyt in pts:
        ax.plot(fx, lx, "o", color=INK, ms=6, zorder=5)
        ax.annotate(txt, xy=(fx, lx), xytext=xyt, fontsize=8.2, ha="center",
                    arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.text(3e2, 2e-3, "lumped model\nadequate", fontsize=10, color="#006B4F", ha="center",
            weight="bold")
    ax.text(5e8, 1e4, "distributed\n(transmission-line)\nmodel needed", fontsize=10,
            color="#A03C00", ha="center", weight="bold")
    ax.set_xlim(10, 1e11)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("frequency $f$ (Hz)")
    ax.set_ylabel("length (m)")
    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7])
    ax.set_yticklabels(["0.1 mm", "1 mm", "1 cm", "10 cm", "1 m", "10 m", "100 m", "1 km",
                        "10 km", "100 km", "1000 km", "10 000 km"], fontsize=8.5)
    ax.set_xticks([10, 1e3, 1e5, 1e7, 1e9, 1e11])
    ax.set_xticklabels(["10 Hz", "1 kHz", "100 kHz", "10 MHz", "1 GHz", "100 GHz"], fontsize=8.5)
    ax.legend(loc="upper right", fontsize=8.2, frameon=True, framealpha=0.9, edgecolor="none")
    save(fig, "01", "fig-1-4-lumped-validity-map")


# ---------------------------------------------------------------- Figure 1.5
def fig_1_5():
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(6.8, 4.6),
                                   gridspec_kw=dict(width_ratios=[1.0, 1.0], wspace=0.04))
    XL, YL = (-2.2, 9.2), (-4.6, 7.0)
    # left: voltmeter loading on a divider
    d = _sd(axl, fontsize=8.5, unit=2.4)
    with d:
        elm.SourceV().at((0, 0)).up().length(4.8).label("10 V", loc="top")
        elm.Line().right().length(3.4)
        elm.Resistor().down().length(2.4).label(r"100 k$\Omega$", loc="bot")
        elm.Dot()
        elm.Resistor().down().length(2.4).label(r"100 k$\Omega$", loc="bot")
        elm.Line().left().length(3.4)
        elm.Ground().at((1.7, 0))
        elm.Line().at((3.4, 2.4)).right().length(3.2)
        elm.Dot()
        elm.Line().at((6.6, 2.4)).right().length(1.5)
        elm.Resistor().down().length(2.4).label(r"$R_{in}$", loc="bot")
        elm.Line().left().length(1.5)
        elm.MeterV().at((6.6, 2.4)).down().length(2.4)
        elm.Dot().at((6.6, 0))
        elm.Line().at((6.6, 0)).left().length(3.2)
        elm.Dot().at((3.4, 0))
    axl.add_patch(FancyBboxPatch((5.85, -0.35), 3.25, 3.15, boxstyle="round,pad=0.05",
                                 fc="none", ec=BLUE, ls="--", lw=1.0))
    axl.text(7.35, 3.05, "voltmeter model", ha="center", fontsize=8, color=BLUE)
    axl.text(3.2, 2.62, "5.000 V\n(true)", ha="right", va="center", fontsize=8, color="#555555")
    _finish(d, axl, xlim=XL, ylim=YL)
    axl.text(-2.1, -1.3, r"$R_{in}=10\ \mathrm{M\Omega}$ (DMM):" "\nreads 4.975 V (−0.5 %)",
             fontsize=8.2, va="top")
    axl.text(-2.1, -2.8, r"$R_{in}=200\ \mathrm{k\Omega}$ (20 k$\Omega$/V analog" "\n"
             "meter, 10 V range): reads 4.00 V (−20 %)", fontsize=8.2, va="top", color=RED)
    axl.text(-2.1, 6.9, "(a) voltmeter loading", fontsize=9.5, weight="bold", va="top")

    # right: ammeter burden in a coin-cell circuit
    d = _sd(axr, fontsize=8.5, unit=2.4)
    with d:
        elm.SourceV().at((0, 0)).up().length(2.4)
        elm.Resistor().up().length(2.4).label(r"$R_s$", loc="top")
        elm.Line().right().length(0.6)
        elm.MeterA().right().length(1.8)
        elm.Resistor().right().length(2.0).label(r"1.8 $\Omega$ burden", loc="top")
        elm.Line().right().length(0.6)
        elm.SourceI().down().length(4.8).label(["", "load", ""], loc="bot")
        elm.Line().left().length(5.0)
        elm.Ground().at((2.5, 0))
    axr.add_patch(FancyBboxPatch((0.45, 3.3), 4.15, 2.8, boxstyle="round,pad=0.05",
                                 fc="none", ec=BLUE, ls="--", lw=1.0))
    axr.text(2.55, 3.9, "DMM on mA range", ha="center", va="center", fontsize=8, color=BLUE)
    axr.text(-0.75, 1.2, "3 V\ncoin\ncell", ha="right", va="center", fontsize=8.5)
    axr.text(5.6, 1.85, "12 mA\nbursts", ha="left", va="top", fontsize=8)
    _finish(d, axr, xlim=XL, ylim=YL)
    # current burst sketch
    t = np.linspace(0, 1, 600)
    i = np.where((t % 0.33) < 0.06, 1.0, 0.03)
    axr.plot(1.0 + 3.6 * t, -3.2 + 1.0 * i, color=GREEN, lw=1.2)
    axr.plot([1.0, 4.6], [-3.2, -3.2], color="#999999", lw=0.6)
    axr.text(0.9, -2.2, "12 mA", ha="right", va="center", fontsize=7.5, color=GREEN)
    axr.text(2.8, -3.5, "load current vs time", ha="center", va="top", fontsize=7.5,
             color=GREEN)
    axr.text(-2.1, -1.0, "burden 21.6 mV at 12 mA", fontsize=8.2, va="top", color=RED)
    axr.text(-2.1, 6.9, "(b) ammeter burden", fontsize=9.5, weight="bold", va="top")
    save(fig, "01", "fig-1-5-meter-loading")


if __name__ == "__main__":
    fig_1_1()
    fig_1_2()
    fig_1_3()
    fig_1_4()
    fig_1_5()
