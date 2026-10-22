"""Figures for Chapter 31 — Optical Communications.

Run from the repository root:  python figures/scripts/ch31.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from scipy.special import erfc
from scipy.optimize import brentq

from figstyle import new_fig, save, box, arrow, COLORS, INK

CORE = "#CFE2F3"
CLAD = "#EEF3F8"


# ---------------------------------------------------------------------------
def fig_31_1():
    """Step-index MM, graded-index MM and single-mode fibre: profiles and guiding."""
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(3, 2, width_ratios=[1, 5.2], hspace=0.55, wspace=0.06)
    rc = 62.5                           # cladding radius (um)
    ylim = (-72, 72)
    L = 600.0                           # drawn length (schematic, not to scale along the axis)
    x_air = -200.0
    rows = [
        ("Step-index multimode: core 50 µm, $n_1$ = 1.48, $n_2$ = 1.465", 25.0, "step"),
        ("Graded-index multimode: core 50 µm, parabolic profile", 25.0, "graded"),
        ("Single-mode: core 8.2 µm, MFD 10.4 µm at 1550 nm", 4.1, "single"),
    ]
    for i, (title, a, kind) in enumerate(rows):
        axp = fig.add_subplot(gs[i, 0])
        ax = fig.add_subplot(gs[i, 1], sharey=axp)
        # ---- index profile
        r = np.linspace(-rc, rc, 801)
        if kind == "step":
            n1, n2 = 1.48, 1.465
            n = np.where(np.abs(r) <= a, n1, n2)
        elif kind == "graded":
            n1, n2 = 1.48, 1.465
            n = np.where(np.abs(r) <= a, n1 - (n1 - n2) * (r / a) ** 2, n2)
        else:
            n1, n2 = 1.4675, 1.4624
            n = np.where(np.abs(r) <= a, n1, n2)
        axp.plot(n, r, color=COLORS[0], lw=1.4)
        axp.set_xlim(1.458, 1.486)
        axp.set_ylim(*ylim)
        axp.set_xticks([1.46, 1.48])
        axp.tick_params(labelsize=7.5)
        axp.set_yticks([-62.5, -a, 0, a, 62.5] if a > 10 else [-62.5, 0, 62.5])
        axp.set_yticklabels([f"{v:g}" for v in ([-62.5, -a, 0, a, 62.5] if a > 10 else [-62.5, 0, 62.5])])
        if i == 1:
            axp.set_ylabel("radius $r$ (µm)", fontsize=8.5)
        if i == 2:
            axp.set_xlabel("$n(r)$", fontsize=8.5)
        axp.spines["top"].set_visible(False)
        axp.spines["right"].set_visible(False)
        # ---- longitudinal section
        ax.add_patch(Rectangle((0, -rc), L, 2 * rc, fc=CLAD, ec="#888888", lw=0.8))
        if kind == "graded":
            for k in range(30):
                rr = a * (k + 0.5) / 30
                shade = 0.62 + 0.38 * (rr / a) ** 2
                c = (0.81 * shade + 0.19 * 0.93, 0.89 * shade + 0.11 * 0.95, 0.95)
                ax.add_patch(Rectangle((0, -rr), L, 2 * rr, fc=CORE, ec="none", alpha=0.10))
        ax.add_patch(Rectangle((0, -a), L, 2 * a, fc=CORE, ec="#6A8CAF", lw=0.8, alpha=0.9 if kind != "graded" else 0.5))
        ax.set_xlim(x_air, L + 5)
        ax.set_ylim(*ylim)
        ax.axis("off")
        ax.set_title(title, fontsize=9, loc="left", pad=3)
        ax.text(L - 5, -rc + 3, "cladding 125 µm", ha="right", va="bottom", fontsize=7.5, color="#555555")
        if kind == "step":
            # internal ray angles (drawing coordinates, vertical exaggeration)
            for slope, col in [(0.16, COLORS[1]), (0.33, COLORS[3])]:
                xs, ys = [0.0], [0.0]
                y, x, s = 0.0, 0.0, slope
                while x < L:
                    yt = a if s > 0 else -a
                    dx = (yt - y) / s
                    if x + dx > L:
                        xs.append(L); ys.append(y + s * (L - x)); break
                    x += dx; y = yt; s = -s
                    xs.append(x); ys.append(y)
                ax.plot(xs, ys, color=col, lw=1.1)
            # acceptance cone in air (drawn half-angle)
            tcone, xc0 = 0.62, -95.0
            for sgn in (1, -1):
                ax.plot([xc0, 0], [sgn * tcone * (-xc0), 0], color=COLORS[2], lw=0.9, ls="--")
            ax.add_patch(Polygon([[xc0, -tcone * xc0], [0, 0], [xc0, tcone * xc0]],
                                 closed=True, fc=COLORS[2], alpha=0.10, ec="none"))
            for slope, col in [(0.16, COLORS[1]), (0.33, COLORS[3])]:
                ax.plot([-80, 0], [-80 * 1.6 * slope, 0], color=col, lw=1.1)
            ax.text(x_air + 5, 0, "acceptance\ncone\n$\\theta_a$ = 12°\nNA = 0.21", fontsize=7.2, ha="left",
                    va="center", color="#00664A")
        elif kind == "graded":
            x = np.linspace(0, L, 600)
            P = 300.0
            for amp, col in [(10, COLORS[1]), (17, COLORS[3]), (23, COLORS[4])]:
                ax.plot(x, amp * np.sin(2 * np.pi * x / P), color=col, lw=1.1)
            for xf in (P / 2, P, 1.5 * P, 2 * P):
                if xf < L:
                    ax.plot(xf, 0, "o", ms=3, color=INK)
            ax.text(-8, 0, "rays refocus\nperiodically", ha="right", va="center", fontsize=7.5)
        else:
            w = 5.2                     # mode-field radius (MFD/2)
            rr = np.linspace(-3 * w, 3 * w, 200)
            for x0 in (120, 330, 540):
                prof = 45 * np.exp(-(rr / w) ** 2)
                ax.plot(x0 + prof, rr, color=COLORS[1], lw=1.1)
                ax.plot([x0, x0], [rr[0], rr[-1]], color="#999999", lw=0.5)
            ax.axhspan(-w, w, xmin=(0 - x_air) / (L + 5 - x_air), xmax=(L - x_air) / (L + 5 - x_air), color=COLORS[1], alpha=0.12, lw=0)
            ax.annotate("mode field (MFD 10.4 µm)\nspills into the cladding", xy=(170, 5.0), xytext=(185, 38),
                        fontsize=7.5, color=COLORS[1],
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.7, mutation_scale=7))
            ax.annotate("core 8.2 µm", xy=(30, 4.1), xytext=(-8, 30), fontsize=7.5, ha="right",
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.7, mutation_scale=7))
    fig.text(0.99, 0.005, "vertical scale in µm, identical in all three; length not to scale",
             ha="right", va="bottom", fontsize=7.5, color="#555555")
    save(fig, "31", "fig-31-1-fibre-guiding-modes")


# ---------------------------------------------------------------------------
def _atten_parts(lam_nm):
    lam = lam_nm / 1000.0
    ray = 0.85 / lam ** 4
    ir = 7.81e11 * np.exp(-48.48 / lam)
    uv = 0.35 * np.exp(-(lam - 0.85) / 0.187)          # short-wavelength excess (UV tail, defects)
    oh = 0.057 * np.exp(-0.5 * ((lam_nm - 1383) / 14.0) ** 2)
    return ray, ir, uv, oh, 0.005


def fig_31_2():
    """Attenuation spectrum of low-water-peak silica fibre."""
    lam = np.linspace(800, 1700, 1500)
    ray, ir, uv, oh, c = _atten_parts(lam)
    tot = ray + ir + uv + oh + c
    old = tot + 1.69 * np.exp(-0.5 * ((lam - 1383) / 16.0) ** 2) + 0.12 * np.exp(-0.5 * ((lam - 1240) / 15.0) ** 2) \
        + 0.30 * np.exp(-0.5 * ((lam - 945) / 12.0) ** 2)
    fig, ax = new_fig(6.4, 4.0)
    bands = [("O", 1260, 1360), ("E", 1360, 1460), ("S", 1460, 1530), ("C", 1530, 1565), ("L", 1565, 1625)]
    shades = ["#E8F0F8", "#F4ECE4", "#E8F4EE", "#FBE3D2", "#EFE6F3"]
    for (nm, a, b), sh in zip(bands, shades):
        ax.axvspan(a, b, color=sh, lw=0)
        ax.text((a + b) / 2, 3.03, nm, ha="center", va="bottom", fontsize=9, fontweight="bold", clip_on=False)
    ax.plot(lam, old, color="#888888", ls=":", lw=1.5, label="older fibre with water peak")
    ax.plot(lam, ray, color=COLORS[0], ls="--", lw=1.1, label=r"Rayleigh, 0.85 dB/km $\times$ (1 µm/$\lambda$)$^4$")
    m = lam > 1450
    ax.plot(lam[m], ir[m], color=COLORS[3], ls="--", lw=1.1, label="infrared absorption")
    ax.plot(lam, tot, color=INK, lw=1.9, label="low-water-peak fibre (G.652.D)")
    for l0 in (850, 1310, 1550):
        i = np.argmin(abs(lam - l0))
        ax.plot(l0, tot[i], "o", color=COLORS[1], ms=5, mec="white", mew=0.8, zorder=5)
        tx, ty = {850: (862, 2.3), 1310: (1215, 0.85), 1550: (1540, 0.62)}[l0]
        ax.annotate(f"{l0} nm\n{tot[i]:.2f} dB/km", xy=(l0, tot[i]), xytext=(tx, ty),
                    fontsize=7.8, ha="left" if l0 == 850 else "center",
                    arrowprops=dict(arrowstyle="-", color="#777777", lw=0.6))
    i83 = np.argmin(abs(lam - 1383))
    ax.annotate("residual OH\npeak", xy=(1383, tot[i83]), xytext=(1425, 0.95), fontsize=7.5, ha="left",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.6))
    ax.text(1405, 1.65, "OH peak in\nolder fibre", fontsize=7.5, color="#666666", ha="left", va="center")
    ax.set_xlim(800, 1700)
    ax.set_ylim(0, 3)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("attenuation (dB/km)")
    ax.legend(loc="upper left", fontsize=7.8, bbox_to_anchor=(0.215, 0.995), frameon=True, framealpha=0.95,
              edgecolor="#CCCCCC")
    save(fig, "31", "fig-31-2-attenuation-spectrum")


# ---------------------------------------------------------------------------
def _sellmeier_D(lam_nm):
    """Material dispersion of fused silica (Malitson Sellmeier), ps/(nm km)."""
    B = [0.6961663, 0.4079426, 0.8974794]
    Cl = [0.0684043, 0.1162414, 9.896161]
    lam = lam_nm / 1000.0
    h = 1e-3

    def n(l):
        return np.sqrt(1 + sum(b * l ** 2 / (l ** 2 - c ** 2) for b, c in zip(B, Cl)))
    d2 = (n(lam + h) - 2 * n(lam) + n(lam - h)) / h ** 2           # 1/um^2
    c = 2.998e8
    return -(lam * 1e-6) / c * d2 * 1e12 * 1e12 / 1e9 * 1e3           # ps/(nm km)


def _D(lam, l0, S0):
    return S0 / 4 * (lam - l0 ** 4 / lam ** 3)


def fig_31_3():
    """Chromatic dispersion of G.652, G.655 and G.654 fibre."""
    lam = np.linspace(1250, 1650, 500)
    S652 = 17.0 / ((1550 - 1312 ** 4 / 1550 ** 3) / 4)
    D652 = _D(lam, 1312, S652)
    D655 = _D(lam, 1450, 4.0 / ((1550 - 1450 ** 4 / 1550 ** 3) / 4))
    D654 = _D(lam, 1290, 20.5 / ((1550 - 1290 ** 4 / 1550 ** 3) / 4))
    DM = _sellmeier_D(lam)
    DW = D652 - DM
    fig, ax = new_fig(6.4, 4.0)
    ax.axvspan(1530, 1565, color="#FBE3D2", lw=0)
    ax.text(1547.5, -9.6, "C band", ha="center", va="bottom", fontsize=8.5)
    ax.axhline(0, color=INK, lw=0.6)
    for l0 in (1310, 1550):
        ax.axvline(l0, color="#777777", ls="--", lw=0.8)
    ax.plot(lam, DM, color=COLORS[0], lw=0.9, ls="--", label="G.652 material part (silica)")
    ax.plot(lam, DW, color=COLORS[0], lw=0.9, ls=":", label="G.652 waveguide part")
    ax.plot(lam, D654, color=COLORS[2], label="G.654 large-$A_{eff}$")
    ax.plot(lam, D652, color=COLORS[0], label="G.652 standard SMF")
    ax.plot(lam, D655, color=COLORS[1], label="G.655 NZ-DSF")
    for D, val, col, (tx, ty) in [(D652, 17.0, COLORS[0], (1572, 15.4)), (D655, 4.0, COLORS[1], (1556, 5.6)),
                                  (D654, 20.5, COLORS[2], (1572, 19.8))]:
        ax.plot(1550, val, "o", color=col, ms=5, mec="white", mew=0.8, zorder=5)
        ax.text(tx, ty, f"{val:g}", color=col, fontsize=8.5, va="center")
    ax.plot(1312, 0, "o", color=COLORS[0], ms=5, mec="white", mew=0.8, zorder=5)
    ax.text(1317, -1.9, r"$\lambda_0$ = 1312 nm", fontsize=8, color=COLORS[0], va="center")
    ax.plot(1450, 0, "o", color=COLORS[1], ms=5, mec="white", mew=0.8, zorder=5)
    ax.text(1456, -1.9, r"$\lambda_0\approx$ 1450 nm", fontsize=8, color=COLORS[1], va="center")
    ax.set_xlim(1250, 1650)
    ax.set_ylim(-10, 25)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel(r"dispersion $D$ (ps/(nm$\cdot$km))")
    ax.legend(loc="upper left", fontsize=7.8, frameon=True, framealpha=0.95, edgecolor="#CCCCCC")
    save(fig, "31", "fig-31-3-chromatic-dispersion")


# ---------------------------------------------------------------------------
def _li(I, Ith, eta, s=0.8):
    stim = eta * s * np.log1p(np.exp((I - Ith) / s))
    spont = 0.004 * np.minimum(I, Ith)
    return stim + spont


def fig_31_4():
    """L-I curves of a DFB laser at three temperatures with an OOK bias point."""
    fig = plt.figure(figsize=(6.4, 5.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.15], hspace=0.08)
    ax = fig.add_subplot(gs[0])
    axb = fig.add_subplot(gs[1], sharex=ax)
    I = np.linspace(0, 80, 800)
    sets = [(25, 10, 0.20, COLORS[0]), (50, 16, 0.17, COLORS[4]), (75, 26, 0.14, COLORS[1])]
    for T, Ith, eta, c in sets:
        ax.plot(I, _li(I, Ith, eta), color=c, label=f"{T} °C: $I_{{th}}$ = {Ith} mA, {eta:.2f} W/A")
        ax.plot(Ith, _li(Ith, Ith, eta), "|", color=c, ms=9, mew=1.4)
    # operating point on the 25 C curve
    i0, i1, ib = 20, 50, 35
    p0, p1, pb = (_li(np.array(v), 10, 0.20) for v in (i0, i1, ib))
    for iv, pv in [(i0, p0), (i1, p1)]:
        ax.plot([iv, iv], [0, pv], color="#888888", ls=":", lw=0.9)
        ax.plot([0, iv], [pv, pv], color="#888888", ls=":", lw=0.9)
        ax.plot(iv, pv, "o", color=COLORS[0], ms=5, mec="white", mew=0.8, zorder=5)
    ax.plot(ib, pb, "s", color=INK, ms=5, zorder=6)
    ax.annotate("bias 35 mA", xy=(ib, pb), xytext=(41, 3.6), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    # optical output waveform drawn just right of the y axis
    tt = np.array([0, 1, 1, 2, 2, 3, 3, 4, 4, 5])
    lv = np.array([p0, p0, p1, p1, p0, p0, p1, p1, p0, p0])
    xw = 1.0 + tt * 2.6
    ax.plot(xw, lv, color=COLORS[2], lw=1.8)
    ax.text(1.0, p1 + 0.35, f"$P_1$ = {p1:.0f} mW", fontsize=8.5, color=COLORS[2], va="bottom")
    ax.text(1.0, p0 - 0.3, f"$P_0$ = {p0:.0f} mW", fontsize=8.5, color=COLORS[2], va="top")
    ax.text(1.0, 9.6, "optical output\n(time →)", fontsize=8, color=COLORS[2], va="bottom")
    ax.text(57, 1.2, f"extinction ratio $P_1/P_0$ = {p1/p0:.0f} ({10*np.log10(p1/p0):.0f} dB)",
            fontsize=8.5, ha="left")
    ax.set_ylim(0, 12)
    ax.set_xlim(0, 80)
    ax.set_ylabel("optical output power (mW)")
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(0.2, 1.0))
    plt.setp(ax.get_xticklabels(), visible=False)
    # drive current waveform below the axis (time downward)
    td = np.array([0, 1, 1, 2, 2, 3, 3, 4, 4, 5])
    cur = np.array([i0, i0, i1, i1, i0, i0, i1, i1, i0, i0])
    axb.plot(cur, td, color=COLORS[0], lw=1.8)
    axb.axvline(ib, color=INK, ls="--", lw=0.8)
    axb.text(i0 - 1, 2.5, "20 mA", ha="right", va="center", fontsize=8)
    axb.text(i1 + 1, 2.5, "50 mA", ha="left", va="center", fontsize=8)
    axb.text(ib, -0.25, "35 mA", ha="center", va="bottom", fontsize=8)
    axb.text(62, 2.5, "drive current\n(time ↓)", fontsize=8, color=COLORS[0], va="center")
    axb.set_ylim(5.2, -0.4)
    axb.set_yticks([])
    axb.spines["left"].set_visible(False)
    axb.set_xlabel("drive current (mA)")
    save(fig, "31", "fig-31-4-laser-li-curve")


# ---------------------------------------------------------------------------
Qf = lambda x: 0.5 * erfc(np.asarray(x) / np.sqrt(2))   # noqa: E731


def _q_factor(P_dbm, M=1.0, kA=0.5, R=1.0, B=7.5e9, i_n=15e-12):
    q = 1.602e-19
    P = 1e-3 * 10 ** (np.asarray(P_dbm) / 10)
    FA = kA * M + (1 - kA) * (2 - 1 / M) if M > 1 else 1.0
    s_th = i_n * np.sqrt(B)
    I1 = M * R * 2 * P
    s1 = np.sqrt(s_th ** 2 + 2 * q * M ** 2 * FA * R * 2 * P * B)
    return I1 / (s1 + s_th)


def fig_31_5():
    """BER versus average received power, 10 Gb/s PIN-TIA and APD (M = 10) receivers."""
    P = np.linspace(-34, -14, 600)
    fig, ax = new_fig(6.4, 4.0)
    sens = {}
    for M, c, name in [(1, COLORS[0], "PIN + TIA"), (10, COLORS[1], "APD ($M$ = 10, $k_A$ = 0.5)")]:
        ber = Qf(_q_factor(P, M))
        ax.semilogy(P, ber, color=c, label=name)
        sens[M] = brentq(lambda p: _q_factor(p, M) - 7, -45, -5)
    ax.semilogy(P + 2, Qf(_q_factor(P, 1)), color=COLORS[0], ls="--", lw=1.2,
                label="PIN, 2 dB dispersion penalty")
    b7 = Qf(7)
    for M, c in [(1, COLORS[0]), (10, COLORS[1])]:
        ax.plot(sens[M], b7, "o", color=c, ms=5, mec="white", mew=0.8, zorder=5)
        ax.text(sens[M] + 0.25, b7 * 3, f"{sens[M]:.1f} dBm".replace("-", "−"), color=c, fontsize=8.5, ha="left")
    ax.axhline(1e-12, color=INK, ls="--", lw=0.8)
    ax.text(-33.8, 1.5e-12, "BER = $10^{-12}$", fontsize=8, va="bottom")
    ax.axhline(3.8e-3, color=COLORS[2], ls="--", lw=0.8)
    ax.text(-33.8, 4.8e-3, "HD-FEC threshold $3.8\\times10^{-3}$", fontsize=8, va="bottom", color=COLORS[2])
    ya = 2e-14
    ax.annotate("", xy=(sens[10], ya), xytext=(sens[1], ya),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, mutation_scale=9))
    for M in (1, 10):
        ax.plot([sens[M], sens[M]], [ya, b7], color="#888888", lw=0.6, ls=":")
    ax.text((sens[1] + sens[10]) / 2, ya * 0.35, f"APD advantage {sens[1] - sens[10]:.1f} dB", ha="center",
            va="top", fontsize=8.5)
    ax.set_xlim(-34, -14)
    ax.set_ylim(1e-15, 1e-2)
    ax.set_xlabel("average received power (dBm)")
    ax.set_ylabel("bit-error ratio")
    ax.set_title(r"10 Gb/s NRZ at 1550 nm: $\mathcal{R}$ = 1.0 A/W, $B_n$ = 7.5 GHz, TIA 15 pA/$\sqrt{\mathrm{Hz}}$",
                 fontsize=9)
    ax.grid(True, which="major", lw=0.5)
    ax.legend(loc="center", fontsize=7.8, bbox_to_anchor=(0.42, 0.62), frameon=True, framealpha=0.95,
              edgecolor="#CCCCCC")
    save(fig, "31", "fig-31-5-ber-vs-received-power")


# ---------------------------------------------------------------------------
def _tri(ax, x, y, w=0.9, h=0.8, text="", fc="#E8F4EE"):
    ax.add_patch(Polygon([[x, y - h / 2], [x, y + h / 2], [x + w, y]], closed=True, fc=fc, ec=INK, lw=0.9))
    if text:
        ax.text(x + w / 2, y + h / 2 + 0.08, text, ha="center", va="bottom", fontsize=7.2)


def _spool(ax, x, y, text="80 km"):
    from matplotlib.patches import Circle
    for dr in (0.32, 0.22):
        ax.add_patch(Circle((x, y), dr, fc="none", ec=COLORS[0], lw=1.0))
    ax.text(x, y - 0.42, text, ha="center", va="top", fontsize=7)


def fig_31_6():
    """DWDM line: block diagram plus per-channel power and OSNR along 800 km."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.0, 0.60, 1.0, 0.40])
    ax.set_xlim(0, 17.6)
    ax.set_ylim(0, 4.4)
    ax.set_aspect("equal")
    ax.axis("off")
    yc = 2.2
    # transmitters
    freqs = ["193.10 THz", "193.15 THz", "⋮", "Tx $N$"]
    for k, f in enumerate(freqs):
        yy = 3.5 - k * 0.85
        if f == "⋮":
            ax.text(0.85, yy + 0.2, "⋮", ha="center", va="center", fontsize=10)
            continue
        box(ax, 0.1, yy - 0.3, 1.5, 0.6, f, fontsize=6.8)
        ax.plot([1.6, 2.2], [yy, yc + (yy - yc) * 0.3], color=INK, lw=0.7)
    ax.text(0.85, 4.15, "transponders\n(50 GHz grid)", ha="center", va="bottom", fontsize=7)
    ax.add_patch(Polygon([[2.2, yc - 1.0], [2.2, yc + 1.0], [3.0, yc + 0.45], [3.0, yc - 0.45]], closed=True,
                         fc="#EFE6F3", ec=INK, lw=0.9))
    ax.text(2.6, yc - 1.15, "AWG\nmux", ha="center", va="top", fontsize=7)
    ax.plot([3.0, 3.3], [yc, yc], color=INK, lw=1.0)
    _tri(ax, 3.3, yc, text="booster\n0 dBm/ch")
    x = 4.2
    seq = [("span", "span 1"), ("amp", "EDFA\n20 dB, NF 5"), ("span", "span 2"), ("amp", "EDFA"),
           ("dots", ""), ("span", "span 10"), ("amp", "pre-amp")]
    for kind, t in seq:
        if kind == "span":
            ax.plot([x, x + 0.35], [yc, yc], color=INK, lw=1.0)
            _spool(ax, x + 0.75, yc, t + "\n80 km")
            ax.plot([x + 1.15, x + 1.5], [yc, yc], color=INK, lw=1.0)
            x += 1.5
        elif kind == "amp":
            _tri(ax, x, yc, text=t)
            x += 0.9
        else:
            ax.plot([x, x + 0.25], [yc, yc], color=INK, lw=1.0)
            ax.text(x + 0.6, yc, "···", ha="center", va="center", fontsize=11)
            ax.plot([x + 0.95, x + 1.2], [yc, yc], color=INK, lw=1.0)
            x += 1.2
    ax.plot([x, x + 0.3], [yc, yc], color=INK, lw=1.0)
    x += 0.3
    ax.add_patch(Polygon([[x, yc - 0.45], [x, yc + 0.45], [x + 0.8, yc + 1.0], [x + 0.8, yc - 1.0]], closed=True,
                         fc="#EFE6F3", ec=INK, lw=0.9))
    ax.text(x + 0.4, yc - 1.15, "AWG\ndemux", ha="center", va="top", fontsize=7)
    xr = x + 1.35
    for k, lab in enumerate(["coh. Rx", "coh. Rx", "⋮", "coh. Rx"]):
        yy = 3.5 - k * 0.85
        if lab == "⋮":
            ax.text(xr + 0.6, yy + 0.2, "⋮", ha="center", va="center", fontsize=10)
            continue
        ax.plot([x + 0.8, xr], [yc + (yy - yc) * 0.3, yy], color=INK, lw=0.7)
        box(ax, xr, yy - 0.3, 1.2, 0.6, lab, fontsize=6.8)
    ax.annotate("", xy=(13.6, 0.25), xytext=(4.2, 0.25),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.8, mutation_scale=7))
    ax.text(8.9, 0.3, "10 spans × 80 km G.652, 20 dB loss each", ha="center", va="bottom", fontsize=7.5)

    # ---- power and OSNR along the line
    axp = fig.add_axes([0.09, 0.08, 0.80, 0.46])
    nsp, Ls = 10, 80.0
    z, p = [], []
    for n in range(nsp):
        zz = np.linspace(n * Ls, (n + 1) * Ls, 50)
        z.extend(zz)
        p.extend(0 - 20 * (zz - n * Ls) / Ls)
    z = np.array(z)
    p = np.array(p)
    axp.plot(z, p, color=COLORS[0], lw=1.2, alpha=0.75, label="per-channel power")
    for n in range(1, nsp + 1):
        axp.plot([n * Ls, n * Ls], [-20, 0], color=COLORS[0], lw=1.0, alpha=0.75)
    axp.set_xlim(0, 800)
    axp.set_ylim(-24, 4)
    axp.set_xlabel("distance (km)")
    axp.set_ylabel("power per channel (dBm)", color=COLORS[0])
    axp.tick_params(axis="y", colors=COLORS[0])
    axp.set_xticks(np.arange(0, 801, 80))
    axp.text(40, -22.6, "−20 dB per 80 km span", ha="center", fontsize=7.5, color=COLORS[0])
    axo = axp.twinx()
    axo.spines["right"].set_visible(True)
    n = np.arange(1, nsp + 1)
    osnr = 58 + 0 - 20 - 5 - 10 * np.log10(n)
    axo.plot(n * Ls, osnr, "o-", color=COLORS[1], ms=4.5, lw=1.4, mec="white", mew=0.7, label="OSNR")
    for nn, o in zip(n, osnr):
        if nn in (1, 2, 5, 10):
            axo.text(nn * Ls + (12 if nn == 1 else -6), o + (0.15 if nn == 1 else 0.45), f"{o:.1f}",
                     ha="right" if nn > 1 else "left", va="bottom",
                     fontsize=7.8, color=COLORS[1], bbox=dict(fc="white", ec="none", pad=0.8))
    axo.set_ylim(20, 36)
    axo.set_ylabel("OSNR in 0.1 nm (dB)", color=COLORS[1])
    axo.tick_params(axis="y", colors=COLORS[1])
    axo.text(560, 30.3, r"OSNR $= 33 - 10\log_{10} n$ after $n$ spans", fontsize=8, color=COLORS[1], ha="center", bbox=dict(fc="white", ec="none", pad=1.0))
    save(fig, "31", "fig-31-6-dwdm-link")


if __name__ == "__main__":
    fig_31_1()
    fig_31_2()
    fig_31_3()
    fig_31_4()
    fig_31_5()
    fig_31_6()
