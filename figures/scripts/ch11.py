"""Figures for Chapter 11 — Laplace-Domain Circuit Analysis.

Run from the repository root:  python figures/scripts/ch11.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Ellipse  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")


# --------------------------------------------------------------------------- 11.1
def _terminals(d, x, ytop, ybot, xv):
    """Open terminals, V(s) polarity marks at x and the I(s) label on the top lead."""
    elm.Dot(open=True).at((x, ytop))
    elm.Dot(open=True).at((x, ybot))
    elm.Label().at((x - 0.4, ytop)).label("+", fontsize=12)
    elm.Label().at((x - 0.4, ybot)).label("−", fontsize=12)
    elm.Label().at((xv, (ytop + ybot) / 2)).label("$V(s)$", fontsize=11, halign="right")
    elm.Label().at((x + 0.3, ytop - 0.3)).label("$I(s)$", fontsize=10, halign="left")


def _series(d, x, y0, e1, e2):
    """Two elements in series hanging below the terminal at (x, y0)."""
    elm.Line().down(0.6).at((x, y0))
    a = e1().down(2.2)
    b = e2().down(2.2)
    elm.Line().down(0.6)
    yb = y0 - 0.6 - 4.4 - 0.6
    _terminals(d, x, y0, yb, x - 0.6)
    _arrow_down(x, y0)
    return a, b, yb


def _arrow_down(x, y0):
    """Small arrowhead on the top lead showing I(s) entering the + terminal."""
    elm.Arrow(headwidth=0.25, headlength=0.3).at((x, y0 - 0.05)).to((x, y0 - 0.5))


def _parallel(d, x, y0, e1, e2, w=2.4):
    """Two elements in parallel between the terminals at (x, y0) and (x, ybottom)."""
    elm.Line().down(0.6).at((x, y0))
    elm.Line().right(w / 2).at((x, y0 - 0.6))
    elm.Line().left(w / 2).at((x, y0 - 0.6))
    elm.Dot().at((x, y0 - 0.6))
    a = e1().down(4.4).at((x - w / 2, y0 - 0.6))
    b = e2().down(4.4).at((x + w / 2, y0 - 0.6))
    yj = y0 - 5.0
    elm.Line().right(w).at((x - w / 2, yj))
    elm.Dot().at((x, yj))
    elm.Line().down(0.6).at((x, yj))
    yb = yj - 0.6
    _terminals(d, x, y0, yb, x - w / 2 - 0.5)
    _arrow_down(x, y0)
    return a, b, yb


def fig_11_1():
    """s-domain models of R, L and C with initial-condition sources."""
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=11, unit=2.2, lw=1.4)
        X1, X2 = 0.0, 11.0
        EQ1, EQ2 = X1 + 2.2, X2 + 3.0
        # row 1: resistor
        Y = 0.0
        elm.Line().down(0.6).at((X1, Y))
        elm.Resistor().down(4.4).label("$R$", loc="bottom")
        elm.Line().down(0.6)
        _terminals(d, X1, Y, Y - 5.6, X1 - 0.6)
        _arrow_down(X1, Y)
        elm.Label().at((EQ1, Y - 2.8)).label("$V(s)=R\\,I(s)$", fontsize=12, halign="left")
        elm.Label().at((X1 - 2.6, Y + 0.7)).label("Resistor", fontsize=12, halign="left")
        # row 2: inductor
        Y = -8.0
        elm.Label().at((X1 - 2.6, Y + 0.7)).label("Inductor, $i_L(0^-)=I_0$", fontsize=12,
                                                  halign="left")
        # series: source L*I0 with + towards the - terminal (opposes V)
        _series(d, X1, Y, lambda: elm.Inductor2().label("$sL$", loc="bottom"),
                lambda: elm.SourceV().label("$LI_0$", loc="bottom"))
        elm.Label().at((EQ1, Y - 2.4)).label("$V(s)=sL\\,I(s)-LI_0$", fontsize=12,
                                             halign="left")
        elm.Label().at((EQ1, Y - 3.3)).label("(series form)", fontsize=10, halign="left")
        # parallel: current source I0/s in the direction of I(s)
        _parallel(d, X2, Y, lambda: elm.Inductor2().label("$sL$", loc="bottom"),
                  lambda: elm.SourceI().label("$\\dfrac{I_0}{s}$", loc="bottom"))
        elm.Label().at((EQ2, Y - 2.4)).label("$I(s)=\\dfrac{V(s)}{sL}+\\dfrac{I_0}{s}$",
                                             fontsize=12, halign="left")
        elm.Label().at((EQ2, Y - 3.5)).label("(parallel form)", fontsize=10, halign="left")
        # row 3: capacitor
        Y = -16.0
        elm.Label().at((X1 - 2.6, Y + 0.7)).label("Capacitor, $v_C(0^-)=V_0$", fontsize=12,
                                                  halign="left")
        # series: source V0/s with + towards the + terminal
        _series(d, X1, Y, lambda: elm.Capacitor().label("$\\dfrac{1}{sC}$", loc="bottom"),
                lambda: elm.SourceV().reverse().label("$\\dfrac{V_0}{s}$", loc="bottom"))
        elm.Label().at((EQ1, Y - 2.4)).label("$V(s)=\\dfrac{I(s)}{sC}+\\dfrac{V_0}{s}$",
                                             fontsize=12, halign="left")
        elm.Label().at((EQ1, Y - 3.5)).label("(series form)", fontsize=10, halign="left")
        # parallel: current source C*V0 directed against I(s)
        _parallel(d, X2, Y, lambda: elm.Capacitor().label("$sC$", loc="bottom"),
                  lambda: elm.SourceI().reverse().label("$CV_0$", loc="bottom"))
        elm.Label().at((EQ2, Y - 2.4)).label("$I(s)=sC\\,V(s)-CV_0$", fontsize=12,
                                             halign="left")
        elm.Label().at((EQ2, Y - 3.3)).label("(parallel form)", fontsize=10, halign="left")
    f = d.draw(show=False)
    f.fig.set_size_inches(6.8, 7.4)
    save(f.fig, "11", "fig-11-1-s-domain-element-models")


# --------------------------------------------------------------------------- 11.2
def fig_11_2():
    """DC-link precharge from 12 V: underdamped (10 ohm) and critically damped (20 ohm)."""
    t = np.linspace(0, 0.020, 4001)
    wd = np.sqrt(1e6 - 500 ** 2)
    vu = 48 - 36 * np.exp(-500 * t) * (np.cos(wd * t) + (500 / wd) * np.sin(wd * t))
    iu = 3600 / wd * np.exp(-500 * t) * np.sin(wd * t)
    vc = 48 - 36 * (1 + 1000 * t) * np.exp(-1000 * t)
    ic = 3600 * t * np.exp(-1000 * t)
    tm = t * 1e3
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.0), sharex=True)
    a1.plot(tm, vu, color=COLORS[0], label="$R$ = 10 Ω (ζ = 0.5)")
    a1.plot(tm, vc, color=COLORS[1], ls="--", label="$R$ = 20 Ω (critically damped)")
    a1.axhline(48, color=INK, ls=":", lw=1)
    a1.axhline(50, color=COLORS[3], ls=":", lw=1.2)
    a1.text(19.8, 47.3, "48 V final", ha="right", va="top", fontsize=8.5)
    a1.text(19.8, 50.6, "50 V capacitor rating", ha="right", va="bottom", fontsize=8.5,
            color=COLORS[3])
    tp = np.pi / wd
    vp = 48 + 36 * np.exp(-500 * tp)
    a1.plot(tp * 1e3, vp, "o", color=COLORS[0], ms=5)
    a1.annotate(f"peak {vp:.1f} V at {tp * 1e3:.2f} ms", xy=(tp * 1e3, vp),
                xytext=(5.5, 57), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    a1.text(0.4, 5.5, "$v_C(0)$ = 12 V", fontsize=8.5, va="bottom")
    a1.set_ylim(0, 60)
    a1.set_ylabel("$v_C$ (V)")
    a1.legend(loc="lower right", fontsize=8.5)
    a2.plot(tm, iu, color=COLORS[0])
    a2.plot(tm, ic, color=COLORS[1], ls="--")
    a2.axhline(0, color=INK, lw=0.5)
    tpi = np.arctan(wd / 500) / wd
    ipk = 3600 / wd * np.exp(-500 * tpi) * np.sin(wd * tpi)
    a2.plot(tpi * 1e3, ipk, "o", color=COLORS[0], ms=5)
    a2.annotate(f"peak {ipk:.2f} A at {tpi * 1e3:.2f} ms", xy=(tpi * 1e3, ipk),
                xytext=(3.2, 2.25), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    a2.plot(1.0, 3.6 * np.exp(-1), "s", color=COLORS[1], ms=5)
    a2.annotate(f"peak {3.6 * np.exp(-1):.2f} A at 1.0 ms", xy=(1.0, 3.6 * np.exp(-1)),
                xytext=(3.2, 1.25), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    a2.text(8, 1.9, "$i$ = 4.157 $e^{-500t}$ sin 866$t$  (10 Ω)\n$i$ = 3600 $t\\,e^{-1000t}$  (20 Ω)",
            fontsize=8.5, va="center")
    a2.set_ylim(-0.5, 2.5)
    a2.set_xlim(0, 20)
    a2.set_ylabel("$i$ (A)")
    a2.set_xlabel("time $t$ (ms)")
    fig.tight_layout()
    save(fig, "11", "fig-11-2-precharge-response")


# --------------------------------------------------------------------------- 11.3
def fig_11_3():
    """s-plane pole map with the impulse-response shapes each pole produces."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.08, 0.10, 0.52, 0.84])
    ax.axvspan(-3.4, 0, color=COLORS[2], alpha=0.08, lw=0)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.text(-1.0, 2.75, "stable (left half-plane)", ha="center", fontsize=8.5, color="#1B6F55")
    ax.text(0.65, 2.75, "unstable", ha="center", fontsize=8.5, color=COLORS[1])
    poles = [(-2.0, 0.0, "1"), (-0.5, 2.0, "2"), (-1.5, 1.5, "3"), (0.0, 2.0, "4"), (0.3, 1.5, "5")]
    cols = [COLORS[0], COLORS[3], COLORS[2], COLORS[4], COLORS[1]]
    for (s, w, k), c in zip(poles, cols):
        pts = [(s, w)] if w == 0 else [(s, w), (s, -w)]
        for (x, y) in pts:
            ax.plot(x, y, "x", color=c, ms=10, mew=2.2)
        ax.text(s + 0.12, w + 0.12, k, fontsize=9, color="white", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.15", fc=c, ec="none"))
    ax.set_xlim(-3.4, 1.4)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xlabel("$\\sigma$ (normalised)")
    ax.set_ylabel("$j\\omega$ (normalised)")
    ax.set_xticks([-3, -2, -1, 0, 1])
    # secondary inset: precharge poles
    ins = ax.inset_axes([0.03, 0.03, 0.33, 0.33])
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
    ins.plot(1000 * np.cos(th), 1000 * np.sin(th), color=INK, lw=0.8)
    ins.plot([0, -1000 * np.cos(np.radians(60))], [0, 1000 * np.sin(np.radians(60))], color=INK,
             ls="--", lw=0.8)
    ins.plot([0, -1000 * np.cos(np.radians(60))], [0, -1000 * np.sin(np.radians(60))], color=INK,
             ls="--", lw=0.8)
    ins.plot([-500, -500], [866, -866], "x", color=COLORS[0], ms=6, mew=1.6)
    ins.axhline(0, color=INK, lw=0.5)
    ins.axvline(0, color=INK, lw=0.5)
    ins.set_xlim(-1250, 950)
    ins.set_ylim(-1300, 1350)
    ins.set_aspect("equal")
    ins.set_xticks([])
    ins.set_yticks([])
    ins.set_facecolor("white")
    ins.text(-460, 1040, "−500 + j866", fontsize=6.5, va="bottom")
    ins.text(60, 300, "ζ = 0.5\n(60°)", fontsize=6.5)
    ins.text(-1220, -1220, "$\\omega_0$ = 1000 rad/s", fontsize=6.5, va="bottom")
    ins.set_title("precharge poles (rad/s)", fontsize=7, pad=2)
    # impulse-response sketches
    t = np.linspace(0, 10, 600)
    names = ["decaying exponential", "long ringing", "short ringing", "constant oscillation",
             "growing oscillation"]
    for idx, ((s, w, k), c, nm) in enumerate(zip(poles, cols, names)):
        b = fig.add_axes([0.70, 0.80 - idx * 0.175, 0.27, 0.13])
        h = np.exp(s * t) * (np.sin(w * t) if w else 1.0)
        b.plot(t, h, color=c, lw=1.4)
        b.axhline(0, color=INK, lw=0.5)
        b.set_xlim(0, 10)
        b.set_xticks([0, 5, 10] if idx == 4 else [])
        b.set_yticks([])
        b.spines["left"].set_visible(False)
        if idx < 4:
            b.spines["bottom"].set_visible(False)
        m = np.max(np.abs(h))
        b.set_ylim(-1.1 * m, 1.1 * m)
        lab = (f"$p$ = {s:g}" if w == 0 else f"$p$ = {s:g} ± j{w:g}").replace("-", "−")
        b.set_title(f"({k}) {nm}:  {lab}", fontsize=7.5, loc="left", pad=2, color=c)
        if idx == 4:
            b.set_xlabel("$t$ (normalised)", fontsize=8)
            b.tick_params(labelsize=7.5)
    fig.text(0.835, 0.965, "impulse response $h(t)$", ha="center", fontsize=9)
    save(fig, "11", "fig-11-3-s-plane-pole-map")


# --------------------------------------------------------------------------- 11.4
def fig_11_4():
    """Two-section RC ladder: poles and step response versus a single section."""
    tau = 1e-4
    p1 = (-3 + np.sqrt(5)) / (2 * tau)
    p2 = (-3 - np.sqrt(5)) / (2 * tau)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1, 1.3]))
    a1.axhline(0, color=INK, lw=0.8)
    a1.axvline(0, color=INK, lw=0.8)
    a1.plot([p1, p2], [0, 0], "x", color=COLORS[0], ms=11, mew=2.4, label="ladder: −3820, −26 180")
    a1.plot(-1e4, 0.42, "x", color="#888888", ms=10, mew=2.0, label="single section: −10 000")
    a1.plot([-1e4, -1e4], [-0.42, -0.42], "x", color=COLORS[1], ms=10, mew=2.0)
    a1.plot(-1e4 + 500, -0.42, "x", color=COLORS[1], ms=10, mew=2.0,
            label="two isolated sections:\ndouble pole at −10 000")
    a1.add_patch(Ellipse((-1e4 + 250, -0.42), 3000, 0.36, fc="none", ec=COLORS[1], ls="--", lw=1.0))
    a1.text(p1, 0.15, "−3820", ha="center", va="bottom", fontsize=8, color=COLORS[0])
    a1.text(p2, 0.15, "−26 180", ha="center", va="bottom", fontsize=8, color=COLORS[0])
    a1.set_xlim(-30000, 1500)
    a1.set_ylim(-1.6, 1.6)
    a1.set_yticks([])
    a1.set_xticks([-30000, -20000, -10000, 0])
    a1.set_xticklabels(["−30 000", "−20 000", "−10 000", "0"], fontsize=8)
    a1.set_xlabel("$\\sigma$ (rad/s)")
    a1.set_ylabel("$j\\omega$")
    a1.legend(loc="upper left", fontsize=7.3, bbox_to_anchor=(0.0, 1.02))
    a1.set_title("pole positions", fontsize=9.5)
    t = np.linspace(0, 2e-3, 4001)
    ylad = 1 - 1.1708 * np.exp(p1 * t) + 0.1708 * np.exp(p2 * t)
    ys = 1 - np.exp(-t / tau)
    yi = 1 - (1 + t / tau) * np.exp(-t / tau)
    tm = t * 1e3
    a2.plot(tm, ylad, color=COLORS[0], label="ladder (loaded)")
    a2.plot(tm, ys, color="#777777", ls="--", label="single section")
    a2.plot(tm, yi, color=COLORS[1], ls=":", lw=2.0, label="two isolated sections")
    f = lambda x: 1 - 1.1708 * np.exp(p1 * x) + 0.1708 * np.exp(p2 * x)  # noqa: E731
    t10 = brentq(lambda x: f(x) - 0.1, 1e-7, 1e-3)
    t90 = brentq(lambda x: f(x) - 0.9, 1e-5, 2e-3)
    for lvl in (0.1, 0.9):
        a2.axhline(lvl, color=INK, lw=0.6, ls=":")
        a2.text(1.98, lvl + 0.015, f"{lvl * 100:.0f} %", ha="right", va="bottom", fontsize=8)
    for tt in (t10, t90):
        a2.plot([tt * 1e3] * 2, [0, f(tt)], color=COLORS[0], lw=0.7)
    a2.annotate("", xy=(t90 * 1e3, 0.04), xytext=(t10 * 1e3, 0.04),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=COLORS[0], mutation_scale=8,
                                shrinkA=0, shrinkB=0))
    a2.text(t90 * 1e3 + 0.04, 0.04, f"rise time {(t90 - t10) * 1e3:.2f} ms", ha="left",
            va="bottom", fontsize=8, color=COLORS[0])
    a2.set_xlim(0, 2)
    a2.set_ylim(0, 1.1)
    a2.set_xlabel("time $t$ (ms)")
    a2.set_ylabel("$v_o$ (V)  for a 1 V step")
    a2.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.18))
    a2.set_title("step response", fontsize=9.5)
    fig.tight_layout()
    save(fig, "11", "fig-11-4-rc-ladder-poles-step")


# --------------------------------------------------------------------------- 11.5
def fig_11_5():
    """Energising R = 1 ohm, L = 31.8 mH at a voltage zero on 230 V, 50 Hz."""
    R, w = 1.0, 2 * np.pi * 50
    L = 10 / w
    tau = L / R
    Z = np.hypot(R, w * L)
    phi = np.arctan(w * L / R)
    Im = 325.3 / Z
    k = 325.3 * w * L / Z ** 2
    t = np.linspace(0, 0.1, 10001)
    iss = Im * np.sin(w * t - phi)
    itr = k * np.exp(-t / tau)
    i = iss + itr
    v = 325.3 * np.sin(w * t)
    fig, ax = new_fig(6.6, 4.0)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(t * 1e3, v, color="#AAAAAA", lw=0.9, label="supply voltage (right axis)")
    ax2.set_ylim(-325 * 40 / 60 * 1.5, 325 * 1.5)
    ax2.set_ylim(-325, 325 * 60 / 40)
    ax2.set_ylabel("voltage (V)", color="#777777")
    ax.plot(t * 1e3, iss, color=COLORS[0], ls="--", lw=1.3,
            label=f"steady state {Im:.2f} sin(ωt − {np.degrees(phi):.2f}°)")
    ax.plot(t * 1e3, itr, color=COLORS[1], ls=":", lw=1.8,
            label=f"transient {k:.2f} e$^{{-t/{tau * 1e3:.2f}\\,\\mathrm{{ms}}}}$")
    ax.plot(t * 1e3, i, color=INK, lw=2.0, label="total current")
    j = np.argmax(i)
    ax.plot(t[j] * 1e3, i[j], "o", color=INK, ms=5)
    ax.annotate(f"first peak {i[j]:.1f} A\nat {t[j] * 1e3:.2f} ms", xy=(t[j] * 1e3, i[j]),
                xytext=(16, 55), fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(-40, 60)
    ax.set_xlabel("time $t$ (ms)")
    ax.set_ylabel("current (A)")
    ax.text(99, 59, "switching at θ = 84.3° (near a voltage peak)\ngives no transient term",
            ha="right", va="top", fontsize=8.5,
            bbox=dict(fc="white", ec="#BBBBBB", lw=0.6, boxstyle="round,pad=0.3"))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
              fontsize=8)
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    save(fig, "11", "fig-11-5-rl-ac-energisation")


if __name__ == "__main__":
    fig_11_1()
    fig_11_2()
    fig_11_3()
    fig_11_4()
    fig_11_5()
