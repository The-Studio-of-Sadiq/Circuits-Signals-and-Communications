"""Figures for Chapter 2 — Fundamental Circuit Laws.

Run from the repository root:  python figures/scripts/ch02.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, box, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")
BLUE, RED, GREEN, PINK, ORANGE = COLORS[0], COLORS[1], COLORS[2], COLORS[3], COLORS[4]


def _sd(ax, fontsize=9, unit=3.0):
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


def _cur(ax, x0, y0, x1, y1, text, tx, ty, color=BLUE, ha="center", fs=8.5):
    """Short current arrow from (x0, y0) to (x1, y1) with a label at (tx, ty)."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, mutation_scale=11,
                                shrinkA=0, shrinkB=0))
    ax.text(tx, ty, text, ha=ha, va="center", fontsize=fs, color=color)


# ---------------------------------------------------------------- Figure 2.1
# Tungsten lamp: filament temperature from P = a (T - T0) + b (T^4 - T0^4)
# (conduction + radiation), R = R0 (T/T0)^x with R0 = 2.4 ohm cold and 28.8 ohm at 5 W.
_T0, _TH, _R0 = 293.15, 2773.0, 2.4
_X = np.log(28.8 / _R0) / np.log(_TH / _T0)
_A = 0.5 / (_TH - _T0)
_B = 4.5 / (_TH ** 4 - _T0 ** 4)


def _lamp_R(P):
    T = brentq(lambda t: _A * (t - _T0) + _B * (t ** 4 - _T0 ** 4) - P, _T0, 6000)
    return _R0 * (T / _T0) ** _X


def _lamp_current(v):
    if v == 0:
        return 0.0
    s, v = np.sign(v), abs(v)
    return s * brentq(lambda i: i * _lamp_R(v * i) - v, 1e-12, v / _R0)


def fig_2_1():
    v = np.linspace(-2, 14, 801)
    fig, ax = new_fig(6.4, 4.2)
    ax.axhline(0, color="#999999", lw=0.6)
    ax.axvline(0, color="#999999", lw=0.6)
    ax.plot(v, v / 28.8, color=BLUE, label="resistor 28.8 Ω")
    il = np.array([_lamp_current(x) for x in v])
    ax.plot(v, il, color=RED, label="lamp 12 V, 5 W")
    Is, VT = 1e-12, 0.02585
    vd = np.linspace(-2, 0.75, 3000)
    idd = Is * (np.exp(vd / VT) - 1)
    keep = idd <= 0.6
    ax.plot(vd[keep], idd[keep], color=GREEN, label="silicon diode")
    ax.text(9.0, 0.20, "ohmic resistor,\nslope $1/R$  (28.8 Ω)", color=BLUE,
            fontsize=8.5, ha="left", va="top")
    ax.text(11.0, 0.47, "lamp: $R$ rises\nwith temperature", color=RED,
            fontsize=8.5, ha="center", va="bottom")
    ax.annotate("diode:\nno single\nresistance", xy=(0.71, 0.47), xytext=(1.0, 0.47),
                color=GREEN, fontsize=8.5, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.8))
    ax.plot(12, _lamp_current(12), "o", color=RED, ms=5, zorder=5)
    ax.text(12.15, 0.40, "(12 V, 0.417 A)", fontsize=8, ha="left", va="top", color=RED)
    vv = np.linspace(0, 0.75, 10)
    ax.plot(vv, vv / 2.4, color=RED, lw=1.0, ls=":")
    ax.annotate("cold filament: slope ≈ 1/2.4 Ω", xy=(0.3, 0.3 / 2.4), xytext=(1.2, -0.055),
                fontsize=8, color=RED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.7))
    ax.set_xlim(-2, 14)
    ax.set_ylim(-0.1, 0.6)
    ax.set_xlabel("voltage $v$ (V)")
    ax.set_ylabel("current $i$ (A)")
    ax.legend(loc="lower right", fontsize=8.2)
    # inset: tangent at the lamp operating point
    h = 1e-3
    g = (_lamp_current(12 + h) - _lamp_current(12 - h)) / (2 * h)
    ins = ax.inset_axes([0.42, 0.67, 0.25, 0.25])
    vz = np.linspace(10.5, 13.5, 60)
    ins.plot(vz, [_lamp_current(x) for x in vz], color=RED)
    ins.plot(vz, _lamp_current(12) + g * (vz - 12), color=INK, lw=1.0, ls="--")
    ins.plot(vz, vz / 28.8, color=BLUE, lw=1.0, alpha=0.6)
    ins.plot(12, _lamp_current(12), "o", color=RED, ms=4)
    ins.set_xlim(10.5, 13.5)
    ins.set_ylim(0.375, 0.46)
    ins.tick_params(labelsize=7)
    ins.set_xticks([11, 12, 13])
    ins.set_yticks([0.38, 0.42, 0.46])
    ins.set_title(f"tangent: slope (incremental) resistance\n"
                  f"$dv/di$ ≈ {1 / g:.0f} Ω  vs  $v/i$ = 28.8 Ω", fontsize=7.5)
    for sp in ("top", "right"):
        ins.spines[sp].set_visible(True)
    save(fig, "02", "fig-2-1-ohmic-and-nonohmic")


# ---------------------------------------------------------------- Figure 2.2
def _ladder(ax, u=4.0, fontsize=9):
    d = _sd(ax, fontsize=fontsize, unit=u)
    with d:
        elm.SourceV().at((0, 0)).up().length(u)
        elm.Resistor().at((0, u)).right().length(u)
        elm.Resistor().at((u, u)).down().length(u)
        elm.Resistor().at((u, u)).right().length(u)
        elm.Resistor().at((2 * u, u)).down().length(u)
        elm.Line().at((2 * u, u)).right().length(u)
        elm.Resistor().at((3 * u, u)).down().length(u)
        elm.Line().at((0, 0)).right().length(3 * u)
        for x in (u, 2 * u):
            elm.Dot().at((x, u))
            elm.Dot().at((x, 0))
        elm.Ground().at((1.5 * u, 0))
    return d


def fig_2_2():
    u = 4.0
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    d = _ladder(ax, u)
    _finish(d, ax, xlim=(-2.6, 3 * u + 3.4), ylim=(-2.4, u + 1.6))
    fs = 8.5
    ax.text(-0.75, u / 2, "24 V", ha="right", va="center", fontsize=fs)
    ax.text(u / 2, u + 0.5, r"$R_1 = 2\ \Omega$", ha="center", fontsize=fs)
    ax.text(1.5 * u, u + 0.5, r"$R_3 = 4\ \Omega$", ha="center", fontsize=fs)
    for x, t in ((u, "$R_2$\n12 Ω"), (2 * u, "$R_4$\n6 Ω"), (3 * u, "$R_5$\n3 Ω")):
        ax.text(x - 0.5, 1.45, t, ha="right", va="center", fontsize=fs)
    for x, lab in ((0, r"S: $v_S$ = 24 V"), (u, r"A: $v_A$ = 16 V"),
                   (2 * u, r"B: $v_B$ = 5.333 V")):
        ax.plot(x, u, "o", color=INK, ms=4)
        ax.text(x, u + 1.15, lab, ha="center", fontsize=fs, color=GREEN, weight="bold")
    _cur(ax, 0.9, u - 0.4, 2.1, u - 0.4, "$I$ = 4 A", 1.5, u - 0.8)
    _cur(ax, u + 0.9, u - 0.4, u + 2.1, u - 0.4, "$I_3$ = 2.667 A", 1.5 * u, u - 0.8)
    for x, t in ((u, "$I_2$ = 1.333 A"), (2 * u, "$I_4$ = 0.889 A"), (3 * u, "$I_5$ = 1.778 A")):
        _cur(ax, x + 0.4, 2.95, x + 0.4, 2.05, t, x + 0.55, 2.5, ha="left")
    for k in range(3):
        cx = (k + 0.5) * u
        ax.add_patch(FancyBboxPatch((cx - 0.5, 0.3), 1.0, 0.75, boxstyle="round,pad=0.12",
                                    fc="none", ec=PINK, ls="--", lw=1.2))
        ax.text(cx, 0.68, f"M{k + 1}", ha="center", va="center", fontsize=10, color=PINK,
                weight="bold")
    ax.text(1.5 * u, -1.7, "n = 4 nodes,  b = 6 branches,  b − n + 1 = 3 meshes",
            ha="center", fontsize=9)
    save(fig, "02", "fig-2-2-ladder-network")


# ---------------------------------------------------------------- Figure 2.3
def fig_2_3():
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    d = _sd(ax, fontsize=8.5, unit=2.0)
    fs = 8.3
    X, Y = 6.6, 13.4
    a, c, dd, b = (0, 4.2), (-1.9, 2.1), (1.9, 2.1), (0, 0)
    a2, n2, c2, d2, b2 = (X, 4.6), (X, 3.0), (X - 1.6, 1.8), (X + 1.6, 1.8), (X, -0.1)
    with d:
        # panel (a): bridge
        elm.Resistor().endpoints(a, c)
        elm.Resistor().endpoints(a, dd)
        elm.Resistor().endpoints(c, b)
        elm.Resistor().endpoints(dd, b)
        elm.Resistor().endpoints(c, dd)
        for p in (c, dd):
            elm.Dot().at(p)
        elm.Line().at(a).to((0, 4.9))
        elm.Dot(open=True).at((0, 4.9))
        elm.Line().at(b).to((0, -0.7))
        elm.Dot(open=True).at((0, -0.7))
        # panel (b): wye
        elm.Resistor().endpoints(a2, n2)
        elm.Resistor().endpoints(n2, c2)
        elm.Resistor().endpoints(n2, d2)
        elm.Resistor().endpoints(c2, b2)
        elm.Resistor().endpoints(d2, b2)
        for p in (n2, c2, d2):
            elm.Dot().at(p)
        elm.Line().at(a2).to((X, 4.9))
        elm.Dot(open=True).at((X, 4.9))
        elm.Line().at(b2).to((X, -0.7))
        elm.Dot(open=True).at((X, -0.7))
        # panel (c): series-parallel
        elm.Dot(open=True).at((Y, 4.9))
        elm.Resistor().at((Y, 4.9)).down().length(1.6)
        elm.Dot().at((Y, 3.3))
        elm.Line().at((Y - 1.0, 3.3)).to((Y + 1.0, 3.3))
        elm.Resistor().at((Y - 1.0, 3.3)).down().length(1.8)
        elm.Resistor().at((Y - 1.0, 1.5)).down().length(1.8)
        elm.Resistor().at((Y + 1.0, 3.3)).down().length(1.8)
        elm.Resistor().at((Y + 1.0, 1.5)).down().length(1.8)
        elm.Line().at((Y - 1.0, -0.3)).to((Y + 1.0, -0.3))
        elm.Dot().at((Y, -0.3))
        elm.Line().at((Y, -0.3)).to((Y, -0.7))
        elm.Dot(open=True).at((Y, -0.7))
    _finish(d, ax, xlim=(-3.3, 16.4), ylim=(-2.6, 6.2))
    ax.add_patch(Polygon([a, c, dd], closed=True, fc=ORANGE, alpha=0.20, ec="none", zorder=0))
    it = dict(fontsize=9.5, style="italic", va="center")
    # panel (a)
    ax.text(0.25, 4.95, "a", **it)
    ax.text(0.25, -0.7, "b", **it)
    ax.text(c[0] - 0.25, c[1], "c", ha="right", **it)
    ax.text(dd[0] + 0.25, dd[1], "d", ha="left", **it)
    ax.text(-1.55, 3.6, "$R_1$\n10 Ω", fontsize=fs, ha="right", va="center")
    ax.text(1.55, 3.6, "$R_2$\n20 Ω", fontsize=fs, ha="left", va="center")
    ax.text(-1.55, 0.6, "$R_3$\n30 Ω", fontsize=fs, ha="right", va="center")
    ax.text(1.55, 0.6, "$R_4$\n40 Ω", fontsize=fs, ha="left", va="center")
    ax.text(0, 1.82, "$R_5$\n50 Ω", fontsize=7.8, ha="center", va="top")
    # panel (b)
    ax.text(X + 0.25, 4.95, "a", **it)
    ax.text(X + 0.25, -0.7, "b", **it)
    ax.text(X - 0.25, 3.1, "n", ha="right", **it)
    ax.text(X - 1.85, 1.8, "c", ha="right", **it)
    ax.text(X + 1.85, 1.8, "d", ha="left", **it)
    ax.text(X + 0.45, 3.85, "$R_a$ = 2.5 Ω", fontsize=fs, ha="left", va="center")
    ax.text(X - 1.2, 2.85, "$R_c$\n6.25 Ω", fontsize=fs, ha="right", va="center")
    ax.text(X + 1.2, 2.85, "$R_d$\n12.5 Ω", fontsize=fs, ha="left", va="center")
    ax.text(X - 1.2, 0.45, "$R_3$\n30 Ω", fontsize=fs, ha="right", va="center")
    ax.text(X + 1.2, 0.45, "$R_4$\n40 Ω", fontsize=fs, ha="left", va="center")
    # panel (c)
    ax.text(Y + 0.25, 4.95, "a", **it)
    ax.text(Y + 0.25, -0.7, "b", **it)
    ax.text(Y + 0.45, 4.1, "2.5 Ω", fontsize=fs, ha="left", va="center")
    ax.text(Y - 1.45, 2.4, "6.25 Ω", fontsize=fs, ha="right", va="center")
    ax.text(Y - 1.45, 0.6, "30 Ω", fontsize=fs, ha="right", va="center")
    ax.text(Y + 1.45, 2.4, "12.5 Ω", fontsize=fs, ha="left", va="center")
    ax.text(Y + 1.45, 0.6, "40 Ω", fontsize=fs, ha="left", va="center")
    ax.text(Y, -1.25, "36.25 Ω ∥ 52.5 Ω = 21.44 Ω\n" r"$R_{eq}$ = 2.5 + 21.44 = 23.94 Ω",
            fontsize=8.5, ha="center", va="top")
    ax.text(0, -1.25, "unbalanced bridge;\nshaded Δ: $R_1, R_2, R_5$", fontsize=8.3,
            ha="center", va="top")
    ax.text(X, -1.25, "Δ (a–c–d) → Y\n(Δ sum 80 Ω)", fontsize=8.3, ha="center", va="top")
    for x, t in ((0, "(a)"), (X, "(b)"), (Y, "(c)")):
        ax.text(x, 6.0, t, fontsize=10, weight="bold", ha="center", va="top")
    for x0 in (3.55, 10.0):
        ax.annotate("", xy=(x0 + 0.5, 2.2), xytext=(x0 - 0.3, 2.2),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=14))
    save(fig, "02", "fig-2-3-bridge-delta-wye")


# ---------------------------------------------------------------- Figure 2.4
def _ntc(t):
    return 10e3 * np.exp(3950 * (1 / (t + 273.15) - 1 / 298.15))


def fig_2_4():
    T = np.linspace(-10, 100, 500)
    R = _ntc(T)
    vu = 3.3 * R / (10e3 + R)
    Rl = R * 100e3 / (R + 100e3)
    vl = 3.3 * Rl / (10e3 + Rl)
    fig, ax = new_fig(6.6, 4.2)
    ax.plot(T, vu, color=BLUE, label="unloaded")
    ax.plot(T, vl, color=RED, ls="--", label="loaded by 100 kΩ")
    for t in (0, 25, 50, 100):
        r = _ntc(t)
        v = 3.3 * r / (10e3 + r)
        ax.plot(t, v, "o", color=BLUE, ms=4.5, zorder=5)
        ax.text(t + 1.5, v + 0.05, f"{v:.3f} V", fontsize=8, color=BLUE, ha="left", va="bottom")
        if t < 100:
            rl = r * 1e5 / (r + 1e5)
            w = 3.3 * rl / (10e3 + rl)
            ax.plot(t, w, "s", color=RED, ms=4, zorder=5)
            ax.text(t - 1.5, w - 0.05, f"{w:.3f} V", fontsize=8, color=RED, ha="right", va="top")
    dRdT = -3950 / 298.15 ** 2 * 10e3
    slope = 3.3 * 10e3 * dRdT / (20e3) ** 2
    tt = np.linspace(2, 48, 10)
    ax.plot(tt, 1.65 + slope * (tt - 25), color=INK, lw=1.1, ls=(0, (4, 2)))
    ax.annotate(f"tangent at 25 °C:\n{slope * 1e3:.1f} mV/K".replace("-", "−"),
                xy=(43, 1.65 + slope * 18), xytext=(52, 1.55), fontsize=8.3,
                arrowprops=dict(arrowstyle="-", lw=0.8))
    ax.set_xlim(-10, 100)
    ax.set_ylim(0, 3.3)
    ax.set_xlabel("temperature (°C)")
    ax.set_ylabel(r"output voltage $v_{out}$ (V)")
    ax.grid(True, lw=0.5)
    ax.legend(loc="lower left", fontsize=8.5)
    ins = ax.inset_axes([0.60, 0.50, 0.42, 0.52])
    d = _sd(ins, fontsize=7.5, unit=1.6)
    with d:
        elm.SourceV().at((0, 0)).up().length(3.2).label("3.3 V", loc="top")
        elm.Line().right().length(1.6)
        elm.Resistor().down().length(1.6).label("10 kΩ", loc="bot")
        elm.Dot()
        elm.Thermistor().down().length(1.6).label(["", "NTC", ""], loc="bot")
        elm.Line().left().length(1.6)
        elm.Line().at((1.6, 1.6)).right().length(1.8).linestyle("--")
        elm.Resistor().down().length(1.6).linestyle("--").label("100 kΩ\nload", loc="bot")
        elm.Line().left().length(1.8).linestyle("--")
        elm.Ground().at((0.8, 0))
    _finish(d, ins, pad=0.25)
    ins.text(1.75, 1.75, r"$v_{out}$", fontsize=7.5, ha="left", va="bottom")
    ins.text(1.75, -0.35, "10 kΩ at 25 °C,\nB = 3950 K", fontsize=6.8, ha="left", va="top")
    xl, yl = ins.get_xlim(), ins.get_ylim()
    ins.set_ylim(yl[0] - 1.0, yl[1])
    ins.set_xlim(xl[0], xl[1] + 0.6)
    save(fig, "02", "fig-2-4-ntc-divider")


# ---------------------------------------------------------------- Figure 2.5
def fig_2_5():
    fig, ax = plt.subplots(figsize=(6.8, 4.9))
    d = _sd(ax, fontsize=8.3, unit=2.0)
    fs = 8.3
    top, bot = 4.0, 0.0
    X = 10.6
    Yt, Yb = -3.2, -7.2
    Z = 10.4
    with d:
        # (a) Thevenin forms
        for x in (0.0, 3.2):
            elm.SourceV().at((x, bot)).up().length(2.0)
            elm.Resistor().at((x, 2.0)).up().length(2.0)
        elm.Resistor().at((6.4, top)).down().length(4.0)
        elm.Line().at((0, top)).to((6.4, top))
        elm.Line().at((0, bot)).to((6.4, bot))
        for p in ((3.2, top), (3.2, bot)):
            elm.Dot().at(p)
        # (b) Norton forms
        for x in (X, X + 3.7):
            elm.SourceI().at((x, bot)).up().length(4.0)
            elm.Resistor().at((x + 1.3, top)).down().length(4.0)
            for p in ((x + 1.3, top), (x + 1.3, bot)):
                elm.Dot().at(p)
        elm.Resistor().at((X + 7.5, top)).down().length(4.0)
        elm.Line().at((X, top)).to((X + 7.5, top))
        elm.Line().at((X, bot)).to((X + 7.5, bot))
        for p in ((X + 3.7, top), (X + 3.7, bot)):
            elm.Dot().at(p)
        # (c) combined Norton, then Thevenin
        elm.SourceI().at((0.0, Yb)).up().length(4.0)
        elm.Resistor().at((1.3, Yt)).down().length(4.0)
        elm.Resistor().at((4.6, Yt)).down().length(4.0)
        elm.Line().at((0, Yt)).to((4.6, Yt))
        elm.Line().at((0, Yb)).to((4.6, Yb))
        for p in ((1.3, Yt), (1.3, Yb)):
            elm.Dot().at(p)
        elm.SourceV().at((Z, Yb)).up().length(4.0)
        elm.Resistor().at((Z, Yt)).right().length(3.0)
        elm.Resistor().at((Z + 3.0, Yt)).down().length(4.0)
        elm.Line().at((Z + 3.0, Yb)).to((Z, Yb))
    _finish(d, ax, xlim=(-1.9, 20.2), ylim=(-9.0, 5.8))
    L = dict(fontsize=fs, va="center")
    # (a)
    ax.text(-0.6, 3.0, "0.5 Ω", ha="right", **L)
    ax.text(-0.6, 1.0, "14 V", ha="right", **L)
    ax.text(2.6, 3.0, "0.05 Ω", ha="right", **L)
    ax.text(2.6, 1.0, "12.6 V", ha="right", **L)
    ax.text(6.95, 2.0, "2 Ω", ha="left", **L)
    for x, t in ((0, "charger"), (3.2, "battery"), (6.4, "load")):
        ax.text(x, 4.35, t, fontsize=fs, ha="center", color=BLUE)
    # (b)
    for x, i_s, rs in ((X, "28 A", "0.5 Ω"), (X + 3.7, "252 A", "0.05 Ω")):
        ax.text(x - 0.6, 2.0, i_s, ha="right", **L)
        ax.text(x + 1.75, 0.85, rs, ha="left", **L)
    ax.text(X + 8.05, 2.0, "2 Ω", ha="left", **L)
    ax.text(X + 3.5, -0.5, "each: $I_s = V_s/R_s$, same $R_s$", fontsize=fs, ha="center",
            va="top")
    # (c)
    ax.text(-0.6, -5.2, "280 A", ha="right", **L)
    ax.text(1.75, -5.2, "0.04545 Ω", ha="left", **L)
    ax.text(5.15, -5.2, "2 Ω", ha="left", **L)
    ax.text(2.3, -7.7, "28 + 252 = 280 A;  0.5 ∥ 0.05 = 0.04545 Ω", fontsize=fs, ha="center",
            va="top")
    ax.text(Z - 0.6, -5.2, "12.727 V", ha="right", **L)
    ax.text(Z + 1.5, Yt + 0.5, "0.04545 Ω", ha="center", va="bottom", fontsize=fs)
    ax.text(Z + 3.55, -5.2, "2 Ω", ha="left", **L)
    ax.text(Z + 1.5, -7.7, "280 A × 0.04545 Ω = 12.727 V", fontsize=fs, ha="center", va="top")
    ax.annotate("", xy=(7.4, -5.2), xytext=(6.3, -5.2),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=14))
    box(ax, 15.0, -7.3, 5.0, 4.2, fc="#F3F7EE")
    ax.text(17.5, -5.2, "bus voltage 12.444 V\nload current 6.222 A\ncharger: 3.111 A out\n"
            "battery: 3.111 A out\n(discharging)", fontsize=7.8, ha="center", va="center",
            linespacing=1.4)
    ax.text(-1.8, 5.75, "(a) Thévenin models", fontsize=9.5, weight="bold", va="top")
    ax.text(X - 1.7, 5.75, "(b) Norton equivalents", fontsize=9.5, weight="bold", va="top")
    ax.text(-1.8, -1.55, "(c) combined Norton source, converted back to Thévenin form",
            fontsize=9.5, weight="bold", va="top")
    save(fig, "02", "fig-2-5-source-transformation")


# ---------------------------------------------------------------- Figure 2.6
def fig_2_6():
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(6.8, 3.8),
                                   gridspec_kw=dict(width_ratios=[1.0, 1.0], wspace=0.06))
    u = 2.0
    d = _ladder(axl, u, fontsize=8)
    _finish(d, axl, xlim=(-1.6, 3 * u + 1.2), ylim=(-2.6, u + 2.1))
    fs = 8
    axl.text(-0.45, u / 2, "24 V", ha="right", va="center", fontsize=fs)
    axl.text(u / 2, u + 0.35, "$R_1$", ha="center", fontsize=fs)
    axl.text(1.5 * u, u + 0.35, "$R_3$", ha="center", fontsize=fs)
    for x, t in ((u, "$R_2$"), (2 * u, "$R_4$"), (3 * u, "$R_5$")):
        axl.text(x + 0.35, u / 2, t, ha="left", va="center", fontsize=fs)
    for x, t in ((0, "S"), (u, "A"), (2 * u, "B")):
        axl.text(x, u + 0.9, t, ha="center", fontsize=9.5, weight="bold", color=GREEN)
    axl.text(1.5 * u, -0.8, "0 (ground)", ha="center", va="top", fontsize=8.5, weight="bold",
             color=GREEN)
    axl.text(-1.5, u + 2.0, "(a) the ladder of Figure 2.2", fontsize=9, weight="bold", va="top")

    ax = axr
    ax.set_xlim(-1.0, 5.8)
    ax.set_ylim(-2.6, 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
    P = {"S": np.array([0.0, 2.4]), "A": np.array([2.4, 2.4]), "B": np.array([4.8, 2.4]),
         "0": np.array([2.4, 0.0])}
    ax.add_patch(Polygon([P["0"], P["S"], P["A"]], fc=BLUE, alpha=0.10, ec="none"))
    ax.add_patch(Polygon([P["0"], P["A"], P["B"]], fc=ORANGE, alpha=0.16, ec="none"))
    t = np.linspace(0, 1, 61)[:, None]
    p0, p1 = P["B"], P["0"]
    ctrl = (p0 + p1) / 2 + 1.9 * np.array([1.0, -1.0]) / np.sqrt(2)
    arc = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * ctrl + t ** 2 * p1
    ax.add_patch(Polygon(np.vstack([arc, [p0]]), fc=GREEN, alpha=0.14, ec="none"))
    for pa, pb in (("0", "S"), ("S", "A"), ("A", "0"), ("A", "B"), ("B", "0")):
        ax.annotate("", xy=P[pb], xytext=P[pa],
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=13,
                                    shrinkA=6, shrinkB=6))
    ax.plot(arc[3:-3, 0], arc[3:-3, 1], color=INK, lw=1.4)
    k = 36
    ax.annotate("", xy=arc[k + 1, :], xytext=arc[k - 1, :],
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=13))
    f8 = dict(fontsize=7.8, va="center")
    ax.text(0.95, 0.95, "$b_1$ (source)", ha="right", **f8)
    ax.text(1.2, 2.68, "$b_2$ ($R_1$)", ha="center", **f8)
    ax.text(3.6, 2.68, "$b_4$ ($R_3$)", ha="center", **f8)
    ax.text(2.3, 1.15, "$b_3$ ($R_2$)", ha="right", **f8)
    ax.text(3.6, 1.2, "$b_5$ ($R_4$)", ha="center", bbox=dict(fc="white", ec="none", pad=1.0),
            **f8)
    ax.text(4.5, -0.25, "$b_6$ ($R_5$)", ha="left", **f8)
    for name, (x, y) in P.items():
        ax.plot(x, y, "o", ms=8, color=INK, zorder=5)
    ax.text(-0.25, 2.65, "S", fontsize=10, weight="bold", color=GREEN, ha="center")
    ax.text(2.4, 2.9, "A", fontsize=10, weight="bold", color=GREEN, ha="center")
    ax.text(5.05, 2.65, "B", fontsize=10, weight="bold", color=GREEN, ha="center")
    ax.text(2.1, -0.3, "0", fontsize=10, weight="bold", color=GREEN, ha="center")
    ax.text(1.45, 1.95, "M1", fontsize=9.5, color=BLUE, weight="bold", ha="center")
    ax.text(3.35, 2.0, "M2", fontsize=9.5, color="#A06A00", weight="bold", ha="center")
    ax.text(4.2, 0.62, "M3", fontsize=9.5, color=GREEN, weight="bold", ha="center")
    ax.text(-0.9, 4.05, "(b) its graph", fontsize=9, weight="bold", va="top")
    box(ax, -0.9, -2.5, 6.6, 1.55, fc="#F6F6F6")
    ax.text(2.4, -1.72, "n = 4,  b = 6\nn − 1 = 3 independent KCL equations\n"
            "b − n + 1 = 3 independent KVL equations", fontsize=7.8, ha="center",
            va="center", linespacing=1.3)
    save(fig, "02", "fig-2-6-circuit-graph")


if __name__ == "__main__":
    fig_2_1()
    fig_2_2()
    fig_2_3()
    fig_2_4()
    fig_2_5()
    fig_2_6()
