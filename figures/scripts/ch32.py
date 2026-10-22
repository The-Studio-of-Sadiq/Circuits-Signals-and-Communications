"""Figures for Chapter 32 — RF and Microwave Fundamentals.

Run from the repository root:  python figures/scripts/ch32.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon  # noqa: E402
from scipy import special  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402

schemdraw.use("matplotlib")
C0 = 2.998e8


# ---------------------------------------------------------------------------
def fig_capacitor_srf():
    """Fig 32.1: |Z| of real SMD capacitors (series R-L-C) versus frequency."""
    f = np.logspace(6, 10, 2000)
    w = 2 * np.pi * f
    L = 0.7e-9
    parts = [("A: 1 nF, ESR 0.1 Ω", 1e-9, 0.1, COLORS[0]),
             ("B: 10 pF, ESR 0.3 Ω", 10e-12, 0.3, COLORS[1])]
    fig, ax = new_fig(6.4, 4.2)
    for lab, C, R, col in parts:
        Z = np.abs(R + 1j * w * L + 1 / (1j * w * C))
        ax.loglog(f, Z, color=col, label=lab)
        ax.loglog(f, 1 / (w * C), "--", color=col, lw=0.9, alpha=0.7)
        fsrf = 1 / (2 * np.pi * np.sqrt(L * C))
        ax.plot(fsrf, R, "o", color=col, ms=5)
        ax.annotate(f"SRF {fsrf/1e6:.0f} MHz" if fsrf < 1e9 else f"SRF {fsrf/1e9:.1f} GHz",
                    xy=(fsrf, R), xytext=(fsrf * 0.33, R * 0.30 if R < 0.2 else R * 0.25),
                    fontsize=8.5, color=col, ha="center",
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.7))
    ax.loglog(f, w * L, ":", color=INK, lw=1.2)
    ax.text(3e7, 2 * np.pi * 3e7 * L * 1.7, r"$2\pi fL$, 0.7 nH", fontsize=8.5,
            rotation=27, ha="center", va="bottom")
    ax.text(2.4e6, 1 / (2 * np.pi * 2.4e6 * 1e-9) * 0.45, r"$1/(2\pi fC)$, 1 nF", fontsize=8.5,
            color=COLORS[0], rotation=-27, ha="center", va="top")
    ax.text(3.5e7, 1 / (2 * np.pi * 3.5e7 * 10e-12) * 0.45, r"$1/(2\pi fC)$, 10 pF", fontsize=8.5,
            color=COLORS[1], rotation=-27, ha="center", va="top")
    # 2.4 GHz marker
    f24 = 2.4e9
    ax.plot([f24, f24], [0.01, 120], color="0.45", lw=0.9, ls="-.")
    ax.text(f24 * 1.07, 90, "2.4 GHz", fontsize=8.5, color="0.3", va="top")
    for lab, C, R, col in parts:
        Z = abs(R + 1j * 2 * np.pi * f24 * L + 1 / (1j * 2 * np.pi * f24 * C))
        ax.plot(f24, Z, "s", color=col, ms=5)
        ax.text(f24 * (0.8 if C > 1e-10 else 0.88), Z * (2.1 if C > 1e-10 else 1.0), f"{Z:.1f} Ω", fontsize=8.5, color=col,
                va="center", ha="right", bbox=dict(fc="white", ec="none", pad=0.5))
    # regions
    ax.text(3e6, 0.15, "capacitive", fontsize=9, color="0.35", style="italic", ha="center")
    ax.text(5.0e9, 1.0, "inductive", fontsize=9, color="0.35", style="italic", ha="center")
    ax.set_xlim(1e6, 1e10)
    ax.set_ylim(0.01, 1000)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Impedance magnitude |Z| (Ω)")
    ax.grid(True, which="major", color=GRID, lw=0.6)
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.36), fontsize=8.5)
    # inset: series RLC equivalent circuit
    ins = fig.add_axes([0.70, 0.74, 0.25, 0.11])
    ins.axis("off")
    with schemdraw.Drawing(canvas=ins, show=False) as d:
        d.config(unit=1.6, fontsize=8.5, lw=1.0)
        elm.Dot(open=True)
        elm.Resistor().right().label("ESR", loc="top")
        elm.Inductor().right().label("ESL", loc="top")
        elm.Capacitor().right().label("C", loc="top")
        elm.Dot(open=True)
        d.draw(show=False)
    ins.set_aspect("equal")
    return save(fig, "32", "fig-32-1-capacitor-srf")


# ---------------------------------------------------------------------------
def _rl_single(f):
    w = 2 * np.pi * f
    z = 10 + 1j * w * 1.33e-9
    Z = 1 / (1 / z + 1j * w * 2.65e-12)
    G = (Z - 50) / (Z + 50)
    return -20 * np.log10(np.abs(G))


def _rl_two(f, f0=2.4e9):
    w0 = 2 * np.pi * f0
    w = 2 * np.pi * f
    Rm = np.sqrt(50 * 10)
    Q1 = np.sqrt(Rm / 10 - 1)
    Q2 = np.sqrt(50 / Rm - 1)
    L1, C1 = Q1 * 10 / w0, Q1 / Rm / w0
    L2, C2 = Q2 * Rm / w0, Q2 / 50 / w0
    z = 10 + 1j * w * L1
    z = 1 / (1 / z + 1j * w * C1)
    z = z + 1j * w * L2
    z = 1 / (1 / z + 1j * w * C2)
    G = (z - 50) / (z + 50)
    return -20 * np.log10(np.abs(G))


def fig_l_network():
    """Fig 32.2: L-network schematic and return loss versus frequency."""
    fig = plt.figure(figsize=(6.8, 3.4))
    axs = fig.add_axes([0.0, 0.05, 0.47, 0.9])
    axs.axis("off")
    with schemdraw.Drawing(canvas=axs, show=False) as d:
        d.config(unit=2.2, fontsize=9, lw=1.1)
        p1 = elm.Dot(open=True).label("50 Ω\nport", loc="left")
        elm.Line().right(d.unit * 0.6)
        top = elm.Dot()
        d.push()
        elm.Capacitor().down().label("C\n2.65 pF", loc="bottom")
        gl = elm.Ground()
        d.pop()
        elm.Inductor().right().label("L = 1.33 nH", loc="top")
        elm.Resistor().down().label("$R_L$\n10 Ω", loc="bottom")
        elm.Ground()
        d.draw(show=False)
    axs.set_aspect("equal")
    x0, y0 = p1.center
    axs.annotate("", xy=(x0 + 1.25, y0 + 0.45), xytext=(x0 + 0.05, y0 + 0.45),
                 arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.1, mutation_scale=9))
    axs.text(x0 + 0.05, y0 + 0.68, "$Z_\\mathrm{in}=50\\ \\Omega$", fontsize=9, color=COLORS[0])
    axs.text(x0 + 2.1, y0 - 3.4, "2.4 GHz, $Q=2$\n$X_s=20\\ \\Omega$, $X_p=25\\ \\Omega$",
             fontsize=8.5, ha="center", va="top", color="0.25")
    xl, yl = axs.get_xlim(), axs.get_ylim()
    axs.set_xlim(xl[0] - 0.4, xl[1] + 0.3)
    axs.set_ylim(yl[0] - 1.0, yl[1] + 0.6)

    ax = fig.add_axes([0.58, 0.17, 0.40, 0.75])
    f = np.linspace(2.0e9, 2.8e9, 1601)
    rl1 = np.clip(_rl_single(f), 0, 60)
    rl2 = np.clip(_rl_two(f), 0, 60)
    ax.plot(f / 1e9, rl1, color=COLORS[0], label="single L (Q = 2)")
    ax.plot(f / 1e9, rl2, "--", color=COLORS[1], label="two-section\n(via 22.4 Ω)")
    ax.axhline(10, color="0.4", lw=0.9, ls=":")
    ax.text(2.78, 9.6, "10 dB", fontsize=8.5, color="0.3", va="bottom", ha="right")
    for fx in (2.2e9, 2.6e9):
        v = _rl_single(np.array([fx]))[0]
        ax.plot(fx / 1e9, v, "o", color=COLORS[0], ms=4)
        ax.text(fx / 1e9 + (0.02 if fx < 2.4e9 else -0.02), v - 0.5, f"{v:.1f} dB", fontsize=8,
                ha="left" if fx < 2.4e9 else "right", va="bottom", color=COLORS[0])
    ax.set_xlim(2.0, 2.8)
    ax.set_ylim(40, 0)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Return loss (dB)")
    ax.grid(True, color=GRID, lw=0.6)
    ax.legend(loc="upper center", fontsize=7.8, ncol=2, bbox_to_anchor=(0.5, 1.0), handlelength=1.6,
              columnspacing=0.8)
    ax.text(2.33, 39, "null at\n2.4 GHz", fontsize=8, ha="right", va="bottom", color="0.3")
    return save(fig, "32", "fig-32-2-l-network-match")


# ---------------------------------------------------------------------------
def _farrow(ax, p0, p1, text="", color=INK, rad=0.0, tx=None, ty=None, fs=9.5, lw=1.2):
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11, color=color, lw=lw,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=7, shrinkB=7)
    ax.add_patch(a)
    if text:
        if tx is None:
            tx = (p0[0] + p1[0]) / 2
        if ty is None:
            ty = (p0[1] + p1[1]) / 2
        ax.text(tx, ty, text, fontsize=fs, ha="center", va="center", color=color)


def fig_two_port_waves():
    """Fig 32.3: incident/reflected waves at a two-port and the S-parameter flow graph."""
    fig, ax = schematic(6.4, 5.0, xlim=(0, 10), ylim=(0, 7.8))
    # --- top: two-port
    box(ax, 4.0, 5.3, 2.0, 1.8, "[S]", fontsize=13)
    for xa, xb in ((0.9, 4.0), (6.0, 9.1)):
        for yy in (5.75, 6.65):
            ax.plot([xa, xb], [yy, yy], color=INK, lw=1.1)
    ax.text(2.45, 6.2, "$Z_0=50\\ \\Omega$ reference line", fontsize=8.5, ha="center", va="center")
    ax.text(7.55, 6.2, "$Z_0=50\\ \\Omega$ reference line", fontsize=8.5, ha="center", va="center")
    ax.text(3.85, 7.3, "port 1", fontsize=9, ha="right")
    ax.text(6.15, 7.3, "port 2", fontsize=9, ha="left")
    c1, c2 = COLORS[0], COLORS[1]
    arrow(ax, 1.6, 7.0, 3.3, 7.0, color=c1)
    ax.text(1.4, 7.0, "$a_1$", fontsize=11, color=c1, ha="right", va="center")
    arrow(ax, 3.3, 5.35, 1.6, 5.35 + 0.0, color=c2)
    ax.text(1.4, 5.0, "", fontsize=1)
    ax.text(1.4, 5.35, "$b_1$", fontsize=11, color=c2, ha="right", va="center")
    arrow(ax, 8.4, 7.0, 6.7, 7.0, color=c1)
    ax.text(8.6, 7.0, "$a_2$", fontsize=11, color=c1, ha="left", va="center")
    arrow(ax, 6.7, 5.35, 8.4, 5.35, color=c2)
    ax.text(8.6, 5.35, "$b_2$", fontsize=11, color=c2, ha="left", va="center")
    ax.text(5.0, 4.8, "incident waves $a_n$, reflected waves $b_n$  ($|a_n|^2$, $|b_n|^2$ = power)",
            fontsize=8.5, ha="center", color="0.3")
    # --- bottom: flow graph
    xs, ys = (2.6, 7.4), (3.5, 1.2)
    N = {"a1": (xs[0], ys[0]), "b2": (xs[1], ys[0]), "b1": (xs[0], ys[1]), "a2": (xs[1], ys[1])}
    lab = {"a1": "$a_1$", "b1": "$b_1$", "a2": "$a_2$", "b2": "$b_2$"}
    for k, (x, y) in N.items():
        ax.add_patch(Circle((x, y), 0.09, color=INK, zorder=5))
        off = -0.32 if x < 5 else 0.32
        ax.text(x + off * (1.0 if k in ("a2", "b2") else 1.0), y + (0.3 if y > 2 else -0.3), lab[k],
                fontsize=11, ha="center", va="center")
    _farrow(ax, N["a1"], N["b2"], "$S_{21}$", ty=ys[0] + 0.25)
    _farrow(ax, N["a2"], N["b1"], "$S_{12}$", ty=ys[1] - 0.25)
    _farrow(ax, N["a1"], N["b1"], "$S_{11}$", tx=xs[0] + 0.42)
    _farrow(ax, N["a2"], N["b2"], "$S_{22}$", tx=xs[1] - 0.42)
    _farrow(ax, N["b1"], N["a1"], "$\\Gamma_S$", color=COLORS[2], rad=-0.6, tx=xs[0] - 1.05,
            ty=(ys[0] + ys[1]) / 2)
    _farrow(ax, N["b2"], N["a2"], "$\\Gamma_L$", color=COLORS[2], rad=-0.6, tx=xs[1] + 1.05,
            ty=(ys[0] + ys[1]) / 2)
    ax.text(0.9, 2.35, "source", fontsize=8.5, color=COLORS[2], ha="center", rotation=90, va="center")
    ax.text(9.15, 2.35, "load", fontsize=8.5, color=COLORS[2], ha="center", rotation=90, va="center")
    ax.text(5.0, 0.35,
            "$\\Gamma_\\mathrm{in}=\\dfrac{b_1}{a_1}=S_{11}+\\dfrac{S_{12}S_{21}\\Gamma_L}{1-S_{22}\\Gamma_L}$",
            fontsize=10.5, ha="center", va="center")
    ax.plot([0.3, 9.7], [4.45, 4.45], color=GRID, lw=0.8)
    return save(fig, "32", "fig-32-3-two-port-waves")


# ---------------------------------------------------------------------------
def fig_resonator():
    """Fig 32.4: transmission of resonators with loaded Q = 100, 1000, 3900 at 10 GHz."""
    fig = plt.figure(figsize=(6.8, 3.7))
    ax = fig.add_axes([0.09, 0.14, 0.58, 0.80])
    f0 = 10e9
    f = np.linspace(9.9e9, 10.1e9, 4001)
    for Q, col, ls in ((100, COLORS[0], "-"), (1000, COLORS[1], "-"), (3900, COLORS[2], "-")):
        H = 1 / (1 + 1j * Q * (f / f0 - f0 / f))
        ax.plot(f / 1e9, 20 * np.log10(np.abs(H)), color=col, ls=ls,
                label=f"$Q_L$ = {Q}  (BW {f0/Q/1e6:.3g} MHz)")
    ax.axhline(-3, color="0.4", ls="--", lw=0.9)
    ax.text(9.902, -2.6, "−3 dB", fontsize=8.5, color="0.3", va="bottom")
    # bandwidth arrows
    for Q, col, y in ((100, COLORS[0], -3), (1000, COLORS[1], -3), (3900, COLORS[2], -3)):
        bw = f0 / Q / 1e9
        if bw < 0.15:
            ax.annotate("", xy=(10 - bw / 2, y), xytext=(10 + bw / 2, y),
                        arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.0, mutation_scale=7,
                                        shrinkA=0, shrinkB=0))
    ax.annotate("100 MHz", xy=(10.05, -3), xytext=(10.07, -8), fontsize=8, color=COLORS[0],
                ha="center", arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    ax.annotate("10 MHz", xy=(10.005, -3.2), xytext=(10.035, -13), fontsize=8, color=COLORS[1],
                ha="center", arrowprops=dict(arrowstyle="-", color=COLORS[1], lw=0.6))
    ax.annotate("2.56 MHz", xy=(9.9987, -3.2), xytext=(9.96, -13), fontsize=8, color=COLORS[2],
                ha="center", arrowprops=dict(arrowstyle="-", color=COLORS[2], lw=0.6))
    ax.set_xlim(9.9, 10.1)
    ax.set_xticks([9.9, 9.95, 10.0, 10.05, 10.1])
    ax.set_ylim(-30, 1)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Normalised transmission (dB)")
    ax.grid(True, color=GRID, lw=0.6)
    ax.legend(loc="lower center", fontsize=7.8, bbox_to_anchor=(0.5, 0.0))

    # --- cavity sketch (oblique view)
    ac = fig.add_axes([0.69, 0.10, 0.31, 0.86])
    ac.set_xlim(-0.4, 4.4)
    ac.set_ylim(-1.6, 5.4)
    ac.set_aspect("equal")
    ac.axis("off")
    a, b, d = 2.286, 1.016, 1.985   # cm
    ox, oy = 0.85, 0.55            # oblique offset per unit depth
    P = lambda x, y, z: (x + ox * z, y + oy * z + 0.0)  # noqa: E731
    yb = 1.2
    def face(pts, **kw):
        ac.add_patch(Polygon([P(*p) for p in pts], closed=True, **kw))
    # back/hidden edges first
    for p0, p1 in (((0, yb, 0), (0, yb, d)), ((0, yb, d), (a, yb, d)), ((0, yb, d), (0, yb + b, d))):
        ac.plot(*zip(P(*p0), P(*p1)), color="0.55", lw=0.7, ls=":")
    face([(a, yb, 0), (a, yb, d), (a, yb + b, d), (a, yb + b, 0)], fc="#D7DFE9", ec=INK, lw=1.0,
         alpha=0.6)
    face([(0, yb + b, 0), (a, yb + b, 0), (a, yb + b, d), (0, yb + b, d)], fc="#E9EEF4", ec=INK, lw=1.0,
         alpha=0.6)
    # mid-length cross-section z = d/2 where the TE101 field peaks
    zm = d / 2
    face([(0, yb, zm), (a, yb, zm), (a, yb + b, zm), (0, yb + b, zm)], fc="none", ec="0.5", lw=0.7,
         ls="--")
    for xi in np.linspace(0.22, a - 0.22, 7):
        h = 0.8 * b * np.sin(np.pi * xi / a)
        x0, y0 = P(xi, yb + b / 2 - h / 2, zm)
        ac.annotate("", xy=(x0, y0 + h), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=1.1, mutation_scale=7,
                                    shrinkA=0, shrinkB=0))
    # output iris on back wall (hidden, dashed) and front wall with input iris
    cx, cy = P(a / 2, yb + b / 2, d)
    ac.add_patch(Rectangle((cx - 0.25, cy - 0.15), 0.5, 0.3, fc="none", ec=COLORS[0], lw=1.0, ls="--"))
    face([(0, yb, 0), (a, yb, 0), (a, yb + b, 0), (0, yb + b, 0)], fc="none", ec=INK, lw=1.1)
    cx0, cy0 = P(a / 2, yb + b / 2, 0)
    ac.add_patch(Rectangle((cx0 - 0.25, cy0 - 0.15), 0.5, 0.3, fc="white", ec=COLORS[0], lw=1.3))
    ac.text(cx0, cy0 - 0.2, "input iris (z = 0)", fontsize=7, color=COLORS[0], ha="center", va="top")
    ac.annotate("output iris (z = d)", xy=(cx + 0.25, cy + 0.15), xytext=(cx + 0.3, 3.75),
                fontsize=7.5, color=COLORS[0], ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-", color=COLORS[0], lw=0.6))
    # dimensions
    ac.annotate("", xy=P(a, yb - 0.3, 0), xytext=P(0, yb - 0.3, 0),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK, mutation_scale=6, shrinkA=0, shrinkB=0))
    ac.text(*P(a / 2, yb - 0.4, 0), "a = 22.86 mm", fontsize=8, ha="center", va="top")
    p0, p1 = P(-0.25, yb, 0), P(-0.25, yb + b, 0)
    ac.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK,
                                                       mutation_scale=6, shrinkA=0, shrinkB=0))
    ac.text(p0[0] - 0.08, (p0[1] + p1[1]) / 2, "b = 10.16 mm", fontsize=8, ha="right", va="center",
            rotation=90)
    p0, p1 = P(a + 0.2, yb, 0), P(a + 0.2, yb, d)
    ac.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=INK,
                                                       mutation_scale=6, shrinkA=0, shrinkB=0))
    ac.text((p0[0] + p1[0]) / 2 + 0.12, (p0[1] + p1[1]) / 2 - 0.08, "d = 19.85 mm", fontsize=8,
            ha="center", va="top", rotation=33, rotation_mode="anchor")
    ac.text(2.0, 5.3, "TE$_{101}$ cavity, 10 GHz", fontsize=9, ha="center", va="top")
    ac.text(2.0, 4.85, "E normal to broad walls,\n∝ sin(πx/a) sin(πz/d)", fontsize=7.5, ha="center", va="top",
            color=COLORS[1])
    return save(fig, "32", "fig-32-4-resonator-response")


# ---------------------------------------------------------------------------
def fig_patterns():
    """Fig 32.5: half-wave dipole E-plane pattern and tapered 1.2 m dish at 12 GHz."""
    fig = plt.figure(figsize=(6.8, 3.6))
    axp = fig.add_axes([0.02, 0.08, 0.40, 0.80], projection="polar")
    th = np.linspace(0, 2 * np.pi, 3601)
    sn = np.sin(th)
    F = np.where(np.abs(sn) < 1e-9, 0.0, np.abs(np.cos(np.pi / 2 * np.cos(th)) / np.where(sn == 0, 1, sn)))
    dB = np.clip(20 * np.log10(np.maximum(F, 1e-6)), -30, 0)
    axp.set_theta_zero_location("N")
    axp.set_theta_direction(-1)
    axp.plot(th, dB + 30, color=COLORS[0])
    axp.set_ylim(0, 30)
    axp.set_yticks([10, 20, 30])
    axp.set_yticklabels(["−20 dB", "−10", "0"], fontsize=7, color="0.4")
    axp.set_rlabel_position(160)
    axp.set_xticks(np.radians(np.arange(0, 360, 30)))
    axp.set_xticklabels([f"{a}°" for a in range(0, 360, 30)], fontsize=7.5)
    axp.grid(color=GRID, lw=0.6)
    # half-power points at 51 and 129 degrees from the dipole axis (both lobes)
    t1 = np.radians(90 - 39)
    for tt in (t1, np.pi - t1, 2 * np.pi - t1, np.pi + t1):
        axp.plot([tt, tt], [0, 27], color=COLORS[1], lw=0.9, ls="--")
    axp.text(np.radians(90), 14, "HPBW\n78°", fontsize=8.5, color=COLORS[1], ha="center", va="center",
             bbox=dict(fc="white", ec="none", pad=0.5))
    # dipole drawn vertically at centre
    axp.plot([0, 0], [0, 6], color=INK, lw=2.5)
    axp.plot([np.pi, np.pi], [0, 6], color=INK, lw=2.5)
    axp.text(np.radians(8), 21, "null on\naxis", fontsize=7.5, color="0.3", ha="left", va="center")
    axp.set_title("(a) half-wave dipole, E-plane", fontsize=9.5, pad=14)

    ax = fig.add_axes([0.56, 0.16, 0.42, 0.70])
    lam = C0 / 12e9
    D = 1.2
    Cped = 0.08  # pedestal of the (1-r^2) taper, about -22 dB edge illumination
    ang = np.radians(np.linspace(-6, 6, 4801))
    u = np.pi * D / lam * np.sin(ang)
    u = np.where(np.abs(u) < 1e-9, 1e-9, u)
    E = Cped * 2 * special.jv(1, u) / u + (1 - Cped) * 4 * special.jv(2, u) / u ** 2
    E /= (Cped + (1 - Cped) * 0.5)
    pdB = np.clip(20 * np.log10(np.abs(E)), -40, 0)
    ax.plot(np.degrees(ang), pdB, color=COLORS[0])
    i3 = np.argmin(np.abs(pdB[len(pdB) // 2:] + 3)) + len(pdB) // 2
    th3 = np.degrees(ang[i3])
    ax.axhline(-3, color="0.4", lw=0.8, ls="--")
    ax.annotate("", xy=(th3, -3), xytext=(-th3, -3),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.0, mutation_scale=7,
                                shrinkA=0, shrinkB=0))
    ax.text(th3 + 0.3, -2.4, f"HPBW {2*th3:.2f}°\n(±{th3:.2f}°)", fontsize=8, color=COLORS[1],
            va="bottom", ha="left")
    # first sidelobe
    half = pdB[len(pdB) // 2:]
    from scipy.signal import argrelmax
    m = argrelmax(half)[0][0] + len(pdB) // 2
    ax.annotate(f"first sidelobe {pdB[m]:.0f} dB".replace("-", "−"), xy=(np.degrees(ang[m]), pdB[m]),
                xytext=(3.4, -15), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.text(-5.8, -6.0, "peak gain 41.4 dBi\n(η = 0.6, λ = 25 mm)", fontsize=8, va="top")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-40, 1)
    ax.set_xlabel("Angle from boresight (degrees)")
    ax.set_ylabel("Relative power (dB)")
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_title("(b) 1.2 m dish at 12 GHz, tapered aperture", fontsize=9.5)
    print(f"  dish HPBW {2*th3:.3f} deg, sidelobe {pdB[m]:.1f} dB")
    return save(fig, "32", "fig-32-5-radiation-patterns")


# ---------------------------------------------------------------------------
def fig_vna():
    """Fig 32.6: two-port VNA block diagram with calibration standards and error adapter."""
    fig, ax = schematic(6.8, 6.9, xlim=(0, 13.6), ylim=(-4.4, 10.3))
    blue, red, green = COLORS[0], COLORS[1], COLORS[2]
    # IF + DSP
    box(ax, 0.8, 9.0, 12.0, 1.15,
        "IF + DSP: S-parameters as receiver ratios\n"
        "forward  $S_{11}=A/R_1$,  $S_{21}=B/R_1$;     reverse  $S_{22}=B/R_2$,  $S_{12}=A/R_2$", fontsize=8, fc="#F4EEF6")
    # receivers
    rx = {"R1": 1.6, "A": 3.6, "B": 10.0, "R2": 12.0}
    names = {"R1": "$R_1$", "A": "$A$", "B": "$B$", "R2": "$R_2$"}
    for k, xc in rx.items():
        box(ax, xc - 0.6, 7.5, 1.2, 0.75, names[k], fontsize=10, fc="#EAF4EE")
        arrow(ax, xc, 8.25, xc, 9.0)
    ax.text(6.9, 7.85, "receivers (down-converters)", fontsize=7.5, ha="center", color="0.35")
    # synthesiser and switch
    box(ax, 5.25, 6.55, 3.3, 0.95, "swept synthesiser\n10 MHz – 20 GHz", fontsize=8, fc="#FFF3DD")
    box(ax, 6.3, 5.55, 1.2, 0.65, "switch", fontsize=8)
    arrow(ax, 6.9, 6.55, 6.9, 6.2)
    ys = 5.87
    # source arms with gaps where the b-sample lines cross
    for xa, xb, ls in ((1.6, 3.45, "-"), (3.75, 6.3, "-"), (7.5, 9.85, "--"), (10.15, 12.0, "--")):
        ax.plot([xa, xb], [ys, ys], color=INK, lw=1.1, ls=ls)
    ax.text(5.0, ys + 0.12, "forward", fontsize=7.5, ha="center", va="bottom")
    ax.text(8.8, ys + 0.12, "reverse", fontsize=7.5, ha="center", va="bottom")
    for xs_ in (1.6, 12.0):
        ax.plot(xs_, ys, "o", color=INK, ms=3.5)
        arrow(ax, xs_, ys, xs_, 7.5)
        ax.plot([xs_, xs_], [ys, 2.45], color=INK, lw=1.1)
    ax.text(1.45, 6.7, "$a$", fontsize=10, color=blue, ha="right")
    ax.text(12.15, 6.7, "$a$", fontsize=10, color=blue, ha="left")
    # directional couplers: main line + coupled line in a box
    for (x0, x1, xm, xc_out, sign) in ((1.15, 4.1, 1.6, 3.6, 1), (9.5, 12.45, 12.0, 10.0, -1)):
        box(ax, x0, 2.05, x1 - x0, 1.25, "", fc="#EEF3F8")
        ax.plot([x0 + 0.25, x1 - 0.25], [2.95, 2.95], color=red, lw=1.0)
        ax.text((x0 + x1) / 2, 1.95, "directional coupler", fontsize=7.5, ha="center", va="top")
    # main lines from splitter drop to ports
    ax.plot([1.6, 1.6, 5.6], [2.45, 2.45, 2.45], color=INK, lw=1.1)
    ax.plot([12.0, 8.0], [2.45, 2.45], color=INK, lw=1.1)
    # coupled (reflected-wave) arms up to A and B
    for xc_out in (3.6, 10.0):
        ax.plot([xc_out, xc_out], [2.95, 7.1], color=red, lw=1.1)
        arrow(ax, xc_out, 7.1, xc_out, 7.5, color=red)
    ax.text(3.75, 4.4, "$b$", fontsize=10, color=red, ha="left")
    ax.text(9.85, 4.4, "$b$", fontsize=10, color=red, ha="right")
    # ports, reference planes, DUT
    ax.text(4.85, 2.55, "port 1", fontsize=8, ha="center", va="bottom")
    ax.text(8.75, 2.55, "port 2", fontsize=8, ha="center", va="bottom")
    box(ax, 5.85, 1.95, 1.9, 1.0, "DUT", fontsize=10, fc="#FFFFFF")
    ax.plot([5.6, 5.85], [2.45, 2.45], color=INK, lw=1.1)
    ax.plot([7.75, 8.0], [2.45, 2.45], color=INK, lw=1.1)
    for xp in (5.6, 8.0):
        ax.plot([xp, xp], [1.35, 3.5], color=green, lw=1.3, ls="--")
    ax.text(6.8, 1.25, "reference planes", fontsize=7.5, color=green, ha="center", va="top")

    # ---- calibration inset
    ax.plot([0.2, 13.4], [0.45, 0.45], color=GRID, lw=0.8)
    ax.text(0.3, 0.05, "Calibration standards (SOLT)", fontsize=9, va="top", weight="bold")
    y0 = -2.0
    for x, n in zip([0.6, 2.4, 4.2, 6.0], ["Short", "Open", "Load\n50 Ω", "Through"]):
        ax.plot([x, x + 1.0], [y0 + 0.8, y0 + 0.8], color=INK, lw=1.1)
        ax.plot(x, y0 + 0.8, "o", mfc="white", mec=INK, ms=4)
        if n == "Short":
            ax.plot([x + 1.0, x + 1.0], [y0 + 0.8, y0 - 0.1], color=INK, lw=1.1)
            ax.plot([x + 0.75, x + 1.25], [y0 - 0.1, y0 - 0.1], color=INK, lw=1.6)
        elif n == "Open":
            ax.plot(x + 1.0, y0 + 0.8, "o", mfc="white", mec=INK, ms=4)
        elif n.startswith("Load"):
            zz = np.array([0, 1, -1, 1, -1, 1, -1, 0])
            ax.plot(x + 1.0 + 0.12 * zz, y0 + 0.8 - np.linspace(0, 0.8, 8), color=INK, lw=1.0)
            ax.plot([x + 0.8, x + 1.2], [y0 - 0.05, y0 - 0.05], color=INK, lw=1.6)
        else:
            ax.plot(x + 1.0, y0 + 0.8, "o", mfc="white", mec=INK, ms=4)
            ax.plot([x + 1.0, x + 1.5], [y0 + 0.8, y0 + 0.8], color=INK, lw=1.1)
            ax.plot(x + 1.5, y0 + 0.8, "o", mfc="white", mec=INK, ms=4)
        ax.text(x + 0.6, y0 - 0.45, n, fontsize=8.5, ha="center", va="top")
    # error adapter flow graph
    bx, by, bw, bh = 8.0, -4.2, 5.4, 4.3
    box(ax, bx, by, bw, bh, "", fc="#F7F7F7")
    ax.text(bx + bw / 2, by + bh - 0.2, "error adapter (port 1)", fontsize=8.5, ha="center", va="top")
    n = {"a0": (bx + 0.9, by + 3.05), "a1": (bx + 4.5, by + 3.05),
         "b0": (bx + 0.9, by + 1.85), "b1": (bx + 4.5, by + 1.85)}
    for k, (x, y) in n.items():
        ax.add_patch(Circle((x, y), 0.08, color=INK, zorder=5))
    _farrow(ax, n["a0"], n["a1"], "$e_{10}$", ty=n["a0"][1] + 0.28, fs=9)
    _farrow(ax, n["b1"], n["b0"], "$e_{01}$", ty=n["b0"][1] - 0.28, fs=9)
    _farrow(ax, n["a0"], n["b0"], "$e_{00}$", tx=n["a0"][0] - 0.4, fs=9)
    _farrow(ax, n["b1"], n["a1"], "$e_{11}$", tx=n["a1"][0] - 0.4, fs=9)
    ax.text(n["a0"][0] - 0.15, n["a0"][1] + 0.3, "VNA", fontsize=7.5, ha="right", color="0.35")
    ax.text(n["a1"][0] + 0.15, n["a1"][1] + 0.3, "DUT", fontsize=7.5, ha="left", color="0.35")
    ax.text(bx + bw / 2, by + 0.65,
            "$e_{00}$ directivity,  $e_{11}$ source match,\n$e_{10}e_{01}$ reflection tracking",
            fontsize=7.8, ha="center", va="center")
    return save(fig, "32", "fig-32-6-vna-setup")


if __name__ == "__main__":
    fig_capacitor_srf()
    fig_l_network()
    fig_two_port_waves()
    fig_resonator()
    fig_patterns()
    fig_vna()
