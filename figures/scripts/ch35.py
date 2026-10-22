"""Figures for Chapter 35 — Control Design Fundamentals.

Run from the repository root:  python figures/scripts/ch35.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Arc, Polygon  # noqa: E402
from scipy import signal  # noqa: E402

from figstyle import new_fig, schematic, box, arrow, save, COLORS, INK, GRID  # noqa: E402


# ---------------------------------------------------------------------------
# block-diagram helpers
def sj(ax, x, y, r=0.22, signs=None, fs=8):
    ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.1, zorder=3))
    off = {"w": (-r - 0.08, r * 0.85), "s": (r * 0.9, -r - 0.12), "n": (r * 0.9 + 0.08, r + 0.1),
           "e": (r + 0.08, r * 0.85)}
    for pos, sg in (signs or {}).items():
        dx, dy = off[pos]
        ax.text(x + dx, y + dy, sg, fontsize=fs + 1, ha="center", va="center")


def blk(ax, xc, yc, w, h, text, fs=9, fc="#EEF3F8"):
    box(ax, xc - w / 2, yc - h / 2, w, h, text, fontsize=fs, fc=fc)


def line(ax, pts, color=INK, lw=1.1, ls="-", head=True, double=False):
    xs, ys = zip(*pts)
    if double:
        ax.plot(xs, ys, color=color, lw=3.2, solid_capstyle="butt", zorder=1)
        ax.plot(xs, ys, color="white", lw=1.4, solid_capstyle="butt", zorder=1)
    else:
        ax.plot(xs, ys, color=color, lw=lw, ls=ls)
    if head:
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10,
                                    shrinkA=0, shrinkB=0))


def dot(ax, x, y):
    ax.plot(x, y, "o", color=INK, ms=3.5, zorder=4)


def lab(ax, x, y, t, fs=9, **kw):
    kw.setdefault("ha", "center")
    kw.setdefault("va", "bottom")
    ax.text(x, y, t, fontsize=fs, **kw)


def settling(t, y, band=0.02, fv=1.0):
    out = np.where(np.abs(y - fv) > band * abs(fv))[0]
    return t[out[-1]] if len(out) else 0.0


# ---------------------------------------------------------------------------
def fig_step_specs():
    """Fig 35.1: step-response specifications on a zeta = 0.5, wn = 0.833 response."""
    fig, ax = new_fig(6.4, 3.9)
    z, wn = 0.5, 5 / 6
    t = np.linspace(0, 15, 15001)
    _, y = signal.step(([wn ** 2], [1, 2 * z * wn, wn ** 2]), T=t)
    t10, t90 = t[np.argmax(y >= 0.1)], t[np.argmax(y >= 0.9)]
    ip = y.argmax()
    ts = settling(t, y)
    ax.axhspan(0.98, 1.02, color=COLORS[2], alpha=0.15, lw=0)
    ax.axhline(1.0, color="0.4", lw=0.8, ls="--")
    ax.plot(t, y, color=COLORS[0], lw=2.0)
    for lv in (0.1, 0.9):
        ax.axhline(lv, color="0.6", lw=0.7, ls=":")
        ax.text(14.9, lv + 0.015, f"{lv:.0%}".replace("%", " %"), fontsize=7.5, color="0.4", ha="right", va="bottom")
    ax.plot([t10, t90], [0.1, 0.9], "o", color=COLORS[1], ms=4)
    ax.annotate("", xy=(t90, 0.04), xytext=(t10, 0.04),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.0, mutation_scale=8, shrinkA=0, shrinkB=0))
    for tv in (t10, t90):
        ax.plot([tv, tv], [0.04, 0.9 if tv == t90 else 0.1], color=COLORS[1], lw=0.7, ls=":")
    ax.text((t10 + t90) / 2, 0.065, f"$t_r$ = {t90 - t10:.2f} s", fontsize=8, color=COLORS[1], ha="center", va="bottom")
    # peak
    ax.plot(t[ip], y[ip], "o", color=COLORS[3], ms=5)
    ax.plot([t[ip], t[ip]], [0, y[ip]], color=COLORS[3], lw=0.7, ls=":")
    ax.text(t[ip], 0.0 + 0.2, f"$t_p$ = {t[ip]:.2f} s", fontsize=8, color=COLORS[3], ha="left", va="bottom",
            rotation=90)
    ax.annotate("", xy=(t[ip] + 0.6, y[ip]), xytext=(t[ip] + 0.6, 1.0),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[3], lw=1.0, mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(t[ip] + 0.75, 1.215, f"$M_p$ = {100*(y[ip]-1):.1f} %  (peak {y[ip]:.3f})",
            fontsize=8, color=COLORS[3], va="center")
    # settling
    ax.plot([ts, ts], [0, 1.0], color=COLORS[2], lw=1.0, ls="--")
    ax.text(ts + 0.12, 0.80, f"$t_s$ = {ts:.1f} s\n(±2 % band)", fontsize=8, color=COLORS[2], va="center")
    ax.text(14.9, 1.03, "final value 1", fontsize=7.5, color="0.4", ha="right", va="bottom")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output $y(t)$")
    ax.grid(True, color=GRID, lw=0.5)
    # inset s-plane
    ins = ax.inset_axes([0.71, 0.13, 0.27, 0.40])
    sr, si = -z * wn, wn * np.sqrt(1 - z ** 2)
    ins.axhline(0, color=INK, lw=0.6)
    ins.axvline(0, color=INK, lw=0.6)
    for sg in (1, -1):
        ins.plot(sr, sg * si, "x", color=INK, ms=7, mew=1.8)
        ins.plot([0, sr], [0, sg * si], color=COLORS[0], lw=0.9)
    ins.add_patch(Arc((0, 0), 0.5, 0.5, theta1=120, theta2=180, color=COLORS[1], lw=1.1))
    ins.text(-0.32, 0.2, "60°", fontsize=7, color=COLORS[1], ha="right")
    ins.text(sr + 0.04, si + 0.05, f"${sr:.3f}\\pm j{si:.3f}$", fontsize=6.5, ha="left", va="bottom")
    ins.text(sr / 2 + 0.07, si / 2 + 0.05, "$\\omega_n$", fontsize=8, color=COLORS[0], ha="left")
    ins.set_xlim(-1.0, 0.3)
    ins.set_ylim(-1.0, 1.0)
    ins.set_aspect("equal")
    ins.set_xticks([-0.5, 0])
    ins.set_yticks([-0.5, 0, 0.5])
    ins.tick_params(labelsize=6.5)
    ins.set_title("s-plane", fontsize=7.5, pad=2)
    print(f"  35.1 tr {t90-t10:.2f} tp {t[ip]:.2f} Mp {100*(y[ip]-1):.1f} ts {ts:.2f}")
    return save(fig, "35", "fig-35-1-step-response-specs")


# ---------------------------------------------------------------------------
def fig_practical_pid():
    """Fig 35.2: practical PID with set-point weighting, filtered D on measurement, anti-windup."""
    fig, ax = schematic(6.8, 4.6, xlim=(0, 13.6), ylim=(0, 9.2))
    yP, yI, yD = 7.0, 4.6, 2.0
    # inputs
    lab(ax, 0.3, 8.35, "$r$ (set point)", ha="left")
    lab(ax, 0.3, 0.55, "$y$ (measurement)", ha="left")
    xr, xy_ = 0.9, 1.4
    ax.plot([xr, xr], [8.3, yI], color=INK, lw=1.1)
    ax.plot([xy_, xy_], [0.85, yP - 0.6], color=INK, lw=1.1)
    dot(ax, xr, yI)
    dot(ax, xy_, yI - 0.75)
    dot(ax, xy_, yD)
    # P path: b r - y
    blk(ax, 2.2, yP + 0.0, 0.7, 0.6, "$b$", fs=9)
    ax.plot([xr, xr], [yP, yP], color=INK)
    dot(ax, xr, yP)
    line(ax, [(xr, yP), (1.85, yP)])
    line(ax, [(2.55, yP), (3.38, yP)])
    sj(ax, 3.6, yP, signs={"w": "+", "s": "−"})
    line(ax, [(xy_, yP - 0.6), (3.6, yP - 0.6), (3.6, yP - 0.22)])
    line(ax, [(3.82, yP), (4.9, yP)])
    blk(ax, 5.5, yP, 1.2, 0.7, "$K_p$", fs=10)
    # I path: r - y
    line(ax, [(xr, yI), (2.98, yI)])
    sj(ax, 3.2, yI, signs={"w": "+", "s": "−"})
    line(ax, [(xy_, yI - 0.75), (3.2, yI - 0.75), (3.2, yI - 0.22)])
    line(ax, [(3.42, yI), (4.4, yI)])
    blk(ax, 5.0, yI, 1.2, 1.05, "$\\dfrac{K_p}{T_i}$", fs=10)
    line(ax, [(5.6, yI), (6.38, yI)])
    sj(ax, 6.6, yI, signs={"w": "+", "s": "+"})
    line(ax, [(6.82, yI), (7.3, yI)])
    blk(ax, 7.75, yI, 0.9, 0.75, "$\\dfrac{1}{s}$", fs=10)
    # D path: -y
    line(ax, [(xy_, yD), (2.6, yD)])
    blk(ax, 3.0, yD, 0.7, 0.6, "$-1$", fs=9)
    line(ax, [(3.35, yD), (4.0, yD)])
    blk(ax, 5.5, yD, 3.0, 1.0, "$\\dfrac{K_pT_ds}{1+T_ds/N}$", fs=10)
    # sum
    xs = 9.0
    sj(ax, xs, yI, signs={"n": "+", "w": "+", "s": "+"})
    line(ax, [(6.1, yP), (xs, yP), (xs, yI + 0.22)])
    line(ax, [(8.2, yI), (xs - 0.22, yI)])
    line(ax, [(7.0, yD), (xs, yD), (xs, yI - 0.22)])
    # saturation
    line(ax, [(xs + 0.22, yI), (10.4, yI)])
    lab(ax, 9.8, yI + 0.1, "$v$")
    bx = 11.0
    blk(ax, bx, yI, 1.2, 1.0, "", fs=9)
    ax.plot([bx - 0.45, bx - 0.2, bx + 0.2, bx + 0.45], [yI - 0.3, yI - 0.3, yI + 0.3, yI + 0.3], color=INK, lw=1.2)
    ax.text(bx, yI + 0.6, "$u_{min}$, $u_{max}$", fontsize=8, ha="center", va="bottom")
    line(ax, [(bx + 0.6, yI), (13.3, yI)])
    lab(ax, 12.9, yI + 0.1, "$u$")
    ax.text(13.3, yI - 0.15, "to plant", fontsize=7.5, ha="right", va="top", color="0.35")
    # anti-windup: (u - v) / Tt
    dot(ax, 12.2, yI)
    dot(ax, 9.9, yI)
    ya = 3.2
    sj(ax, 11.0, ya)
    line(ax, [(12.2, yI), (12.2, ya), (11.22, ya)])
    line(ax, [(9.9, yI), (9.9, ya - 0.0), (10.78, ya)])
    ax.text(10.62, ya + 0.22, "−", fontsize=9, ha="center")
    ax.text(11.42, ya + 0.22, "+", fontsize=9, ha="center")
    line(ax, [(11.0, ya - 0.22), (11.0, 2.9 - 0.3), (8.6, 2.9 - 0.3)], head=False)
    blk(ax, 8.0, 2.6, 1.0, 0.85, "$\\dfrac{1}{T_t}$", fs=9.5, fc="#FFF3DD")
    line(ax, [(7.5, 2.6), (6.6, 2.6), (6.6, yI - 0.22)])
    ax.text(11.12, 2.78, "$u-v$", fontsize=8.5, ha="left", va="center", color=COLORS[1])
    ax.text(6.75, 3.15, "anti-windup\n(back-calculation)", fontsize=7.5, color=COLORS[1], ha="left", va="bottom")
    # labels
    ax.text(4.2, 8.25, "proportional on weighted set point", fontsize=7.5, color="0.35", ha="left")
    ax.text(3.6, 5.3, "integral on error", fontsize=7.5, color="0.35", ha="left")
    ax.text(4.0, 0.85, "filtered derivative on measurement (no derivative kick)", fontsize=7.5,
            color="0.35", ha="left")
    box(ax, 10.3, 6.9, 3.2, 1.6, "", fc="#F7F7F7")
    ax.text(11.9, 7.7, "$b=0$ – $1$\n$N=5$ – $20$\n$T_d<T_t<T_i$", fontsize=8.5, ha="center", va="center",
            linespacing=1.4)
    return save(fig, "35", "fig-35-2-practical-pid")


# ---------------------------------------------------------------------------
def _sim_pi(Kp, Ti, mode, K=2.0, tau=120.0, th=20.0, dt=0.01, T=600.0):
    """Exact-delay simulation of PI + FOPDT (sample dt)."""
    n = int(round(T / dt))
    nd = int(round(th / dt))
    ubuf = np.zeros(n + nd + 1)
    a = np.exp(-dt / tau)
    yv, I = 0.0, 0.0
    out = np.zeros(n)
    r = 1.0 if mode == "sp" else 0.0
    dist = 1.0 if mode == "load" else 0.0
    for k in range(n):
        e = r - yv
        I += Kp / Ti * e * dt
        ubuf[k + nd] = Kp * e + I + dist
        yv = a * yv + (1 - a) * K * ubuf[k]
        out[k] = yv
    return np.arange(1, n + 1) * dt, out


def fig_tuning():
    """Fig 35.3: SIMC vs Ziegler-Nichols PI on K=2, tau=120 s, theta=20 s."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.0), sharex=True,
                                 gridspec_kw=dict(hspace=0.22))
    tunings = [("SIMC", 1.5, 120.0, "-", COLORS[0], 61), ("Ziegler–Nichols", 2.7, 66.6, "--", COLORS[1], 29)]
    for name, Kp, Ti, ls, col, pm in tunings:
        t, y = _sim_pi(Kp, Ti, "sp")
        ts = settling(t, y)
        os_ = (y.max() - 1) * 100
        a1.plot(t, y, ls, color=col, label=f"{name}: $K_p$ = {Kp}, $T_i$ = {Ti:g} s  (PM ≈ {pm}°)")
        a1.plot([ts, ts], [0, 1], ":", color=col, lw=0.9)
        print(f"  35.3 {name}: OS {os_:.1f}% ts {ts:.0f}s")
        a1.text(ts + 5, 0.12 if name == "SIMC" else 0.25, f"$t_s$ ≈ {ts:.0f} s", fontsize=7.8, color=col)
        ip = y.argmax()
        a1.annotate(f"{os_:.1f} %", xy=(t[ip], y[ip]), xytext=(t[ip] + (40 if name != "SIMC" else 50), y[ip] + (0.05 if name != "SIMC" else 0.3)), fontsize=8, color=col,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=col))
        t, yl = _sim_pi(Kp, Ti, "load")
        a2.plot(t, yl, ls, color=col, label=name)
        ip = yl.argmax()
        a2.annotate(f"peak {yl[ip]:.2f} °C", xy=(t[ip], yl[ip]), xytext=(t[ip] + 45, yl[ip] + 0.04),
                    fontsize=8, color=col, arrowprops=dict(arrowstyle="-", lw=0.6, color=col))
        print(f"  35.3 {name}: load peak {yl[ip]:.3f} at {t[ip]:.0f}s, IAE {np.sum(np.abs(yl))*0.01:.0f}")
    a1.axhspan(0.98, 1.02, color="0.85", lw=0)
    a1.axhline(1, color="0.4", lw=0.8, ls="--")
    a1.annotate("dead time 20 s", xy=(20, 0.0), xytext=(45, 0.45), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    a1.set_ylim(0, 1.75)
    a1.set_ylabel("Normalised temperature")
    a1.set_title("(a) unit set-point step", fontsize=9.5, loc="left")
    a1.legend(loc="upper right", fontsize=7.6)
    a1.grid(True, color=GRID, lw=0.5)
    a2.axhline(0, color="0.4", lw=0.8)
    a2.set_ylim(-0.1, 0.65)
    a2.set_xlim(0, 600)
    a2.set_xlabel("Time (s)")
    a2.set_ylabel("Temperature deviation (°C)")
    a2.set_title("(b) 1 % heater-equivalent load step at t = 0 (2 °C open-loop)", fontsize=9.5, loc="left")
    a2.legend(loc="upper right", fontsize=7.8)
    a2.grid(True, color=GRID, lw=0.5)
    return save(fig, "35", "fig-35-3-tuning-comparison")


# ---------------------------------------------------------------------------
def fig_lead_lag():
    """Fig 35.4: Bode of P, lead and lag on the antenna servo + inset step responses."""
    fig = plt.figure(figsize=(6.8, 5.4))
    am = fig.add_axes([0.10, 0.55, 0.58, 0.40])
    ap = fig.add_axes([0.10, 0.09, 0.58, 0.40], sharex=am)
    w = np.logspace(-3, 2, 3000)
    s = 1j * w
    G = 1 / (s * (s + 1) * (s + 5))
    designs = [("P-only $K=10$", 10 + 0 * s, ([10], [1]), "-", COLORS[1]),
               ("lead $10(s+1)/(0.1s+1)$", 10 * (s + 1) / (0.1 * s + 1), ([10, 10], [0.1, 1]), "-", COLORS[0]),
               ("lag $3.588(s+0.06)/(s+0.0215)$", 3.588 * (s + 0.06) / (s + 0.0215),
                ([3.588, 3.588 * 0.06], [1, 0.0215]), "--", COLORS[2])]
    wf = np.logspace(-3, 2, 400001)
    sf = 1j * wf
    Gf = 1 / (sf * (sf + 1) * (sf + 5))
    results = []
    for name, C, (nc, dc), ls, col in designs:
        L = C * G
        am.semilogx(w, 20 * np.log10(np.abs(L)), ls, color=col, label=name)
        ap.semilogx(w, np.degrees(np.unwrap(np.angle(L))), ls, color=col)
        Cf = np.polyval(nc, sf) / np.polyval(dc, sf)
        Lf = Cf * Gf
        i = np.argmin(np.abs(np.abs(Lf) - 1))
        wc = wf[i]
        pm = 180 + np.degrees(np.unwrap(np.angle(Lf)))[i]
        results.append((name, nc, dc, wc, pm, col, ls))
        am.plot(wc, 0, "o", color=col, ms=4.5, zorder=5)
        ap.annotate("", xy=(wc, -180 + pm), xytext=(wc, -180),
                    arrowprops=dict(arrowstyle="<|-|>", color=col, lw=1.1, mutation_scale=8, shrinkA=0, shrinkB=0))
    am.axhline(0, color="0.4", lw=0.8)
    ap.axhline(-180, color="0.4", lw=0.8)
    pmtxt = {COLORS[1]: (0.38, -200), COLORS[0]: (3.0, -125), COLORS[2]: (0.0015, -155)}
    for name, nc, dc, wc, pm, col, ls in results:
        x, yv = pmtxt[col]
        ap.text(x, yv, f"PM {pm:.1f}° at {wc:.2f} rad/s", fontsize=7.6, color=col,
                ha="left" if col != COLORS[1] else "right", va="center")
    am.set_ylim(-80, 80)
    am.set_ylabel("|L| (dB)")
    am.grid(True, which="both", color=GRID, lw=0.5)
    am.legend(loc="lower left", fontsize=7.6)
    am.tick_params(labelbottom=False)
    am.text(0.08, 62, "low-frequency gain of lag = P-only ($K_v$ = 2)", fontsize=7.5, color="0.3", va="top")
    ap.set_ylim(-270, -90)
    ap.set_yticks([-270, -225, -180, -135, -90])
    ap.set_ylabel("∠L (degrees)")
    ap.set_xlabel("Frequency ω (rad/s)")
    ap.set_xlim(1e-3, 100)
    ap.grid(True, which="both", color=GRID, lw=0.5)
    # inset step responses (closed loop, unity feedback)
    ai = fig.add_axes([0.76, 0.30, 0.23, 0.42])
    t = np.linspace(0, 20, 20001)
    for name, nc, dc, wc, pm, col, ls in results:
        nL = np.polymul(nc, [1])
        dL = np.polymul(dc, [1, 6, 5, 0])
        _, yv = signal.step((nL, np.polyadd(dL, nL)), T=t)
        os_ = (yv.max() - 1) * 100
        ts = settling(t, yv)
        short = name.split(" ")[0]
        ai.plot(t, yv, ls, color=col, lw=1.4, label=f"{short}: {os_:.1f} %, $t_s$ {ts:.1f} s")
        print(f"  35.4 {short}: wc {wc:.3f} PM {pm:.1f} OS {os_:.1f} ts {ts:.1f}")
    ai.axhline(1, color="0.5", lw=0.7, ls=":")
    ai.set_xlim(0, 20)
    ai.set_ylim(0, 1.6)
    ai.tick_params(labelsize=7)
    ai.set_xlabel("Time (s)", fontsize=8)
    ai.set_title("closed-loop step", fontsize=8.5)
    ai.grid(True, color=GRID, lw=0.5)
    ai.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=7.2, handlelength=1.4)
    return save(fig, "35", "fig-35-4-lead-lag-bode")


# ---------------------------------------------------------------------------
def fig_state_feedback():
    """Fig 35.5: state feedback u = -K x_hat + N r with a Luenberger observer."""
    fig, ax = schematic(6.8, 5.0, xlim=(0, 13.6), ylim=(0, 10.0))
    blue, orange = COLORS[0], COLORS[1]
    # ---- plant (top)
    yp = 8.0
    box(ax, 3.3, 6.65, 9.9, 2.75, "", fc="#F5F8FB", ec="0.6")
    ax.text(3.45, 9.25, "plant", fontsize=8.5, color="0.35", va="center")
    blk(ax, 4.5, yp, 0.9, 0.7, "$B$", fs=10)
    line(ax, [(4.95, yp), (5.98, yp)], double=True)
    sj(ax, 6.2, yp, signs={"w": "+", "s": "+"})
    line(ax, [(6.42, yp), (7.2, yp)], double=True)
    lab(ax, 6.8, yp + 0.12, "$\\dot{\\mathbf{x}}$")
    blk(ax, 7.7, yp, 0.9, 0.75, "$\\dfrac{1}{s}$", fs=10)
    line(ax, [(8.15, yp), (10.3, yp)], double=True)
    lab(ax, 9.0, yp + 0.12, "$\\mathbf{x}$")
    dot(ax, 9.3, yp)
    blk(ax, 10.75, yp, 0.9, 0.7, "$C$", fs=10)
    line(ax, [(11.2, yp), (13.4, yp)])
    lab(ax, 12.4, yp + 0.12, "$y$")
    dot(ax, 12.0, yp)
    line(ax, [(9.3, yp), (9.3, 7.05), (8.15, 7.05)], double=True, head=False)
    blk(ax, 7.7, 7.05, 0.9, 0.6, "$A$", fs=10)
    line(ax, [(7.25, 7.05), (6.2, 7.05), (6.2, yp - 0.22)], double=True)
    # ---- observer (bottom)
    yo = 3.6
    box(ax, 3.3, 1.35, 9.9, 3.85, "", fc="#FBF7F2", ec="0.6")
    ax.text(3.45, 4.95, "observer", fontsize=8.5, color="0.35", va="center")
    blk(ax, 4.5, yo, 0.9, 0.7, "$B$", fs=10)
    line(ax, [(4.95, yo), (5.98, yo)], double=True)
    sj(ax, 6.2, yo, signs={"w": "+", "s": "+", "n": "+"})
    line(ax, [(6.42, yo), (7.2, yo)], double=True)
    blk(ax, 7.7, yo, 0.9, 0.75, "$\\dfrac{1}{s}$", fs=10)
    line(ax, [(8.15, yo), (9.3, yo)], double=True, head=False)
    lab(ax, 8.75, yo + 0.12, "$\\hat{\\mathbf{x}}$")
    dot(ax, 9.3, yo)
    line(ax, [(9.3, yo), (9.3, 2.6), (8.15, 2.6)], double=True, head=False)
    blk(ax, 7.7, 2.6, 0.9, 0.6, "$A$", fs=10)
    line(ax, [(7.25, 2.6), (6.2, 2.6), (6.2, yo - 0.22)], double=True)
    # C x_hat and innovation
    line(ax, [(9.3, yo), (10.3, yo)], double=True)
    blk(ax, 10.75, yo, 0.9, 0.7, "$C$", fs=10)
    line(ax, [(11.2, yo), (11.78, yo)])
    lab(ax, 11.5, yo - 0.5, "$C\\hat{\\mathbf{x}}$", va="top", fs=8.5)
    sj(ax, 12.0, yo, signs={"n": "+", "s": ""})
    ax.text(11.62, yo + 0.3, "−", fontsize=9, ha="center")
    line(ax, [(12.0, yp), (12.0, yo + 0.22)])
    line(ax, [(12.0, yo - 0.22), (12.0, 4.55 - 0.0)], head=False)
    # innovation y - C x_hat goes up then left to L
    ax.plot([12.0, 12.0], [yo - 0.22, yo - 0.22], color=INK)
    line(ax, [(12.22, yo), (12.6, yo), (12.6, 4.65), (7.4, 4.65)], head=False)
    blk(ax, 6.9, 4.65, 1.0, 0.6, "$L$", fs=10, fc="#FFF3DD")
    line(ax, [(6.4, 4.65), (6.2, 4.65), (6.2, yo + 0.22)])
    ax.text(10.0, 4.75, "$y-C\\hat{\\mathbf{x}}$", fontsize=8.5, ha="center", va="bottom")
    # ---- controller (left)
    yc = 5.8
    lab(ax, 0.3, yc + 0.12, "$r$", ha="left")
    line(ax, [(0.3, yc), (0.9, yc)])
    blk(ax, 1.35, yc, 0.9, 0.7, "$N$", fs=10)
    line(ax, [(1.8, yc), (2.38, yc)])
    sj(ax, 2.6, yc, signs={"w": "+", "s": "−"})
    line(ax, [(2.82, yc), (3.0, yc)], head=False)
    ax.plot([3.0, 3.0], [yo, yp], color=INK, lw=1.1)
    lab(ax, 3.15, yc + 0.1, "$u$", ha="left")
    dot(ax, 3.0, yc)
    line(ax, [(3.0, yp), (4.05, yp)])
    line(ax, [(3.0, yo), (4.05, yo)])
    # K feedback from x_hat
    line(ax, [(9.3, yo - 0.0), (9.3, 1.85), (3.35, 1.85)], double=True, head=False)
    blk(ax, 2.6, 1.85, 1.4, 0.65, "$K$", fs=10, fc="#EAF4EE")
    line(ax, [(1.9, 1.85), (1.4, 1.85), (1.4, 4.4), (2.6, 4.4), (2.6, yc - 0.22)])
    lab(ax, 1.3, 3.1, "$K\\hat{\\mathbf{x}}$", ha="right", va="center", fs=8.5)
    # numbers
    ax.text(0.15, 0.85, "motor example:  $K=[5\\ \\ 0.6]$,  $N=5$  →  controller poles $-7\\pm j7.14$;"
            "     $L=[68\\ \\ 2364]^T$  →  observer poles $-35\\pm j35.7$",
            fontsize=7.5, ha="left", va="center")
    ax.text(0.15, 0.3, "double lines carry vectors (state $\\mathbf{x}$, estimate $\\hat{\\mathbf{x}}$);"
            "  $u=-K\\hat{\\mathbf{x}}+Nr$", fontsize=7.8, ha="left", va="center", color="0.35")
    return save(fig, "35", "fig-35-5-state-feedback-observer")


# ---------------------------------------------------------------------------
def fig_digital_loop():
    """Fig 35.6: digital control loop and timing diagram."""
    fig = plt.figure(figsize=(6.8, 5.6))
    ax = fig.add_axes([0.0, 0.50, 1.0, 0.50])
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    y = 3.6
    lab(ax, 0.55, y + 0.12, "$r[k]$")
    line(ax, [(0.2, y), (1.18, y)])
    sj(ax, 1.4, y, signs={"w": "+", "s": "−"})
    line(ax, [(1.62, y), (2.3, y)])
    lab(ax, 1.95, y + 0.12, "$e[k]$", fs=8.5)
    blk(ax, 3.45, y, 2.3, 1.1, "controller $D(z)$\ndifference eq.", fs=8)
    line(ax, [(4.6, y), (5.3, y)])
    lab(ax, 4.95, y + 0.12, "$u[k]$", fs=8.5)
    blk(ax, 6.4, y, 2.2, 1.1, "DAC / PWM\nzero-order hold", fs=8)
    line(ax, [(7.5, y), (8.4, y)])
    lab(ax, 7.95, y + 0.12, "$u(t)$", fs=8.5)
    blk(ax, 9.4, y, 2.0, 1.1, "plant $G(s)$", fs=9, fc="#EAF4EE")
    line(ax, [(10.4, y), (13.3, y)])
    lab(ax, 12.6, y + 0.12, "$y(t)$")
    dot(ax, 11.6, y)
    yb = 1.5
    line(ax, [(11.6, y), (11.6, yb), (10.4, yb)])
    blk(ax, 9.4, yb, 2.0, 1.0, "anti-aliasing\nfilter", fs=8)
    line(ax, [(8.4, yb), (7.5, yb)])
    blk(ax, 6.4, yb, 2.2, 1.0, "ADC sampler\nperiod $T$", fs=8)
    line(ax, [(5.3, yb), (1.4, yb), (1.4, y - 0.22)])
    lab(ax, 3.4, yb + 0.12, "$y[k]$", fs=8.5)
    clk = COLORS[1]
    blk(ax, 3.9, 2.55, 1.3, 0.55, "clock", fs=8, fc="#FFF3DD")
    ax.plot([4.55, 5.6], [2.55, 2.55], color=clk, lw=1.0, ls="--")
    ax.annotate("", xy=(5.6, y - 0.55), xytext=(5.6, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=clk, lw=1.0, ls="--", mutation_scale=9))
    ax.annotate("", xy=(5.6, yb + 0.5), xytext=(5.6, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=clk, lw=1.0, ls="--", mutation_scale=9))
    ax.text(0.25, 0.45, "10 kHz sampling ($T$ = 100 µs) for a 100 Hz crossover:  hold ≈ $T/2$ delay → 1.8° lag,"
            "  plus one sample of computation delay → 3.6°", fontsize=7.6, ha="left", va="center", color="0.25")

    # ---- timing diagram: output (top) and held control signal (bottom)
    T, Tc = 1.0, 0.3
    tt = np.linspace(0, 5.2, 2000)

    def ycont(x):
        return 0.6 + 0.3 * np.sin(2 * np.pi * x / 6.0 + 0.4) + 0.06 * np.sin(2 * np.pi * x / 2.3)

    k = np.arange(0, 6)
    a_y = fig.add_axes([0.08, 0.30, 0.88, 0.15])
    a_u = fig.add_axes([0.08, 0.06, 0.88, 0.17], sharex=a_y)
    a_y.plot(tt, ycont(tt), color=COLORS[0], lw=1.6, label="$y(t)$")
    a_y.plot(k, ycont(k), "o", color=COLORS[0], ms=5, zorder=5, label="samples $y[k]$ at $t=kT$")
    uk = 1.2 - ycont(k)                       # illustrative proportional law
    ts_, us_ = [0.0, Tc], [1.2 - ycont(-1.0), 1.2 - ycont(-1.0)]
    for i, kk in enumerate(k[:-1]):
        ts_ += [kk + Tc, kk + 1 + Tc]
        us_ += [uk[i], uk[i]]
    ts_ += [5 + Tc, 5.2]
    us_ += [uk[5], uk[5]]
    a_u.plot(ts_, us_, color=COLORS[1], lw=1.6, label="$u(t)$ held, updated at $kT+T_c$")
    a_u.plot(tt, 1.2 - ycont(tt - Tc - T / 2), "--", color=COLORS[1], lw=1.0,
             label="staircase average: delay $T_c+T/2$")
    a_u.plot(tt, 1.2 - ycont(tt), ":", color="0.5", lw=1.0, label="ideal continuous law")
    for a in (a_y, a_u):
        for kk in k:
            a.axvline(kk, color="0.85", lw=0.8, zorder=0)
        a.set_yticks([])
        a.spines["left"].set_color("0.6")
    yl = a_u.get_ylim()
    a_u.set_ylim(yl[0] - 0.15, yl[1])
    yl = a_u.get_ylim()
    ya = yl[0] + 0.08 * (yl[1] - yl[0])
    a_u.annotate("", xy=(2 + Tc, ya), xytext=(2, ya),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    a_u.text(2 + Tc + 0.05, ya, "$T_c$", fontsize=8.5, ha="left", va="center")
    a_u.annotate("", xy=(4, ya), xytext=(3, ya),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=INK, mutation_scale=7, shrinkA=0, shrinkB=0))
    a_u.text(3.5, ya + 0.03 * (yl[1] - yl[0]), "$T$", fontsize=8.5, ha="center", va="bottom")
    a_y.set_ylabel("output", fontsize=8.5)
    a_u.set_ylabel("control", fontsize=8.5)
    a_u.set_xlim(0, 5.2)
    a_u.set_xticks(k)
    a_u.set_xticklabels(["0", "$T$", "$2T$", "$3T$", "$4T$", "$5T$"])
    a_y.tick_params(labelbottom=False)
    a_u.set_xlabel("time")
    a_y.legend(loc="lower right", fontsize=7.3, ncol=2, bbox_to_anchor=(1.0, 0.98))
    a_u.legend(loc="lower right", fontsize=7.3, ncol=3, bbox_to_anchor=(1.0, 0.98))
    return save(fig, "35", "fig-35-6-digital-control-loop")


if __name__ == "__main__":
    fig_step_specs()
    fig_practical_pid()
    fig_tuning()
    fig_lead_lag()
    fig_state_feedback()
    fig_digital_loop()
