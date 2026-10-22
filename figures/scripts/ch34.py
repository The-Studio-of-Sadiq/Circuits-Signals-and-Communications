"""Figures for Chapter 34 — Feedback and Stability.

Run from the repository root:  python figures/scripts/ch34.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Arc  # noqa: E402
from scipy import signal  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402


# ---------------------------------------------------------------------------
# block-diagram helpers
def sj(ax, x, y, r=0.22, signs=None, fs=8):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    off = {"w": (-r - 0.07, r * 0.8), "s": (r * 0.85, -r - 0.1), "n": (r * 0.85 + 0.1, r + 0.08),
           "e": (r + 0.07, r * 0.8)}
    for pos, sg in (signs or {}).items():
        dx, dy = off[pos]
        ax.text(x + dx, y + dy, sg, fontsize=fs + 1, ha="center", va="center")


def blk(ax, xc, yc, w, h, text, fs=9, fc="#EEF3F8"):
    box(ax, xc - w / 2, yc - h / 2, w, h, text, fontsize=fs, fc=fc)


def line(ax, pts, color=INK, lw=1.1, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-2],), ys[:-1] + (ys[-2],), color=color, lw=lw, ls=ls)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10,
                                shrinkA=0, shrinkB=0))


def dot(ax, x, y):
    ax.plot(x, y, "o", color=INK, ms=3.5, zorder=4)


def lab(ax, x, y, t, fs=9, **kw):
    kw.setdefault("ha", "center")
    kw.setdefault("va", "bottom")
    ax.text(x, y, t, fontsize=fs, **kw)


# servo loop L(s) = K / [s (s+1)(s+5)]
DEN_OL = [1, 6, 5, 0]


def Ljw(K, w):
    s = 1j * w
    return K / (s * (s + 1) * (s + 5))


# ---------------------------------------------------------------------------
def fig_open_closed():
    """Fig 34.1: open-loop and closed-loop structures."""
    fig, ax = schematic(6.8, 4.6, xlim=(0, 13.6), ylim=(0, 9.2))
    grey = "0.35"
    # ---- open loop (top)
    y = 7.4
    ax.text(0.1, 8.85, "Open loop", fontsize=10, weight="bold", va="center")
    line(ax, [(0.3, y), (2.3, y)])
    lab(ax, 1.0, y + 0.1, "$r$")
    lab(ax, 1.0, y - 0.55, "reference", fs=7.5, color=grey)
    blk(ax, 3.1, y, 1.6, 0.85, "$C(s)$", fs=10)
    line(ax, [(3.9, y), (5.6, y)])
    lab(ax, 4.75, y + 0.1, "$u$")
    blk(ax, 6.4, y, 1.6, 0.85, "$G(s)$", fs=10)
    line(ax, [(7.2, y), (8.88, y)])
    sj(ax, 9.1, y, signs={"w": "+", "n": "+"})
    blk(ax, 9.1, y + 1.05, 1.2, 0.6, "$G_d(s)$", fs=9)
    line(ax, [(9.1, y + 0.75), (9.1, y + 0.22)])
    line(ax, [(10.3, y + 1.05), (9.7, y + 1.05)])
    lab(ax, 10.6, y + 0.95, "$d$", ha="left")
    lab(ax, 10.95, y + 0.95, "disturbance", fs=7.5, color=grey, ha="left")
    line(ax, [(9.32, y), (11.4, y)])
    lab(ax, 10.6, y + 0.1, "$y$")
    ax.text(11.6, y, "$Y=CGR+G_dD$", fontsize=9, va="center")

    ax.plot([0.2, 13.4], [5.85, 5.85], color=GRID, lw=0.8)
    # ---- closed loop (bottom)
    y = 3.9
    ax.text(0.1, 5.45, "Closed loop", fontsize=10, weight="bold", va="center")
    line(ax, [(0.3, y), (1.38, y)])
    lab(ax, 0.75, y + 0.1, "$r$")
    lab(ax, 0.75, y - 0.55, "reference", fs=7.5, color=grey)
    sj(ax, 1.6, y, signs={"w": "+", "s": "−"})
    line(ax, [(1.82, y), (3.0, y)])
    lab(ax, 2.4, y + 0.1, "$e$")
    lab(ax, 2.4, y - 0.55, "error", fs=7.5, color=grey)
    blk(ax, 3.8, y, 1.6, 0.85, "$C(s)$", fs=10)
    line(ax, [(4.6, y), (6.0, y)])
    lab(ax, 5.3, y + 0.1, "$u$")
    lab(ax, 5.3, y - 0.55, "control", fs=7.5, color=grey)
    blk(ax, 6.8, y, 1.6, 0.85, "$G(s)$", fs=10)
    ax.text(6.8, y + 0.5, "plant", fontsize=7.5, color=grey, ha="center", va="bottom")
    line(ax, [(7.6, y), (8.88, y)])
    sj(ax, 9.1, y, signs={"w": "+", "n": "+"})
    blk(ax, 9.1, y + 1.05, 1.2, 0.6, "$G_d(s)$", fs=9)
    line(ax, [(9.1, y + 0.75), (9.1, y + 0.22)])
    line(ax, [(10.3, y + 1.05), (9.7, y + 1.05)])
    lab(ax, 10.6, y + 0.95, "$d$", ha="left")
    lab(ax, 10.95, y + 0.95, "disturbance", fs=7.5, color=grey, ha="left")
    line(ax, [(9.32, y), (12.6, y)])
    lab(ax, 11.9, y + 0.1, "$y$")
    lab(ax, 11.9, y - 0.55, "output", fs=7.5, color=grey)
    dot(ax, 11.0, y)
    # feedback path through sensor H(s), noise n added at sensor output
    yf = 1.45
    line(ax, [(11.0, y), (11.0, yf), (8.0, yf)])
    blk(ax, 7.2, yf, 1.6, 0.8, "$H(s)$", fs=10)
    ax.text(7.2, yf - 0.62, "sensor", fontsize=7.5, color=grey, ha="center", va="top")
    line(ax, [(6.4, yf), (4.12, yf)])
    sj(ax, 3.9, yf, signs={"e": "+", "s": "+"})
    line(ax, [(3.9, 0.35), (3.9, yf - 0.22)])
    lab(ax, 4.1, 0.25, "$n$  measurement noise", fs=8.5, ha="left", va="bottom")
    line(ax, [(3.68, yf), (1.6, yf), (1.6, y - 0.22)])
    # dashed loop arrow circulating inside the loop
    cx, cy, rx, ry = 6.6, 2.62, 3.6, 0.42
    th = np.linspace(np.radians(160), np.radians(160 - 340), 200)
    ax.plot(cx + rx * np.cos(th), cy + ry * np.sin(th), "--", color=COLORS[0], lw=1.1)
    ax.annotate("", xy=(cx + rx * np.cos(th[-1]), cy + ry * np.sin(th[-1])),
                xytext=(cx + rx * np.cos(th[-4]), cy + ry * np.sin(th[-4])),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.1, mutation_scale=10))
    ax.text(cx, cy, "loop transfer function  $L(s)=C(s)G(s)H(s)$", fontsize=8.5, color=COLORS[0],
            ha="center", va="center")
    return save(fig, "34", "fig-34-1-open-closed-loop")


# ---------------------------------------------------------------------------
def fig_pole_locations():
    """Fig 34.2: pole positions in the s-plane and their impulse responses."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.30, 0.12, 0.40, 0.76])
    ax.axvspan(-3, 0, color=COLORS[2], alpha=0.08, lw=0)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    r = np.linspace(0, 3.6, 2)
    for sg in (1, -1):
        ax.plot(-r * np.cos(np.radians(60)), sg * r * np.sin(np.radians(60)), "--", color="0.5", lw=0.9)
    ax.text(-1.95, 2.7, "$\\zeta=0.5$", fontsize=8.5, color="0.35", ha="right", va="center")
    ax.text(-2.9, -2.85, "stable (LHP)", fontsize=9, color=COLORS[2], ha="left", va="bottom")
    ax.text(0.95, -2.85, "unstable", fontsize=9, color=COLORS[1], ha="right", va="bottom")
    poles = [(-2, 0, "a"), (-0.5, 2, "b"), (0, 2, "c"), (0.5, 2, "d"), (0.5, 0, "e")]
    for (sr, si, k) in poles:
        ax.plot(sr, si, "x", color=INK, ms=8, mew=2)
        if si:
            ax.plot(sr, -si, "x", color=INK, ms=8, mew=2)
        ax.text(sr + 0.08, si + 0.12, k, fontsize=9, weight="bold", color=COLORS[0])
    ax.set_xlim(-3, 1)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("$\\sigma$ (s$^{-1}$)")
    ax.set_ylabel("$j\\omega$ (rad/s)")
    ax.set_aspect("equal")
    ax.grid(True, color=GRID, lw=0.5)
    ax.set_title("s-plane", fontsize=10)
    # insets
    t = np.linspace(0, 10, 1001)
    resp = {"a": (np.exp(-2 * t), "real pole −2: monotonic decay"),
            "b": (np.exp(-0.5 * t) * np.sin(2 * t), "−0.5 ± j2: decaying oscillation"),
            "c": (np.sin(2 * t), "± j2: sustained oscillation"),
            "d": (np.exp(0.5 * t) * np.sin(2 * t), "+0.5 ± j2: growing oscillation"),
            "e": (np.exp(0.5 * t), "real pole +0.5: exponential growth")}
    pos = {"a": [0.02, 0.10, 0.24, 0.20], "b": [0.02, 0.62, 0.24, 0.20],
           "c": [0.74, 0.70, 0.24, 0.17], "d": [0.74, 0.41, 0.24, 0.17], "e": [0.74, 0.12, 0.24, 0.17]}
    for k, (yv, title) in resp.items():
        a = fig.add_axes(pos[k])
        a.plot(t, yv, color=COLORS[1 if k in "de" else 0], lw=1.3)
        a.axhline(0, color="0.6", lw=0.6)
        a.set_xlim(0, 10)
        a.set_xticks([0, 5, 10])
        a.set_yticks([])
        a.tick_params(labelsize=7)
        a.set_title(f"({k}) {title}", fontsize=7.5, loc="left")
        if k in ("a", "e"):
            a.set_xlabel("t (s)", fontsize=7.5, labelpad=1)
        for sp in ("left",):
            a.spines[sp].set_color("0.6")
    return save(fig, "34", "fig-34-2-pole-locations")


# ---------------------------------------------------------------------------
def fig_root_locus():
    """Fig 34.3: root locus of K/[s(s+1)(s+5)]."""
    fig, ax = new_fig(6.4, 4.2)
    Ks = np.concatenate([np.linspace(0, 1.128, 400), np.geomspace(1.1281, 2000, 4000)])
    roots = np.array([np.sort_complex(np.roots([1, 6, 5, K])) for K in Ks])
    # track branches by continuity
    br = [roots[0].copy()]
    for rr in roots[1:]:
        prev = br[-1]
        used = []
        new = np.empty(3, complex)
        for i in range(3):
            d = np.abs(rr - prev[i])
            for u in used:
                d[u] = np.inf
            j = int(np.argmin(d))
            used.append(j)
            new[i] = rr[j]
        br.append(new)
    br = np.array(br)
    for i in range(3):
        ax.plot(br[:, i].real, br[:, i].imag, color=COLORS[0], lw=2.0, zorder=3)
    # asymptotes
    for ang in (60, -60, 180):
        rr = np.linspace(0, 8, 2)
        ax.plot(-2 + rr * np.cos(np.radians(ang)), rr * np.sin(np.radians(ang)), "--", color="0.55", lw=0.9)
    ax.plot(-2, 0, "+", color="0.4", ms=8)
    ax.text(-2.2, -0.12, "centroid −2", fontsize=8, color="0.35", ha="right", va="top")
    ax.text(-0.65, 3.85, "asymptote ±60°", fontsize=8, color="0.35", ha="left", va="top")
    # zeta = 0.5 ray
    rr = np.linspace(0, 4.5, 2)
    ax.plot(rr * np.cos(np.radians(120)), rr * np.sin(np.radians(120)), ":", color=COLORS[2], lw=1.4)
    ax.text(-2.2, 3.55, "$\\zeta=0.5$", fontsize=8.5, color=COLORS[2], ha="right")
    # open-loop poles
    for p in (0, -1, -5):
        ax.plot(p, 0, "x", color=INK, ms=9, mew=2, zorder=5)
    # breakaway
    ax.plot(-0.4725, 0, "o", mfc="white", mec=INK, ms=6, zorder=5)
    ax.annotate("breakaway −0.4725\n$K=1.128$", xy=(-0.4725, 0), xytext=(-3.3, -1.5), fontsize=8,
                ha="center", arrowprops=dict(arrowstyle="-", lw=0.6))
    # zeta=0.5 point
    for sg in (1, -1):
        ax.plot(-0.417, sg * 0.722, "s", color=COLORS[2], ms=5, zorder=5)
    ax.annotate("$-0.417\\pm j0.722$\n$K=3.59$", xy=(-0.417, 0.722), xytext=(-3.6, 1.45), fontsize=8,
                ha="center", color=COLORS[2], arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[2]))
    # imaginary axis crossing
    for sg in (1, -1):
        ax.plot(0, sg * 2.236, "D", color=COLORS[1], ms=5, zorder=5)
    ax.text(0.15, 2.236, "$\\pm j2.236$, $K=30$", fontsize=8, color=COLORS[1], va="center")
    # K = 10 poles
    p10 = np.roots([1, 6, 5, 10])
    for p in p10:
        ax.plot(p.real, p.imag, "o", color=COLORS[3], ms=6, zorder=6)
    ax.annotate("$K=10$: $-0.291\\pm j1.327$", xy=(-0.291, 1.327), xytext=(0.15, 1.2), fontsize=8,
                color=COLORS[3], va="center")
    ax.annotate("$K=10$: $-5.418$", xy=(-5.418, 0), xytext=(-6.4, 0.6), fontsize=8, color=COLORS[3],
                ha="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[3]))
    ax.axhline(0, color=INK, lw=0.6)
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlim(-8, 2)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.set_xlabel("$\\sigma$ (s$^{-1}$)")
    ax.set_ylabel("$j\\omega$ (rad/s)")
    ax.grid(True, color=GRID, lw=0.5)
    return save(fig, "34", "fig-34-3-root-locus-servo")


# ---------------------------------------------------------------------------
def _margins(K):
    w = np.logspace(-3, 2, 200001)
    L = Ljw(K, w)
    mag = np.abs(L)
    ph = np.degrees(np.unwrap(np.angle(L)))
    i = np.argmin(np.abs(mag - 1))
    j = np.argmin(np.abs(ph + 180))
    return w[i], 180 + ph[i], w[j], -20 * np.log10(mag[j])


def fig_bode():
    """Fig 34.4: Bode plot with margins for K = 10 and K = 3.588."""
    fig, (am, ap) = plt.subplots(2, 1, figsize=(6.4, 5.2), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.15, 1], hspace=0.08))
    w = np.logspace(-2, 2, 2000)
    for K, ls, col in ((10, "-", COLORS[0]), (3.588, "--", COLORS[1])):
        L = Ljw(K, w)
        am.semilogx(w, 20 * np.log10(np.abs(L)), ls, color=col, label=f"$K={K:g}$")
    ph = np.degrees(np.unwrap(np.angle(Ljw(1, w))))
    ap.semilogx(w, ph, color=INK, label="phase (same for both gains)")
    am.axhline(0, color="0.4", lw=0.8)
    ap.axhline(-180, color="0.4", lw=0.8)
    for wc in (1, 5):
        for a in (am, ap):
            a.axvline(wc, color="0.75", lw=0.8, ls=":")
    am.text(1.0, -97, "1 rad/s ", fontsize=7.5, color="0.4", va="bottom", ha="right")
    am.text(5.0, -97, " 5 rad/s", fontsize=7.5, color="0.4", va="bottom", ha="left")
    am.text(0.035, 31, "−20 dB/dec", fontsize=8, rotation=-14)
    am.text(1.45, -52, "−40 dB/dec", fontsize=8, rotation=-28, ha="center")
    am.text(13, -42, "−60 dB/dec", fontsize=8, rotation=-36)
    wc, pm, w180, gm = _margins(10)
    wc2, pm2, _, gm2 = _margins(3.588)
    # gain margins at the phase crossover
    am.axvline(w180, color="0.55", lw=0.8, ls="--")
    for xo, g, col in ((w180 * 0.96, gm, COLORS[0]), (w180 * 1.04, gm2, COLORS[1])):
        am.annotate("", xy=(xo, 0), xytext=(xo, -g),
                    arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.1, mutation_scale=8,
                                    shrinkA=0, shrinkB=0))
    am.text(3.0, 16, f"GM {gm:.1f} dB ($K=10$)", fontsize=7.8, color=COLORS[0], ha="left")
    am.text(3.0, 4, f"GM {gm2:.1f} dB ($K=3.588$)", fontsize=7.8, color=COLORS[1], ha="left")
    am.text(w180 * 1.05, 42, f"$\\omega_{{180}}$ = {w180:.3f}", fontsize=7.8, color="0.3", ha="left")
    am.plot([wc], [0], "o", color=COLORS[0], ms=4, zorder=5)
    am.plot([wc2], [0], "o", color=COLORS[1], ms=4, zorder=5)
    # phase margins at the gain crossovers
    ap.axvline(w180, color="0.55", lw=0.8, ls="--")
    ap.plot([w180], [-180], "o", color=INK, ms=4)
    for x, p, col in ((wc, pm, COLORS[0]), (wc2, pm2, COLORS[1])):
        ap.annotate("", xy=(x, -180 + p), xytext=(x, -180),
                    arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.1, mutation_scale=8,
                                    shrinkA=0, shrinkB=0))
    ap.text(wc2 * 0.88, -152, f"PM {pm2:.1f}°\n$\\omega_c$ = {wc2:.3f}", fontsize=7.6, color=COLORS[1],
            ha="right", va="center")
    ap.text(wc * 0.92, -188, f"PM {pm:.1f}°, $\\omega_c$ = {wc:.2f}", fontsize=7.6, color=COLORS[0],
            ha="right", va="top")
    am.set_ylim(-100, 60)
    am.set_ylabel("|L| (dB)")
    am.grid(True, which="both", color=GRID, lw=0.5)
    am.legend(loc="lower left", fontsize=8.5)
    ap.set_ylim(-270, -90)
    ap.set_yticks([-270, -225, -180, -135, -90])
    ap.set_ylabel("∠L (degrees)")
    ap.set_xlabel("Frequency ω (rad/s)")
    ap.set_xlim(0.01, 100)
    ap.grid(True, which="both", color=GRID, lw=0.5)
    ap.legend(loc="lower left", fontsize=8)
    print(f"  34.4 K=10: wc {wc:.3f} PM {pm:.2f} w180 {w180:.3f} GM {gm:.2f}; K=3.588: wc {wc2:.3f} PM {pm2:.2f} GM {gm2:.2f}")
    return save(fig, "34", "fig-34-4-bode-margins-servo")


# ---------------------------------------------------------------------------
def fig_nyquist():
    """Fig 34.5: Nyquist plots of the servo (K = 10) and of K/[(s-1)(s+2)]."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    w = np.geomspace(0.05, 200, 6000)
    L = Ljw(10, w)
    a1.plot(L.real, L.imag, color=COLORS[0], label="ω > 0")
    a1.plot(L.real, -L.imag, "--", color=COLORS[0], lw=1.0, alpha=0.6, label="ω < 0 (mirror)")
    th = np.linspace(0, 2 * np.pi, 400)
    a1.plot(np.cos(th), np.sin(th), ":", color="0.45", lw=1.0)
    a1.axvline(-2.4, color="0.6", lw=0.8, ls="-.")
    a1.text(-2.33, -1.0, "asymptote\nRe = −2.4", fontsize=7.5, color="0.35", ha="left", va="center")
    a1.plot(-1, 0, "x", color=COLORS[1], ms=9, mew=2, zorder=6)
    a1.text(-1.07, -0.07, "−1", fontsize=9, color=COLORS[1], ha="right", va="top")
    a1.plot(-1 / 3, 0, "o", color=INK, ms=4, zorder=6)
    a1.annotate("−0.333 at ω = 2.236\nGM = 1/0.333 = 3", xy=(-1 / 3, 0), xytext=(0.45, -1.45), fontsize=7.5,
                ha="right", va="top", arrowprops=dict(arrowstyle="-", lw=0.6))
    wc = 1.2271
    Lc = Ljw(10, wc)
    a1.plot(Lc.real, Lc.imag, "o", color=COLORS[2], ms=5, zorder=6)
    a1.plot([0, Lc.real], [0, Lc.imag], color=COLORS[2], lw=0.9)
    pm = np.degrees(np.angle(Lc)) + 180
    a1.add_patch(Arc((0, 0), 1.3, 1.3, theta1=180, theta2=180 + pm, color=COLORS[2], lw=1.3))
    a1.annotate(f"PM {pm:.1f}° at ω = 1.23\n(|L| = 1)", xy=(-0.64, -0.14), xytext=(-1.3, -0.33), fontsize=7.5, color=COLORS[2], ha="right", va="center", arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[2]))

    # direction arrow
    k = np.argmin(np.abs(w - 1.6))
    a1.annotate("", xy=(L.real[k + 40], L.imag[k + 40]), xytext=(L.real[k], L.imag[k]),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=1.2, mutation_scale=11))
    a1.set_xlim(-3, 0.5)
    a1.set_ylim(-2.5, 0.5)
    a1.set_aspect("equal")
    a1.axhline(0, color=INK, lw=0.6)
    a1.axvline(0, color=INK, lw=0.6)
    a1.grid(True, color=GRID, lw=0.5)
    a1.set_xlabel("Re L(jω)")
    a1.set_ylabel("Im L(jω)")
    a1.set_title("(a) $10/[s(s+1)(s+5)]$: stable", fontsize=9.5)
    a1.legend(loc="lower right", fontsize=7.5)

    w = np.concatenate([np.linspace(0, 1, 400), np.geomspace(1.0001, 500, 4000)])
    for K, col in ((1, COLORS[1]), (4, COLORS[0])):
        s = 1j * w
        L = K / ((s - 1) * (s + 2))
        a2.plot(L.real, L.imag, color=col, label=f"$K={K}$")
        a2.plot(L.real, -L.imag, "--", color=col, lw=1.0, alpha=0.7)
        for kk in (int(len(w) * 0.12), ):
            a2.annotate("", xy=(L.real[kk + 30], L.imag[kk + 30]), xytext=(L.real[kk], L.imag[kk]),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2, mutation_scale=11))
            a2.annotate("", xy=(L.real[kk + 30], -L.imag[kk + 30]), xytext=(L.real[kk], -L.imag[kk]),
                        arrowprops=dict(arrowstyle="<|-", color=col, lw=1.0, mutation_scale=10))
        a2.plot(-K / 2, 0, "o", color=col, ms=4)
    a2.plot(-1, 0, "x", color=INK, ms=9, mew=2, zorder=6)
    a2.text(-1.0, 0.08, "−1", fontsize=9, ha="center", va="bottom")
    a2.text(-0.6, -0.04, "−0.5", fontsize=7.5, color=COLORS[1], ha="right", va="top")
    a2.text(-2.06, -0.05, "−2", fontsize=7.5, color=COLORS[0], ha="right", va="top")
    a2.text(-2.45, 0.95, "$K=4$: one CCW encirclement,\n$N=-1$, $Z=N+P=0$ → stable", fontsize=7.5,
            color=COLORS[0], ha="left", va="top")
    a2.text(-2.45, -0.62, "$K=1$: no encirclement,\n$Z=P=1$ → unstable", fontsize=7.5,
            color=COLORS[1], ha="left", va="top")
    a2.set_xlim(-2.5, 0.5)
    a2.set_ylim(-1.1, 1.1)
    a2.set_aspect("equal")
    a2.axhline(0, color=INK, lw=0.6)
    a2.axvline(0, color=INK, lw=0.6)
    a2.grid(True, color=GRID, lw=0.5)
    a2.set_xlabel("Re L(jω)")
    a2.set_title("(b) $K/[(s-1)(s+2)]$, $P=1$", fontsize=9.5)
    a2.legend(loc="lower right", fontsize=7.5)
    fig.tight_layout()
    return save(fig, "34", "fig-34-5-nyquist-plots")


# ---------------------------------------------------------------------------
def fig_steps():
    """Fig 34.6: closed-loop step responses for K = 1.128, 3.588, 10, 30."""
    fig, ax = new_fig(6.4, 4.2)
    t = np.linspace(0, 20, 20001)
    ax.axhspan(0.98, 1.02, color="0.8", alpha=0.6, lw=0)
    ax.axhline(1.0, color="0.4", lw=0.8, ls="--")
    wb = dict(fc="white", ec="none", pad=0.6, alpha=0.9)
    cases = [(30, 0.0, "0.6"), (1.128, 75.1, COLORS[2]), (3.588, 51.7, COLORS[0]), (10, 25.4, COLORS[1])]
    handles = {}
    for K, pm, col in cases:
        _, y = signal.step(([K], [1, 6, 5, K]), T=t)
        os_ = (y.max() - 1) * 100
        out = np.where(np.abs(y - 1) > 0.02)[0]
        ts = t[out[-1]] if len(out) else 0
        h, = ax.plot(t, y, color=col, lw=1.0 if K == 30 else 1.9, zorder=2 if K == 30 else 3,
                     label=f"$K={K:g}$, PM {pm:g}°")
        handles[K] = h
        print(f"  34.6 K={K}: OS {os_:.1f}% peak {t[y.argmax()]:.2f}s ts {ts:.1f}s")
        if K in (3.588, 10):
            ip = y.argmax()
            xt, yt = (6.3, 1.40) if K == 3.588 else (3.6, 1.68)
            ax.annotate(f"{os_:.1f} % at {t[ip]:.1f} s", xy=(t[ip], y[ip]), xytext=(xt, yt), fontsize=8,
                        color=col, bbox=wb, arrowprops=dict(arrowstyle="-", lw=0.7, color=col))
            ax.plot([ts, ts], [0, 0.98], ":", color=col, lw=1.0)
            ax.text(ts + 0.12, 0.2 if K == 3.588 else 0.35, f"$t_s$ = {ts:.1f} s", fontsize=7.8, color=col,
                    bbox=wb)
        if K == 1.128:
            ax.text(14.3, 0.80, f"no overshoot,\n$t_s$ ≈ {ts:.1f} s", fontsize=7.8, color=col, va="top", bbox=wb)
    ax.text(19.9, 2.02, "$K=30$: sustained oscillation, period 2.81 s", fontsize=7.8, color="0.35",
            ha="right", va="bottom", bbox=wb)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 2.2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output $y(t)$")
    ax.grid(True, color=GRID, lw=0.5)
    ax.legend(handles=[handles[k] for k in (1.128, 3.588, 10, 30)], loc="lower center",
              bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=7.8, handlelength=1.5, columnspacing=1.0)
    return save(fig, "34", "fig-34-6-servo-step-responses")


if __name__ == "__main__":
    fig_open_closed()
    fig_pole_locations()
    fig_root_locus()
    fig_bode()
    fig_nyquist()
    fig_steps()
