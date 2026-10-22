"""Figures for Chapter 14 — Transmission Lines.

Run from the repository root:  python figures/scripts/ch14.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle, Arc, FancyArrowPatch  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

schemdraw.use("matplotlib")

COPPER = "#C87533"
DIEL = "#E8E2C8"
GREY = "#8A8A8A"


# ---------------------------------------------------------------- 14.1
def _coax(ax, cx, cy):
    ax.add_patch(Circle((cx, cy), 1.0, fc=COPPER, ec=INK, lw=0.8))
    ax.add_patch(Circle((cx, cy), 0.85, fc=DIEL, ec=INK, lw=0.6))
    ax.add_patch(Circle((cx, cy), 0.25, fc=COPPER, ec=INK, lw=0.8))
    ax.text(cx, cy - 1.25, "coaxial cable", ha="center", va="top", fontsize=8.5)


def _microstrip(ax, cx, cy):
    ax.add_patch(Rectangle((cx - 1.2, cy - 0.75), 2.4, 0.12, fc=COPPER, ec=INK, lw=0.6))
    ax.add_patch(Rectangle((cx - 1.2, cy - 0.63), 2.4, 0.55, fc=DIEL, ec=INK, lw=0.6))
    ax.add_patch(Rectangle((cx - 0.35, cy - 0.08), 0.7, 0.14, fc=COPPER, ec=INK, lw=0.6))
    ax.text(cx, cy - 1.0, "microstrip over ground", ha="center", va="top", fontsize=8.5)


def _twowire(ax, cx, cy):
    for dx in (-0.6, 0.6):
        ax.add_patch(Circle((cx + dx, cy), 0.28, fc=COPPER, ec=INK, lw=0.8))
    ax.text(cx, cy - 0.65, "two-wire line", ha="center", va="top", fontsize=8.5)


def fig_14_1():
    """Cross-sections and the lumped RLGC ladder of a transmission line."""
    fig = plt.figure(figsize=(6.8, 3.4))
    a0 = fig.add_axes([0.0, 0.0, 0.16, 1.0])
    a0.set_xlim(-1.5, 1.5)
    a0.set_ylim(-1.2, 8.3)
    a0.set_aspect("equal")
    a0.axis("off")
    _coax(a0, 0, 6.6)
    _microstrip(a0, 0, 3.6)
    _twowire(a0, 0, 1.0)
    ax = fig.add_axes([0.18, 0.0, 0.82, 1.0])
    ax.axis("off")
    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=9, unit=1.6, lw=1.2)
        elm.SourceSin().up(3).at((0, 0))
        x = 0.0
        nodes = [0.0]
        for k in range(3):
            lab = (k == 1)
            elm.Line().at((x, 3)).right(1.0)
            r = elm.Resistor().right(1.4)
            if lab:
                r.label("$R\\,\\Delta z$", loc="top")
            li = elm.Inductor2(loops=3).right(1.4)
            if lab:
                li.label("$L\\,\\Delta z$", loc="top")
            elm.Line().right(1.6)
            x += 5.4
            elm.Dot()
            nodes.append(x)
            elm.Line().at((x, 3)).down(1.0)
            elm.Line().at((x - 0.55, 2.0)).right(1.1)
            g = elm.Resistor().at((x - 0.55, 2.0)).down(1.4)
            if lab:
                g.label("$G\\,\\Delta z$", loc="top")
            c = elm.Capacitor().at((x + 0.55, 2.0)).down(1.4)
            if lab:
                c.label("$C\\,\\Delta z$", loc="bottom")
            elm.Line().at((x - 0.55, 0.6)).right(1.1)
            elm.Line().at((x, 0.6)).down(0.6)
            elm.Dot().at((x, 0))
        elm.Line().at((x, 3)).right(1.6)
        elm.RBox().down(3).label("$Z_L$", loc="bottom")
        elm.Line().left(x + 1.6)
        xa, xb = nodes[1], nodes[2]
        elm.Label().at((xa - 0.15, 2.5)).label("$v(z,t)$", fontsize=9, halign="right")
        elm.Label().at((xb - 0.15, 2.5)).label("$v(z+\\Delta z,t)$", fontsize=9, halign="right")
        for xx, t in ((xa, "$i(z,t)$"), (xb, "$i(z+\\Delta z,t)$")):
            elm.Arrow(headwidth=0.18, headlength=0.25).at((xx + 0.1, 3)).to((xx + 0.75, 3))
            elm.Label().at((xx + 0.12, 2.45)).label(t, fontsize=8.5, halign="left")
        # position axis
        elm.Arrow(headwidth=0.2, headlength=0.3).at((0.6, -0.9)).to((x + 2.2, -0.9))
        elm.Label().at((x + 2.5, -0.9)).label("$z$", fontsize=10)
        for xx, t in ((xa, "$z$"), (xb, "$z+\\Delta z$")):
            elm.Line().at((xx, -0.75)).down(0.3)
            elm.Label().at((xx, -1.4)).label(t, fontsize=9)
        elm.Label().at(((xa + xb) / 2, -1.4)).label("one section", fontsize=8, color=GREY)
        elm.Label().at((0, 3.6)).label("source", fontsize=8.5, color=GREY)
        elm.Label().at((x + 1.6, 3.6)).label("load", fontsize=8.5, color=GREY)
    d.draw(show=False)
    save(fig, "14", "fig-14-1-distributed-line-section")


# ---------------------------------------------------------------- 14.2
def fig_14_2():
    """Bounce diagram and load-voltage staircase, 25-ohm driver, open 50-ohm line."""
    td = 0.9  # ns
    ell = 15.0  # cm
    Vs, Rs, Z0 = 5.0, 25.0, 50.0
    gs = (Rs - Z0) / (Rs + Z0)
    gl = 1.0
    v1 = Vs * Z0 / (Rs + Z0)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 4.0), gridspec_kw=dict(width_ratios=(1, 1.25),
                                                                             wspace=0.35))
    # lattice
    a1.set_xlim(-2.5, ell + 2.5)
    a1.set_ylim(9.3, -0.5)
    a1.axvline(0, color=INK, lw=1.2)
    a1.axvline(ell, color=INK, lw=1.2)
    wave = v1
    t = 0.0
    x0, x1 = 0.0, ell
    labels = []
    for k in range(10):
        if t + td > 9.0 + 1e-9:
            break
        a1.annotate("", xy=(x1, t + td), xytext=(x0, t),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS[0] if wave > 0 else COLORS[1],
                                    lw=1.2, mutation_scale=9, shrinkA=0, shrinkB=0))
        labels.append(((x0 + x1) / 2, t + td / 2, wave))
        t += td
        wave *= gl if x1 == ell else gs
        x0, x1 = x1, x0
    for k, (xm, tm, w) in enumerate(labels[:6]):
        txt = f"{w:+.2f} V".replace("-", "−")
        a1.text(xm, tm - 0.12, txt, fontsize=7.8, ha="center", va="bottom",
                color=COLORS[0] if w > 0 else COLORS[1])
    a1.text(0, 9.55, "driver (25 Ω)\n$\\Gamma_S$ = −1/3", ha="center", va="top", fontsize=8)
    a1.text(ell, 9.55, "open end\n$\\Gamma_L$ = +1", ha="center", va="top", fontsize=8)
    a1.set_xlabel("position along trace (cm)")
    a1.set_ylabel("time (ns)")
    a1.set_xticks([0, 5, 10, 15])
    a1.set_yticks(range(0, 10))
    a1.spines["bottom"].set_visible(False)
    a1.spines["left"].set_position(("outward", 4))
    a1.xaxis.set_ticks_position("top")
    a1.xaxis.set_label_position("top")
    a1.spines["top"].set_visible(True)
    # staircase
    tt = np.linspace(0, 10, 2001)
    vl = np.zeros_like(tt)
    inc = v1
    for k in range(10):
        tk = (2 * k + 1) * td
        vl += np.where(tt >= tk, inc * (1 + gl), 0)
        inc *= gl * gs
    a2.plot(tt, vl, color=COLORS[0], lw=1.8, label="25 Ω driver, unterminated")
    vst = np.where(tt >= td, 5.0, 0.0)
    a2.plot(tt, vst, color=COLORS[2], lw=1.6, ls="--", label="with 25 Ω series resistor")
    a2.axhline(5.0, color="#999999", lw=0.8, ls=":")
    levels = [(td, 6.67), (3 * td, 4.44), (5 * td, 5.19), (7 * td, 4.94), (9 * td, 5.02)]
    offs = [0.3, -0.35, 0.3, -0.35, 0.3]
    for (tk, v), o in zip(levels, offs):
        a2.text(tk + 0.9, v + o, f"{v:.2f}", fontsize=8, ha="center",
                va="bottom" if o > 0 else "top", color=COLORS[0])
    a2.set_xlim(0, 10)
    a2.set_ylim(0, 7.8)
    a2.set_xlabel("time (ns)")
    a2.set_ylabel("load voltage (V)")
    a2.grid(True, lw=0.4)
    a2.legend(loc="lower right", fontsize=7.8)
    save(fig, "14", "fig-14-2-bounce-diagram-ringing")


# ---------------------------------------------------------------- 14.3
def fig_14_3():
    """Standing-wave patterns on a lossless 50-ohm line for four loads."""
    d = np.linspace(0, 1, 2001)
    Z0 = 50
    loads = [("matched, 50 Ω (VSWR 1)", 50, COLORS[2], "-"),
             ("75 Ω (|Γ| = 0.2, VSWR 1.5)", 75, COLORS[0], "-"),
             ("100 + j50 Ω (|Γ| = 0.447∠26.6°, VSWR 2.62)", 100 + 50j, COLORS[1], "-"),
             ("short circuit (|Γ| = 1, VSWR ∞)", 0, COLORS[3], "--")]
    fig, ax = new_fig(6.6, 4.0)
    for lab, ZL, c, ls in loads:
        g = (ZL - Z0) / (ZL + Z0)
        v = np.abs(1 + g * np.exp(-1j * 4 * np.pi * d))
        ax.plot(d, v, color=c, ls=ls, label=lab)
    g = (100 + 50j - 50) / (150 + 50j)
    dmax = np.angle(g) / (4 * np.pi)
    ax.plot([dmax], [1 + abs(g)], "o", color=COLORS[1], ms=5, zorder=5)
    ax.annotate(f"$V_{{max}}$ = 1.447\nat d = {dmax:.3f}λ", (dmax, 1 + abs(g)), xytext=(0.005, 1.68),
                fontsize=8, color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    dmin = dmax + 0.25
    ax.plot([dmin], [1 - abs(g)], "o", color=COLORS[1], ms=5, zorder=5)
    ax.annotate("$V_{min}$ = 0.553", (dmin, 1 - abs(g)), xytext=(0.33, 0.30), fontsize=8,
                color=COLORS[1], arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    # half-wavelength period
    y = 2.08
    ax.annotate("", xy=(dmax + 0.5, y), xytext=(dmax, y),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=INK, mutation_scale=8,
                                shrinkA=0, shrinkB=0))
    ax.text(dmax + 0.25, y + 0.03, "λ/2 period", ha="center", va="bottom", fontsize=8)
    for dz in (0.0, 0.5, 1.0):
        ax.plot([dz], [0], "o", color=COLORS[3], ms=4, zorder=5, clip_on=False)
    ax.text(0.52, 0.06, "short: zeros at d = 0, λ/2, λ", fontsize=8, color=COLORS[3])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.25)
    ax.set_xlabel("distance from load  d/λ   (load at left)")
    ax.set_ylabel("|V(d)| / |V$^+$|")
    ax.grid(True, lw=0.4)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=7.8)
    save(fig, "14", "fig-14-3-standing-wave-patterns")


# ---------------------------------------------------------------- 14.4
def _smith_grid(ax):
    unit = Circle((0, 0), 1, fc="none", ec=INK, lw=1.1, zorder=3)
    ax.add_patch(unit)
    clip = Circle((0, 0), 1, transform=ax.transData)
    gc = "#B8B8B8"
    for r in (0.2, 0.5, 1, 2, 5):
        c = Circle((r / (1 + r), 0), 1 / (1 + r), fc="none", ec=gc, lw=0.7)
        ax.add_patch(c)
        ax.text(r / (1 + r) - 1 / (1 + r) + 0.012, 0.012, f"{r:g}", fontsize=7, color="#666666",
                ha="left", va="bottom", rotation=90)
    for x in (0.2, 0.5, 1, 2, 5):
        for sgn in (1, -1):
            c = Circle((1, sgn / x), 1 / x, fc="none", ec=gc, lw=0.7)
            ax.add_patch(c)
            c.set_clip_path(clip)
            z = complex(0, sgn * x)
            G = (z - 1) / (z + 1)
            ax.text(G.real * 1.07, G.imag * 1.07, f"{'+' if sgn > 0 else '−'}j{x:g}", fontsize=7,
                    color="#666666", ha="center", va="center")
    ax.plot([-1, 1], [0, 0], color=gc, lw=0.7)


BB = dict(fc="white", ec="none", alpha=0.8, pad=1.0)


def fig_14_4():
    """Single shunt-stub match of 100 + j50 ohm on a 50-ohm line."""
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.62, 1.62)
    ax.set_ylim(-1.18, 1.18)
    _smith_grid(ax)
    zl = 2 + 1j
    G = (zl - 1) / (zl + 1)
    yG = -G
    rho = abs(G)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(rho * np.cos(th), rho * np.sin(th), color=COLORS[4], lw=1.2, ls="--", zorder=4)
    # r = 1 / g = 1 circle highlighted
    ax.add_patch(Circle((0.5, 0), 0.5, fc="none", ec=COLORS[2], lw=2.0, zorder=4))
    ax.annotate("g = 1 circle\n(chart read as\nadmittance)", (0.5 + 0.5 * np.cos(-1.1), 0.5 * np.sin(-1.1)),
                xytext=(1.02, -0.85), fontsize=8, color=COLORS[2], ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[2]))
    # points
    ax.plot([G.real], [G.imag], "o", color=COLORS[1], ms=7, zorder=6)
    ax.annotate("$z_L$ = 2 + j1\nΓ = 0.447∠26.6°", (G.real, G.imag), xytext=(1.05, 0.66),
                fontsize=8.5, color=COLORS[1], va="center", ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[1]))
    ax.plot([yG.real], [yG.imag], "s", color=COLORS[0], ms=7, zorder=6)
    ax.text(yG.real - 0.04, yG.imag - 0.06, "$y_L$ = 0.4 − j0.2", fontsize=8.5, color=COLORS[0],
            ha="right", va="top", bbox=BB)
    ax.plot([G.real, yG.real], [G.imag, yG.imag], color="#999999", lw=0.7, ls=":")
    ax.plot([rho], [0], "D", color=COLORS[4], ms=5, zorder=6)
    ax.annotate("VSWR = 2.62\n(r = 2.62)", (rho, 0), xytext=(1.08, 0.32), fontsize=8,
                color="#9A6A00", arrowprops=dict(arrowstyle="-", lw=0.7, color="#9A6A00"))
    # rotation toward generator: clockwise from angle(yG) to angle(y = 1 + j1)
    y1 = (1 + 1j - 1) / (1 + 1j + 1)
    y2 = (1 - 1j - 1) / (1 - 1j + 1)
    a0 = np.angle(yG)            # -153.4 deg
    a1 = np.angle(y1)            # +63.4 deg
    a0u = a0 % (2 * np.pi)       # 206.6 deg
    angs = np.linspace(a0u, a1, 200)
    rr = rho + 0.06
    ax.plot(rr * np.cos(angs), rr * np.sin(angs), color=COLORS[0], lw=1.6, zorder=5)
    ax.annotate("", xy=(rho * np.cos(a1) * 1.0, rho * np.sin(a1)),
                xytext=(rr * np.cos(a1 + 0.12), rr * np.sin(a1 + 0.12)),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.6, mutation_scale=12,
                                shrinkA=0, shrinkB=0))
    am = np.radians(150)
    ax.annotate("$d_1$ = 0.199λ\ntoward generator\n(clockwise)", (rr * np.cos(am), rr * np.sin(am)),
                xytext=(-1.05, 0.55), fontsize=8.5, color=COLORS[0], ha="right", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[0]))
    ax.plot([y1.real], [y1.imag], "o", color=COLORS[0], ms=7, zorder=6, mfc="white", mew=2)
    ax.text(y1.real - 0.07, y1.imag + 0.13, "y = 1 + j1", fontsize=8.5, color=COLORS[0],
            va="bottom", ha="right", bbox=BB)
    # stub: along g = 1 circle from y1 to centre
    c0 = 0.5
    b0 = np.angle(y1 - c0)
    bb = np.linspace(b0, np.pi, 100)
    ax.plot(c0 + 0.5 * np.cos(bb), 0.5 * np.sin(bb), color=COLORS[3], lw=2.4, zorder=5)
    ax.annotate("", xy=(0.0, 0.0), xytext=(c0 + 0.5 * np.cos(np.pi - 0.15), 0.5 * np.sin(np.pi - 0.15)),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[3], lw=2.0, mutation_scale=12,
                                shrinkA=0, shrinkB=0))
    ax.annotate("shorted stub 0.125λ\ngives −j1  →  y = 1 (matched)", (0.03, 0.22),
                xytext=(-1.05, 0.98), fontsize=8.5, color=COLORS[3], ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=COLORS[3]))
    ax.plot([0], [0], "*", color=INK, ms=10, zorder=7)
    # second solution
    ax.plot([y2.real], [y2.imag], "o", color=GREY, ms=7, zorder=6, mfc="white", mew=2)
    ax.annotate("alternative:\ny = 1 − j1 at $d_2$ = 0.375λ\n(shorted stub 0.375λ\ngives +j1)",
                (y2.real, y2.imag), xytext=(-1.05, -0.75), fontsize=8, color="#555555", ha="right",
                arrowprops=dict(arrowstyle="-", lw=0.7, color="#555555"))
    ax.text(1.6, 1.12, "$Z_0$ = 50 Ω\ndashed: |Γ| = 0.447\n(VSWR 2.62) circle", fontsize=8,
            color="#9A6A00", va="top", ha="right")
    save(fig, "14", "fig-14-4-smith-chart-stub-match")


# ---------------------------------------------------------------- 14.5
def _fit(fm, vals):
    """Least-squares fit of a*sqrt(f) + b*f (non-negative) in relative error."""
    from scipy.optimize import nnls
    A = np.column_stack([np.sqrt(fm), fm]) / np.array(vals)[:, None]
    coef, _ = nnls(A, np.ones(len(vals)))
    return coef


def fig_14_5():
    """Attenuation versus frequency for coax cables and FR-4 microstrip."""
    data = [
        ("RG-58", [1, 10, 100, 1000], [1.4, 4.5, 16, 65], COLORS[0], 3000),
        ("RG-213", [10, 100, 1000], [2, 7, 27], COLORS[2], 3000),
        ("LMR-400", [10, 100, 1000], [1.3, 4, 13], COLORS[3], 3000),
        ("FR-4 50 Ω microstrip", [10, 100, 1000, 10000], [100, 300, 900, 5000], COLORS[1], 10000),
    ]
    fig, ax = new_fig(6.4, 4.4)
    for name, fm, vals, c, fmax in data:
        a, b = _fit(np.array(fm, float), vals)
        f = np.logspace(0, np.log10(fmax), 300)
        ax.loglog(f * 1e6, a * np.sqrt(f) + b * f, color=c, label=name)
        ax.loglog(np.array(fm) * 1e6, vals, "o", color=c, ms=4.5)
    # reference slopes
    f = np.logspace(0.3, 2.3, 10)
    ax.loglog(f * 1e6, 0.25 * np.sqrt(f), color="#777777", lw=1.0, ls=":")
    ax.text(30e6, 0.25 * np.sqrt(30) * 0.62, "∝ √f (conductor loss)", fontsize=8, color="#555555",
            rotation=14, ha="center")
    f = np.logspace(2.7, 4, 10)
    ax.loglog(f * 1e6, 0.12 * f, color="#777777", lw=1.0, ls="-.")
    ax.text(2.2e9, 0.12 * 2200 * 1.6, "∝ f (dielectric loss)", fontsize=8, color="#555555",
            rotation=27, ha="center")
    ax2 = ax.secondary_yaxis("right", functions=(lambda v: v / 1e4, lambda v: v * 1e4))
    ax2.set_ylabel("dB/cm")
    ax.set_xlim(1e6, 1e10)
    ax.set_ylim(0.1, 1e4)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("attenuation (dB/100 m)")
    ax.grid(True, which="major", lw=0.5)
    ax.grid(True, which="minor", lw=0.25)
    ax.legend(loc="upper left", fontsize=8.5)
    ax.text(0.99, 0.02, "markers: typical data-sheet values; lines: fit $a\\sqrt{f}+bf$",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#555555")
    save(fig, "14", "fig-14-5-cable-attenuation")


# ---------------------------------------------------------------- 14.6
def _xs_microstrip(ax):
    w, t, h = 0.35, 0.035, 0.2
    L = 1.6
    ax.add_patch(Rectangle((-L / 2, -t), L, t, fc=COPPER, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-L / 2, 0), L, h, fc=DIEL, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-w / 2, h), w, t, fc=COPPER, ec=INK, lw=0.5))
    ax.annotate("", xy=(w / 2, h + 0.11), xytext=(-w / 2, h + 0.11),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.6, mutation_scale=5, shrinkA=0, shrinkB=0))
    ax.text(0, h + 0.13, "w = 0.35", fontsize=7, ha="center", va="bottom")
    ax.annotate("", xy=(0.62, h), xytext=(0.62, 0),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.6, mutation_scale=5, shrinkA=0, shrinkB=0))
    ax.text(0.66, h / 2, "h = 0.2", fontsize=7, va="center")
    ax.text(-0.78, h / 2, "FR-4\nεr = 4.3", fontsize=6.5, va="center")
    ax.set_title("surface microstrip, t = 35 µm:  $Z_0$ ≈ 48.6 Ω", fontsize=8, pad=2)
    ax.set_xlim(-0.85, 0.95)
    ax.set_ylim(-0.08, 0.42)


def _xs_stripline(ax):
    w, t, b = 0.14, 0.035, 0.4
    L = 1.6
    ax.add_patch(Rectangle((-L / 2, -t), L, t, fc=COPPER, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-L / 2, 0), L, b, fc=DIEL, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-L / 2, b), L, t, fc=COPPER, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-w / 2, b / 2 - t / 2), w, t, fc=COPPER, ec=INK, lw=0.5))
    ax.annotate("", xy=(0.62, b), xytext=(0.62, 0),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.6, mutation_scale=5, shrinkA=0, shrinkB=0))
    ax.text(0.66, b / 2, "b = 0.4", fontsize=7, va="center")
    ax.text(0.12, b / 2, "w = 0.14", fontsize=7, va="center")
    ax.set_title("symmetric stripline between planes:  ≈ 48 Ω", fontsize=8, pad=2)
    ax.set_xlim(-0.85, 0.95)
    ax.set_ylim(-0.08, 0.48)


def _xs_diffpair(ax):
    w, s, t, h = 0.2, 0.15, 0.035, 0.2
    L = 1.6
    ax.add_patch(Rectangle((-L / 2, -t), L, t, fc=COPPER, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((-L / 2, 0), L, h, fc=DIEL, ec=INK, lw=0.5))
    xl, xr = -s / 2 - w, s / 2
    ax.add_patch(Rectangle((xl, h), w, t, fc=COPPER, ec=INK, lw=0.5))
    ax.add_patch(Rectangle((xr, h), w, t, fc=COPPER, ec=INK, lw=0.5))
    ax.text(xl + w / 2, h + t + 0.02, "+", fontsize=8, ha="center", va="bottom")
    ax.text(xr + w / 2, h + t + 0.02, "−", fontsize=8, ha="center", va="bottom")
    # odd-mode field lines: arcs from + trace to - trace
    for r in (0.12, 0.19, 0.27):
        ax.add_patch(Arc((0, h + t / 2), 2 * r, 1.4 * r, theta1=0, theta2=180, color=COLORS[0],
                         lw=0.7))
        ax.add_patch(Arc((0, h + t / 2), 2 * r, 1.0 * r, theta1=180, theta2=360, color=COLORS[0],
                         lw=0.7, ls="--"))
    for xx in (xl + 0.04, xl + w - 0.04, xr + 0.04, xr + w - 0.04):
        ax.plot([xx, xx], [h, 0.005], color=COLORS[0], lw=0.6, ls=":")
    ax.text(0.7, h / 2, "s = 0.15\nw = 0.2", fontsize=7, va="center")
    ax.set_title("edge-coupled differential pair:  $Z_{diff}$ ≈ 100 Ω", fontsize=8, pad=2)
    ax.set_xlim(-0.85, 0.95)
    ax.set_ylim(-0.08, 0.48)


def fig_14_6():
    """PCB line cross-sections (to scale, mm) and critical length versus rise time."""
    fig = plt.figure(figsize=(6.8, 4.4))
    ys = [0.68, 0.36, 0.04]
    for y, fn in zip(ys, (_xs_microstrip, _xs_stripline, _xs_diffpair)):
        a = fig.add_axes([0.0, y, 0.40, 0.27])
        a.set_aspect("equal")
        a.axis("off")
        fn(a)
    fig.text(0.20, 0.985, "cross-sections to scale (mm)", ha="center", va="top", fontsize=8.5,
             color="#555555")
    ax = fig.add_axes([0.53, 0.12, 0.45, 0.80])
    tr = np.logspace(-11, -8, 200)
    dps = 6.9e-12  # s per mm
    l6 = tr / 6 / dps
    l2 = tr / 2 / dps
    ax.loglog(tr * 1e12, l6, color=COLORS[0], label="$t_d = t_r/6$ (conservative)")
    ax.loglog(tr * 1e12, l2, color=COLORS[1], ls="--", label="$2t_d = t_r$ (reflections visible)")
    ax.fill_between(tr * 1e12, l6, 1e5, color=COLORS[0], alpha=0.10, lw=0)
    ax.text(32, 25, "treat as a\ntransmission line", fontsize=9, color="#1F4E79", ha="center")
    ax.text(2000, 0.6, "lumped\nconnection", fontsize=9, color="#555555", ha="center")
    for v, c in ((1000 / 6 / 6.9, COLORS[0]), (1000 / 2 / 6.9, COLORS[1])):
        ax.plot([1000], [v], "o", color=c, ms=5, zorder=5)
        ax.text(1000 * 1.25, v, f"{v:.0f} mm", fontsize=8, color=c, va="center")
    ax.axvline(1000, color="#999999", lw=0.7, ls=":")
    ax.text(1000, 0.13, "$t_r$ = 1 ns", fontsize=8, ha="center", va="bottom", color="#555555")
    ax.set_xlim(10, 1e4)
    ax.set_ylim(0.1, 1000)
    ax.set_xlabel("rise time $t_r$ (ps)")
    ax.set_ylabel("critical length (mm)")
    ax.grid(True, which="major", lw=0.5)
    ax.grid(True, which="minor", lw=0.25)
    ax.legend(loc="upper left", fontsize=7.6)
    ax.set_title("FR-4 stripline, 6.9 ps/mm", fontsize=9)
    save(fig, "14", "fig-14-6-pcb-interconnects")


if __name__ == "__main__":
    fig_14_1()
    fig_14_2()
    fig_14_3()
    fig_14_4()
    fig_14_5()
    fig_14_6()
