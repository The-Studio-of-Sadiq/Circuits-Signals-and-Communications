"""Figures for Chapter 20 — Discrete-Time Signals and Systems.

Run from the repository root:  python figures/scripts/ch20.py
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, ConnectionPatch, Wedge, Arc
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, save, COLORS, INK, GRID  # noqa: E402

CH = "20"
GREEN, RED, ORANGE, BLUE = COLORS[2], COLORS[1], COLORS[4], COLORS[0]


def _stem(ax, n, x, color=INK, ms=4.5, mfc=None, lw=1.1, zorder=3, label=None):
    ml, sl, bl = ax.stem(n, x, basefmt=" ", label=label)
    plt.setp(sl, color=color, lw=lw, zorder=zorder)
    plt.setp(ml, color=color, ms=ms, zorder=zorder + 1, mfc=mfc if mfc else color)
    return ml, sl


def _zplane_axes(ax, lim):
    ax.set_aspect("equal")
    ax.axhline(0, color="0.5", lw=0.6)
    ax.axvline(0, color="0.5", lw=0.6)
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=INK, lw=1.2))
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("Re $z$")
    ax.set_ylabel("Im $z$")


def fig_20_1():
    """Elementary sequences."""
    n = np.arange(-5, 21)
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 4.6), sharex=True)
    ax = axs[0, 0]
    _stem(ax, n, (n == 0).astype(float), color=BLUE)
    ax.set_title(r"(a) unit impulse $\delta[n]$", loc="left", fontsize=10)
    ax.set_ylim(-0.2, 1.25)
    ax = axs[0, 1]
    _stem(ax, n, (n >= 0).astype(float), color=BLUE)
    ax.set_title(r"(b) unit step $u[n]$", loc="left", fontsize=10)
    ax.set_ylim(-0.2, 1.25)
    ax = axs[1, 0]
    u = (n >= 0).astype(float)
    _stem(ax, n + 0.0, 0.8 ** n * u, color=BLUE, label=r"$0.8^n u[n]$")
    ml, sl = _stem(ax, n, (-0.8) ** n * u, color=RED, mfc="white", label=r"$(-0.8)^n u[n]$")
    ax.set_title("(c) exponentials", loc="left", fontsize=10)
    ax.set_ylim(-1.0, 1.25)
    ax.legend(loc="upper right", fontsize=8.5, handlelength=1.2)
    ax = axs[1, 1]
    t = np.linspace(-5, 20, 1000)
    ax.plot(t, np.cos(0.3 * np.pi * t), color="0.75", lw=1.0)
    _stem(ax, n, np.cos(0.3 * np.pi * n), color=BLUE)
    for k in (0, 20):
        ax.plot(k, 1, "o", ms=9, mfc="none", mec=RED, mew=1.6, zorder=6)
    ax.annotate("", xy=(20, 1.12), xytext=(0, 1.12),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=0.9, mutation_scale=8))
    ax.text(10, 1.17, "period N = 20 (three cycles)", ha="center", va="bottom", fontsize=8.5, color=RED)
    ax.set_title(r"(d) $\cos(0.3\pi n)$", loc="left", fontsize=10)
    ax.set_ylim(-1.2, 1.5)
    for ax in axs.flat:
        ax.axhline(0, color=INK, lw=0.6)
        ax.set_xlim(-5.5, 20.5)
        ax.set_xticks([-5, 0, 5, 10, 15, 20])
    for ax in axs[1]:
        ax.set_xlabel("$n$")
    fig.tight_layout(h_pad=0.8, w_pad=1.0)
    save(fig, CH, "fig-20-1-basic-sequences")


def fig_20_2():
    """Graphical convolution of x = [3, 1, 2] with h = [1, 0.5, 0.25]."""
    h = np.array([1, 0.5, 0.25])
    x = np.array([3, 1, 2])
    y = np.convolve(x, h)
    k = np.arange(-3, 6)
    hk = np.array([h[i] if 0 <= i < 3 else 0 for i in k])
    xr = np.array([x[2 - i] if 0 <= 2 - i < 3 else 0 for i in k])
    prod = hk * xr
    fig = plt.figure(figsize=(6.8, 4.6))
    gs = fig.add_gridspec(3, 2, width_ratios=[1, 1.05], hspace=0.65, wspace=0.35)
    a1 = fig.add_subplot(gs[0, 0])
    a2 = fig.add_subplot(gs[1, 0], sharex=a1)
    a3 = fig.add_subplot(gs[2, 0], sharex=a1)
    ar = fig.add_subplot(gs[:, 1])
    _stem(a1, k, hk, color=BLUE)
    a1.set_title("$h[k]$ (channel)", loc="left", fontsize=10)
    a1.set_ylim(0, 1.35)
    _stem(a2, k + 0.12, hk, color="0.7", ms=3.5)
    _stem(a2, k - 0.12, xr, color=ORANGE)
    a2.set_title("$x[2-k]$ (orange) over $h[k]$ (grey)", loc="left", fontsize=10)
    a2.set_ylim(0, 3.9)
    _stem(a3, k, prod, color=GREEN)
    for kk, p in zip(k, prod):
        if p:
            a3.text(kk, p + 0.18, f"{p:g}", ha="center", va="bottom", fontsize=8.5, color=GREEN)
    a3.set_title("products $h[k]\\,x[2-k]$", loc="left", fontsize=10)
    a3.text(5.4, 2.1, "sum\n= 0.75 + 0.5 + 2\n= 3.25 = $y[2]$", ha="right", va="center", fontsize=8,
            color=INK)
    a3.set_ylim(0, 2.9)
    a3.set_xlim(-3.5, 5.5)
    a3.set_xlabel("$k$")
    for ax in (a1, a2, a3):
        ax.set_xlim(-3.5, 5.5)
        ax.set_xticks(range(-3, 6))
        ax.axhline(0, color=INK, lw=0.6)
        ax.tick_params(labelsize=8)
    n = np.arange(-1, 6)
    yy = np.array([y[i] if 0 <= i < 5 else 0 for i in n])
    _stem(ar, n, yy, color=INK, ms=5.5)
    _stem(ar, [2], [y[2]], color=GREEN, ms=8, lw=2.2)
    for i, v in enumerate(y):
        ar.text(i, v + 0.12, f"{v:g}", ha="center", va="bottom", fontsize=9,
                color=GREEN if i == 2 else INK)
    ar.axhline(0, color=INK, lw=0.6)
    ar.set_xlim(-1.5, 5.5)
    ar.set_ylim(0, 3.8)
    ar.set_xticks(range(-1, 6))
    ar.set_xlabel("$n$")
    ar.set_ylabel("$y[n]$")
    ar.set_title("output $y = x * h$", loc="left", fontsize=10)
    save(fig, CH, "fig-20-2-graphical-convolution")


def _adder(ax, x, y, r=0.28):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.2, zorder=4))
    ax.text(x, y, "+", ha="center", va="center", fontsize=12, zorder=5)


def _gain(ax, x, y, direction, label, size=0.36, lab_off=(0, 0.32), ha="center"):
    """Triangle gain symbol centred at (x, y) pointing 'left' or 'right' or 'up'."""
    s = size
    if direction == "right":
        pts = [(x - s / 2, y - s / 2), (x - s / 2, y + s / 2), (x + s / 2, y)]
    elif direction == "left":
        pts = [(x + s / 2, y - s / 2), (x + s / 2, y + s / 2), (x - s / 2, y)]
    else:
        pts = [(x - s / 2, y - s / 2), (x + s / 2, y - s / 2), (x, y + s / 2)]
    ax.add_patch(Polygon(pts, closed=True, fc="#EEF3F8", ec=INK, lw=1.1, zorder=4))
    ax.text(x + lab_off[0], y + lab_off[1], label, ha=ha, va="bottom", fontsize=8.5, zorder=5)


def _line(ax, pts, arrow=False):
    xs, ys = zip(*pts)
    if not arrow:
        ax.plot(xs, ys, color=INK, lw=1.1, zorder=2)
    else:
        ax.plot(xs[:-1], ys[:-1], color=INK, lw=1.1, zorder=2)
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, shrinkA=0, shrinkB=0,
                                    mutation_scale=10), zorder=3)


def fig_20_3():
    """Direct form II biquad with the 50 Hz notch coefficients."""
    fig, ax = schematic(6.8, 4.4, xlim=(0, 11.5), ylim=(0.3, 7.6))
    yt, ym, yb = 6.2, 3.9, 1.6
    xa, xn, xb = 3.2, 5.8, 8.4
    r = 0.28
    # input
    ax.text(0.2, yt, "$x[n]$", ha="left", va="center", fontsize=11)
    _line(ax, [(0.95, yt), (xa - r, yt)], arrow=True)
    _adder(ax, xa, yt)
    _adder(ax, xa, ym)
    # left adders chain: ym adder output up into top adder
    _line(ax, [(xa, ym + r), (xa, yt - r)], arrow=True)
    # top adder output to node w[n]
    _line(ax, [(xa + r, yt), (xn, yt)])
    ax.plot(xn, yt, "o", color=INK, ms=4, zorder=5)
    ax.text(xn - 0.08, yt + 0.22, "$w[n]$", ha="right", va="bottom", fontsize=10)
    # delay chain
    for y0, y1, lab in ((yt, ym, "$w[n-1]$"), (ym, yb, "$w[n-2]$")):
        yc = (y0 + y1) / 2
        _line(ax, [(xn, y0), (xn, yc + 0.35)], arrow=True)
        ax.add_patch(Rectangle((xn - 0.42, yc - 0.35), 0.84, 0.7, fc="#EEF3F8", ec=INK, lw=1.1, zorder=4))
        ax.text(xn, yc, "$z^{-1}$", ha="center", va="center", fontsize=11, zorder=5)
        _line(ax, [(xn, yc - 0.35), (xn, y1)])
        ax.plot(xn, y1, "o", color=INK, ms=4, zorder=5)
        ax.text(xn + 0.1, y1 + 0.12, lab, ha="left", va="bottom", fontsize=9.5)
    # feedback branches
    gx = (xa + xn) / 2
    _line(ax, [(xn, ym), (gx + 0.2, ym)])
    _gain(ax, gx, ym, "left", "$-a_1$ = 1.5371", lab_off=(0, -0.62))
    _line(ax, [(gx - 0.2, ym), (xa + r, ym)], arrow=True)
    _line(ax, [(xn, yb), (gx + 0.2, yb)])
    _gain(ax, gx, yb, "left", "$-a_2$ = $-$0.9025", lab_off=(0, -0.62))
    _line(ax, [(gx - 0.2, yb), (xa, yb), (xa, ym - r)], arrow=True)
    # feed-forward branches
    _adder(ax, xb + 1.0, yt)
    _adder(ax, xb + 1.0, ym)
    fx = (xn + xb + 1.0) / 2 + 0.1
    for y0, lab in ((yt, "$b_0$ = 0.9565"), (ym, "$b_1$ = $-$1.5477"), (yb, "$b_2$ = 0.9565")):
        _line(ax, [(xn, y0), (fx - 0.2, y0)])
        _gain(ax, fx, y0, "right", lab, lab_off=(0, 0.26) if y0 == yt else (0, -0.62))
    _line(ax, [(fx + 0.2, yt), (xb + 1.0 - r, yt)], arrow=True)
    _line(ax, [(fx + 0.2, ym), (xb + 1.0 - r, ym)], arrow=True)
    _line(ax, [(fx + 0.2, yb), (xb + 1.0, yb), (xb + 1.0, ym - r)], arrow=True)
    _line(ax, [(xb + 1.0, ym + r), (xb + 1.0, yt - r)], arrow=True)
    _line(ax, [(xb + 1.0 + r, yt), (10.75, yt)], arrow=True)
    ax.text(10.8, yt, "$y[n]$", ha="left", va="center", fontsize=11)
    ax.text(5.75, 0.45,
            r"$H(z)=\dfrac{b_0+b_1z^{-1}+b_2z^{-2}}{1+a_1z^{-1}+a_2z^{-2}}$,   $a_1$ = $-$1.5371, $a_2$ = 0.9025",
            ha="center", va="center", fontsize=9.5)
    ax.text(0.2, 7.3, "feedback (poles)", fontsize=9, color="0.35")
    ax.text(11.3, 7.3, "feed-forward (zeros)", fontsize=9, color="0.35", ha="right")
    save(fig, CH, "fig-20-3-biquad-direct-form-ii")


def fig_20_4():
    """Mapping of the s-plane to the z-plane, z = exp(sT), T = 1 ms."""
    T = 1e-3
    wmax = np.pi / T
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1, 1.05]))
    # s-plane
    ylim = 4600
    a1.add_patch(Rectangle((-400, -ylim), 400, 2 * ylim, color=COLORS[5], alpha=0.10, lw=0))
    a1.add_patch(Rectangle((-400, -wmax), 400, 2 * wmax, color=COLORS[5], alpha=0.22, lw=0))
    for yy in (wmax, -wmax):
        a1.axhline(yy, color="0.4", ls="--", lw=0.9)
    a1.text(-395, wmax + 120, r"$+\pi/T$", fontsize=8.5, va="bottom")
    a1.text(-395, -wmax - 120, r"$-\pi/T$", fontsize=8.5, va="top")
    a1.text(-250, -1700, "primary strip\n(T = 1 ms)", ha="center", fontsize=8.5, color="0.25")
    a1.text(-250, 4000, "left half-plane", ha="center", fontsize=8.5, color="0.25")
    a1.axhline(0, color="0.5", lw=0.6)
    a1.axvline(0, color=INK, lw=2.0)
    a1.text(8, -4300, r"$j\omega$" + "\naxis", fontsize=8.5, color=INK, ha="left", va="bottom")
    w50 = 2 * np.pi * 50
    a1.axvline(-100, color=BLUE, ls=":", lw=1.2)
    a1.plot([-400, 0], [w50, w50], color=ORANGE, ls=":", lw=1.2)
    a1.plot([-100, -100], [w50, -w50], "x", color=RED, ms=9, mew=2, zorder=5)
    a1.text(-110, 700, r"$-100 \pm j2\pi\,50$", fontsize=8.5, color=RED, ha="right", va="bottom")
    a1.text(-92, 2300, r"$\sigma$ = $-$100", rotation=90, fontsize=8, color=BLUE, ha="left", va="center")
    a1.text(-395, w50 + 80, r"$\omega$ = $2\pi\,50$", fontsize=8, color=ORANGE, va="bottom")
    a1.set_xlim(-400, 100)
    a1.set_ylim(-ylim, ylim)
    a1.set_xticks([-400, -300, -200, -100, 0, 100])
    a1.set_yticks([-2 * np.pi * 500, -2 * np.pi * 250, 0, 2 * np.pi * 250, 2 * np.pi * 500])
    a1.set_yticklabels([r"$-2\pi$500", r"$-2\pi$250", "0", r"$2\pi$250", r"$2\pi$500"], fontsize=8)
    a1.tick_params(axis="x", labelsize=8)
    a1.set_xlabel(r"$\sigma$ (s$^{-1}$)")
    a1.set_ylabel(r"$j\omega$ (rad/s)")
    a1.set_title("s-plane", fontsize=10)
    # z-plane
    a2.add_patch(Circle((0, 0), 1, color=COLORS[5], alpha=0.22, lw=0))
    _zplane_axes(a2, 1.2)
    a2.add_patch(Circle((0, 0), 1, fill=False, ec=INK, lw=2.0))
    r = np.exp(-100 * T)
    th = 2 * np.pi * 50 * T
    a2.add_patch(Circle((0, 0), r, fill=False, ec=BLUE, ls="--", lw=1.1))
    for sgn in (1, -1):
        a2.plot([0, 1.2 * np.cos(th)], [0, sgn * 1.2 * np.sin(th)], color=ORANGE, ls=":", lw=1.2)
        a2.plot(r * np.cos(th), sgn * r * np.sin(th), "x", color=RED, ms=9, mew=2, zorder=5)
    a2.text(-0.02, 0.36, "0.8606 ± j0.2796", fontsize=8, color=RED, ha="center")
    a2.add_patch(Arc((0, 0), 0.9, 0.9, theta1=0, theta2=18, color=ORANGE, lw=1))
    a2.text(0.56, 0.085, "18°", fontsize=8, color=ORANGE, va="center")
    a2.text(0, -0.62, "circle r = 0.9048\n(image of $\\sigma$ = $-$100)", fontsize=8, color=BLUE, ha="center")
    a2.text(0, -1.15, "unit circle = image of $j\\omega$ axis", fontsize=8, ha="center", va="bottom")
    a2.text(0, 1.04, "interior = image of LHP", fontsize=8, ha="center", va="bottom", color="0.25")
    a2.set_title("z-plane", fontsize=10)
    a2.tick_params(labelsize=8)
    fig.tight_layout(w_pad=4.5)
    p1 = a1.get_position()
    p2 = a2.get_position()
    xm0, xm1 = p1.x1 + 0.015, p2.x0 - 0.09
    ym = (p1.y0 + p1.y1) / 2
    fig.add_artist(matplotlib_arrow(xm0, ym, xm1, ym))
    fig.text((xm0 + xm1) / 2, ym + 0.03, r"$z=e^{sT}$", ha="center", va="bottom", fontsize=10.5)
    save(fig, CH, "fig-20-4-s-to-z-mapping")


def matplotlib_arrow(x0, y0, x1, y1):
    """Figure-coordinate arrow artist."""
    from matplotlib.patches import FancyArrowPatch
    return FancyArrowPatch((x0, y0), (x1, y1), transform=plt.gcf().transFigure, arrowstyle="-|>",
                           mutation_scale=14, lw=1.4, color=INK)


def fig_20_5():
    """Pole locations and the corresponding impulse responses."""
    cases = [((-1.8, 0.9), GREEN, "stable: $1-1.8z^{-1}+0.9z^{-2}$"),
             ((-1.8, 1.01), RED, "unstable: $1-1.8z^{-1}+1.01z^{-2}$"),
             ((-1.0, -0.5), ORANGE, "unstable: $1-z^{-1}-0.5z^{-2}$")]
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(3, 2, width_ratios=[1, 1.25], height_ratios=[1, 1, 1], hspace=0.55, wspace=0.3)
    az = fig.add_subplot(gs[0:2, 0])
    at = fig.add_subplot(gs[2, 0])
    _zplane_axes(az, 1.6)
    for (a1, a2), c, _ in cases:
        p = np.roots([1, a1, a2])
        az.plot(p.real, p.imag, "x", color=c, ms=9, mew=2, zorder=5)
    az.text(0.62, 0.05, "0.9 ± j0.3\n|p| = 0.9487", fontsize=7.5, color=GREEN, ha="right", va="bottom")
    az.text(0.95, 0.62, "0.9 ± j0.447\n|p| = 1.005", fontsize=7.5, color=RED, ha="left", va="bottom")
    az.text(1.366, -0.14, "1.366", fontsize=7.5, color=ORANGE, ha="center", va="top")
    az.text(-0.366, -0.14, "$-$0.366", fontsize=7.5, color=ORANGE, ha="center", va="top")
    az.set_xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    az.set_yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    az.tick_params(labelsize=7.5)
    az.set_title("z-plane poles", fontsize=10)
    # stability triangle
    at.add_patch(Polygon([(-2, 1), (2, 1), (0, -1)], closed=True, fc=COLORS[5], alpha=0.25, ec=INK, lw=1))
    a1g = np.linspace(-2, 2, 200)
    at.plot(a1g, a1g ** 2 / 4, color="0.45", ls="--", lw=0.8)
    at.text(0.75, 0.45, "complex\npoles", ha="center", fontsize=7, color="0.35")
    for (a1, a2), c, _ in cases:
        at.plot(a1, a2, "o", color=c, ms=5.5, zorder=5)
    at.text(-1.62, 1.08, "(−1.8, 1.01)", fontsize=7, color=RED, va="bottom")
    at.text(-1.62, 0.78, "(−1.8, 0.9)", fontsize=7, color=GREEN, va="top")
    at.text(-0.85, -0.5, "(−1, −0.5)", fontsize=7, color=ORANGE, va="center")
    at.set_xlim(-2.3, 2.3)
    at.set_ylim(-1.2, 1.4)
    at.set_xlabel("$a_1$", labelpad=1)
    at.set_ylabel("$a_2$")
    at.tick_params(labelsize=7.5)
    at.set_title("stability triangle", fontsize=10)
    n = np.arange(81)
    d = (n == 0).astype(float)
    for i, ((a1, a2), c, lab) in enumerate(cases):
        ax = fig.add_subplot(gs[i, 1])
        h = signal.lfilter([1], [1, a1, a2], d)
        if i == 2:
            hc = np.minimum(h, 100)
            _stem(ax, n, hc, color=c, ms=2.5, lw=0.8)
            ax.axhline(100, color=c, ls=":", lw=0.8)
            ax.text(79, 104, "clipped at 100", ha="right", va="bottom", fontsize=8, color=c)
            ax.set_ylim(0, 125)
        else:
            _stem(ax, n, h, color=c, ms=2.5, lw=0.8)
        ax.axhline(0, color=INK, lw=0.5)
        ax.set_xlim(-1, 81)
        ax.set_title(lab, loc="left", fontsize=8.5, color=c)
        ax.tick_params(labelsize=7.5)
        ax.set_ylabel("$h[n]$", fontsize=9)
        if i == 0:
            ax.text(79, -1.6, "period ≈ 19.5 samples", ha="right", va="bottom", fontsize=7.5, color=c)
        if i == 2:
            ax.set_xlabel("$n$")
    save(fig, CH, "fig-20-5-pole-location-responses")


def fig_20_6():
    """ECG 50 Hz notch: pole-zero plot and magnitude response."""
    fs = 500.0
    w0 = 2 * np.pi * 50 / fs

    def notch(r):
        b = np.array([1, -2 * np.cos(w0), 1])
        a = np.array([1, -2 * r * np.cos(w0), r * r])
        return b * a.sum() / b.sum(), a

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.5), gridspec_kw=dict(width_ratios=[1, 1.35]))
    _zplane_axes(a1, 1.3)
    for s in (1, -1):
        a1.plot(np.cos(w0), s * np.sin(w0), "o", mfc="white", mec=BLUE, ms=8, mew=1.6, zorder=5)
        a1.plot(0.95 * np.cos(w0), s * 0.95 * np.sin(w0), "x", color=RED, ms=8, mew=1.8, zorder=6)
    a1.plot([0, np.cos(w0)], [0, np.sin(w0)], color="0.5", lw=0.7, ls=":")
    a1.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=36, color=INK, lw=0.9))
    a1.text(0.36, 0.11, "36°", fontsize=8)
    a1.text(np.cos(w0) + 0.06, np.sin(w0) + 0.06, "50 Hz", fontsize=8.5, color=BLUE)
    a1.text(1.04, -0.12, "0 Hz", fontsize=8, ha="left", va="top")
    a1.text(-1.04, -0.12, "250 Hz", fontsize=8, ha="right", va="top")
    a1.plot([1, -1], [0, 0], "|", color=INK, ms=6)
    a1.text(-1.25, 1.18, "o zeros on circle\nx poles at r = 0.95", fontsize=7.5, va="top")
    a1.tick_params(labelsize=7.5)
    a1.set_xlim(-1.35, 1.35)
    a1.set_ylim(-1.35, 1.35)
    a1.set_title("z-plane", fontsize=10)

    f = np.linspace(0, 250, 25001)
    for r, ls, c, lab in ((0.95, "-", INK, "r = 0.95"), (0.99, "--", COLORS[3], "r = 0.99 (≈1.6 Hz wide)")):
        b, a = notch(r)
        _, H = signal.freqz(b, a, worN=2 * np.pi * f / fs)
        a2.plot(f, 20 * np.log10(np.abs(H) + 1e-12), ls=ls, color=c, lw=1.4 if ls == "-" else 1.2, label=lab)
    a2.axhline(-3, color="0.5", ls=":", lw=0.9)
    for fx in (45.96, 54.03):
        a2.plot([fx, fx], [-40, -3], color="0.5", lw=0.7, ls=":")
    a2.annotate("−3 dB: 45.96 Hz and 54.03 Hz\n(width 8.07 Hz)", xy=(54.03, -3), xytext=(85, -14),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
    a2.set_xlim(0, 250)
    a2.set_ylim(-40, 2)
    a2.set_xlabel("frequency (Hz)")
    a2.set_ylabel("magnitude (dB)")
    a2.legend(loc="lower right", fontsize=8.5)
    a2.set_title(r"$|H(e^{j\Omega})|$, $f_s$ = 500 Sa/s", fontsize=10)
    fig.tight_layout(w_pad=1.5)
    save(fig, CH, "fig-20-6-ecg-notch-pole-zero")


if __name__ == "__main__":
    fig_20_1()
    fig_20_2()
    fig_20_3()
    fig_20_4()
    fig_20_5()
    fig_20_6()
