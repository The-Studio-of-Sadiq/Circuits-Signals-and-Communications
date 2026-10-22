"""Figures for Chapter 9 — AC Power.

Run from the repository root:  python figures/scripts/ch09.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK  # noqa: E402

F = 50.0
W = 2 * np.pi * F


def _vec(ax, x0, y0, x1, y1, color, lw=2.0, ls="-", ms=14):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def fig_9_1():
    """v, i and p(t) of the compressor (230 V, 23 A, pf 0.8 lagging)."""
    V, I, phi = 230.0, 23.0, np.arccos(0.8)
    t = np.linspace(0, 0.020, 4001)
    v = np.sqrt(2) * V * np.cos(W * t)
    i = np.sqrt(2) * I * np.cos(W * t - phi)
    p = v * i
    P, Q = V * I * np.cos(phi), V * I * np.sin(phi)
    pa = P * (1 + np.cos(2 * W * t))
    pr = Q * np.sin(2 * W * t)
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(6.6, 5.0), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1, 1.5]))
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    tm = t * 1e3
    ax.plot(tm, v, color=COLORS[0], lw=1.5, label="$v(t)$")
    ax2.plot(tm, i, color=COLORS[1], lw=1.5, label="$i(t)$")
    ax.set_ylim(-400, 400)
    ax2.set_ylim(-40, 40)
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_ylabel("voltage (V)", color=COLORS[0])
    ax2.set_ylabel("current (A)", color=COLORS[1])
    ax.text(7.2, 330, "$v$ = 325.3 cos ωt  (V)", color=COLORS[0], fontsize=8.5, va="center")
    ax2.text(7.2, 23, "$i$ = 32.5 cos(ωt − 36.87°)  (A)", color=COLORS[1], fontsize=8.5,
             va="center")
    bx.plot(tm, p / 1e3, color=INK, lw=2.0, label=r"$p(t)=v\,i$")
    bx.fill_between(tm, p / 1e3, 0, where=p < 0, color=COLORS[3], alpha=0.45, lw=0,
                    label="$p<0$: energy returned to supply")
    bx.plot(tm, pa / 1e3, color=COLORS[2], ls=":", lw=1.5, label=r"active part $P(1+\cos2\omega t)$")
    bx.plot(tm, pr / 1e3, color=COLORS[4], ls=":", lw=1.5, label=r"reactive part $Q\sin2\omega t$")
    bx.axhline(P / 1e3, color=INK, ls="--", lw=0.9)
    bx.axhline(0, color=INK, lw=0.6)
    bx.text(5.6, P / 1e3 + 0.12, "average $P$ = 4232 W", va="bottom", ha="center", fontsize=8.5)
    k = np.argmax(p)
    bx.annotate(f"max {p.max() / 1e3:.2f} kW", xy=(tm[k], p.max() / 1e3), xytext=(tm[k] + 1.6, 9.6),
                fontsize=8.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.6))
    k = np.argmin(p)
    bx.annotate(f"min −{abs(p.min()) / 1e3:.2f} kW\n(negative for 20.5 % of the cycle)",
                xy=(tm[k], p.min() / 1e3), xytext=(tm[k] + 1.4, -1.0),
                fontsize=8.5, va="center", arrowprops=dict(arrowstyle="-", lw=0.6))
    bx.set_ylim(-2, 10)
    bx.set_xlim(0, 20)
    bx.set_xlabel("time $t$ (ms)")
    bx.set_ylabel("power (kW)")
    bx.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=8)
    fig.tight_layout()
    save(fig, "09", "fig-9-1-instantaneous-power")


def fig_9_2():
    """Power triangle of the compressor, with mirror for a capacitive load."""
    P, Q = 4232.0, 3174.0
    S = np.hypot(P, Q)
    fig, ax = new_fig(6.4, 4.6)
    ax.axhline(0, color=INK, lw=0.7)
    ax.axvline(0, color=INK, lw=0.7)
    # mirror (capacitive)
    ax.fill([0, P, P], [0, 0, -Q], color=COLORS[0], alpha=0.06, lw=0)
    ax.plot([0, P, P, 0], [0, 0, -Q, 0], color=COLORS[0], ls="--", lw=1.1)
    ax.text(P + 100, -Q / 2, "$Q<0$\n(capacitive,\nleading)", va="center", fontsize=9,
            color=COLORS[0])
    # main
    ax.fill([0, P, P], [0, 0, Q], color=COLORS[1], alpha=0.08, lw=0)
    _vec(ax, 0, 0, P, 0, COLORS[2], lw=2.4)
    _vec(ax, P, 0, P, Q, COLORS[1], lw=2.4)
    _vec(ax, 0, 0, P, Q, COLORS[3], lw=2.6)
    ax.text(P / 2, -120, "$P$ = 4232 W", ha="center", va="top", fontsize=10, color=COLORS[2])
    ax.text(P + 100, Q / 2, "$jQ$ = j3174 var\n(inductive, lagging)", va="center", fontsize=9.5,
            color=COLORS[1])
    ax.text(250, 2350, "$S$ = 4232 + j3174 VA\n|$S$| = 5290 VA", ha="left",
            va="bottom", fontsize=10, color=COLORS[3])
    ax.plot([P - 180, P - 180, P], [0, 180, 180], color=INK, lw=0.8)
    ax.add_patch(Arc((0, 0), 2400, 2400, theta1=0, theta2=36.87, color=INK, lw=1))
    ax.text(1350 * np.cos(np.radians(18)), 1350 * np.sin(np.radians(18)), "$\\varphi$ = 36.87°",
            fontsize=9.5, va="center")
    ax.text(150, -Q - 150, "power factor = cos $\\varphi$ = 0.80 lagging (upper triangle)",
            fontsize=9, va="top")
    ax.set_xlim(-300, 6200)
    ax.set_ylim(-3900, 3700)
    ax.set_aspect("equal")
    ax.set_xlabel("$P$ (W)")
    ax.set_ylabel("$Q$ (var)")
    save(fig, "09", "fig-9-2-power-triangle")


def fig_9_3():
    """Power-factor correction of a 400 kW plant from 0.75 to 0.95."""
    P = 400.0
    Q1 = P * np.tan(np.arccos(0.75))
    Q2 = P * np.tan(np.arccos(0.95))
    S1, S2 = np.hypot(P, Q1), np.hypot(P, Q2)
    QC = Q1 - Q2
    fig, ax = new_fig(6.8, 4.6)
    ax.axhline(0, color=INK, lw=0.7)
    # transformer rating arc
    th = np.linspace(0, 43, 200)
    ax.plot(630 * np.cos(np.radians(th)), 630 * np.sin(np.radians(th)), color=INK, lw=1.0, ls="-.")
    ax.text(630 * np.cos(np.radians(40)) + 8, 630 * np.sin(np.radians(40)) + 4,
            "630 kVA transformer rating", fontsize=8.5, va="bottom")
    # original
    ax.fill([0, P, P], [0, 0, Q1], color=COLORS[1], alpha=0.07, lw=0)
    _vec(ax, 0, 0, P, Q1, COLORS[1], lw=2.2)
    ax.text(30, 215, f"$S_1$ = {S1:.1f} kVA\n$\\varphi_1$ = 41.4° (pf 0.75)",
            ha="left", fontsize=9, color=COLORS[1])
    # corrected
    _vec(ax, 0, 0, P, Q2, COLORS[0], lw=2.2)
    ax.text(205, 78, f"$S_2$ = {S2:.1f} kVA, $\\varphi_2$ = 18.2°", rotation=18.2,
            rotation_mode="anchor", ha="center", va="bottom", fontsize=8.5, color=COLORS[0])
    _vec(ax, 0, 0, P, 0, COLORS[2], lw=2.2)
    ax.text(P / 2, -12, "$P$ = 400 kW", ha="center", va="top", fontsize=9.5, color=COLORS[2])
    # capacitor
    _vec(ax, P, Q1, P, Q2, COLORS[3], lw=2.6)
    ax.text(P + 10, (Q1 + Q2) / 2, f"$Q_C$ = −{QC:.1f} kvar\ncapacitor bank", fontsize=8.5,
            va="center", color=COLORS[3])
    # dotted extension to unity
    ax.plot([P, P], [Q2, 0], color="#777777", ls=":", lw=2.0)
    ax.text(P + 10, Q2 / 2 - 5, f"further {Q2:.1f} kvar\nfor pf = 1:\ndiminishing returns", fontsize=8.5,
            va="center", color="#555555")
    ax.text(P, Q1 + 12, f"$Q_1$ = {Q1:.1f} kvar", fontsize=8.5, va="bottom", ha="center",
            color=COLORS[1])
    ax.text(P + 10, Q2 + 6, f"$Q_2$ = {Q2:.1f} kvar", fontsize=8.5, va="bottom",
            color=COLORS[0])
    ax.add_patch(Arc((0, 0), 160, 160, theta1=0, theta2=18.2, color=COLORS[0], lw=1))
    ax.add_patch(Arc((0, 0), 240, 240, theta1=0, theta2=41.4, color=COLORS[1], lw=1))
    ax.set_xlim(0, 720)
    ax.set_ylim(-45, 450)
    ax.set_aspect("equal")
    ax.set_xlabel("$P$ (kW)")
    ax.set_ylabel("$Q$ (kvar)")
    save(fig, "09", "fig-9-3-pf-correction")


def fig_9_4():
    """Rectifier-capacitor supply current: waveform and harmonic spectrum."""
    Ih = {1: 1.0, 3: 0.8, 5: 0.6, 7: 0.4, 9: 0.2}
    lag = np.radians(5)
    t = np.linspace(0, 0.020, 4001)
    v = 325.3 * np.cos(W * t)
    # cosine harmonics with a common time shift (5 deg of fundamental): pulses centred near
    # the voltage peaks, fundamental lagging the voltage by 5 deg
    i = sum(np.sqrt(2) * a * np.cos(h * (W * t - lag)) for h, a in Ih.items())
    Irms = np.sqrt(sum(a ** 2 for a in Ih.values()))
    thd = np.sqrt(sum(a ** 2 for h, a in Ih.items() if h > 1)) / Ih[1]
    pf = np.cos(lag) / np.sqrt(1 + thd ** 2)
    fig, (a1, a3) = plt.subplots(1, 2, figsize=(6.8, 3.8), gridspec_kw=dict(width_ratios=[1.35, 1]))
    a2 = a1.twinx()
    a2.spines["right"].set_visible(True)
    a1.plot(t * 1e3, v, color=COLORS[0], lw=1.3, label="$v$ (V)")
    a2.plot(t * 1e3, i, color=COLORS[1], lw=1.8, label="$i$ (A)")
    a1.set_ylim(-400, 400)
    a2.set_ylim(-5, 5)
    a1.axhline(0, color=INK, lw=0.5)
    a1.set_xlim(0, 20)
    a1.set_xlabel("time $t$ (ms)")
    a1.set_ylabel("voltage (V)", color=COLORS[0])
    a2.set_ylabel("current (A)", color=COLORS[1])
    a2.text(0.6, 4.5, f"peak {i.max():.2f} A", fontsize=8, color=COLORS[1], va="center")
    h1, l1 = a1.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    a1.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=8, ncol=2)
    hs = np.arange(1, 12)
    vals = [Ih.get(h, 0.0) for h in hs]
    a3.bar(hs, vals, width=0.6, color=[COLORS[0] if h == 1 else COLORS[1] for h in hs])
    for h, val in zip(hs, vals):
        if val > 0:
            a3.text(h, val + 0.02, f"{val:.1f}", ha="center", va="bottom", fontsize=8)
    a3.set_xticks(hs)
    a3.tick_params(axis="x", labelsize=8)
    a3.set_xlabel("harmonic order $h$")
    a3.set_ylabel("RMS current $I_h$ (A)")
    a3.set_ylim(0, 1.6)
    a3.text(11.4, 1.57, f"$I_{{rms}}$ = {Irms:.2f} A\nTHD = {thd * 100:.0f} %\n"
            f"displacement PF = {np.cos(lag):.3f}\ntrue PF = {pf:.2f}",
            ha="right", va="top", fontsize=8.5,
            bbox=dict(fc="white", ec="#BBBBBB", lw=0.6, boxstyle="round,pad=0.3"))
    fig.tight_layout()
    save(fig, "09", "fig-9-4-distorted-current")


def _ct(ax, x, y, r=0.32):
    ax.add_patch(Circle((x, y), r, fc="none", ec=INK, lw=1.4))
    ax.add_patch(Circle((x, y), r * 0.72, fc="none", ec=INK, lw=0.8))


def fig_9_5():
    """Signal chain of a digital power analyser fed from instrument transformers."""
    fig, ax = schematic(6.8, 4.9, xlim=(0, 15.6), ylim=(0.3, 11.5))
    yL, yN = 10.2, 8.4
    lw_p = 2.2
    # primary circuit
    ax.plot([0.3, 5.9], [yL, yL], color=INK, lw=lw_p)
    ax.plot([0.3, 5.9], [yN, yN], color=INK, lw=lw_p)
    ax.text(6.55, yL, "line (11 kV)", fontsize=8, va="center")
    ax.text(6.55, yN, "neutral", fontsize=8, va="center")
    box(ax, 5.15, 8.75, 1.15, 1.1, "load", fontsize=8, fc="#F4F4F4")
    ax.plot([5.72, 5.72], [9.85, yL], color=INK, lw=1.3)
    ax.plot([5.72, 5.72], [8.75, yN], color=INK, lw=1.3)
    ax.plot([5.9, 6.4], [yL, yL], color=INK, lw=lw_p)
    ax.plot([5.9, 6.4], [yN, yN], color=INK, lw=lw_p)
    # VT: primary winding across line-neutral, secondary coupled beside it
    xv, yv0 = 1.4, 9.3
    ax.plot([xv, xv], [yL, yv0 + 0.34], color=INK, lw=1.2)
    ax.plot([xv, xv], [yN, yv0 - 0.34], color=INK, lw=1.2)
    ax.add_patch(Circle((xv, yv0), 0.34, fc="white", ec=INK, lw=1.3))
    ax.add_patch(Circle((xv + 0.48, yv0), 0.34, fc="none", ec=INK, lw=1.3))
    ax.text(0.2, 10.55, "VT 11 kV / 110 V\nphase error $\\delta_{VT}$", ha="left",
            va="bottom", fontsize=7.6)
    # CT ring on the line conductor
    xc = 3.7
    ax.add_patch(Circle((xc, yL), 0.27, fc="none", ec=INK, lw=1.4))
    ax.add_patch(Circle((xc, yL), 0.18, fc="none", ec=INK, lw=0.8))
    ax.text(3.0, 10.55, "CT 400 A / 5 A (or 1 A)\nphase error $\\delta_{CT}$", ha="left",
            va="bottom", fontsize=7.6)
    # secondary leads
    yi, yv = 6.4, 4.4
    ax.plot([xv + 0.82, 2.5, 2.5, 3.0], [yv0, yv0, yv, yv], color=COLORS[0], lw=1.3)
    ax.plot([xc, xc], [yL - 0.27, yi + 0.6], color=COLORS[1], lw=1.3)
    ax.text(2.35, 7.4, "$v_s$ (110 V)", color=COLORS[0], fontsize=8, va="center", ha="right")
    ax.text(xc + 0.1, 7.6, "$i_s$ (5 A)", color=COLORS[1], fontsize=8, va="center")
    # conditioning
    box(ax, 3.0, yi - 0.6, 2.6, 1.2, "shunt / burden\n+ anti-alias LPF", fontsize=7.6)
    box(ax, 3.0, yv - 0.6, 2.6, 1.2, "attenuator\n+ anti-alias LPF", fontsize=7.6)
    # ADCs
    box(ax, 6.2, yi - 0.6, 1.8, 1.2, "ADC", fontsize=8.5)
    box(ax, 6.2, yv - 0.6, 1.8, 1.2, "ADC", fontsize=8.5)
    arrow(ax, 5.6, yi, 6.2, yi)
    arrow(ax, 5.6, yv, 6.2, yv)
    ax.text(7.1, (yi + yv) / 2, "simultaneous\nsampling", ha="center", va="center", fontsize=7.3)
    ax.text(7.1, yv - 0.75, "24 bit,\n8–50 kS/s", ha="center", va="top", fontsize=7.3)
    # DSP
    yb, yt = yv - 0.8, yi + 0.8
    box(ax, 8.7, yb, 2.8, yt - yb,
        "DSP\n\n$P=\\frac{1}{N}\\sum v[n]\\,i[n]$\n\naverage over an\ninteger number\nof cycles",
        fontsize=7.6, fc="#E9F4EE")
    arrow(ax, 8.0, yi, 8.7, yi)
    arrow(ax, 8.0, yv, 8.7, yv)
    ax.text(8.35, yi + 0.08, "$i[n]$", ha="center", va="bottom", fontsize=7.6)
    ax.text(8.35, yv + 0.08, "$v[n]$", ha="center", va="bottom", fontsize=7.6)
    # synchronisation
    box(ax, 8.6, 0.6, 3.0, 1.3, "zero-crossing / PLL\ncycle sync", fontsize=7.6,
        fc="#F6F0E4")
    ax.plot([8.35, 8.35, 8.6], [yv, 1.25, 1.25], color=INK, lw=0.8, ls="--")
    arrow(ax, 10.1, 1.9, 10.1, yb)
    # outputs
    box(ax, 12.2, yb, 2.9, yt - yb,
        "outputs\n\n$P$, $V_{rms}$, $I_{rms}$\n$S$, PF\nharmonics\nenergy:\nkWh, kvarh",
        fontsize=7.6, fc="#F4F4F4")
    arrow(ax, 11.5, (yi + yv) / 2, 12.2, (yi + yv) / 2)
    # phase-error note
    ax.text(0.3, 1.5,
            "Transformer phase errors $\\delta_{VT}$, $\\delta_{CT}$ (minutes of arc)\n"
            "add to the measured angle: $\\varphi_{meas}=\\varphi+\\delta_{VT}-\\delta_{CT}$\n"
            "($\\delta$ positive when the secondary leads);\n"
            "power error ≈ $\\delta\\,\\tan\\varphi$, large at low PF.",
            fontsize=7.4, va="center")
    save(fig, "09", "fig-9-5-power-measurement-chain")


if __name__ == "__main__":
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    fig_9_5()
