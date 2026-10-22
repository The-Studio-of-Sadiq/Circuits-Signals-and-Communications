"""Figures for Chapter 28 — Information Theory and Coding. Run from the repository root: python figures/scripts/ch28.py"""
from math import comb

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from scipy.special import erfc, erfcinv

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK

CH = "28"


def Q(x):
    return 0.5 * erfc(np.asarray(x) / np.sqrt(2))


def Hb(p):
    p = np.asarray(p, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    return np.nan_to_num(h)


# ----------------------------------------------------------------------------- Figure 28.1
def fig_28_1():
    """Binary entropy function and BSC capacity."""
    p = np.linspace(0, 1, 1001)
    fig, ax = new_fig(6.0, 3.9)
    ax.plot(p, Hb(p), color=COLORS[0], lw=2.0, label="$H_b(p)$")
    ax.plot(p, 1 - Hb(p), color=COLORS[1], lw=1.4, alpha=0.55, label="$1-H_b(p)$")
    ax.annotate("BSC capacity\n$C = 1-H_b(p)$", xy=(0.86, 0.41), xytext=(0.66, 0.5), color=COLORS[1], fontsize=9,
                ha="center", va="center", arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.8))
    ax.text(0.5, 0.92, "$H_b(p)$", color=COLORS[0], fontsize=10, ha="center", va="top")
    pts = [(0.01, "(0.01, 0.081)", (0.035, 0.17)), (0.1, "(0.1, 0.469)", (0.135, 0.36)),
           (0.11, "(0.11, 0.500)", (0.16, 0.56)), (0.5, "(0.5, 1.0)", (0.5, 1.035))]
    for x, lab, (tx, ty) in pts:
        ax.plot([x], [Hb(x)], "o", color=COLORS[0], ms=5, zorder=5)
        ax.text(tx, ty, lab, fontsize=8.5, ha="left" if x < 0.5 else "center", va="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("probability p")
    ax.set_ylabel("bits")
    ax.grid(True, lw=0.5)
    save(fig, CH, "fig-28-1-binary-entropy")


# ----------------------------------------------------------------------------- Figure 28.2
def fig_28_2():
    """Bandwidth-efficiency plane with the Shannon bound and practical schemes."""
    eta = np.logspace(-1, 1, 600)
    xb = 10 * np.log10((2 ** eta - 1) / eta)
    fig, ax = new_fig(6.4, 4.4)
    ax.fill_betweenx(eta, -2, xb, color="#E8E8E8", lw=0)
    ax.plot(xb, eta, color=INK, lw=2.0)
    ax.axvline(-1.59, color=COLORS[1], lw=1.0, ls="--")
    ax.text(-1.45, 6.5, "Shannon limit\n−1.59 dB", fontsize=8.5, color=COLORS[1], va="center")
    ax.text(0.3, 2.6, "unachievable", fontsize=9.5, color="#666666", rotation=62, ha="center", va="center")
    ax.text(11.8, 1.3, "achievable region: $E_b/N_0 \\geq (2^{\\eta}-1)/\\eta$", fontsize=8.5, color="#444444")
    unc = [("BPSK", 9.6, 1, (0.4, 0)), ("QPSK", 9.6, 2, (0.4, 0)), ("8-PSK", 13.0, 3, (0.4, 0)),
           ("16-QAM", 13.4, 4, (0.4, 0)), ("64-QAM", 17.8, 6, (0.4, 0)), ("256-QAM", 22.5, 8, (-0.45, 0)),
           ("noncoherent BFSK", 13.4, 0.5, (0.4, 0))]
    for name, x, y, (dx, dy) in unc:
        ax.plot([x], [y], "o", color=COLORS[0], ms=6, zorder=5)
        ax.text(x + dx, y * 10 ** dy, name, fontsize=8.5, va="center", ha="left" if dx > 0 else "right")
    cod = [("K = 7, R = 1/2 conv. + BPSK", 4.4, 0.5, (0.4, 0)), ("R = 1/2 LDPC + BPSK", 1.0, 0.5, (-0.6, -0.1))]
    for name, x, y, (dx, dy) in cod:
        ax.plot([x], [y], "s", color=COLORS[2], ms=6, zorder=5)
        ax.text(x + dx, y * 10 ** dy, name, fontsize=8, va="center", ha="left", color="#00704F")
    ax.annotate("", xy=(1.15, 0.52), xytext=(9.45, 0.97),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=1.3))
    ax.text(5.6, 0.83, "coding gain", fontsize=9, color="#00704F", rotation=-6, ha="center")
    ax.plot([], [], "o", color=COLORS[0], label="uncoded, BER $10^{-5}$")
    ax.plot([], [], "s", color=COLORS[2], label="coded, BER $10^{-5}$")
    ax.plot([], [], color=INK, label="Shannon bound")
    ax.legend(loc="upper left", bbox_to_anchor=(0.62, 0.31), fontsize=8)
    ax.set_yscale("log")
    ax.set_xlim(-2, 24)
    ax.set_ylim(0.1, 10)
    ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10"])
    ax.set_xlabel("$E_b/N_0$ (dB)")
    ax.set_ylabel("spectral efficiency η (b/s/Hz)")
    ax.grid(True, which="major", lw=0.5)
    save(fig, CH, "fig-28-2-bandwidth-efficiency-plane")


# ----------------------------------------------------------------------------- Figure 28.3
def fig_28_3():
    """Huffman code tree for the five-state breaker monitor."""
    fig, ax = schematic(6.4, 4.0, xlim=(0, 10), ylim=(-0.9, 5.2))
    nodes = {"root": (5.0, 4.5, "1.0"), "a": (2.5, 3.2, "0.4"), "b": (7.3, 3.2, "0.6"),
             "c": (6.0, 1.9, "0.2")}
    leaves = {"ON": (1.2, 1.6, "open–normal", "0.2", "00"), "CA": (3.6, 1.6, "closed–alarm", "0.2", "01"),
              "OA": (4.9, 0.25, "open–alarm", "0.1", "100"), "F": (7.1, 0.25, "fault", "0.1", "101"),
              "CN": (8.85, 1.6, "closed–normal", "0.4", "11")}
    edges = [("root", "a", "0"), ("root", "b", "1"), ("a", "ON", "0"), ("a", "CA", "1"),
             ("b", "c", "0"), ("b", "CN", "1"), ("c", "OA", "0"), ("c", "F", "1")]

    def pos(k):
        return (nodes[k][0], nodes[k][1]) if k in nodes else (leaves[k][0], leaves[k][1] + 0.45)

    for a, b, bit in edges:
        (x0, y0), (x1, y1) = pos(a), pos(b)
        ax.plot([x0, x1], [y0, y1], color=INK, lw=1.2, zorder=1)
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        off = -0.22 if bit == "0" else 0.22
        ax.text(xm + off, ym + 0.12, bit, fontsize=10, color=COLORS[1], fontweight="bold", ha="center", va="center")
    for k, (x, y, p) in nodes.items():
        ax.add_patch(Circle((x, y), 0.33, fc="#EEF3F8", ec=INK, lw=1.1, zorder=2))
        ax.text(x, y, p, ha="center", va="center", fontsize=9, zorder=3)
    for k, (x, y, name, p, cw) in leaves.items():
        box(ax, x - 0.95, y - 0.55, 1.9, 1.0, "", fc="#FFF4E0")
        ax.text(x, y + 0.24, name, ha="center", va="center", fontsize=8)
        ax.text(x, y - 0.03, f"p = {p}", ha="center", va="center", fontsize=8)
        ax.text(x, y - 0.33, cw, ha="center", va="center", fontsize=9.5, color=COLORS[0], fontweight="bold")
    ax.text(5.0, -0.7, "average length $\\bar L$ = 2.2 bits   ·   entropy H = 2.122 bits   ·   efficiency 96.5 %",
            ha="center", fontsize=9)
    save(fig, CH, "fig-28-3-huffman-tree")


# ----------------------------------------------------------------------------- Figure 28.4
def _xor(ax, x, y, r=0.32):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=3))
    ax.plot([x - r, x + r], [y, y], color=INK, lw=1.2, zorder=4)
    ax.plot([x, x], [y - r, y + r], color=INK, lw=1.2, zorder=4)


def fig_28_4():
    """(7,5) convolutional encoder and its trellis with the path for input 101100."""
    fig = plt.figure(figsize=(6.8, 3.6))
    ax = fig.add_axes([0.0, 0.02, 0.42, 0.96])
    ax.set_xlim(0, 10.2)
    ax.set_ylim(-0.2, 8.4)
    ax.set_aspect("equal")
    ax.axis("off")
    y0 = 4.0
    lw = 1.1
    # input and register
    arrow(ax, 0.2, y0, 2.6, y0)
    ax.text(0.2, y0 + 0.25, "$u_k$", fontsize=10)
    ax.plot([1.5], [y0], "o", color=INK, ms=3.5)
    box(ax, 2.6, y0 - 0.5, 1.3, 1.0, "$u_{k-1}$", fontsize=9)
    arrow(ax, 3.9, y0, 4.9, y0)
    ax.plot([4.4], [y0], "o", color=INK, ms=3.5)
    box(ax, 4.9, y0 - 0.5, 1.3, 1.0, "$u_{k-2}$", fontsize=9)
    ax.plot([6.2, 6.9], [y0, y0], color=INK, lw=lw)
    ax.plot([6.9], [y0], "o", color=INK, ms=3.5)
    ax.text(4.25, y0 - 1.0, "shift register", ha="center", fontsize=7.5, color="#555555")
    yu, yl = 6.6, 1.4
    xa = 4.4
    # upper adder: u_k, u_k-1, u_k-2
    ax.plot([1.5, 1.5, xa - 0.32], [y0, yu, yu], color=INK, lw=lw)
    arrow(ax, xa - 0.6, yu, xa - 0.32, yu)
    arrow(ax, xa, y0, xa, yu - 0.32)
    ax.plot([6.9, 6.9, xa + 0.6], [y0, yu, yu], color=INK, lw=lw)
    arrow(ax, xa + 0.6, yu, xa + 0.32, yu)
    _xor(ax, xa, yu)
    # lower adder: u_k, u_k-2
    ax.plot([1.5, 1.5, xa - 0.6], [y0, yl, yl], color=INK, lw=lw)
    arrow(ax, xa - 0.6, yl, xa - 0.32, yl)
    ax.plot([6.9, 6.9, xa + 0.6], [y0, yl, yl], color=INK, lw=lw)
    arrow(ax, xa + 0.6, yl, xa + 0.32, yl)
    _xor(ax, xa, yl)
    # outputs to commutator
    xc = 8.4
    ax.plot([xa, xa, xc], [yu + 0.32, 7.6, 7.6], color=INK, lw=lw)
    ax.plot([xc, xc], [7.6, y0 + 0.6], color=INK, lw=lw)
    ax.plot([xa, xa, xc], [yl - 0.32, 0.4, 0.4], color=INK, lw=lw)
    ax.plot([xc, xc], [0.4, y0 - 0.6], color=INK, lw=lw)
    ax.text(6.2, 7.75, "$c^{(1)}_k$  (g₁ = 111)", fontsize=8.5)
    ax.text(6.2, 0.05, "$c^{(2)}_k$  (g₂ = 101)", fontsize=8.5)
    ax.plot([xc], [y0 + 0.6], "o", color=INK, ms=4, mfc="white")
    ax.plot([xc], [y0 - 0.6], "o", color=INK, ms=4, mfc="white")
    ax.plot([9.2, xc + 0.08], [y0, y0 + 0.55], color=INK, lw=1.4)
    ax.plot([9.2], [y0], "o", color=INK, ms=3.5)
    arrow(ax, 9.2, y0, 10.1, y0)
    ax.text(9.0, y0 - 1.55, "commutator", ha="center", fontsize=7.5)
    ax.text(9.75, y0 + 0.25, "out", ha="center", fontsize=7.5)
    ax.text(0.1, 8.2, "(a) encoder, R = 1/2, K = 3", fontsize=9.5)

    # trellis
    at = fig.add_axes([0.5, 0.14, 0.49, 0.7])
    states = ["00", "10", "01", "11"]
    ys = {"00": 3, "10": 2, "01": 1, "11": 0}

    def step(s, u):
        a, b = int(s[0]), int(s[1])
        return f"{u}{a}", f"{u ^ a ^ b}{u ^ b}"

    reach = {0: {"00"}}
    for t in range(6):
        reach[t + 1] = set()
        for s in reach[t]:
            for u in (0, 1):
                ns, out = step(s, u)
                reach[t + 1].add(ns)
                at.plot([t, t + 1], [ys[s], ys[ns]], color="#9A9A9A", lw=0.9,
                        ls="-" if u == 0 else (0, (3, 2)), zorder=1)
                if t == 2:
                    # staggered positions along each branch so that the eight labels do not collide
                    fx = {("00", 0): 0.5, ("00", 1): 0.4, ("10", 0): 0.22, ("10", 1): 0.45,
                          ("01", 0): 0.62, ("01", 1): 0.72, ("11", 0): 0.6, ("11", 1): 0.35}[(s, u)]
                    xm, ym = t + fx, ys[s] + fx * (ys[ns] - ys[s])
                    dy = 0.13 if ys[ns] == ys[s] else 0.0
                    at.text(xm, ym + dy, f"{u}/{out}", fontsize=6.8, ha="center", va="center",
                            bbox=dict(fc="white", ec="#BBBBBB", lw=0.4, pad=0.6), zorder=6)
    path_in = [1, 0, 1, 1, 0, 0]
    s = "00"
    outs = []
    for t, u in enumerate(path_in):
        ns, out = step(s, u)
        at.plot([t, t + 1], [ys[s], ys[ns]], color=COLORS[1], lw=2.6, ls="-" if u == 0 else (0, (3, 1.5)), zorder=3)
        outs.append(out)
        at.text(t + 0.5, -0.62, out, ha="center", fontsize=8.5, color=COLORS[1], fontweight="bold")
        at.text(t + 0.5, -0.95, f"u = {u}", ha="center", fontsize=7.5, color="#555555")
        s = ns
    for t in range(7):
        for st in states:
            r = st in reach[t]
            at.plot([t], [ys[st]], "o", color=INK, ms=4.5, mfc=INK if r else "white", zorder=5)
    at.set_xlim(-0.15, 6.15)
    at.set_ylim(-1.1, 3.4)
    at.set_yticks([3, 2, 1, 0])
    at.set_yticklabels(states)
    at.set_xticks(range(7))

    at.text(-0.55, 3.55, "state\n$u_{k-1}u_{k-2}$", ha="center", va="bottom", fontsize=7.5)
    at.spines["left"].set_visible(False)
    at.spines["bottom"].set_visible(False)
    at.tick_params(length=0)
    at.xaxis.set_label_position("top")
    at.xaxis.tick_top()
    at.text(-0.1, -0.62, "out", ha="right", fontsize=7.5, color=COLORS[1])
    at.plot([], [], color="#9A9A9A", ls="-", label="input 0")
    at.plot([], [], color="#9A9A9A", ls=(0, (3, 2)), label="input 1")
    at.plot([], [], color=COLORS[1], lw=2.6, label="path for 1 0 1 1 0 0")
    at.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=7.5)
    at.set_title("(b) trellis, time steps k = 0…6; labels input/output at k = 2→3", fontsize=9, pad=26)
    save(fig, CH, "fig-28-4-convolutional-encoder-trellis")


# ----------------------------------------------------------------------------- Figure 28.5
H74 = np.array([[1, 0, 1, 1, 1, 0, 0],
                [1, 1, 1, 0, 0, 1, 0],
                [0, 1, 1, 1, 0, 0, 1]])


def fig_28_5():
    """Coded BER on AWGN (uncoded, Hamming, K=7 conv., LDPC) and Tanner graph of Hamming (7,4)."""
    x = np.linspace(-2, 12, 1401)
    g = 10 ** (x / 10)
    unc = Q(np.sqrt(2 * g))
    # Hamming (7,4), hard decision, bounded-distance decoding
    p = Q(np.sqrt(2 * g * 4 / 7))
    ham = sum(min(j + 1, 7) / 7 * comb(7, j) * p ** j * (1 - p) ** (7 - j) for j in range(2, 8))
    # K = 7 (171,133) convolutional code, soft Viterbi: union bound, 0.25 dB quantisation loss
    Bd = {10: 36, 12: 211, 14: 1404, 16: 11633, 18: 77433, 20: 502690}
    gq = 10 ** ((x - 0.25) / 10)
    conv = sum(b * Q(np.sqrt(2 * d * 0.5 * gq)) for d, b in Bd.items())
    conv = np.where(conv <= 0.05, conv, np.nan)
    # LDPC, rate 1/2, n = 64800: illustrative waterfall fitted to 1e-5 at 1.0 dB
    s = 0.2
    x0 = 1.0 - s * erfcinv(2e-5 / 0.1)
    ldpc = 0.05 * erfc((x - x0) / s)

    fig = plt.figure(figsize=(6.8, 4.2))
    ax = fig.add_axes([0.09, 0.12, 0.56, 0.84])
    ax.semilogy(x, unc, color=INK, lw=1.8, label="uncoded BPSK")
    ax.semilogy(x, ham, color=COLORS[0], lw=1.6, label="Hamming (7,4), hard")
    ax.semilogy(x, conv, color=COLORS[2], lw=1.6, label="K = 7, R = 1/2 conv., soft Viterbi")
    ax.semilogy(np.where(x >= 0, x, np.nan), ldpc, color=COLORS[1], lw=1.8, label="R = 1/2 LDPC, n = 64 800 (model)")
    ax.axhline(1e-5, color="#999999", lw=0.7, ls=":")
    for xv, lab, c in [(0.19, "rate-1/2 binary-input limit 0.19 dB", COLORS[3]),
                       (-1.59, "Shannon limit −1.59 dB", COLORS[4])]:
        ax.axvline(xv, color=c, lw=1.1, ls="--")
        ax.text(xv + 0.12, 2e-7, lab, rotation=90, fontsize=7.5, color=c, va="bottom")
    for xv, c in [(9.6, INK), (9.2, COLORS[0]), (4.4, COLORS[2]), (1.0, COLORS[1])]:
        ax.plot([xv], [1e-5], "o", color=c, ms=4, zorder=5)
    ax.text(9.6, 1.5e-5, "9.6", fontsize=7.5, ha="left")
    ax.text(9.15, 6e-6, "9.2", fontsize=7.5, ha="right", color=COLORS[0])
    ax.text(4.55, 1.4e-5, "4.4", fontsize=7.5, color=COLORS[2])
    ax.text(1.15, 1.4e-5, "1.0", fontsize=7.5, color=COLORS[1])
    ax.set_xlim(-2, 12)
    ax.set_ylim(1e-7, 1e-1)
    ax.set_xlabel("$E_b/N_0$ (dB)")
    ax.set_ylabel("bit error rate")
    ax.grid(True, which="major", lw=0.5)
    fig.legend(loc="lower left", bbox_to_anchor=(0.665, 0.1), fontsize=7.5, frameon=False)

    # Tanner graph
    at = fig.add_axes([0.67, 0.4, 0.33, 0.58])
    at.set_xlim(-0.6, 6.6)
    at.set_ylim(-1.2, 5.4)
    at.axis("off")
    at.set_aspect("equal")
    vx = np.arange(7)
    cx = np.array([1.0, 3.0, 5.0])
    yv, yc = 3.6, 0.6
    for i in range(3):
        for j in range(7):
            if H74[i, j]:
                at.plot([vx[j], cx[i]], [yv, yc], color=COLORS[0], lw=0.9, zorder=1)
    for j in range(7):
        at.add_patch(Circle((vx[j], yv), 0.3, fc="white", ec=INK, lw=1.1, zorder=3))
        at.text(vx[j], yv + 0.6, f"$v_{j+1}$", ha="center", fontsize=8.5)
    for i in range(3):
        at.add_patch(Rectangle((cx[i] - 0.3, yc - 0.3), 0.6, 0.6, fc="#EEF3F8", ec=INK, lw=1.1, zorder=3))
        at.text(cx[i], yc - 0.75, f"$c_{i+1}$", ha="center", fontsize=8.5)
    at.text(3.0, 5.05, "Tanner graph, Hamming (7,4)", ha="center", fontsize=9)
    at.text(3.0, 4.55, "variable nodes (code bits)", ha="center", fontsize=7.5, color="#555555")
    at.text(3.0, -1.15, "check nodes (rows of H)", ha="center", fontsize=7.5, color="#555555")
    save(fig, CH, "fig-28-5-coded-ber-and-tanner-graph")


if __name__ == "__main__":
    fig_28_1()
    fig_28_2()
    fig_28_3()
    fig_28_4()
    fig_28_5()
