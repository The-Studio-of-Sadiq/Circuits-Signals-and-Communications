"""Figures for Chapter 10 — Three-Phase Circuits.

Run from the repository root:  python figures/scripts/ch10.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle, Polygon, Rectangle, FancyArrowPatch  # noqa: E402

from figstyle import new_fig, schematic, box, save, COLORS, INK  # noqa: E402

F = 50.0
W = 2 * np.pi * F
A = np.exp(1j * 2 * np.pi / 3)  # operator a = 1 /120 deg


def _vec(ax, z0, z1, color, lw=2.0, ls="-", ms=13, alpha=1.0, zorder=3):
    ax.annotate("", xy=(z1.real, z1.imag), xytext=(z0.real, z0.imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, alpha=alpha,
                                shrinkA=0, shrinkB=0, mutation_scale=ms), zorder=zorder)


def _arr(ax, x0, y0, x1, y1, color=INK, lw=1.0, ms=9, both=False):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def fig_10_1():
    """Balanced three-phase voltages of a 230 V, 50 Hz supply."""
    t = np.linspace(0, 0.040, 4001)
    Vm = 325.0
    va = Vm * np.sin(W * t)
    vb = Vm * np.sin(W * t - 2 * np.pi / 3)
    vc = Vm * np.sin(W * t - 4 * np.pi / 3)
    fig, ax = new_fig(6.6, 3.9)
    tm = t * 1e3
    ax.plot(tm, va, color=COLORS[0], ls="-", label="$v_a$ = 325 sin ωt")
    ax.plot(tm, vb, color=COLORS[1], ls="--", label="$v_b$ (lags 120°, 6.67 ms)")
    ax.plot(tm, vc, color=COLORS[2], ls=":", lw=2.2, label="$v_c$ (lags 240°, 13.33 ms)")
    s = va + vb + vc
    ax.plot(tm, s, color=INK, lw=0.9)
    ax.text(39.5, 12, "$v_a+v_b+v_c=0$", ha="right", va="bottom", fontsize=8.5)
    for k, (t0, col, name) in enumerate([(0, COLORS[0], "a"), (20 / 3, COLORS[1], "b"),
                                         (40 / 3, COLORS[2], "c")]):
        ax.axvline(t0, color=col, lw=0.8, ls="-", alpha=0.6, ymin=0.06, ymax=0.5)
        tp = t0 + 5
        ax.plot(tp, Vm, "o", color=col, ms=5)
        ax.text(tp, Vm + 15, f"{name}: {tp:.2f} ms".replace(".00", ""), ha="center", va="bottom",
                fontsize=8, color=col)
        ax.text(t0 + 0.25, -370, f"{t0:.2f} ms".replace("0.00", "0"), fontsize=7.5, color=col,
                va="bottom")
    ax.set_xlim(0, 40)
    ax.set_ylim(-400, 400)
    ax.set_xlabel("time $t$ (ms)")
    ax.set_ylabel("voltage (V)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=8.3)
    save(fig, "10", "fig-10-1-three-phase-waveforms")


def _zbox(ax, p0, p1, label="", w=0.32, frac=0.42, lab_off=0.32, fs=9, lab_side=1):
    """Impedance drawn as an IEC rectangle centred on the segment p0-p1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    h = frac * L / 2
    m = (p0 + p1) / 2
    ax.plot([p0[0], (m - h * u)[0]], [p0[1], (m - h * u)[1]], color=INK, lw=1.3)
    ax.plot([(m + h * u)[0], p1[0]], [(m + h * u)[1], p1[1]], color=INK, lw=1.3)
    corners = [m - h * u - w / 2 * n, m + h * u - w / 2 * n, m + h * u + w / 2 * n, m - h * u + w / 2 * n]
    ax.add_patch(Polygon(corners, closed=True, fc="white", ec=INK, lw=1.3, zorder=3))
    if label:
        q = m + lab_side * lab_off * n
        ax.text(q[0], q[1], label, ha="center", va="center", fontsize=fs)
    return m, u, n


def fig_10_2():
    """Star and delta connections with line and phase quantities."""
    fig, ax = schematic(6.9, 3.9, xlim=(-0.4, 13.8), ylim=(-1.6, 6.2))
    cI = COLORS[1]
    cV = COLORS[0]
    # ---------------- (a) star
    n = np.array([3.6, 2.0])
    Pa = np.array([4.9, 2.0])     # right arm (phase a)
    Pb = np.array([2.5, 3.4])     # upper-left arm (phase b)
    Pc = np.array([2.5, 0.6])     # lower-left arm (phase c)
    for P, lab, side in [(Pa, "$Z$", -1), (Pb, "$Z$", -1), (Pc, "$Z$", 1)]:
        _zbox(ax, P, n, lab, lab_side=side)
    ax.add_patch(Circle(n, 0.07, color=INK, zorder=4))
    ax.text(n[0] + 0.12, n[1] - 0.12, "$n$", fontsize=10, va="top")
    ya, yb, yc = 4.6, 3.4, 0.6
    # line wiring
    ax.plot([0, 4.9, 4.9], [ya, ya, 2.0], color=INK, lw=1.3)
    ax.plot([0, 2.5], [yb, yb], color=INK, lw=1.3)
    ax.plot([0, 2.5], [yc, yc], color=INK, lw=1.3)
    for y, nm in [(ya, "a"), (yb, "b"), (yc, "c")]:
        ax.add_patch(Circle((0, y), 0.07, fc="white", ec=INK, zorder=4))
        ax.text(-0.15, y, nm, ha="right", va="center", fontsize=10)
    # neutral conductor
    ax.plot([n[0], n[0], 0], [n[1], -0.5, -0.5], color=INK, lw=1.2, ls="--")
    ax.add_patch(Circle((0, -0.5), 0.07, fc="white", ec=INK, zorder=4))
    ax.text(-0.15, -0.5, "N", ha="right", va="center", fontsize=10)
    # line currents
    for y, nm in [(ya, "a"), (yb, "b"), (yc, "c")]:
        _arr(ax, 0.45, y, 1.05, y, color=cI, lw=1.4, ms=11)
        ax.text(0.75, y + 0.12, f"$I_{nm}$", color=cI, ha="center", va="bottom", fontsize=9)
    _arr(ax, 1.6, -0.5, 1.0, -0.5, color=cI, lw=1.4, ms=11)
    ax.text(1.3, -0.62, "$I_n$", color=cI, ha="center", va="top", fontsize=9)
    # voltages
    _arr(ax, 1.75, yb + 0.05, 1.75, ya - 0.05, color=cV, lw=1.0)
    ax.text(1.85, (ya + yb) / 2, "$V_{ab}$", color=cV, fontsize=9, va="center")
    _arr(ax, n[0] + 0.3, n[1] + 0.15, 4.75, ya - 0.2, color=cV, lw=1.0)
    ax.text(4.0, 3.6, "$V_{an}$", color=cV, fontsize=9, ha="right", va="center")
    ax.text(2.6, -1.0, "(a) star", fontsize=10, ha="center", fontweight="bold")
    ax.text(0.0, 5.55, "$V_{an}$: phase voltage    $V_{ab}$: line voltage\n"
            "$I_a$: line current = phase current", fontsize=8, va="bottom")
    # ---------------- (b) delta
    x0 = 7.6
    Na = np.array([10.7, 4.6])
    Nb = np.array([8.9, 1.3])
    Nc = np.array([12.5, 1.3])
    _zbox(ax, Na, Nb, "$Z$", lab_side=-1)
    _zbox(ax, Nb, Nc, "$Z$", lab_side=-1)
    _zbox(ax, Nc, Na, "$Z$", lab_side=-1)
    for P in (Na, Nb, Nc):
        ax.add_patch(Circle(P, 0.07, color=INK, zorder=4))
    ya2, yb2, yc2 = 4.6, 1.3, -0.1
    ax.plot([x0, Na[0]], [ya2, ya2], color=INK, lw=1.3)
    ax.plot([x0, Nb[0]], [yb2, yb2], color=INK, lw=1.3)
    ax.plot([x0, Nc[0], Nc[0]], [yc2, yc2, Nc[1]], color=INK, lw=1.3)
    for y, nm in [(ya2, "a"), (yb2, "b"), (yc2, "c")]:
        ax.add_patch(Circle((x0, y), 0.07, fc="white", ec=INK, zorder=4))
        ax.text(x0 - 0.15, y, nm, ha="right", va="center", fontsize=10)
        _arr(ax, x0 + 0.35, y, x0 + 0.95, y, color=cI, lw=1.4, ms=11)
        ax.text(x0 + 0.65, y + 0.12, f"$I_{nm}$", color=cI, ha="center", va="bottom", fontsize=9)
    ax.text(Na[0] + 0.1, Na[1] + 0.12, "a", fontsize=9, va="bottom")
    ax.text(Nb[0] - 0.12, Nb[1] + 0.12, "b", fontsize=9, ha="right", va="bottom")
    ax.text(Nc[0] + 0.15, Nc[1] + 0.12, "c", fontsize=9, va="bottom")
    # phase currents inside the triangle (circulating a->b->c->a)
    cen = (Na + Nb + Nc) / 3
    for P, Q, nm in [(Na, Nb, "ab"), (Nb, Nc, "bc"), (Nc, Na, "ca")]:
        L = np.hypot(*(Q - P))
        u = (Q - P) / L
        q = P + 0.17 * L * u
        _arr(ax, *(q - 0.22 * u), *(q + 0.22 * u), color=COLORS[3], lw=1.6, ms=11)
        m = (P + Q) / 2
        inward = (cen - m) / np.hypot(*(cen - m))
        r = q + 0.42 * inward + 0.15 * u
        ax.text(r[0], r[1], f"$I_{{{nm}}}$", color=COLORS[3], fontsize=9, ha="center",
                va="center")
    ax.text(cen[0], cen[1] - 0.15, "phase\ncurrents", color=COLORS[3], fontsize=7.5,
            ha="center", va="center")
    # V_ab outside a-b edge
    u = (Nb - Na) / np.hypot(*(Nb - Na))
    nrm = np.array([u[1], -u[0]])
    if np.dot(nrm, cen - Na) > 0:
        nrm = -nrm
    p0 = Na + 0.85 * nrm + 0.35 * u
    p1 = Nb + 0.85 * nrm - 0.35 * u
    _arr(ax, *p1, *p0, color=cV, lw=1.0)
    pm = (p0 + p1) / 2 + 0.3 * nrm
    ax.text(pm[0], pm[1], "$V_{ab}$", color=cV, fontsize=9, ha="center", va="center")
    ax.text(10.1, -1.0, "(b) delta", fontsize=10, ha="center", fontweight="bold")
    ax.text(x0, 5.55, "$V_{ab}$: line voltage = phase voltage\n"
            "$I_{ab}$: phase current    $I_a$: line current", fontsize=8, va="bottom")
    save(fig, "10", "fig-10-2-star-delta-connections")


def fig_10_3():
    """Phase and line voltage phasors of a positive-sequence star."""
    Vp = 230.0
    Van, Vbn, Vcn = Vp, Vp * A ** 2, Vp * A
    Vab, Vbc, Vca = Van - Vbn, Vbn - Vcn, Vcn - Van
    fig, ax = new_fig(6.2, 5.0)
    ax.axis("off")
    ax.set_aspect("equal")
    o = 0j
    light = 0.35
    # line voltages from the origin (light)
    for V, col in [(Vab, COLORS[0]), (Vbc, COLORS[1]), (Vca, COLORS[2])]:
        _vec(ax, o, V, col, lw=1.6, alpha=light, zorder=1)
    # phase phasors
    for V, col, lab, off in [(Van, COLORS[0], "$V_{an}$ = 230∠0°", (10, -16)),
                             (Vbn, COLORS[1], "$V_{bn}$ = 230∠−120°", (-12, -14)),
                             (Vcn, COLORS[2], "$V_{cn}$ = 230∠120°", (14, 16))]:
        _vec(ax, o, V, col, lw=2.4)
        ax.text(V.real + off[0], V.imag + off[1], lab, color=col, fontsize=9,
                ha="left" if off[0] > 0 else "right", va="center")
    # closed triangle joining tips
    for Z0, Z1, col in [(Vbn, Van, COLORS[0]), (Vcn, Vbn, COLORS[1]), (Van, Vcn, COLORS[2])]:
        _vec(ax, Z0, Z1, col, lw=1.6, ls="-")
    # labels of line voltages from origin
    for V, col, lab in [(Vab, COLORS[0], "$V_{ab}$ = 400∠30°"), (Vbc, COLORS[1], "$V_{bc}$ = 400∠−90°"),
                        (Vca, COLORS[2], "$V_{ca}$ = 400∠150°")]:
        d = V / abs(V)
        p = V + 22 * d
        ax.text(p.real, p.imag, lab, color=col, fontsize=9, alpha=0.9,
                ha="left" if d.real > 0.2 else ("right" if d.real < -0.2 else "center"),
                va="bottom" if d.imag > 0.2 else ("top" if d.imag < -0.2 else "center"))
    # construction Van + (-Vbn) = Vab
    _vec(ax, Van, Van - Vbn, COLORS[1], lw=1.2, ls="--")
    mid = Van + (-Vbn) * 0.5
    ax.text(mid.real + 12, mid.imag, "$-V_{bn}$", color=COLORS[1], fontsize=9, va="center")
    ax.text(150, 250, "$V_{ab}=V_{an}+(-V_{bn})$", fontsize=9, ha="left")
    # 30 deg arc
    ax.add_patch(Arc((0, 0), 170, 170, theta1=0, theta2=30, color=INK, lw=1))
    ax.text(100 * np.cos(np.radians(15)), 100 * np.sin(np.radians(15)), "30°", fontsize=9,
            va="center")
    ax.add_patch(Circle((0, 0), 4, color=INK))
    ax.text(-10, -14, "$n$", fontsize=10, ha="right")
    # rotation arrow
    th = np.radians(np.linspace(-55, -15, 30))
    R = 330
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1)
    ax.annotate("", xy=(R * np.cos(th[-1]), R * np.sin(th[-1])),
                xytext=(R * np.cos(th[-3]), R * np.sin(th[-3])),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1, mutation_scale=10))
    ax.text(R * np.cos(np.radians(-40)) + 12, R * np.sin(np.radians(-40)) - 10,
            "rotation (ω),\nsequence abc", fontsize=8.5, ha="left", va="top")
    ax.set_xlim(-420, 470)
    ax.set_ylim(-430, 330)
    save(fig, "10", "fig-10-3-line-phase-phasors")


def fig_10_4():
    """Neutral displacement with a broken neutral and unbalanced resistive loads."""
    Vp = 230.0
    Vs = np.array([Vp, Vp * A ** 2, Vp * A])
    R = np.array([5.75, 11.5, 23.0])
    Y = 1 / R
    VN = np.sum(Vs * Y) / np.sum(Y)
    VL = Vs - VN
    fig, ax = new_fig(6.4, 5.0)
    ax.axis("off")
    ax.set_aspect("equal")
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(Vp * np.cos(th), Vp * np.sin(th), color="#999999", ls="--", lw=0.8)
    ax.text(Vp * np.cos(np.radians(200)) - 8, Vp * np.sin(np.radians(200)), "230 V",
            color="#777777", fontsize=8, ha="right")
    # line triangle
    tri = np.append(Vs, Vs[0])
    ax.plot(tri.real, tri.imag, color="#888888", lw=1.0)
    ax.text(-124, 45, "400 V", color="#777777", fontsize=8, ha="right", va="center")
    names = ["a", "b", "c"]
    cols = [COLORS[0], COLORS[1], COLORS[2]]
    for V, nm, col in zip(Vs, names, cols):
        _vec(ax, 0j, V, col, lw=1.2, alpha=0.45)
        ax.add_patch(Circle((V.real, V.imag), 4, color=INK, zorder=5))
    ax.text(Vs[0].real + 10, Vs[0].imag - 4, "a", fontsize=11, va="center")
    ax.text(Vs[1].real - 8, Vs[1].imag - 8, "b", fontsize=11, ha="right", va="top")
    ax.text(Vs[2].real - 8, Vs[2].imag + 8, "c", fontsize=11, ha="right", va="bottom")
    # load voltages from N
    for V, nm, col in zip(VL, names, cols):
        _vec(ax, VN, VN + V, col, lw=2.4)
    labpos = [((105, 14), f"$V_{{aN}}$ = {abs(VL[0]):.1f} V", "left"),
              ((55, -155), f"$V_{{bN}}$ = {abs(VL[1]):.1f} V", "left"),
              ((0, 110), f"$V_{{cN}}$ = {abs(VL[2]):.1f} V", "left")]
    for (xy, lab, ha), col in zip(labpos, cols):
        ax.text(xy[0], xy[1], lab, color=col, fontsize=9.5, ha=ha, va="center",
                fontweight="bold", bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.0),
                zorder=7)
    # neutrals
    ax.add_patch(Circle((0, 0), 5, color=INK, zorder=6))
    ax.text(-16, -4, "$n$\n(source)", fontsize=8.5, ha="right", va="center")
    ax.add_patch(Circle((VN.real, VN.imag), 7, color=COLORS[3], zorder=6))
    _vec(ax, 0j, VN, COLORS[3], lw=1.6)
    ax.text(100, -48, f"$N$ (load)\n$V_{{Nn}}$ = {abs(VN):.1f} V ∠{np.degrees(np.angle(VN)):.1f}°"
            .replace("-", "−"), color=COLORS[3], fontsize=9, ha="left", va="top")
    ax.text(-400, -300, "$R_a$ = 5.75 Ω (9.2 kW)\n$R_b$ = 11.5 Ω (4.6 kW)\n$R_c$ = 23 Ω (2.3 kW)\n"
            "neutral broken", fontsize=9, va="top",
            bbox=dict(fc="white", ec="#BBBBBB", lw=0.6, boxstyle="round,pad=0.4"))
    ax.set_xlim(-410, 330)
    ax.set_ylim(-330, 300)
    save(fig, "10", "fig-10-4-broken-neutral-phasors")


def fig_10_5():
    """Two-wattmeter connection and readings versus load angle."""
    fig = plt.figure(figsize=(6.9, 3.6))
    ax = fig.add_axes([0.0, 0.05, 0.44, 0.9])
    bx = fig.add_axes([0.56, 0.16, 0.42, 0.64])
    ax.set_xlim(-0.3, 6.6)
    ax.set_ylim(-0.3, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ys = {"a": 3.8, "b": 2.4, "c": 1.0}
    box(ax, -0.2, 0.4, 1.1, 4.0, "3-phase\nsource", fontsize=8, fc="#F4F4F4")
    box(ax, 5.3, 0.4, 1.2, 4.0, "load\n(three-\nwire)", fontsize=8, fc="#F4F4F4")
    for k, y in ys.items():
        ax.plot([0.9, 5.3], [y, y], color=INK, lw=1.3)
        ax.text(1.05, y + 0.08, k, fontsize=10, va="bottom")
    # wattmeters
    for name, line, xw, sgn in [("W$_1$", "a", 2.9, -1), ("W$_2$", "c", 2.9, 1)]:
        y = ys[line]
        ax.add_patch(Circle((xw, y), 0.55, fc="white", ec=INK, lw=1.3, zorder=3))
        ax.plot([xw - 0.38, xw + 0.38], [y, y], color=INK, lw=3.0, zorder=4)   # current coil
        ax.text(xw, y + sgn * -0.25 if False else y + 0.62, name, ha="center", va="bottom",
                fontsize=9)
        # voltage coil lead to line b
        xv = xw + 0.95
        ax.plot([xv, xv], [y, ys["b"]], color=COLORS[0], lw=1.1)
        ax.add_patch(Rectangle((xv - 0.12, (y + ys["b"]) / 2 - 0.3), 0.24, 0.6, fc="white",
                               ec=COLORS[0], lw=1.1, zorder=3))
        for yy in (y, ys["b"]):
            ax.add_patch(Circle((xv, yy), 0.06, color=INK, zorder=4))
    ax.text(4.0, 3.1, "voltage\ncoil", fontsize=7, color=COLORS[0], ha="left", va="center")
    ax.text(2.9, 0.15, "current coil in line", fontsize=7, ha="center", va="top")
    ax.text(3.2, 4.95, "W$_1$: $I_a$, $V_{ab}$      W$_2$: $I_c$, $V_{cb}$", fontsize=8,
            ha="center", va="bottom")
    # plot
    phi = np.linspace(-90, 90, 721)
    pr = np.radians(phi)
    w1 = np.cos(np.radians(30) + pr)
    w2 = np.cos(np.radians(30) - pr)
    bx.axhline(0, color=INK, lw=0.6)
    bx.plot(phi, w1, color=COLORS[0], label=r"$W_1=\cos(30^\circ+\varphi)$")
    bx.plot(phi, w2, color=COLORS[1], ls="--", label=r"$W_2=\cos(30^\circ-\varphi)$")
    bx.plot(phi, w1 + w2, color=INK, lw=1.4, ls="-.", label="$W_1+W_2=\\sqrt{3}\\cos\\varphi$")
    p0 = 36.87
    for val, col in [(np.cos(np.radians(30 + p0)), COLORS[0]), (np.cos(np.radians(30 - p0)), COLORS[1])]:
        bx.plot(p0, val, "o", color=col, ms=5)
    bx.axvline(p0, color="#999999", lw=0.7, ls=":")
    bx.text(p0 - 2, 0.30, "0.393", fontsize=8, color=COLORS[0], ha="right")
    bx.text(p0 - 2, 1.04, "0.993", fontsize=8, color=COLORS[1], ha="right")
    bx.text(p0 + 1.5, 1.62, "36.87°\n(pf 0.8)", fontsize=7.5, color="#555555", va="center")
    bx.plot(60, 0, "s", color=COLORS[0], ms=5)
    bx.annotate("$W_1$ = 0 at 60° (pf 0.5)", xy=(60, 0), xytext=(-25, -0.4), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    bx.set_xlim(-90, 90)
    bx.set_ylim(-0.6, 1.85)
    bx.set_xticks([-90, -60, -30, 0, 30, 60, 90])
    bx.set_xlabel("load angle $\\varphi$ (°)  [lagging > 0]")
    bx.set_ylabel("reading / $V_LI_L$")
    bx.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7.5)
    save(fig, "10", "fig-10-5-two-wattmeter-method")


def fig_10_6():
    """Phase and neutral currents with third-harmonic content."""
    t = np.linspace(0, 0.040, 4001)
    wt = W * t
    I1, I3 = 141.4, 99.0
    # third harmonic in antiphase with sin(3 wt) so the current peaks at the voltage peak
    ph = [I1 * np.sin(wt - k * 2 * np.pi / 3) - I3 * np.sin(3 * (wt - k * 2 * np.pi / 3))
          for k in range(3)]
    iN = sum(ph)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.8), sharex=True)
    tm = t * 1e3
    for y, col, ls, nm in zip(ph, COLORS[:3], ["-", "--", ":"], "abc"):
        a1.plot(tm, y, color=col, ls=ls, lw=1.6 if ls != ":" else 2.0, label=f"$i_{nm}$")
    a1.set_ylim(-350, 350)
    a1.set_ylabel("phase current (A)")
    a1.axhline(0, color=INK, lw=0.5)
    a1.legend(loc="lower right", bbox_to_anchor=(1.0, 0.98), ncol=3, fontsize=8.5)
    a1.text(0.5, -335, "each phase: 100 A at 50 Hz + 70 A at 150 Hz (rms);  phase rms 122 A",
            fontsize=8.5, va="bottom")
    a2.plot(tm, iN, color=COLORS[3], lw=1.8,
            label=f"$i_N=i_a+i_b+i_c$: 150 Hz, peak {np.max(iN):.0f} A, neutral rms 210 A")
    a2.plot(tm, np.zeros_like(tm), color=INK, ls="--", lw=1.0,
            label="fundamental-only neutral current (zero)")
    a2.set_ylim(-350, 350)
    a2.set_ylabel("neutral current (A)")
    a2.set_xlabel("time $t$ (ms)")
    a2.set_xlim(0, 40)
    a2.legend(loc="lower center", fontsize=8, ncol=1, bbox_to_anchor=(0.5, 0.98))
    fig.tight_layout()
    save(fig, "10", "fig-10-6-triplen-neutral-current")


if __name__ == "__main__":
    fig_10_1()
    fig_10_2()
    fig_10_3()
    fig_10_4()
    fig_10_5()
    fig_10_6()
