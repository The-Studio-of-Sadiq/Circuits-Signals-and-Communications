"""Figures for Chapter 3 — Network Analysis.

Run from the repository root:  python figures/scripts/ch03.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Arc  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import schematic, box, save, COLORS, INK  # noqa: E402

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


def _loop(ax, cx, cy, r, color=PINK, lw=1.3):
    """Clockwise circular mesh-current arrow centred at (cx, cy)."""
    ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=-60, theta2=240, color=color, lw=lw))
    ang = np.deg2rad(-60)
    x, y = cx + r * np.cos(ang), cy + r * np.sin(ang)
    tx, ty = np.sin(ang), -np.cos(ang)
    ax.annotate("", xy=(x + 0.05 * tx, y + 0.05 * ty), xytext=(x - 0.25 * tx, y - 0.25 * ty),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12,
                                shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- Figure 3.1
def fig_3_1():
    u = 3.0
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    d = _sd(ax, fontsize=9, unit=u)
    with d:
        elm.SourceV().at((0, 0)).up().length(u)
        elm.Resistor().at((0, u)).right().length(u)
        elm.Resistor().at((u, u)).down().length(u)
        elm.Resistor().at((u, u)).right().length(u)
        elm.Resistor().at((2 * u, u)).down().length(u)
        elm.Resistor().at((2 * u, u)).right().length(u)
        elm.SourceV().at((3 * u, 0)).up().length(u)
        elm.Line().at((0, 0)).right().length(3 * u)
        for x in (u, 2 * u):
            elm.Dot().at((x, u))
            elm.Dot().at((x, 0))
        elm.Ground().at((1.5 * u, 0))
    _finish(d, ax, xlim=(-2.8, 3 * u + 2.8), ylim=(-1.4, u + 1.6))
    fs = 8.8
    ax.text(-0.6, u / 2, "$V_1$\n10 V", ha="right", va="center", fontsize=fs)
    ax.text(3 * u + 0.6, u / 2, "$V_2$\n5 V", ha="left", va="center", fontsize=fs)
    for x, t in ((u / 2, r"$R_1$ = 1 k$\Omega$"), (1.5 * u, r"$R_3$ = 1 k$\Omega$"),
                 (2.5 * u, r"$R_5$ = 2 k$\Omega$")):
        ax.text(x, u + 0.45, t, ha="center", fontsize=fs)
    for x, t in ((u, "$R_2$\n2 kΩ"), (2 * u, "$R_4$\n4 kΩ")):
        ax.text(x - 0.45, 2.15, t, ha="right", va="center", fontsize=fs)
    for x, n, t in ((u, "a", r"$v_a$ = 5.926 V"), (2 * u, "b", r"$v_b$ = 4.815 V")):
        ax.text(x, u + 1.1, t, ha="center", fontsize=fs, color=GREEN, weight="bold")
        ax.text(x + 0.18, u - 0.2, n, ha="left", va="top", fontsize=9.5, style="italic",
                weight="bold")
    for k, t in enumerate(("$i_1$ = 4.074 mA", "$i_2$ = 1.111 mA", "$i_3$ = −0.093 mA")):
        cx = k * u + 1.5
        _loop(ax, cx, 1.3, 0.4)
        ax.text(cx, 0.45, t, ha="center", va="center", fontsize=8, color=PINK)
    save(fig, "03", "fig-3-1-two-source-network")


# ---------------------------------------------------------------- Figure 3.2
def fig_3_2():
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(6.8, 3.9),
                                   gridspec_kw=dict(width_ratios=[1.2, 1.0], wspace=0.06))
    fs = 8.3
    # ---- supernode
    d = _sd(axl, fontsize=8.5, unit=2.5)
    a, b, c = (1.6, 3.0), (4.4, 3.0), (7.0, 3.0)
    with d:
        elm.SourceI().at((0, 0)).up().length(3.0)
        elm.Line().at((0, 3.0)).to(a)
        elm.Resistor().at(a).down().length(3.0)
        elm.SourceV().at(b).left().length(2.8)
        elm.Resistor().at(b).down().length(3.0)
        elm.Resistor().at(b).right().length(2.6)
        elm.Resistor().at(c).down().length(3.0)
        elm.Line().at(a).to((1.6, 4.9))
        elm.Resistor().at((1.6, 4.9)).right().length(5.4)
        elm.Line().at((7.0, 4.9)).to(c)
        elm.Line().at((0, 0)).to((7.0, 0))
        for p in (a, b, c, (1.6, 0), (4.4, 0)):
            elm.Dot().at(p)
        elm.Ground().at((3.0, 0))
    _finish(d, axl, xlim=(-1.6, 8.6), ylim=(-2.0, 6.2))
    axl.add_patch(Ellipse((3.0, 3.0), 4.1, 1.95, fc="none", ec=PINK, ls="--", lw=1.3))
    axl.text(3.0, 4.42, "supernode", ha="center", va="center", fontsize=8.5, color=PINK,
             weight="bold")
    axl.text(3.0, 2.48, "6 V", ha="center", va="top", fontsize=fs)
    axl.text(-0.55, 1.5, "2 mA", ha="right", va="center", fontsize=fs)
    axl.text(1.95, 1.2, "4 kΩ", ha="left", va="center", fontsize=fs)
    axl.text(4.75, 1.2, "2 kΩ", ha="left", va="center", fontsize=fs)
    axl.text(5.7, 3.4, "1 kΩ", ha="center", va="bottom", fontsize=fs)
    axl.text(7.35, 1.5, "3 kΩ", ha="left", va="center", fontsize=fs)
    axl.text(4.3, 5.3, "6 kΩ", ha="center", va="bottom", fontsize=fs)
    axl.text(1.4, 3.3, "a", ha="right", fontsize=9.5, style="italic", weight="bold")
    axl.text(4.6, 3.3, "b", ha="left", fontsize=9.5, style="italic", weight="bold")
    axl.text(7.15, 3.25, "c", ha="left", fontsize=9.5, style="italic", weight="bold")
    axl.text(3.5, -1.15, r"$v_a$ = 6.275 V,  $v_b$ = 0.275 V,  $v_c$ = 0.881 V",
             ha="center", va="center", fontsize=8.5, color=GREEN)
    axl.text(-1.5, 6.15, "(a) supernode", fontsize=9.5, weight="bold", va="top")

    # ---- supermesh
    d = _sd(axr, fontsize=8.5, unit=2.5)
    with d:
        elm.SourceV().at((0, 0)).up().length(3.0)
        elm.Resistor().at((0, 3.0)).right().length(3.0)
        elm.SourceI().at((3.0, 0)).up().length(3.0)
        elm.Resistor().at((3.0, 3.0)).right().length(3.0)
        elm.Resistor().at((6.0, 3.0)).down().length(3.0)
        elm.Line().at((0, 0)).to((6.0, 0))
        for p in ((3.0, 3.0), (3.0, 0)):
            elm.Dot().at(p)
    _finish(d, axr, xlim=(-2.0, 8.2), ylim=(-2.0, 6.2))
    axr.add_patch(FancyBboxPatch((-0.85, -0.55), 8.75, 4.6, boxstyle="round,pad=0.05",
                                 fc="none", ec=PINK, ls="--", lw=1.3))
    axr.text(3.5, 4.6, "supermesh (outer loop)", ha="center", va="center", fontsize=8.5,
             color=PINK, weight="bold")
    axr.text(-0.6, 1.5, "24 V", ha="right", va="center", fontsize=fs)
    axr.text(1.5, 3.4, "$R_1$ = 1 kΩ", ha="center", va="bottom", fontsize=fs)
    axr.text(4.5, 3.4, "$R_2$ = 2 kΩ", ha="center", va="bottom", fontsize=fs)
    axr.text(6.4, 1.5, "$R_3$\n3 kΩ", ha="left", va="center", fontsize=fs)
    axr.text(3.4, 2.3, "4 mA", ha="left", va="center", fontsize=fs)
    _loop(axr, 1.25, 1.65, 0.4)
    _loop(axr, 4.75, 1.55, 0.4)
    axr.text(1.25, 0.6, "$i_1$ =\n0.667 mA", ha="center", va="center", fontsize=8, color=PINK)
    axr.text(4.75, 0.55, "$i_2$ =\n4.667 mA", ha="center", va="center", fontsize=8, color=PINK)
    axr.text(-1.9, 6.15, "(b) supermesh", fontsize=9.5, weight="bold", va="top")
    save(fig, "03", "fig-3-2-supernode-supermesh")


# ---------------------------------------------------------------- Figure 3.3
def fig_3_3():
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    d = _sd(ax, fontsize=8.5, unit=3.0)
    XC, XL = 12.0, 15.0
    with d:
        elm.SourceSin().at((0, 0)).up().length(6.0)
        elm.Resistor().at((0, 6.0)).right().length(3.5)
        elm.Resistor().at((3.5, 6.0)).down().length(3.0)
        elm.Line().at((3.5, 3.0)).to((8.0, 3.0))
        elm.Resistor().at((5.5, 3.0)).down().length(3.0)
        elm.SourceControlledI().at((8.0, 6.0)).down().length(3.0)
        elm.Line().at((8.0, 6.0)).to((XL, 6.0))
        elm.Resistor().at((XC, 6.0)).down().length(6.0)
        elm.Resistor().at((XL, 6.0)).down().length(6.0)
        elm.Line().at((0, 0)).to((XL, 0))
        for p in ((3.5, 6.0), (3.5, 3.0), (5.5, 3.0), (8.0, 6.0), (XC, 6.0), (XC, 0),
                  (5.5, 0)):
            elm.Dot().at(p)
        elm.Ground().at((7.5, 0))
    _finish(d, ax, xlim=(-2.0, 18.2), ylim=(-2.9, 7.6))
    fs = 8.5
    ax.text(-0.75, 3.0, "$v_s$", ha="right", va="center", fontsize=9.5)
    ax.text(1.75, 6.45, r"$R_s$ = 1 kΩ", ha="center", fontsize=fs)
    ax.text(3.15, 4.5, r"$r_\pi$" "\n2.585 kΩ", ha="right", va="center", fontsize=fs)
    ax.text(3.8, 5.35, "+", ha="left", va="center", fontsize=11, color=RED)
    ax.text(3.8, 3.6, "−", ha="left", va="center", fontsize=11, color=RED)
    ax.text(3.85, 4.5, r"$v_\pi$", ha="left", va="center", fontsize=10, color=RED)
    ax.text(5.85, 1.5, r"$R_E$" "\n200 Ω", ha="left", va="center", fontsize=fs)
    ax.text(8.6, 4.5, r"$g_m v_\pi$" "\n" r"$g_m$ = 38.7 mS", ha="left", va="center", fontsize=fs)
    ax.text(XC + 0.35, 3.0, r"$R_C$" "\n4.7 kΩ", ha="left", va="center", fontsize=fs)
    ax.text(XL + 0.35, 3.0, r"$R_L$" "\n10 kΩ", ha="left", va="center", fontsize=fs)
    nd = dict(fontsize=8.5, color=GREEN, weight="bold")
    it = dict(fontsize=10, style="italic", weight="bold")
    ax.text(3.5, 6.95, "$v_b$ = 0.958 mV", ha="center", **nd)
    ax.text(3.75, 6.25, "b", ha="left", va="bottom", **it)
    ax.text(5.65, 2.55, "$v_e$ = 0.849 mV", ha="left", va="top", **nd)
    ax.text(5.3, 3.25, "e", ha="right", va="bottom", **it)
    ax.text(8.0, 6.95, "$v_c$ = −13.44 mV", ha="center", **nd)
    ax.text(8.25, 6.25, "c", ha="left", va="bottom", **it)
    box(ax, 9.6, -2.75, 7.9, 1.45, fc="#F6F6F6")
    ax.text(13.55, -2.02, r"$v_\pi = v_b - v_e$,  $v_s$ = 1 mV" "\n"
            r"gain $v_c/v_s$ = −13.44;  without $R_E$: −89.2",
            ha="center", va="center", fontsize=8.3)
    save(fig, "03", "fig-3-3-degenerated-amplifier-model")


# ---------------------------------------------------------------- Figure 3.4
P34 = {"0": np.array([0.0, 0.0]), "1": np.array([0.0, 3.0]),
       "2": np.array([-1.8, 1.5]), "3": np.array([1.8, 1.5])}
XB1 = -3.3   # b1 (the excitation) is routed round the left of node 2
B1_PATH = np.array([P34["0"], [XB1, 0.0], [XB1, 3.0], P34["1"]])
EDGES34 = {"b2": ("1", "2"), "b3": ("2", "0"), "b4": ("1", "3"), "b5": ("3", "0"),
           "b6": ("2", "3")}


def _graph(ax, lw=1.6, node_ms=7, labels=True, fs=8.3):
    tree = {"b1", "b3", "b5"}
    for name, (pa, pb) in EDGES34.items():
        is_tree = name in tree
        A, B = P34[pa], P34[pb]
        ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=lw * (1.8 if is_tree else 1.0),
                ls="-" if is_tree else (0, (4, 2.5)))
        m = A + 0.58 * (B - A)
        dv = (B - A) / np.linalg.norm(B - A)
        ax.annotate("", xy=m + 0.12 * dv, xytext=m - 0.12 * dv,
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=0, mutation_scale=12))
    ax.plot(B1_PATH[:, 0], B1_PATH[:, 1], color=INK, lw=lw * 1.8, solid_joinstyle="round")
    ax.annotate("", xy=(XB1, 1.62), xytext=(XB1, 1.38),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0, mutation_scale=12))
    for n, p in P34.items():
        ax.plot(*p, "o", ms=node_ms, color=INK, zorder=6)
    if labels:
        off = {"0": (0.0, -0.38), "1": (0.0, 0.38), "2": (0.05, 0.42), "3": (0.32, 0.25)}
        for n, p in P34.items():
            ax.text(p[0] + off[n][0], p[1] + off[n][1], n, ha="center", va="center",
                    fontsize=fs + 1.5, weight="bold", color=GREEN)


def fig_3_4():
    fig = plt.figure(figsize=(6.8, 5.0))
    axg = fig.add_axes([0.0, 0.40, 0.52, 0.60])
    axm = fig.add_axes([0.52, 0.40, 0.48, 0.60])
    axs = [fig.add_axes([0.0 + 0.335 * k, 0.0, 0.33, 0.36]) for k in range(3)]
    ax = axg
    _graph(ax)
    f7 = dict(fontsize=7.6, va="center")
    ax.text(XB1 - 0.15, 1.5, "$b_1$\nsource\n5 V", ha="right", **f7)
    ax.text(-1.15, 2.6, "$b_2$\n$R_1$ 350 Ω", ha="right", **f7)
    ax.text(-1.15, 0.45, "$b_3$ gauge\n350.7 Ω", ha="right", **f7)
    ax.text(1.15, 2.6, "$b_4$\n$R_3$ 350 Ω", ha="left", **f7)
    ax.text(1.15, 0.45, "$b_5$\n$R_4$ 350 Ω", ha="left", **f7)
    ax.text(0.0, 1.75, "$b_6$ detector 1 kΩ", ha="center", va="bottom", fontsize=7.6)
    ax.set_xlim(-4.9, 3.6)
    ax.set_ylim(-1.0, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot([-4.6, -4.0], [-0.8, -0.8], color=INK, lw=2.9)
    ax.text(-3.9, -0.8, "tree twigs $b_1, b_3, b_5$", fontsize=7.5, va="center")
    ax.plot([0.7, 1.3], [-0.8, -0.8], color=INK, lw=1.6, ls=(0, (4, 2.5)))
    ax.text(1.4, -0.8, "links", fontsize=7.5, va="center")
    ax.text(-4.8, 3.95, "(a) directed graph, tree and links", fontsize=9, weight="bold",
            va="top")

    ax = axm
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def matrix(x0, y0, name, rows, rlabels, title):
        cw, rh = 1.05, 0.85
        ax.text(x0 - 1.4, y0 + 0.75, title, fontsize=7.8, va="bottom", ha="left")
        for j in range(6):
            ax.text(x0 + 1.15 + j * cw, y0 + 0.3, f"$b_{j + 1}$", ha="center", va="center",
                    fontsize=7.5, color="#666666")
        top = y0 - 0.25
        bot = top - rh * len(rows)
        for i, (rl, row) in enumerate(zip(rlabels, rows)):
            y = top - rh * (i + 0.5)
            ax.text(x0 + 0.35, y, rl, ha="center", va="center", fontsize=7.5, color="#666666")
            for j, v in enumerate(row):
                ax.text(x0 + 1.15 + j * cw, y, f"{v:d}".replace("-", "−"), ha="center",
                        va="center", fontsize=8.5)
        xl, xr = x0 + 0.68, x0 + 1.15 + 5 * cw + 0.47
        for xx, s in ((xl, 1), (xr, -1)):
            ax.plot([xx + 0.15 * s, xx, xx, xx + 0.15 * s], [top, top, bot, bot], color=INK,
                    lw=1.1)
        ax.text(x0 - 0.2, (top + bot) / 2, name, ha="right", va="center", fontsize=10)

    A = [[-1, 1, 0, 1, 0, 0], [0, -1, 1, 0, 0, 1], [0, 0, 0, -1, 1, -1]]
    B = [[1, 1, 1, 0, 0, 0], [1, 0, 0, 1, 1, 0], [0, 0, -1, 0, 1, 1]]
    matrix(1.9, 8.4, r"$\mathbf{A} =$", A, ["1", "2", "3"],
           "reduced incidence matrix (rows: nodes 1, 2, 3)")
    matrix(1.9, 3.9, r"$\mathbf{B} =$", B, ["$L_2$", "$L_4$", "$L_6$"],
           "fundamental loop matrix (tree $b_1, b_3, b_5$)")
    ax.text(0.5, 0.15, r"KCL: $\mathbf{A}\,\mathbf{i}=\mathbf{0}$,   KVL: $\mathbf{B}\,\mathbf{v}"
            r"=\mathbf{0}$,   $\mathbf{A}\,\mathbf{B}^{T} = \mathbf{0}$", fontsize=8.3)

    loops = [(["0", "1", "2"], True, "$L_2$ = {$b_2$, $b_3$, $b_1$}", BLUE),
             (["0", "1", "3"], True, "$L_4$ = {$b_4$, $b_5$, $b_1$}", ORANGE),
             (["2", "3", "0"], False, "$L_6$ = {$b_6$, $b_5$, −$b_3$}", GREEN)]
    for ax, (nodes, uses_b1, title, col) in zip(axs, loops):
        _graph(ax, lw=1.0, node_ms=4.5, labels=False)
        if uses_b1:
            poly = np.vstack([B1_PATH, P34[nodes[2]][None, :]])
        else:
            poly = np.array([P34[n] for n in nodes])
        ax.add_patch(Polygon(poly, fc=col, alpha=0.28, ec="none"))
        ax.set_xlim(-3.7, 2.3)
        ax.set_ylim(-0.4, 3.9)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(-0.7, 3.85, title, ha="center", va="top", fontsize=8)
    fig.text(0.01, 0.375, "(b) fundamental loops, one per link (shaded)", fontsize=9,
             weight="bold", va="bottom")
    save(fig, "03", "fig-3-4-bridge-graph-tree")


# ---------------------------------------------------------------- Figure 3.5
def _diamond(ax, x, y, w, h, text, fs=7.8, fc="#FFF4E0"):
    ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)],
                         closed=True, fc=fc, ec=INK, lw=1.0))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, linespacing=1.15)


def _box_c(ax, x, y, w, h, text, fc="#EEF3F8", fs=7.8):
    box(ax, x - w / 2, y - h / 2, w, h, "", fc=fc)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, linespacing=1.15)


def _arr(ax, pts, label=None, lxy=None, ha="center"):
    pts = np.asarray(pts, float)
    if len(pts) > 2:
        ax.plot(pts[:-1, 0], pts[:-1, 1], color=INK, lw=1.0)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=10,
                                shrinkA=0, shrinkB=0))
    if label:
        ax.text(*lxy, label, fontsize=8, ha=ha, va="center", weight="bold", color="#555555")


def fig_3_5():
    fig, ax = schematic(6.8, 5.25, xlim=(0, 13.6), ylim=(-0.75, 9.75))
    cx = 6.6
    yS, yD1, yD2, yB, yDep, ySol, yD3, yF = 9.4, 8.05, 6.15, 4.7, 3.6, 2.5, 1.15, -0.25
    _box_c(ax, cx, yS, 5.6, 0.55, "Network with b branches, n nodes", fc="#E8F1E4", fs=8.2)
    _diamond(ax, cx, yD1, 6.2, 1.6,
             "Any loop of voltage\nsources only, or cut-set of\ncurrent sources only?")
    _box_c(ax, 12.0, yD1, 3.0, 1.75,
           "Not solvable as drawn\n(inconsistent or\nindeterminate): add\nsource resistance\n"
           "or fix topology", fc="#FBE3DC", fs=7.3)
    _diamond(ax, cx, yD2, 6.4, 1.65,
             "Planar, and fewer\nmeshes (b − n + 1) than\nunknown node voltages?")
    _box_c(ax, 2.15, yB, 4.1, 0.85, "Mesh analysis; supermesh\nfor shared current sources")
    _box_c(ax, 11.3, yB, 3.9, 0.95, "Nodal analysis; supernode\nfor floating voltage\n"
           "sources (or MNA)")
    _box_c(ax, cx, yDep, 5.9, 0.75, "Dependent sources? add control\n"
           "equations; matrix becomes asymmetric")
    _box_c(ax, cx, ySol, 4.6, 0.75, "Solve: Cramer (2–3 unknowns)\nor LU factorisation")
    _diamond(ax, cx, yD3, 5.0, 1.3, "Matrix singular or\nbadly conditioned?")
    _box_c(ax, 11.9, yD3, 3.2, 1.75, "Check floating nodes,\ndependent-source gain\n"
           "at critical value,\nextreme resistance\nratios", fc="#FBE3DC", fs=7.3)
    _box_c(ax, cx, yF, 5.9, 0.75, "Check: KCL at one node, KVL around\none loop, power balance",
           fc="#E8F1E4")
    _arr(ax, [(cx, yS - 0.275), (cx, yD1 + 0.8)])
    _arr(ax, [(cx + 3.1, yD1), (10.5, yD1)], "yes", (10.1, yD1 + 0.22))
    _arr(ax, [(cx, yD1 - 0.8), (cx, yD2 + 0.825)], "no", (cx + 0.25, yD1 - 1.02), ha="left")
    _arr(ax, [(cx - 3.2, yD2), (2.15, yD2), (2.15, yB + 0.425)], "yes", (2.9, yD2 + 0.22))
    _arr(ax, [(cx + 3.2, yD2), (11.3, yD2), (11.3, yB + 0.475)], "no", (10.4, yD2 + 0.22))
    _arr(ax, [(2.15, yB - 0.425), (2.15, yDep), (cx - 2.95, yDep)])
    _arr(ax, [(11.3, yB - 0.475), (11.3, yDep), (cx + 2.95, yDep)])
    _arr(ax, [(cx, yDep - 0.375), (cx, ySol + 0.375)])
    _arr(ax, [(cx, ySol - 0.375), (cx, yD3 + 0.65)])
    _arr(ax, [(cx + 2.5, yD3), (10.3, yD3)], "yes", (9.7, yD3 + 0.22))
    _arr(ax, [(cx, yD3 - 0.65), (cx, yF + 0.375)], "no", (cx + 0.25, yD3 - 0.85), ha="left")
    save(fig, "03", "fig-3-5-analysis-flowchart")


if __name__ == "__main__":
    fig_3_1()
    fig_3_2()
    fig_3_3()
    fig_3_4()
    fig_3_5()
