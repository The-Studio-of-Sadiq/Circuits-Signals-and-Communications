"""Figures for Chapter 8 — Sinusoidal Steady-State Analysis.

Run from the repository root:  python figures/scripts/ch08.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Polygon  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

from figstyle import new_fig, save, COLORS, INK  # noqa: E402

schemdraw.use("matplotlib")

F = 50.0
W = 2 * np.pi * F


def fig_8_1():
    """Mains voltage and lagging current of the compressor."""
    t = np.linspace(0, 0.040, 2000)
    vm, im, phi = 230 * np.sqrt(2), 23 * np.sqrt(2), np.radians(36.87)
    v = vm * np.cos(W * t)
    i = im * np.cos(W * t - phi)
    fig, ax = new_fig(6.4, 3.8)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax.plot(t * 1e3, v, color=COLORS[0], label="$v(t)$, 325.3 V peak")
    ax2.plot(t * 1e3, i, color=COLORS[1], label="$i(t)$, 32.5 A peak")
    ax.set_xlim(0, 40)
    ax.set_ylim(-400, 400)
    ax2.set_ylim(-40, 40)
    ax.set_xlabel("time $t$ (ms)")
    ax.set_ylabel("voltage (V)", color=COLORS[0])
    ax2.set_ylabel("current (A)", color=COLORS[1])
    ax.axhline(0, color=INK, lw=0.6)
    for y, lab in [(vm, "peak 325.3 V"), (230, "RMS 230 V")]:
        ax.axhline(y, color=COLORS[0], ls="--", lw=0.8)
        ax.text(39.5, y + 8, lab, ha="right", va="bottom", fontsize=8.5, color=COLORS[0])
    # period
    ax.annotate("", xy=(20, -365), xytext=(0, -365),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1, mutation_scale=9))
    ax.text(10, -358, "period $T$ = 20 ms", ha="center", va="bottom", fontsize=8.5)
    # lag arrow between peaks at t=0 and t=2.05 ms
    dt = 36.87 / 360 * 20
    ax.plot([dt, dt], [-20, vm * 0.999], color=COLORS[1], lw=0.8, ls=":")
    ax.annotate("", xy=(dt, 285), xytext=(0, 285),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1, mutation_scale=9))
    ax.annotate("current lags by 36.87° = 2.05 ms", xy=(1.0, 285), xytext=(3.2, 372),
                fontsize=8.5, va="center",
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower center", fontsize=8.5, ncol=2,
              bbox_to_anchor=(0.5, 1.0))
    save(fig, "08", "fig-8-1-sinusoid-parameters")


def _angle_arc(ax, center, r, a0, a1, label, lr=None, color=INK, fs=9):
    ax.add_patch(Arc(center, 2 * r, 2 * r, theta1=min(a0, a1), theta2=max(a0, a1),
                     color=color, lw=1))
    am = np.radians((a0 + a1) / 2)
    lr = lr or r * 1.25
    ax.text(center[0] + lr * np.cos(am), center[1] + lr * np.sin(am), label,
            ha="center", va="center", fontsize=fs, color=color)


def _vec(ax, x0, y0, x1, y1, color, lw=2.0, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=14))


def fig_8_2():
    """Impedance plane: R, jX_L, -jX_C and the 8 + j6 ohm load."""
    fig, ax = new_fig(6.4, 4.6)
    ax.axhspan(0, 8.5, color=COLORS[1], alpha=0.06, lw=0)
    ax.axhspan(-8.5, 0, color=COLORS[0], alpha=0.06, lw=0)
    ax.text(12.8, 0.4, "inductive\n($X>0$)", ha="right", fontsize=9, color=COLORS[1])
    ax.text(12.8, -0.4, "capacitive\n($X<0$)", ha="right", va="top", fontsize=9, color=COLORS[0])
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    _vec(ax, 0, 0, 8, 0, COLORS[2])
    ax.text(4, -0.55, "$R$ = 8 Ω", ha="center", va="top", fontsize=9.5, color=COLORS[2])
    _vec(ax, 0, 0, 0, 6, COLORS[1])
    ax.text(0.25, 7.1, "$jX_L$ = j6 Ω\n($L$ = 19.1 mH at 50 Hz)", ha="left", va="center",
            fontsize=9, color=COLORS[1])
    _vec(ax, 0, 0, 0, -6, COLORS[0])
    ax.text(0.25, -4.4, "$-jX_C$ = −j6 Ω\n($C$ = 530 µF at 50 Hz)", ha="left", va="center",
            fontsize=9, color=COLORS[0])
    # triangle
    ax.plot([8, 8], [0, 6], color=COLORS[1], lw=1.2, ls="--")
    ax.text(8.2, 3, "j6", color=COLORS[1], fontsize=9, va="center")
    _vec(ax, 0, 0, 8, 6, COLORS[3], lw=2.4)
    ax.text(8.35, 6.4, "$Z$ = 8 + j6\n    = 10∠36.87° Ω", ha="left", va="bottom",
            fontsize=9.5, color=COLORS[3])
    ax.plot([7.6, 7.6, 8], [0, 0.4, 0.4], color=INK, lw=0.8)
    _angle_arc(ax, (0, 0), 2.6, 0, 36.87, r"$\theta_Z$", lr=3.2)
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-8, 8.5)
    ax.set_xlabel("resistance $R$ (Ω)")
    ax.set_ylabel("reactance $X$ (Ω)  [imaginary axis $jX$]")
    ax.set_xticks(range(0, 13, 2))
    ax.set_yticks(range(-8, 9, 2))
    ax.set_aspect("equal")
    save(fig, "08", "fig-8-2-impedance-plane")


def fig_8_3():
    """Phasor diagram of the series RL compressor model."""
    phi = np.radians(36.87)
    V = 230.0
    I = 23.0 * np.exp(-1j * phi)
    VR = 8 * I
    VL = 1j * 6 * I
    kI = 5.0  # current drawn at 5 V of length per ampere
    fig, ax = new_fig(6.4, 4.4)
    ax.axhline(0, color=INK, lw=0.6)
    ax.axvline(0, color=INK, lw=0.6)
    _vec(ax, 0, 0, V, 0, COLORS[0], lw=2.4)
    ax.text(V, 6, "$\\mathbf{V}$ = 230∠0° V", ha="right", va="bottom", fontsize=9.5, color=COLORS[0])
    _vec(ax, 0, 0, VR.real, VR.imag, COLORS[2])
    ax.text(VR.real * 0.66 - 5, VR.imag * 0.66 - 7, r"$\mathbf{V}_R$ = 184∠−36.87° V",
            rotation=-36.87, rotation_mode="anchor", ha="left", va="top", fontsize=8.5, color=COLORS[2])
    _vec(ax, VR.real, VR.imag, VR.real + VL.real, VR.imag + VL.imag, COLORS[1])
    ax.text(VR.real + VL.real * 0.5 + 10, VR.imag + VL.imag * 0.5,
            "$\\mathbf{V}_L$ = 138∠53.13° V", ha="left", va="center", fontsize=9, color=COLORS[1])
    Is = I * kI
    _vec(ax, 0, 0, Is.real, Is.imag, COLORS[3], lw=2.6)
    ax.text(Is.real * 0.10 - 6, Is.imag * 0.10 - 8, r"$\mathbf{I}$ = 23∠−36.87° A",
            rotation=-36.87, rotation_mode="anchor", ha="left", va="top", fontsize=8.5, color=COLORS[3])
    # right angle at tip of VR
    u = VR / abs(VR)
    n = 1j * u
    s = 10
    p1 = VR - s * u
    p2 = p1 + s * n
    p3 = VR + s * n
    ax.plot([p1.real, p2.real, p3.real], [p1.imag, p2.imag, p3.imag], color=INK, lw=0.8)
    _angle_arc(ax, (0, 0), 38, -36.87, 0, "36.87°", lr=56, fs=8.5)
    ax.text(5, 95, "184 + 138 = 322 V (arithmetic sum)\nbut |$\\mathbf{V}_R+\\mathbf{V}_L$| = 230 V "
            "(phasor sum)", fontsize=8.5, va="bottom",
            bbox=dict(fc="white", ec="#BBBBBB", lw=0.6, boxstyle="round,pad=0.3"))
    ax.set_xlim(-20, 260)
    ax.set_ylim(-180, 140)
    ax.set_aspect("equal")
    ax.set_xlabel("real part (V)")
    ax.set_ylabel("imaginary part (V)")
    # current scale bar
    yb = 62
    ax.plot([0, 25 * kI], [yb, yb], color=COLORS[3], lw=1)
    for k in range(0, 26, 5):
        ax.plot([k * kI] * 2, [yb - 3, yb + 3], color=COLORS[3], lw=1)
        ax.text(k * kI, yb - 5, f"{k}", ha="center", va="top", fontsize=7.5, color=COLORS[3])
    ax.text(25 * kI + 6, yb, "current scale (A)", va="center", fontsize=8, color=COLORS[3])
    save(fig, "08", "fig-8-3-rl-phasor-diagram")


def _mesh_arrow(ax, x, y, r, label, color=COLORS[1]):
    """Clockwise mesh-current arrow (open circle with arrowhead) centred at (x, y)."""
    th = np.radians(np.linspace(120, -200, 80))
    ax.plot(x + r * np.cos(th), y + r * np.sin(th), color=color, lw=1.4)
    ax.annotate("", xy=(x + r * np.cos(th[-1]), y + r * np.sin(th[-1])),
                xytext=(x + r * np.cos(th[-4]), y + r * np.sin(th[-4])),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, mutation_scale=14,
                                shrinkA=0, shrinkB=0))
    ax.text(x, y, label, ha="center", va="center", fontsize=11, color=color)


def fig_8_4():
    """Two-node AC circuit for nodal and mesh analysis."""
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=10, unit=3.2)
        vs = elm.SourceSin().up()
        r1 = elm.Resistor().right().label("$R_1$ = 10 Ω")
        n1 = elm.Dot()
        d.push()
        c = elm.Capacitor().down()
        d.pop()
        lw = elm.Inductor2().right().label("$L$ = 10 mH (+j10 Ω)")
        n2 = elm.Dot()
        r2 = elm.Resistor().down().label("$R_2$ = 10 Ω", loc="bottom")
        b2 = elm.Line().left()
        elm.Dot()
        b1 = elm.Line().left()
        elm.Ground().at(c.end)
    f = d.draw(show=False)
    fig, ax = f.fig, f.ax
    fig.set_size_inches(6.4, 3.4)
    x1, y1 = n1.center
    x2, y2 = n2.center
    xs, ys = vs.center
    ax.text(xs - 0.75, ys, r"$\mathbf{V}_s$ = 10∠0° V" + "\n(rms)", ha="right", va="center",
            fontsize=10)
    ax.text(xs + 0.25, ys + 0.85, "+", ha="left", va="center", fontsize=11)
    ax.text(xs + 0.25, ys - 0.85, "−", ha="left", va="center", fontsize=11)
    xc, yc = c.center
    xr = r2.center[0]
    _mesh_arrow(ax, xs + 0.37 * (xc - xs), yc, 0.42, r"$\mathbf{I}_1$")
    _mesh_arrow(ax, (xc + xr) / 2, yc, 0.5, r"$\mathbf{I}_2$")
    ax.text(xc - 0.3, yc, "$C$ = 100 µF\n(−j10 Ω)", ha="right", va="center", fontsize=10)
    ax.text(x1, y1 + 0.3, r"$\mathbf{V}_1$", ha="center", va="bottom", fontsize=11, color=COLORS[0])
    ax.text(x2, y2 + 0.3, r"$\mathbf{V}_2$", ha="center", va="bottom", fontsize=11, color=COLORS[0])
    ax.text(x2 + 1.9, yc,
            "$\\omega$ = 1000 rad/s\n\n"
            "$\\mathbf{V}_1$ = 6 − j2 V\n$\\mathbf{V}_2$ = 2 − j4 V\n"
            "$\\mathbf{I}_1$ = 0.4 + j0.2 A\n$\\mathbf{I}_2$ = 0.2 − j0.4 A",
            ha="left", va="center", fontsize=9.5,
            bbox=dict(fc="#EEF3F8", ec="#888888", lw=0.7, boxstyle="round,pad=0.4"))
    save(fig, "08", "fig-8-4-nodal-mesh-example")


def fig_8_5():
    """Series RLC resonance curves for Q = 10 and Q = 100 at 1 MHz."""
    L, f0 = 200e-6, 1e6
    C = 1 / ((2 * np.pi * f0) ** 2 * L)
    f = np.linspace(0.9e6, 1.1e6, 4001)
    w = 2 * np.pi * f
    fig, ax = new_fig(6.6, 4.2)
    res = {}
    for Q, col, ls in [(100, COLORS[0], "-"), (10, COLORS[1], "--")]:
        R = 2 * np.pi * f0 * L / Q
        Z = R + 1j * (w * L - 1 / (w * C))
        res[Q] = (R, Z)
        ax.plot(f / 1e6, R / np.abs(Z), color=col, ls=ls,
                label=f"$Q$ = {Q} ($R$ = {R:.4g} Ω), $B$ = {f0 / Q / 1e3:.0f} kHz")
    ax.axhline(1 / np.sqrt(2), xmax=0.76, color=INK, ls="--", lw=0.8)
    ax.text(0.902, 0.72, "0.707 (half power)", fontsize=8.5, va="bottom")
    # Q=100 half-power points
    R100 = res[100][0]
    B = R100 / L / (2 * np.pi)
    fa = (-B / 2 + np.sqrt((B / 2) ** 2 + f0 ** 2)) / 1e6
    fb = (B / 2 + np.sqrt((B / 2) ** 2 + f0 ** 2)) / 1e6
    ax.annotate("", xy=(fb, 0.62), xytext=(fa, 0.62),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=COLORS[0], mutation_scale=8,
                                shrinkA=0, shrinkB=0))
    for x in (fa, fb):
        ax.plot([x, x], [0.6, 1 / np.sqrt(2)], color=COLORS[0], lw=0.7)
    ax.text(0.9915, 0.6, "$B$ = 10 kHz\n(0.995–1.005 MHz)", ha="right", va="top", fontsize=8.5,
            color=COLORS[0])
    for fx, ty in ((1.009e6, 0.37), (1.02e6, 0.27)):
        wx = 2 * np.pi * fx
        r = R100 / abs(R100 + 1j * (wx * L - 1 / (wx * C)))
        ax.plot(fx / 1e6, r, "o", color=COLORS[0], ms=5)
        ax.annotate(f"{fx / 1e6:.3f} MHz: {r:.3f} ({20 * np.log10(r):.1f} dB)".replace("-", "−"),
                    xy=(fx / 1e6, r), xytext=(1.032, ty), fontsize=8.5, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=INK))
    ax.set_xlim(0.9, 1.1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("frequency $f$ (MHz)")
    ax.set_ylabel("$I/I_0$")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8.5, ncol=2)
    # inset phase
    ins = ax.inset_axes([0.79, 0.72, 0.19, 0.22])
    for Q, col, ls in [(100, COLORS[0], "-"), (10, COLORS[1], "--")]:
        ins.plot(f / 1e6, -np.degrees(np.angle(res[Q][1])), color=col, ls=ls, lw=1.2)
    ins.set_ylim(-95, 95)
    ins.set_yticks([-90, 0, 90])
    ins.set_xticks([0.9, 1.0, 1.1])
    ins.tick_params(labelsize=7.5)
    ins.axhline(0, color=INK, lw=0.5)
    ins.set_title("phase of $I$ (°)", fontsize=8)
    save(fig, "08", "fig-8-5-resonance-curves")


def fig_8_6():
    """Bode plots of the audio low-pass and two ECG high-pass sections."""
    f = np.logspace(-2, 6, 2000)
    fcl = 1 / (2 * np.pi * 1600 * 10e-9)
    Hl = 1 / (1 + 1j * f / fcl)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.0), sharex=True)
    for a in (a1, a2):
        a.axvspan(0.05, 150, color=COLORS[3], alpha=0.10, lw=0)
        a.axvspan(20, 20e3, color=COLORS[4], alpha=0.14, lw=0)
        a.set_xscale("log")
    a1.text(np.sqrt(0.05 * 150), -38, "ECG band\n0.05–150 Hz", ha="center", va="bottom",
            fontsize=8, color="#7A3A66")
    a1.text(np.sqrt(20 * 20e3), -38, "audio band\n20 Hz–20 kHz", ha="center", va="bottom",
            fontsize=8, color="#8A5A00")
    a1.plot(f, 20 * np.log10(abs(Hl)), color=COLORS[0], label=f"low-pass, $f_c$ = 9.95 kHz")
    a2.plot(f, np.degrees(np.angle(Hl)), color=COLORS[0])
    # asymptotes LP
    fa = np.logspace(np.log10(fcl), 6, 10)
    a1.plot([1e-2, fcl], [0, 0], color=COLORS[0], ls=":", lw=1)
    a1.plot(fa, -20 * np.log10(fa / fcl), color=COLORS[0], ls=":", lw=1)
    styles = [(0.05, COLORS[2], "-"), (0.5, COLORS[1], "--")]
    for fc, col, ls in styles:
        Hh = (1j * f / fc) / (1 + 1j * f / fc)
        a1.plot(f, 20 * np.log10(abs(Hh)), color=col, ls=ls, label=f"high-pass, $f_c$ = {fc} Hz")
        a2.plot(f, np.degrees(np.angle(Hh)), color=col, ls=ls)
        fb = np.logspace(-2, np.log10(fc), 10)
        a1.plot(fb, 20 * np.log10(fb / fc), color=col, ls=":", lw=1)
    # marked points
    for fc, col, dy, dx in [(0.05, COLORS[2], 0.6, 1.5), (0.5, COLORS[1], -9, 2.5)]:
        H1 = (1j / fc) / (1 + 1j / fc)
        m = 20 * np.log10(abs(H1))
        a1.plot(1, m, "o", color=col, ms=4.5)
        a1.annotate(f"{m:.2f} dB at 1 Hz".replace("-", "−"), xy=(1, m), xytext=(dx, m + dy), fontsize=8, color=col,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=col))
        p = np.degrees(np.angle(H1))
        a2.plot(1, p, "o", color=col, ms=4.5)
    a2.annotate("+2.9° at 1 Hz", xy=(1, 2.86), xytext=(3, 18), fontsize=8, color=COLORS[2],
                arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[2]))
    a2.annotate("+26.6° at 1 Hz", xy=(1, 26.57), xytext=(2.5, 55), fontsize=8, color=COLORS[1],
                arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[1]))
    for fx, txt, dx in [(fcl, "−3 dB at 9.95 kHz", 0.05), (20e3, "−7.0 dB at 20 kHz", 3.0)]:
        H = 1 / (1 + 1j * fx / fcl)
        m = 20 * np.log10(abs(H))
        a1.plot(fx, m, "o", color=COLORS[0], ms=4.5)
        p = np.degrees(np.angle(H))
        a2.plot(fx, p, "o", color=COLORS[0], ms=4.5)
    a1.annotate("−3 dB at 9.95 kHz", xy=(fcl, -3.01), xytext=(1.2e2, -12), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[0]))
    a1.annotate("−7.0 dB at 20 kHz", xy=(20e3, -7.03), xytext=(1.2e5, -2.5), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[0]))
    a2.annotate("−45° at 9.95 kHz", xy=(fcl, -45), xytext=(60, -60), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[0]))
    a2.annotate("−63.6° at 20 kHz", xy=(20e3, -63.6), xytext=(1.3e5, -35), fontsize=8,
                color=COLORS[0], arrowprops=dict(arrowstyle="-", lw=0.6, color=COLORS[0]))
    a1.set_ylim(-40, 3)
    a1.set_ylabel("magnitude (dB)")
    a1.legend(loc="lower center", fontsize=8, ncol=1, bbox_to_anchor=(0.5, 0.18))
    a2.set_ylim(-90, 90)
    a2.set_yticks([-90, -45, 0, 45, 90])
    a2.set_ylabel("phase (°)")
    a2.set_xlabel("frequency $f$ (Hz)")
    a2.set_xlim(1e-2, 1e6)
    for a in (a1, a2):
        a.grid(True, which="major", lw=0.5)
    fig.tight_layout()
    save(fig, "08", "fig-8-6-rc-frequency-response")


if __name__ == "__main__":
    fig_8_1()
    fig_8_2()
    fig_8_3()
    fig_8_4()
    fig_8_5()
    fig_8_6()
