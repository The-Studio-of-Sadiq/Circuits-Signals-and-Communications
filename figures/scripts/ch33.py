"""Figures for Chapter 33 — Dynamic System Modeling.

Run from the repository root:  python figures/scripts/ch33.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon  # noqa: E402
from scipy import signal  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402

schemdraw.use("matplotlib")


# ---------------------------------------------------------------------------
# block-diagram helpers
def sj(ax, x, y, r=0.22, signs=None, fs=8):
    """Summing junction at (x, y); signs = dict(position -> sign) with positions 'w','s','n','e'."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    off = {"w": (-r - 0.05, r * 0.75), "s": (r * 0.75, -r - 0.07), "n": (r * 0.75 + 0.12, r + 0.07),
           "e": (r + 0.05, r * 0.75)}
    for pos, sg in (signs or {}).items():
        dx, dy = off[pos]
        ax.text(x + dx, y + dy, sg, fontsize=fs + 1, ha="center", va="center")


def blk(ax, xc, yc, w, h, text, fs=9, fc="#EEF3F8"):
    box(ax, xc - w / 2, yc - h / 2, w, h, text, fontsize=fs, fc=fc)


def line(ax, pts, color=INK, lw=1.1, ls="-", head=True):
    xs, ys = zip(*pts)
    if head:
        ax.plot(xs[:-1] + (xs[-2],), ys[:-1] + (ys[-2],), color=color, lw=lw, ls=ls)
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10,
                                    shrinkA=0, shrinkB=0, ls=ls))
    else:
        ax.plot(xs, ys, color=color, lw=lw, ls=ls)


def dot(ax, x, y):
    ax.plot(x, y, "o", color=INK, ms=3.5, zorder=4)


def lab(ax, x, y, t, fs=9, **kw):
    kw.setdefault("ha", "center")
    kw.setdefault("va", "bottom")
    ax.text(x, y, t, fontsize=fs, **kw)


# ---------------------------------------------------------------------------
def fig_analogous_systems():
    """Fig 33.1: series RLC, mass-spring-damper, thermal RC with corresponding variables."""
    fig = plt.figure(figsize=(6.8, 4.6))
    # --- left: series RLC
    a1 = fig.add_axes([0.01, 0.42, 0.31, 0.46])
    a1.axis("off")
    with schemdraw.Drawing(canvas=a1, show=False) as d:
        d.config(unit=2.0, fontsize=9, lw=1.1)
        src = elm.SourceV().up()
        w1 = elm.Line().right(1.2)
        elm.Resistor().right()
        ind = elm.Inductor().down()
        cap = elm.Capacitor().left(3.2)
        d.draw(show=False)
    a1.set_aspect("equal")
    sx, sy = src.center
    a1.text(sx - 0.65, sy, "$v_s$", fontsize=10, ha="right", va="center")
    rx = w1.end[0] + 1.0
    a1.text(rx, w1.end[1] + 0.45, "R = 10 Ω", fontsize=9, ha="center", va="bottom")
    ix, iy = ind.center
    a1.text(ix + 0.5, iy, "L = 10 mH", fontsize=9, ha="left", va="center")
    cx, cy = cap.center
    a1.text(cx, cy - 0.5, "C = 10 µF", fontsize=9, ha="center", va="top")
    a1.annotate("", xy=(w1.end[0] - 0.05, w1.end[1] + 0.22), xytext=(w1.start[0] + 0.15, w1.start[1] + 0.22),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.2, mutation_scale=10,
                                shrinkA=0, shrinkB=0))
    a1.text((w1.start[0] + w1.end[0]) / 2, w1.end[1] + 0.3, "$i$", fontsize=10, color=COLORS[1],
            ha="center", va="bottom")
    xl, yl = a1.get_xlim(), a1.get_ylim()
    a1.set_xlim(xl[0] - 0.9, xl[1] + 2.3)
    a1.set_ylim(yl[0] - 0.6, yl[1] + 0.8)

    # --- middle: mass-spring-damper (vertical)
    a2 = fig.add_axes([0.34, 0.42, 0.31, 0.46])
    a2.set_xlim(-2.2, 2.4)
    a2.set_ylim(-0.4, 4.6)
    a2.set_aspect("equal")
    a2.axis("off")
    a2.plot([-1.5, 1.5], [0, 0], color=INK, lw=1.4)
    for xh in np.linspace(-1.4, 1.4, 12):
        a2.plot([xh, xh - 0.18], [0, -0.2], color=INK, lw=0.8)
    ys = np.linspace(0.3, 1.8, 13)
    xs = -0.6 + 0.22 * np.array([0] + [(-1) ** k for k in range(11)] + [0])
    a2.plot([-0.6, -0.6], [0, 0.3], color=INK, lw=1.1)
    a2.plot(xs, ys, color=INK, lw=1.1)
    a2.plot([-0.6, -0.6], [1.8, 2.1], color=INK, lw=1.1)
    a2.text(-0.95, 1.05, "k = 800\nN/m", fontsize=8.5, ha="right", va="center")
    a2.plot([0.6, 0.6], [0, 0.6], color=INK, lw=1.1)
    a2.plot([0.35, 0.35, 0.85, 0.85], [1.35, 0.6, 0.6, 1.35], color=INK, lw=1.1)
    a2.plot([0.42, 0.78], [1.05, 1.05], color=INK, lw=1.6)
    a2.plot([0.6, 0.6], [1.05, 2.1], color=INK, lw=1.1)
    a2.text(0.95, 0.85, "c = 8\nN·s/m", fontsize=8.5, ha="left", va="center")
    a2.add_patch(Rectangle((-1.1, 2.1), 2.2, 1.0, fc="#EEF3F8", ec=INK, lw=1.1))
    a2.text(0, 2.6, "m = 2 kg", fontsize=9, ha="center", va="center")
    a2.annotate("", xy=(0, 4.1), xytext=(0, 3.1),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.3, mutation_scale=11,
                                shrinkA=0, shrinkB=0))
    a2.text(0.12, 3.75, "$f(t)$", fontsize=9.5, color=COLORS[1], ha="left", va="center")
    a2.annotate("", xy=(1.5, 3.4), xytext=(1.5, 2.6),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.1, mutation_scale=9,
                                shrinkA=0, shrinkB=0))
    a2.plot([1.2, 1.7], [2.6, 2.6], color=COLORS[0], lw=0.8)
    a2.text(1.62, 3.05, "$x$\n$u=\\dot x$", fontsize=9, color=COLORS[0], ha="left", va="center")

    # --- right: thermal RC (oven)
    a3 = fig.add_axes([0.67, 0.42, 0.32, 0.46])
    a3.axis("off")
    with schemdraw.Drawing(canvas=a3, show=False) as d:
        d.config(unit=2.0, fontsize=9, lw=1.1)
        q = elm.SourceI().up()
        elm.Line().right(1.6)
        node = elm.Dot()
        d.push()
        cth = elm.Capacitor().down()
        d.pop()
        elm.Line().right(2.0)
        rth = elm.Resistor().down()
        elm.Line().left(3.6)
        d.draw(show=False)
    a3.set_aspect("equal")
    qx, qy = q.center
    a3.text(qx - 0.65, qy, "$\\dot Q_{in}$\n400 W", fontsize=9, ha="right", va="center")
    nx, ny = node.center
    a3.text(nx, ny + 0.25, "$T$", fontsize=10, ha="center", va="bottom")
    cx, cy = cth.center
    a3.text(cx + 0.45, cy, "$C_\\theta$\n2000\nJ/K", fontsize=8.5, ha="left", va="center")
    rx, ry = rth.center
    a3.text(rx + 0.5, ry, "$R_\\theta$\n0.5\nK/W", fontsize=8.5, ha="left", va="center")
    a3.text(nx, cy - 1.25, "bottom rail = ambient $T_a$", fontsize=8, ha="center", va="top", color="0.35")
    xl, yl = a3.get_xlim(), a3.get_ylim()
    a3.set_xlim(xl[0] - 1.5, xl[1] + 1.2)
    a3.set_ylim(yl[0] - 0.9, yl[1] + 0.6)
    for xf, t in ((0.165, "Electrical"), (0.495, "Mechanical"), (0.83, "Thermal (oven)")):
        fig.text(xf, 0.95, t, fontsize=10.5, ha="center", va="center", weight="bold")

    # --- equations + analogy table
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.38])
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1)
    ax.axis("off")
    eqs = [r"$L\dfrac{di}{dt}+Ri+\dfrac{1}{C}\int i\,dt=v_s$",
           r"$m\ddot x+c\dot x+kx=f$",
           r"$C_\theta\dfrac{dT}{dt}=\dot Q_{in}-\dfrac{T-T_a}{R_\theta}$"]
    params = [r"$\omega_n=3162$ rad/s, $\zeta=0.158$",
              r"$\omega_n=20$ rad/s, $\zeta=0.10$",
              r"$\tau=R_\theta C_\theta=1000$ s"]
    for k, (e, p) in enumerate(zip(eqs, params)):
        ax.text(0.5 + k, 0.86, e, fontsize=10, ha="center", va="center")
        ax.text(0.5 + k, 0.63, p, fontsize=8.5, ha="center", va="center", color="0.3")
    ax.plot([0.05, 2.95], [0.50, 0.50], color=GRID, lw=0.8)
    rows = [("across", ["voltage $v$", "velocity $u$", "temperature $T$"], COLORS[0]),
            ("through", ["current $i$", "force $f$", r"heat flow $\dot Q$"], COLORS[1])]
    for j, (nm, items, col) in enumerate(rows):
        y = 0.37 - 0.16 * j
        ax.text(0.02, y, nm + ":", fontsize=8.5, color=col, ha="left", va="center", weight="bold")
        for k, it in enumerate(items):
            ax.text(0.5 + k, y, it, fontsize=9, color=col, ha="center", va="center")
        ax.annotate("", xy=(1.22, y), xytext=(0.78, y), arrowprops=dict(arrowstyle="<->", color=col, lw=0.8))
        ax.annotate("", xy=(2.22, y), xytext=(1.78, y), arrowprops=dict(arrowstyle="<->", color=col, lw=0.8))
    ax.text(2.5, 0.03, "first order only: no inertial (inductor-like) element", fontsize=8,
            ha="center", va="bottom", style="italic", color="0.3")
    ax.text(0.5, 0.03, "force–current analogy: mass ↔ C, spring ↔ L", fontsize=8,
            ha="center", va="bottom", style="italic", color="0.3")
    return save(fig, "33", "fig-33-1-analogous-systems")


# ---------------------------------------------------------------------------
def fig_dc_motor():
    """Fig 33.2: armature circuit, mechanical load and block diagram with back-EMF feedback."""
    fig = plt.figure(figsize=(6.8, 5.0))
    a1 = fig.add_axes([0.02, 0.52, 0.46, 0.40])
    a1.axis("off")
    with schemdraw.Drawing(canvas=a1, show=False) as d:
        d.config(unit=2.0, fontsize=9, lw=1.1)
        s1 = elm.SourceV().up()
        w1 = elm.Line().right(1.0)
        r1 = elm.Resistor().right()
        l1 = elm.Inductor().right()
        e = elm.SourceV().down().reverse()
        elm.Line().left(5.0)
        d.draw(show=False)
    a1.set_aspect("equal")
    sx, sy = s1.center
    a1.text(sx - 0.65, sy, "$v_a$", fontsize=10, ha="right", va="center")
    ex, ey = e.center
    a1.text(ex + 0.65, ey, "$e=K\\omega$\n(back-EMF)", fontsize=9, ha="left", va="center")
    for el, t in ((r1, "R = 2 Ω"), (l1, "L = 1 mH")):
        cx, cy = el.center
        a1.text(cx, cy + 0.45, t, fontsize=9, ha="center", va="bottom")
    a1.annotate("", xy=(w1.end[0] - 0.05, w1.end[1] + 0.22), xytext=(w1.start[0] + 0.15, w1.start[1] + 0.22),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.2, mutation_scale=10,
                                shrinkA=0, shrinkB=0))
    a1.text((w1.start[0] + w1.end[0]) / 2, w1.end[1] + 0.3, "$i$", fontsize=10, color=COLORS[1],
            ha="center", va="bottom")
    xl, yl = a1.get_xlim(), a1.get_ylim()
    a1.set_xlim(xl[0] - 0.9, xl[1] + 2.0)
    a1.set_ylim(yl[0] - 0.3, yl[1] + 0.6)
    fig.text(0.25, 0.965, "Armature circuit", fontsize=10, ha="center", va="center", weight="bold")
    fig.text(0.76, 0.965, "Rotor and load", fontsize=10, ha="center", va="center", weight="bold")

    a2 = fig.add_axes([0.52, 0.50, 0.48, 0.44])
    a2.set_xlim(-2.6, 3.3)
    a2.set_ylim(-1.8, 2.2)
    a2.set_aspect("equal")
    a2.axis("off")
    a2.add_patch(Circle((0, 0), 1.0, fc="#EEF3F8", ec=INK, lw=1.2))
    a2.add_patch(Circle((0, 0), 0.12, fc=INK))
    a2.text(0, -0.45, "$J=5\\times10^{-5}$\nkg·m²", fontsize=8, ha="center", va="center")
    # omega arrow (arc)
    a2.add_patch(FancyArrowPatch((1.25, -0.3), (-0.3, 1.25), connectionstyle="arc3,rad=0.55",
                                 arrowstyle="-|>", mutation_scale=11, color=COLORS[0], lw=1.2))
    a2.text(1.15, 1.05, "$\\omega$", fontsize=11, color=COLORS[0])
    # motor torque
    a2.add_patch(FancyArrowPatch((-1.25, 0.3), (0.3, -1.25), connectionstyle="arc3,rad=0.55",
                                 arrowstyle="-|>", mutation_scale=11, color=COLORS[1], lw=1.2))
    a2.text(-1.55, -1.05, "$\\tau_m=Ki$", fontsize=9.5, color=COLORS[1], ha="center")
    # load torque and friction
    a2.add_patch(FancyArrowPatch((1.55, 0.55), (1.3, -0.95), connectionstyle="arc3,rad=-0.3",
                                 arrowstyle="-|>", mutation_scale=10, color="0.35", lw=1.1))
    a2.text(1.85, 0.05, "load torque $\\tau_L$\n(opposes rotation)", fontsize=8.5, ha="left", va="center")
    a2.text(1.85, -1.1, "viscous friction\n$b=10^{-5}$ N·m·s", fontsize=8.5, ha="left", va="center")
    a2.text(-2.55, 1.7, "$K=0.05$ N·m/A (V·s/rad)", fontsize=8.5, ha="left", va="center")

    # --- block diagram
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.48])
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")
    y = 3.4
    line(ax, [(0.3, y), (1.38, y)])
    lab(ax, 0.6, y + 0.1, "$V_a$")
    sj(ax, 1.6, y, signs={"w": "+", "s": "−"})
    line(ax, [(1.82, y), (2.6, y)])
    lab(ax, 2.2, y + 0.1, "", fs=8)
    blk(ax, 3.45, y, 1.7, 0.95, "$\\dfrac{1}{Ls+R}$", fs=10)
    line(ax, [(4.3, y), (5.1, y)])
    lab(ax, 4.7, y + 0.1, "$I$")
    blk(ax, 5.5, y, 0.8, 0.75, "$K$", fs=10)
    line(ax, [(5.9, y), (6.88, y)])
    lab(ax, 6.35, y + 0.1, "$T_m$")
    sj(ax, 7.1, y, signs={"w": "+", "n": "−"})
    line(ax, [(7.1, y + 1.3), (7.1, y + 0.22)])
    lab(ax, 7.1, y + 1.35, "$T_L$")
    line(ax, [(7.32, y), (8.1, y)])
    blk(ax, 8.95, y, 1.7, 0.95, "$\\dfrac{1}{Js+b}$", fs=10)
    line(ax, [(9.8, y), (11.05, y)])
    lab(ax, 10.2, y + 0.1, "$\\Omega$")
    dot(ax, 10.5, y)
    blk(ax, 11.5, y, 0.9, 0.85, "$\\dfrac{1}{s}$", fs=10)
    line(ax, [(11.95, y), (13.2, y)])
    lab(ax, 12.6, y + 0.1, "$\\Theta$")
    # back-EMF feedback
    yf = 1.6
    line(ax, [(10.5, y), (10.5, yf), (6.0, yf)], head=False)
    line(ax, [(10.5, yf), (6.0, yf)])
    blk(ax, 5.55, yf, 0.9, 0.75, "$K$", fs=10)
    line(ax, [(5.1, yf), (1.6, yf), (1.6, y - 0.22)])
    lab(ax, 3.4, yf + 0.1, "$E=K\\Omega$  (back-EMF)", fs=8.5, color=COLORS[1])
    ax.text(6.8, 0.45, "$\\dfrac{\\Omega}{V_a}=\\dfrac{K}{(Ls+R)(Js+b)+K^2}$   poles  $s=-25.5$  and  "
            "$s=-1975\\ \\mathrm{s^{-1}}$", fontsize=9.5, ha="center", va="center")
    return save(fig, "33", "fig-33-2-dc-motor-model")


# ---------------------------------------------------------------------------
def fig_tank():
    """Fig 33.3: q = 0.01 sqrt(h) and its tangent at h0 = 4 m."""
    fig, ax = new_fig(6.4, 3.9)
    h = np.linspace(0, 8, 801)
    q = 0.01 * np.sqrt(h)
    h0, q0 = 4.0, 0.02
    ql = q0 + 0.0025 * (h - h0)
    ax.fill_between(h, q, ql, color=COLORS[0], alpha=0.12, lw=0)
    ax.plot(h, q, color=COLORS[0], label="$q=0.01\\sqrt{h}$ (Torricelli)")
    ax.plot(h, ql, "--", color=COLORS[1], label="tangent: slope $1/R_\\mathrm{lin}=0.0025$ m²/s")
    ax.plot(h0, q0, "o", color=INK, ms=6, zorder=5)
    ax.annotate("operating point\n$h_0=4$ m, $q_0=0.02$ m³/s", xy=(h0, q0), xytext=(2.7, 0.0045),
                fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    # +20 % inflow
    q1 = 0.024
    ax.axhline(q1, color="0.5", lw=0.8, ls=":")
    ax.text(0.1, q1 + 0.0004, "inflow +20 %: 0.024 m³/s", fontsize=8, color="0.3", va="bottom")
    ax.plot(5.6, q1, "s", color=COLORS[1], ms=6, zorder=5)
    ax.plot(5.76, q1, "o", color=COLORS[0], ms=6, zorder=5)
    for xv, col in ((5.6, COLORS[1]), (5.76, COLORS[0])):
        ax.plot([xv, xv], [0, q1], color=col, lw=0.8, ls=":")
    ax.text(5.55, 0.0035, "linear\n5.6 m", fontsize=8, color=COLORS[1], ha="right", va="bottom")
    ax.text(5.81, 0.0035, "true\n5.76 m", fontsize=8, color=COLORS[0], ha="left", va="bottom")
    ax.annotate("error 0.16 m\n(2.8 % of level,\n9 % of the change)", xy=(5.68, q1), xytext=(6.9, 0.0165),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="-", lw=0.7, color=INK))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 0.03)
    ax.set_xlabel("Tank level $h$ (m)")
    ax.set_ylabel("Outflow $q$ (m³/s)")
    ax.grid(True, color=GRID, lw=0.6)
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.79))
    return save(fig, "33", "fig-33-3-tank-linearisation")


# ---------------------------------------------------------------------------
def fig_servo_reduction():
    """Fig 33.4: three-stage reduction of a position servo with tachometer loop."""
    fig, ax = schematic(6.8, 5.6, xlim=(0, 13.6), ylim=(0, 11.2))
    # Stage 1
    y = 9.3
    ax.text(0.1, 10.85, "Stage 1: original diagram", fontsize=9, weight="bold", va="center")
    line(ax, [(0.2, y), (0.98, y)])
    lab(ax, 0.5, y + 0.1, "$\\Theta_r$")
    sj(ax, 1.2, y, signs={"w": "+", "s": "−"})
    line(ax, [(1.42, y), (2.0, y)])
    blk(ax, 2.6, y, 1.2, 0.8, "$K_p=3$")
    line(ax, [(3.2, y), (3.98, y)])
    sj(ax, 4.2, y, signs={"w": "+", "s": "−"})
    line(ax, [(4.42, y), (5.0, y)])
    blk(ax, 5.6, y, 1.2, 0.8, "$K_a=2$")
    line(ax, [(6.2, y), (6.8, y)])
    blk(ax, 7.9, y, 2.2, 0.95, "$\\dfrac{506}{s+25.5}$", fs=10)
    line(ax, [(9.0, y), (10.6, y)])
    lab(ax, 9.5, y + 0.1, "$\\Omega$")
    dot(ax, 9.9, y)
    blk(ax, 11.1, y, 1.0, 0.8, "$\\dfrac{1}{s}$", fs=10)
    line(ax, [(11.6, y), (13.3, y)])
    lab(ax, 13.0, y + 0.1, "$\\Theta$")
    dot(ax, 12.4, y)
    # tacho loop
    yt = 8.05
    line(ax, [(9.9, y), (9.9, yt), (8.6, yt)])
    blk(ax, 7.9, yt, 1.4, 0.65, "$K_t=0.05$", fs=8.5)
    line(ax, [(7.2, yt), (4.2, yt), (4.2, y - 0.22)])
    ax.text(5.7, yt + 0.08, "tachometer", fontsize=7.5, color="0.35", ha="center", va="bottom")
    # outer loop
    yo = 7.35
    line(ax, [(12.4, y), (12.4, yo), (1.2, yo), (1.2, y - 0.22)])
    ax.text(6.8, yo - 0.1, "unity position feedback", fontsize=7.5, color="0.35", ha="center", va="top")
    # arrow between stages
    ax.annotate("", xy=(6.8, 6.05), xytext=(6.8, 6.75),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=13))
    ax.text(7.05, 6.4, "feedback rule on the inner loop:  $\\dfrac{K_aG_m}{1+K_aG_mK_t}$", fontsize=8.5,
            color=COLORS[0], va="center")
    # Stage 2
    y = 4.6
    ax.text(0.1, 5.6, "Stage 2: tachometer loop collapsed", fontsize=9, weight="bold", va="center")
    line(ax, [(0.2, y), (0.98, y)])
    lab(ax, 0.5, y + 0.1, "$\\Theta_r$")
    sj(ax, 1.2, y, signs={"w": "+", "s": "−"})
    line(ax, [(1.42, y), (2.3, y)])
    blk(ax, 2.9, y, 1.2, 0.8, "$K_p=3$")
    line(ax, [(3.5, y), (4.6, y)])
    blk(ax, 5.8, y, 2.4, 0.95, "$\\dfrac{1012}{s+76.1}$", fs=10, fc="#FFF3DD")
    line(ax, [(7.0, y), (8.4, y)])
    lab(ax, 7.6, y + 0.1, "$\\Omega$")
    blk(ax, 8.9, y, 1.0, 0.8, "$\\dfrac{1}{s}$", fs=10)
    line(ax, [(9.4, y), (11.3, y)])
    lab(ax, 10.9, y + 0.1, "$\\Theta$")
    dot(ax, 10.3, y)
    line(ax, [(10.3, y), (10.3, 3.6), (1.2, 3.6), (1.2, y - 0.22)])
    ax.annotate("", xy=(6.8, 2.35), xytext=(6.8, 3.05),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=13))
    ax.text(7.05, 2.7, "series rule, then feedback rule (unity)", fontsize=8.5, color=COLORS[0],
            va="center")
    # Stage 3
    y = 1.0
    ax.text(0.1, 1.95, "Stage 3: closed loop", fontsize=9, weight="bold", va="center")
    line(ax, [(0.6, y), (2.6, y)])
    lab(ax, 1.4, y + 0.1, "$\\Theta_r$")
    blk(ax, 4.4, y, 3.6, 1.05, "$\\dfrac{3036}{s^2+76.1s+3036}$", fs=10.5, fc="#EAF4EE")
    line(ax, [(6.2, y), (7.6, y)])
    lab(ax, 7.1, y + 0.1, "$\\Theta$")
    ax.text(7.9, y, "$\\omega_n=55.1$ rad/s,  $\\zeta=0.69$\npoles $-38.1\\pm j39.9$,  overshoot ≈ 5 %",
            fontsize=8.5, va="center", ha="left")
    return save(fig, "33", "fig-33-4-servo-block-reduction")


# ---------------------------------------------------------------------------
def fig_sfg():
    """Fig 33.5: signal-flow graph with two forward paths and three loops."""
    fig, ax = schematic(6.8, 3.9, xlim=(0, 13.6), ylim=(-3.6, 4.2))
    xs = {"R": 0.6, "E": 2.8, "x2": 5.3, "x3": 7.8, "Y": 10.3}
    names = {"R": "$R$", "E": "$E$", "x2": "$x_2$", "x3": "$x_3$", "Y": "$Y$"}
    y = 0.0
    for k, x in xs.items():
        ax.add_patch(Circle((x, y), 0.12, color=INK, zorder=5))
        if k == "x3":
            ax.text(x + 0.12, y + 0.3, names[k], fontsize=11, ha="left", va="bottom")
        else:
            ax.text(x - 0.05, y + 0.32, names[k], fontsize=11, ha="right", va="bottom")

    def br(a, b, text, rad=0.0, col=INK, ty=None, lw=1.2):
        p0, p1 = (xs[a], y), (xs[b], y)
        ar = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=12, color=col, lw=lw,
                             connectionstyle=f"arc3,rad={rad}", shrinkA=6, shrinkB=6, zorder=3)
        ax.add_patch(ar)
        if text:
            ax.text((p0[0] + p1[0]) / 2, ty if ty is not None else y + 0.18, text, fontsize=10,
                    ha="center", va="bottom" if (ty is None or ty > 0) else "top", color=col)

    c1, c2, c3 = COLORS[2], COLORS[1], COLORS[3]
    br("R", "E", "1")
    br("E", "x2", "$G_1$")
    br("x2", "x3", "$G_2$")
    br("x3", "Y", "$G_3$")
    br("E", "x3", "$G_4$", rad=-0.7, ty=1.85, col=c3, lw=1.4)
    br("x3", "x2", "$-H_1$", rad=-0.6, ty=-0.82, col=c1, lw=1.4)
    br("Y", "E", "$-H_2$", rad=-0.6, ty=-2.32, col=c2, lw=1.4)

    def loopmark(xc, yc, text, col, r=0.28):
        th = np.linspace(0.3, 2 * np.pi - 0.3, 60)
        ax.plot(xc + r * np.cos(th), yc + r * np.sin(th), color=col, lw=1.0)
        ax.annotate("", xy=(xc + r * np.cos(th[-1]), yc + r * np.sin(th[-1])),
                    xytext=(xc + r * np.cos(th[-3]), yc + r * np.sin(th[-3])),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, mutation_scale=7))
        ax.text(xc + r + 0.12, yc, text, fontsize=9.5, color=col, ha="left", va="center", weight="bold")

    loopmark(6.2, -0.38, "$L_1$", c1, r=0.17)
    loopmark(6.2, -1.45, "$L_2$", c2, r=0.2)
    loopmark(5.1, 1.0, "$L_3$", c3, r=0.18)
    ax.text(11.0, 3.6, "Loops", fontsize=9.5, weight="bold", ha="left")
    ax.text(11.0, 3.0, "$L_1=-G_2H_1$", fontsize=9.5, color=c1, ha="left")
    ax.text(11.0, 2.4, "$L_2=-G_1G_2G_3H_2$", fontsize=9.5, color=c2, ha="left")
    ax.text(11.0, 1.8, "$L_3=-G_4G_3H_2$", fontsize=9.5, color=c3, ha="left")
    ax.text(11.0, 1.0, "Forward paths", fontsize=9.5, weight="bold", ha="left")
    ax.text(11.0, 0.4, "$P_1=G_1G_2G_3$", fontsize=9.5, ha="left")
    ax.text(11.0, -0.2, "$P_2=G_4G_3$", fontsize=9.5, ha="left")
    box(ax, 10.9, -3.45, 2.65, 2.55, "", fc="#F7F7F7")
    ax.text(12.22, -1.1, "$G_1=20$\n$G_2=1/(s+2)$\n$G_3=1/s$,  $G_4=1$\n$H_1=0.5$,  $H_2=1$",
            fontsize=8.5, ha="center", va="top", linespacing=1.5)
    ax.text(1.7, -3.0, "$T=\\dfrac{s+22}{s^2+3.5s+22}$", fontsize=10, ha="center", va="center")
    return save(fig, "33", "fig-33-5-signal-flow-graph")


# ---------------------------------------------------------------------------
def _rise(t, y, fv=1.0):
    return t[np.argmax(y >= 0.9 * fv)] - t[np.argmax(y >= 0.1 * fv)]


def fig_model_reduction():
    """Fig 33.6: dominant-pole / dead-time approximations and loaded vs buffered RC."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.4))
    t = np.linspace(0, 6, 6001)
    _, yf = signal.step(([10], [1, 11, 10]), T=t)
    yd = 1 - np.exp(-t)
    ydt = np.where(t > 0.1, 1 - np.exp(-(t - 0.1)), 0.0)
    e1, e2 = np.abs(yf - yd), np.abs(yf - ydt)
    a1.plot(t, yf, color=COLORS[0], label="full  $10/[(s+1)(s+10)]$")
    a1.plot(t, yd, "--", color=COLORS[1], label="dominant pole  $1/(s+1)$")
    a1.plot(t, ydt, ":", color=COLORS[2], lw=2.0, label="with dead time  $e^{-0.1s}/(s+1)$")
    i = e1.argmax()
    a1.annotate("", xy=(t[i], yd[i]), xytext=(t[i], yf[i]),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
    a1.annotate(f"max diff {e1.max():.3f}\nat t = {t[i]:.2f} s", xy=(t[i] + 0.02, (yd[i] + yf[i]) / 2),
                xytext=(1.5, 0.55), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6))
    a1.text(2.2, 0.35, f"dead-time model: max diff {e2.max():.3f}", fontsize=8, color=COLORS[2])
    a1.set_xlim(0, 6)
    a1.set_ylim(0, 1.05)
    a1.set_xlabel("Time (s)")
    a1.set_ylabel("Step response")
    a1.grid(True, color=GRID, lw=0.6)
    a1.legend(loc="lower right", fontsize=7.3)
    a1.set_title("(a) dominant-pole approximation", fontsize=9.5)

    t = np.linspace(0, 1.5, 15001)
    _, yb = signal.step(([1], [0.01, 0.2, 1]), T=t)
    _, yl = signal.step(([1], [0.01, 0.3, 1]), T=t)
    a2.plot(t, yb, color=COLORS[0], label=f"buffered $1/(0.1s+1)^2$ ($t_r$ = {_rise(t, yb):.2f} s)")
    a2.plot(t, yl, "--", color=COLORS[1], label=f"loaded $1/(0.01s^2+0.3s+1)$ ($t_r$ = {_rise(t, yl):.2f} s)")
    a2.axhline(0.5, color="0.5", lw=0.7, ls=":")
    for yy, col in ((yb, COLORS[0]), (yl, COLORS[1])):
        t50 = t[np.argmax(yy >= 0.5)]
        a2.plot(t50, 0.5, "o", color=col, ms=5, zorder=5)
        a2.plot([t50, t50], [0, 0.5], color=col, lw=0.8, ls=":")
        a2.text(t50 + (0.03 if col == COLORS[1] else -0.03), 0.47 if col == COLORS[1] else 0.53, f"{t50:.2f} s", fontsize=8, color=col,
                ha="left" if col == COLORS[1] else "right", va="top" if col == COLORS[1] else "bottom")
    a2.text(1.48, 0.52, "50 %", fontsize=8, color="0.4", va="bottom", ha="right")
    a2.set_xlim(0, 1.5)
    a2.set_ylim(0, 1)
    a2.set_xlabel("Time (s)")
    a2.grid(True, color=GRID, lw=0.6)
    a2.legend(loc="lower right", fontsize=7.0, bbox_to_anchor=(1.0, 0.02))
    a2.set_title("(b) two RC sections: buffered vs loaded", fontsize=9.5)
    fig.tight_layout()
    print(f"  33.6 max diff {e1.max():.4f} at {t[i] if False else ''} ; dt {e2.max():.4f}")
    return save(fig, "33", "fig-33-6-model-reduction-step")


if __name__ == "__main__":
    fig_analogous_systems()
    fig_dc_motor()
    fig_tank()
    fig_servo_reduction()
    fig_sfg()
    fig_model_reduction()
