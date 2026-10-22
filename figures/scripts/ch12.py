"""Figures for Chapter 12 — Two-Port Networks.

Run from the repository root:  python figures/scripts/ch12.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, box, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Arc, Rectangle  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")

GREY = "#8A8A8A"
LIGHT = "#5A9BD5"


# ---------------------------------------------------------------- helpers
def _terminal(ax, x, y, label=None, side="left", color=INK, size=6.5):
    ax.plot([x], [y], "o", ms=size, mfc="white", mec=color, mew=1.3, zorder=5)
    if label:
        dx = -0.22 if side == "left" else 0.22
        ax.text(x + dx, y, label, ha="right" if side == "left" else "left", va="center",
                fontsize=10, color=color)


def _harrow(ax, x0, x1, y, color=INK, lw=1.3, ms=12):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def _zigzag(ax, x0, y0, x1, y1, color=INK, n=6, amp=0.12, lw=1.3):
    """Resistor zig-zag between two points (straight horizontal or vertical)."""
    p0, p1 = np.array([x0, y0], float), np.array([x1, y1], float)
    L = np.linalg.norm(p1 - p0)
    u = (p1 - p0) / L
    nrm = np.array([-u[1], u[0]])
    lead = 0.2 * L
    pts = [p0, p0 + u * lead]
    seg = (L - 2 * lead) / n
    for k in range(n):
        pts.append(p0 + u * (lead + (k + 0.5) * seg) + nrm * amp * (1 if k % 2 == 0 else -1))
    pts.append(p1 - u * lead)
    pts.append(p1)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw)


def _sd_vport(x, yt, yb, name, side, dx=0.45):
    """Port voltage marking (+, name, -) beside terminals at x (inside a schemdraw context)."""
    sx = dx if side == "rgt" else -dx
    elm.Label().at((x + sx, yt - 0.45)).label("+", fontsize=12)
    elm.Label().at((x + sx * 1.15, (yt + yb) / 2)).label(name, fontsize=11,
                                                        halign="left" if side == "rgt" else "right")
    elm.Label().at((x + sx, yb + 0.45)).label("−", fontsize=12)


def _sd_iarrow(x0, x1, y, name, color=None):
    """Current arrow drawn on a horizontal wire from x0 to x1, labelled above."""
    kw = {"color": color} if color else {}
    elm.Arrow(headwidth=0.25, headlength=0.3, **kw).at((x0, y)).to((x1, y))
    elm.Label().at(((x0 + x1) / 2, y + 0.4)).label(name, fontsize=11, **kw)


# ---------------------------------------------------------------- 12.1
def fig_12_1():
    """Two-port conventions: V1, I1, V2, I2, ABCD current -I2, grey source and load."""
    fig, ax = schematic(6.6, 3.6, xlim=(-0.6, 11.4), ylim=(0.0, 6.4))
    # box
    bx0, bx1, by0, by1 = 3.6, 7.2, 1.2, 4.8
    ax.add_patch(FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0,
                                boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="#EEF3F8", ec=INK, lw=1.2))
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2 + 0.35, "linear two-port", ha="center",
            va="center", fontsize=11, weight="bold", color=INK)
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2 - 0.45,
            "no internal independent\nsources, zero initial state",
            ha="center", va="center", fontsize=8.5, color=INK)
    yt, yb = 4.2, 1.8
    xl, xr = 2.4, 8.4
    # leads
    for y in (yt, yb):
        ax.plot([xl, bx0], [y, y], color=INK, lw=1.3)
        ax.plot([bx1, xr], [y, y], color=INK, lw=1.3)
    _terminal(ax, xl, yt)
    _terminal(ax, xl, yb)
    _terminal(ax, xr, yt)
    _terminal(ax, xr, yb)
    ax.text(xl + 0.05, yt + 0.28, "1", ha="center", va="bottom", fontsize=10)
    ax.text(xl + 0.05, yb - 0.3, "1′", ha="center", va="top", fontsize=10)
    ax.text(xr - 0.05, yt + 0.28, "2", ha="center", va="bottom", fontsize=10)
    ax.text(xr - 0.05, yb - 0.3, "2′", ha="center", va="top", fontsize=10)
    # port voltages
    ax.text(xl + 0.35, yt - 0.45, "+", ha="center", va="center", fontsize=12)
    ax.text(xl + 0.35, yb + 0.45, "−", ha="center", va="center", fontsize=12)
    ax.text(xl + 0.4, (yt + yb) / 2, "$V_1$", ha="left", va="center", fontsize=12)
    ax.text(xr - 0.35, yt - 0.45, "+", ha="center", va="center", fontsize=12)
    ax.text(xr - 0.35, yb + 0.45, "−", ha="center", va="center", fontsize=12)
    ax.text(xr - 0.4, (yt + yb) / 2, "$V_2$", ha="right", va="center", fontsize=12)
    # currents on port 1
    _harrow(ax, 2.75, 3.35, yt, color=COLORS[0])
    ax.text(3.05, yt + 0.18, "$I_1$", ha="center", va="bottom", fontsize=11, color=COLORS[0])
    _harrow(ax, 3.35, 2.75, yb, color=COLORS[0])
    ax.text(3.05, yb - 0.2, "$I_1$", ha="center", va="top", fontsize=11, color=COLORS[0])
    # currents on port 2 (into network at 2)
    _harrow(ax, 8.05, 7.45, yt, color=COLORS[0])
    ax.text(7.75, yt + 0.18, "$I_2$", ha="center", va="bottom", fontsize=11, color=COLORS[0])
    _harrow(ax, 7.45, 8.05, yb, color=COLORS[0])
    ax.text(7.75, yb - 0.2, "$I_2$", ha="center", va="top", fontsize=11, color=COLORS[0])
    # ABCD convention arrow (lighter), above the top lead
    _harrow(ax, 8.6, 9.6, yt + 0.32, color=LIGHT, lw=1.3)
    ax.text(9.1, yt + 0.45, "$-I_2$", ha="center", va="bottom", fontsize=10.5, color=LIGHT)
    ax.text(9.1, yt + 1.05, "ABCD convention:\ncurrent leaving\ntowards the load",
            ha="center", va="bottom", fontsize=8.2, color=LIGHT)
    # grey source on the left
    xs = 0.2
    ax.plot([xl, 1.6], [yt, yt], color=GREY, lw=1.1)
    _zigzag(ax, 0.2, yt, 1.6, yt, color=GREY, lw=1.1)
    ax.text(0.9, yt + 0.25, "$Z_s$", ha="center", va="bottom", fontsize=10, color=GREY)
    ax.plot([xs, xs], [yt, 3.55], color=GREY, lw=1.1)
    circ = plt.Circle((xs, 3.0), 0.55, fc="white", ec=GREY, lw=1.1)
    ax.add_patch(circ)
    ax.text(xs, 3.22, "+", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(xs, 2.75, "−", ha="center", va="center", fontsize=9, color=GREY)
    ax.text(xs - 0.65, 3.0, "$V_s$", ha="right", va="center", fontsize=10, color=GREY)
    ax.plot([xs, xs], [2.45, yb], color=GREY, lw=1.1)
    ax.plot([xs, xl], [yb, yb], color=GREY, lw=1.1)
    # grey load on the right
    xL = 10.4
    ax.plot([xr, xL], [yt, yt], color=GREY, lw=1.1)
    ax.plot([xr, xL], [yb, yb], color=GREY, lw=1.1)
    _zigzag(ax, xL, yt, xL, yb, color=GREY, lw=1.1)
    ax.text(xL + 0.3, (yt + yb) / 2, "$Z_L$", ha="left", va="center", fontsize=10, color=GREY)
    ax.text(1.0, 0.75, "source", ha="center", va="center", fontsize=8.5, color=GREY)
    ax.text(10.1, 0.75, "load", ha="center", va="center", fontsize=8.5, color=GREY)
    ax.text(2.4, 0.75, "port 1", ha="center", va="center", fontsize=9, color=INK)
    ax.text(8.4, 0.75, "port 2", ha="center", va="center", fontsize=9, color=INK)
    save(fig, "12", "fig-12-1-two-port-conventions")


# ---------------------------------------------------------------- 12.2
def fig_12_2():
    """T and pi equivalents of the worked-example two-port."""
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=10, unit=2.4, lw=1.4)
        # ---------- (a) T network
        elm.Dot(open=True).at((0, 3))
        elm.Line().right(1.4)
        elm.Resistor().right(3.0).label("10 Ω", loc="top").label("$Z_{11}-Z_{12}$", loc="bottom")
        elm.Dot()
        d.push()
        elm.Resistor().down(3).label("30 Ω", loc="bottom").label("$Z_{12}$", loc="top")
        elm.Dot()
        d.pop()
        elm.Resistor().right(3.0).label("20 Ω", loc="top").label("$Z_{22}-Z_{12}$", loc="bottom")
        elm.Line().right(1.4)
        elm.Dot(open=True)
        elm.Line().at((0, 0)).right(8.8)
        elm.Dot(open=True).at((0, 0))
        elm.Dot(open=True).at((8.8, 0))
        _sd_iarrow(0.25, 1.15, 3, "$I_1$")
        _sd_iarrow(8.55, 7.65, 3, "$I_2$")
        _sd_vport(0, 3, 0, "$V_1$", "lft")
        _sd_vport(8.8, 3, 0, "$V_2$", "rgt")
        elm.Label().at((4.4, 4.6)).label("(a) T equivalent", fontsize=11)
        # ---------- (b) pi network
        x0 = 12.6
        elm.Dot(open=True).at((x0, 3))
        elm.Line().right(3.0)
        elm.Dot()
        d.push()
        elm.Resistor().down(3).label("55 Ω", loc="bottom").label("$\\dfrac{1}{Y_{11}+Y_{12}}$", loc="top", ofst=0.15)
        elm.Dot()
        d.pop()
        elm.Resistor().right(4.8).label("36.67 Ω", loc="top").label("$-1/Y_{12}$", loc="bottom")
        elm.Dot()
        d.push()
        elm.Resistor().down(3).label("110 Ω", loc="top").label("$\\dfrac{1}{Y_{22}+Y_{12}}$", loc="bottom", ofst=0.15)
        elm.Dot()
        d.pop()
        elm.Line().right(3.0)
        elm.Dot(open=True)
        elm.Line().at((x0, 0)).right(10.8)
        elm.Dot(open=True).at((x0, 0))
        elm.Dot(open=True).at((x0 + 10.8, 0))
        _sd_iarrow(x0 + 0.2, x0 + 1.1, 3, "$I_1$")
        _sd_iarrow(x0 + 10.6, x0 + 9.7, 3, "$I_2$")
        _sd_vport(x0, 3, 0, "$V_1$", "lft")
        _sd_vport(x0 + 10.8, 3, 0, "$V_2$", "rgt")
        elm.Label().at((x0 + 5.4, 4.6)).label("(b) π equivalent", fontsize=11)
    d.draw(show=False)
    ax.text(0.5, -0.03, "Both networks present  $\\mathbf{Z}$ = [40  30 ; 30  50] Ω  at their ports",
            transform=ax.transAxes, ha="center", va="top", fontsize=10)
    save(fig, "12", "fig-12-2-t-and-pi-equivalents")


# ---------------------------------------------------------------- 12.3
def fig_12_3():
    """Single RC section, buffered cascade and loaded passive cascade."""
    f0 = 1 / (2 * np.pi * 1e3 * 100e-9)  # 1591.5 Hz
    f = np.logspace(1, 5, 2000)
    x = f / f0
    h1 = 1 / (1 + 1j * x)
    h2 = h1 ** 2
    hp = 1 / (1 - x ** 2 + 3j * x)
    db = lambda h: 20 * np.log10(np.abs(h))
    fig, ax = new_fig(6.4, 4.0)
    ax.semilogx(f, db(h1), ":", color=COLORS[0], lw=2.0, label="single section  $1/(1+jf/f_0)$")
    ax.semilogx(f, db(h2), "--", color=COLORS[2], lw=1.8, label="buffered cascade  $1/(1+jf/f_0)^2$")
    ax.semilogx(f, db(hp), "-", color=COLORS[1], lw=1.9,
                label="passive cascade  $1/(1-(f/f_0)^2+j3f/f_0)$")
    # markers at f0
    for val, c in ((-3.01, COLORS[0]), (-6.02, COLORS[2]), (-9.54, COLORS[1])):
        ax.plot([f0], [val], "o", color=c, ms=5, zorder=5)
    ax.annotate("−3.01 dB", (f0, -3.01), xytext=(4200, -1.5), fontsize=8.5, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.7))
    ax.annotate("−6.02 dB", (f0, -6.02), xytext=(4200, -5.5), fontsize=8.5, color=COLORS[2],
                arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.7))
    ax.annotate("−9.54 dB", (f0, -9.54), xytext=(4200, -9.5), fontsize=8.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.7))
    ax.axvline(f0, color="#999999", lw=0.7, ls="-", zorder=0)
    ax.text(f0 * 0.93, -40, "$f_0$ = 1591.5 Hz", fontsize=8.5, color="#555555", ha="right")
    # -3 dB of passive cascade
    a = np.sqrt((-7 + np.sqrt(53)) / 2) * f0
    ax.axhline(-3.01, color="#BBBBBB", lw=0.7, ls="-", zorder=0)
    ax.plot([a], [-3.01], "s", color=COLORS[1], ms=5, zorder=5)
    ax.annotate(f"passive cascade −3 dB\nat {a:.0f} Hz", (a, -3.01), xytext=(30, -14),
                fontsize=8.5, color=COLORS[1],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.8, mutation_scale=8))
    # asymptote labels
    fa = np.array([1.2e4, 1e5])
    ax.semilogx(fa, -20 * np.log10(fa / f0), color="#777777", lw=0.8, ls=(0, (1, 2)))
    ax.semilogx(fa, -40 * np.log10(fa / f0), color="#777777", lw=0.8, ls=(0, (1, 2)))
    ax.set_xlim(10, 1e5)
    ax.set_ylim(-60, 3)

    def slope_text(xc, slope, dy, text, va):
        p0 = ax.transData.transform((xc, slope * np.log10(xc / f0)))
        p1 = ax.transData.transform((xc * 2, slope * np.log10(2 * xc / f0)))
        ang = np.degrees(np.arctan2(p1[1] - p0[1], p1[0] - p0[0]))
        ax.text(xc, slope * np.log10(xc / f0) + dy, text, fontsize=8.5, rotation=ang,
                rotation_mode="anchor", ha="center", va=va, color="#444444")

    slope_text(2.6e4, -20, 1.5, "−20 dB/decade", "bottom")
    ax.annotate("−40 dB/decade", (1.5e4, -40 * np.log10(1.5e4 / f0)), xytext=(3.0e3, -50),
                fontsize=8.5, color="#444444", ha="center",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("magnitude (dB)")
    ax.grid(True, which="both", lw=0.4)
    ax.legend(loc="lower left", fontsize=8.5)
    save(fig, "12", "fig-12-3-rc-cascade-response")


# ---------------------------------------------------------------- 12.4
YA = (7.6, 6.5)   # Na port terminal heights (upper, lower)
YB = (3.5, 2.4)   # Nb port terminal heights
EL, ER = 3.2, 6.8  # box edges


def _w(ax, xs, ys, **kw):
    ax.plot(xs, ys, color=kw.pop("color", INK), lw=kw.pop("lw", 1.1), **kw)


def _coil(ax, x, y0, y1, face, color=GREY, n=3):
    """Vertical coil of n bumps between y0 < y1 at x, bumps facing +1 (right) or -1 (left)."""
    h = (y1 - y0) / n
    for k in range(n):
        yc = y0 + (k + 0.5) * h
        th = (-90, 90) if face > 0 else (90, 270)
        ax.add_patch(Arc((x, yc), h * 0.9, h, theta1=th[0], theta2=th[1], color=color,
                         lw=1.1))


def _xfmr(ax, edge, d):
    """Dashed 1:1 isolating transformer on the Nb port at box edge `edge`, outward direction d.
    Returns the x where the outer winding's leads end."""
    x1, x2, x3 = edge + d * 0.35, edge + d * 0.75, edge + d * 0.95
    yu, yl = YB
    ym0, ym1 = yl + 0.2, yu - 0.2
    kw = dict(color=GREY, lw=1.0)
    xa_, xb_ = sorted((edge + d * 0.12, edge + d * 0.98))
    ax.add_patch(Rectangle((xa_, yl - 0.3), xb_ - xa_, yu - yl + 0.6, fill=False, ec=GREY,
                           lw=0.9, ls=(0, (3, 2))))
    _w(ax, [edge, x1, x1], [yu, yu, ym1], **kw)
    _w(ax, [edge, x1, x1], [yl, yl, ym0], **kw)
    _coil(ax, x1, ym0, ym1, d)
    _coil(ax, x2, ym0, ym1, -d)
    xm = (x1 + x2) / 2
    _w(ax, [xm - 0.03, xm - 0.03], [ym0, ym1], **kw)
    _w(ax, [xm + 0.03, xm + 0.03], [ym0, ym1], **kw)
    _w(ax, [x2, x2, x3], [ym1, yu, yu], **kw)
    _w(ax, [x2, x2, x3], [ym0, yl, yl], **kw)
    return x3


def _port_side(ax, side, mode, xfmr):
    edge = EL if side == "L" else ER
    d = -1 if side == "L" else 1
    eb = edge
    if xfmr:
        eb = _xfmr(ax, edge, d)
    xt = edge + d * 2.7  # external terminal
    if mode == "series":
        xs = edge + d * 1.35
        _w(ax, [edge, xs, xs, eb], [YA[1], YA[1], YB[0], YB[0]])
        _w(ax, [edge, xt], [YA[0], YA[0]])
        _w(ax, [eb, xt], [YB[1], YB[1]])
        tops = (YA[0], YB[1])
    else:  # parallel
        xa, xb = edge + d * 1.75, edge + d * 1.25
        _w(ax, [edge, xa], [YA[0], YA[0]])
        _w(ax, [eb, xa], [YB[0], YB[0]])
        _w(ax, [xa, xa], [YB[0], YA[0]])
        _w(ax, [edge, xb], [YA[1], YA[1]])
        _w(ax, [eb, xb], [YB[1], YB[1]])
        _w(ax, [xb, xb], [YB[1], YA[1]])
        for (x, y) in ((xa, YA[0]), (xa, YB[0]), (xb, YA[1]), (xb, YB[1])):
            ax.plot([x], [y], "o", color=INK, ms=3)
        ym = 5.0
        _w(ax, [xa, xt], [YA[0], YA[0]])
        _w(ax, [xb, xb + d * 0.0, xt], [YB[1], YB[1], YB[1]])
        tops = (YA[0], YB[1])
    for y in tops:
        ax.plot([xt], [y], "o", ms=5, mfc="white", mec=INK, mew=1.1, zorder=5)
    lbl = "port 1" if side == "L" else "port 2"
    ax.text(xt, (tops[0] + tops[1]) / 2, lbl, rotation=90, ha="center", va="center",
            fontsize=8, color="#555555")


def _two_boxes(ax):
    for (y0, name) in ((YA[1] - 0.45, "$N_a$"), (YB[1] - 0.45, "$N_b$")):
        ax.add_patch(FancyBboxPatch((EL, y0), ER - EL, 2.0, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc="#EEF3F8", ec=INK, lw=1.0))
        ax.text((EL + ER) / 2, y0 + 1.0, name, ha="center", va="center", fontsize=11)


def fig_12_4():
    """The five interconnections of two two-ports."""
    fig = plt.figure(figsize=(6.8, 5.0))
    W, H = 0.32, 0.47
    pos = [(0.01, 0.51), (0.345, 0.51), (0.68, 0.51), (0.175, 0.0), (0.51, 0.0)]
    axs = []
    for p in pos:
        a = fig.add_axes([p[0], p[1], W, H])
        a.set_xlim(0, 10)
        a.set_ylim(-0.9, 9.9)
        a.set_aspect("equal")
        a.axis("off")
        axs.append(a)
    # (1) cascade
    ax = axs[0]
    for (x0, name) in ((1.0, "$N_a$"), (5.7, "$N_b$")):
        ax.add_patch(FancyBboxPatch((x0, 3.7), 3.3, 2.6, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc="#EEF3F8", ec=INK, lw=1.0))
        ax.text(x0 + 1.65, 5.0, name, ha="center", va="center", fontsize=11)
    for y in (5.8, 4.2):
        _w(ax, [0.2, 1.0], [y, y])
        _w(ax, [4.3, 5.7], [y, y])
        _w(ax, [9.0, 9.8], [y, y])
        for x in (0.2, 9.8):
            ax.plot([x], [y], "o", ms=5, mfc="white", mec=INK, mew=1.1, zorder=5)
    ax.text(5.0, 9.4, "(1) Cascade", ha="center", va="center", fontsize=9.5, weight="bold")
    ax.text(5.0, 1.4, "$\\mathbf{T}=\\mathbf{T}_a\\,\\mathbf{T}_b$", ha="center", va="center",
            fontsize=12, color=COLORS[0])
    ax.text(5.0, 0.0, "port condition always holds", ha="center", va="center", fontsize=7.8,
            color="#555555")
    specs = [
        ("(2) Series–series", "series", "series", "R", "$\\mathbf{Z}=\\mathbf{Z}_a+\\mathbf{Z}_b$", None),
        ("(3) Parallel–parallel", "parallel", "parallel", "R", "$\\mathbf{Y}=\\mathbf{Y}_a+\\mathbf{Y}_b$", None),
        ("(4) Series–parallel", "series", "parallel", "L", "$\\mathbf{h}=\\mathbf{h}_a+\\mathbf{h}_b$",
         "series–shunt feedback"),
        ("(5) Parallel–series", "parallel", "series", "R", "$\\mathbf{g}=\\mathbf{g}_a+\\mathbf{g}_b$", None),
    ]
    for ax, (title, mi, mo, xside, rule, sub) in zip(axs[1:], specs):
        _two_boxes(ax)
        _port_side(ax, "L", mi, xside == "L")
        _port_side(ax, "R", mo, xside == "R")
        ax.text(5.0, 9.4, title, ha="center", va="center", fontsize=9.5, weight="bold")
        if sub:
            ax.text(5.0, 8.7, f"({sub})", ha="center", va="center", fontsize=8, color="#555555")
        ax.text(5.0, -0.1, rule, ha="center", va="center", fontsize=12, color=COLORS[0])
        xl = 3.6 if xside == "L" else 6.4
        ax.text(EL - 0.55 if xside == "L" else ER + 0.55, YB[1] - 0.65, "ideal 1:1 transformer\nensures port condition",
                ha="center", va="top", fontsize=6.8, color=GREY)
    save(fig, "12", "fig-12-4-two-port-interconnections")


# ---------------------------------------------------------------- 12.5
def fig_12_5():
    """h-parameter model of a common-emitter stage with source and load."""
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=10, unit=2.4, lw=1.4)
        elm.SourceV().up(3).at((0, 0))
        elm.Label().at((-0.75, 1.5)).label("$V_s$", fontsize=11, halign="right")
        elm.Resistor().right(2.6).label("$R_s$ = 600 Ω", loc="top")
        elm.Dot(open=True)
        elm.Line().right(2.4)
        elm.Resistor().right(2.6).label("$h_{ie}$ = 1.2 kΩ", loc="top")
        elm.SourceControlledV().down(3).reverse().label("$h_{re}V_2$", loc="top")
        elm.Line().left(7.6)
        # output side
        xo = 10.6
        elm.SourceControlledI().at((xo, 0)).up(3).reverse().label("$h_{fe}I_1$", loc="bottom")
        elm.Line().right(3.0)
        elm.Dot()
        d.push()
        elm.Resistor().down(3).label("$1/h_{oe}$" + chr(10) + "= 40 kΩ", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Line().right(2.4)
        elm.Dot(open=True)
        elm.Line().right(1.6)
        elm.Resistor().down(3).label("$R_L$" + chr(10) + "= 2 kΩ", loc="bottom")
        elm.Line().left(7.0)
        elm.Line().at((7.6, 0)).right(3.0)
        elm.Ground().at((7.6, 0))
        _sd_vport(2.6, 3, 0, "$V_1$", "rgt")
        elm.Dot(open=True).at((2.6, 0))
        _sd_vport(16.0, 3, 0, "$V_2$", "rgt")
        elm.Dot(open=True).at((16.0, 0))
        _sd_iarrow(3.1, 4.3, 3, "$I_1$")
        _sd_iarrow(15.85, 14.95, 3, "$I_2$")
        elm.Label().at((1.3, -0.45)).label("source", fontsize=8.5, color=GREY)
        elm.Label().at((5.2, -0.45)).label("input port (B–E)", fontsize=8.5, color=GREY)
        elm.Label().at((12.6, -0.45)).label("output port (C–E)", fontsize=8.5, color=GREY)
        elm.Label().at((17.0, -0.45)).label("load", fontsize=8.5, color=GREY)
    d.draw(show=False)
    ax.text(0.5, -0.06, "$h_{ie}$ = 1.2 kΩ,  $h_{re}$ = 2.5×10$^{-4}$,  $h_{fe}$ = 100,  "
            "$h_{oe}$ = 25 µS\n"
            "$Z_{in}$ = 1152 Ω     $A_V=V_2/V_1$ = −165     $A_{Vs}$ = −108.7     "
            "$Z_{out}$ = 90 kΩ", transform=ax.transAxes, ha="center", va="top", fontsize=9.5,
            linespacing=1.6,
            bbox=dict(fc="#EEF3F8", ec="#888888", lw=0.7, boxstyle="round,pad=0.4"))
    save(fig, "12", "fig-12-5-h-parameter-amplifier")


# ---------------------------------------------------------------- 12.6
def fig_12_6():
    """Nominal pi line model and sending/receiving-end phasors."""
    Z, Y = 12 + 60j, 420e-6j
    A = 1 + Z * Y / 2
    C = Y * (1 + Z * Y / 4)
    VR = 220e3 / np.sqrt(3)
    IR = 100e6 / (np.sqrt(3) * 220e3 * 0.9) * np.exp(-1j * np.arccos(0.9))
    VS = A * VR + Z * IR
    IS = C * VR + A * IR

    fig = plt.figure(figsize=(6.8, 5.0))
    ax1 = fig.add_axes([0.05, 0.50, 0.90, 0.50])
    ax1.axis("off")
    with schemdraw.Drawing(canvas=ax1, show=False) as d:
        d.config(fontsize=9.5, unit=2.2, lw=1.4)
        elm.Dot(open=True).at((0, 3))
        elm.Line().right(1.6)
        elm.Dot()
        d.push()
        elm.Capacitor().down(3).label("$Y/2$" + chr(10) + "= j210 µS", loc="bottom")
        elm.Dot()
        d.pop()
        elm.Resistor().right(2.4).label("12 Ω", loc="top")
        elm.Inductor2().right(2.4).label("j60 Ω", loc="top")
        elm.Dot()
        d.push()
        elm.Capacitor().down(3).label("$Y/2$" + chr(10) + "= j210 µS", loc="top")
        elm.Dot()
        d.pop()
        elm.Line().right(2.4)
        elm.Dot(open=True)
        elm.Line().right(2.2)
        elm.RBox().down(3).label("load" + chr(10) + "100 MW" + chr(10) + "pf 0.9 lag", loc="bottom")
        elm.Line().left(11.0)
        elm.Dot(open=True).at((0, 0))
        elm.Dot(open=True).at((8.8, 0))
        _sd_vport(0, 3, 0, "$V_S$", "lft")
        _sd_vport(8.8, 3, 0, "$V_R$", "rgt")
        _sd_iarrow(0.2, 1.2, 3, "$I_S$")
        _sd_iarrow(7.0, 8.0, 3, "$I_R$")
        elm.Label().at((4.0, 4.3)).label("series $Z$ = 12 + j60 Ω  (150 km)", fontsize=9.5)
    d.draw(show=False)

    # phasor diagram: voltages to scale (kV); currents on a separate scale
    ax = fig.add_axes([0.02, 0.0, 0.64, 0.48])
    ax.set_aspect("equal")
    ax.axis("off")
    kv = 1 / 1e3
    ki = 0.25

    def ph(z, color, start=0j, lw=1.8):
        z1 = start + z
        ax.annotate("", xy=(z1.real, z1.imag), xytext=(start.real, start.imag),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    mutation_scale=11, shrinkA=0, shrinkB=0))
        return z1

    ax.plot([-3, 150], [0, 0], color="#BBBBBB", lw=0.6, zorder=0)
    vr = ph(VR * kv, COLORS[0])
    avr = A * VR * kv
    vs = ph(VS * kv, COLORS[1])
    ph(Z * IR * kv, COLORS[2], start=avr, lw=1.6)
    ir = ph(IR * ki, COLORS[3])
    is_ = ph(IS * ki, COLORS[4])
    ax.text(70, -2.0, "$V_R$ = 127.0 kV ∠0°", fontsize=8.5, color=COLORS[0], va="top", ha="center")
    ax.text(60, 9.5, "$V_S$ = 137.0 kV ∠6.1°", fontsize=8.5, color=COLORS[1], ha="center",
            va="bottom", rotation=6.1, rotation_mode="anchor")
    mid = avr + Z * IR * kv / 2
    ax.text(mid.real + 2.0, mid.imag - 1.0, "$B\\,I_R$", fontsize=8.5, color=COLORS[2], va="center")
    ax.annotate("$A\\,V_R$", (avr.real - 0.5, 0.2), xytext=(112, -9), fontsize=8, color=COLORS[0],
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.text(ir.real + 2.0, ir.imag, "$I_R$ = 291.6 A ∠−25.8°", fontsize=8.5, color=COLORS[3],
            va="center")
    ax.text(is_.real + 2.0, is_.imag, "$I_S$ = 269.1 A ∠−15.5°", fontsize=8.5,
            color=COLORS[4], va="center")
    ax.add_patch(Arc((0, 0), 70, 70, theta1=0, theta2=np.angle(VS, 1), color=INK, lw=0.9))
    ax.text(37, 1.6, "δ = 6.1°", fontsize=8.5, ha="left", va="bottom")
    ax.set_xlim(-3, 150)
    ax.set_ylim(-36, 20)
    fig.text(0.68, 0.24, "Phasors per phase\n(voltages to scale; currents\non a separate scale)\n\n"
             "load angle δ = 6.1°\nregulation 9.2 %\n$V_S$ = 237.2 kV line-to-line\n"
             "$V_R$ = 220 kV line-to-line", fontsize=8.5, va="center", ha="left", linespacing=1.3,
             bbox=dict(fc="#F5F5F5", ec="#AAAAAA", lw=0.7, boxstyle="round,pad=0.5"))
    save(fig, "12", "fig-12-6-nominal-pi-line")


if __name__ == "__main__":
    fig_12_1()
    fig_12_2()
    fig_12_3()
    fig_12_4()
    fig_12_5()
    fig_12_6()
