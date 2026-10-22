"""Figures for Chapter 30 — Wireless and Mobile Communications.

Run from the repository root:  python figures/scripts/ch30.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Rectangle, FancyArrowPatch
from scipy.special import erfc, comb

from figstyle import new_fig, save, box, arrow, COLORS, INK

C0 = 2.998e8


def Q(x):
    return 0.5 * erfc(np.asarray(x) / np.sqrt(2))


def db2lin(x):
    return 10 ** (np.asarray(x) / 10)


# ---------------------------------------------------------------------------
def fig_30_1():
    """Path loss versus distance at 900 MHz: free space, two-ray, Okumura-Hata urban."""
    f = 900e6
    lam = C0 / f
    ht, hr = 30.0, 1.5
    d = np.logspace(np.log10(100), np.log10(20e3), 6000)          # m
    fs = 20 * np.log10(4 * np.pi * d / lam)
    # exact two-ray (ground reflection coefficient -1, unit antenna gains)
    phase = 2 * np.pi * (np.sqrt(d ** 2 + (ht + hr) ** 2) - np.sqrt(d ** 2 + (ht - hr) ** 2)) / lam
    two = fs - 20 * np.log10(np.abs(1 - np.exp(-1j * phase)) + 1e-12)
    db = 4 * ht * hr / lam
    fmhz = f / 1e6
    a_hm = (1.1 * np.log10(fmhz) - 0.7) * hr - (1.56 * np.log10(fmhz) - 0.8)

    def hata(dkm):
        return (69.55 + 26.16 * np.log10(fmhz) - 13.82 * np.log10(ht) - a_hm
                + (44.9 - 6.55 * np.log10(ht)) * np.log10(dkm))

    dk = d / 1e3
    fig, ax = new_fig(6.4, 4.0)
    valid = dk >= 1
    ax.fill_between(dk[valid], hata(dk[valid]) - 8, hata(dk[valid]) + 8, color=COLORS[1], alpha=0.13, lw=0)
    ax.semilogx(dk, two, color=COLORS[2], lw=1.0, label=r"two-ray, $h_t$ = 30 m, $h_r$ = 1.5 m (40 dB/decade beyond $d_b$)")
    ax.semilogx(dk, fs, color=COLORS[0], label="free space (20 dB/decade)")
    ax.semilogx(dk[valid], hata(dk[valid]), color=COLORS[1], label="Okumura–Hata urban (35.2 dB/decade)")
    ax.semilogx(dk[~valid], hata(dk[~valid]), color=COLORS[1], ls=":", lw=1.4)
    ax.axvline(db / 1e3, color=INK, ls="--", lw=0.9)
    ax.text(db / 1e3 * 1.06, 63, f"breakpoint\n$d_b$ = {db:.0f} m", fontsize=8.5, va="bottom")
    ax.text(12, 140, "shadowing,\n$\\sigma$ = 8 dB", fontsize=8.5, color=COLORS[1], ha="center", va="center")
    ax.text(0.98, 106, "Hata outside\nits 1–20 km range", fontsize=8, color=COLORS[1], ha="center")
    pts = [(2, 20 * np.log10(4 * np.pi * 2000 / lam), COLORS[0], (3.0, 88)),
           (5, 40 * np.log10(5000) - 20 * np.log10(ht * hr), COLORS[2], (3.0, 121)),
           (2, hata(2), COLORS[1], (1.0, 146)),
           (5, hata(5), COLORS[1], (8.5, 152))]
    for x_, y_, c, (tx, ty) in pts:
        ax.plot(x_, y_, "o", color=c, ms=5, mec="white", mew=0.8, zorder=6)
        ax.annotate(f"{y_:.1f} dB", xy=(x_, y_), xytext=(tx, ty), fontsize=8, color=c, ha="center",
                    arrowprops=dict(arrowstyle="-", color=c, lw=0.6))
    ax.set_xlim(0.1, 20)
    ax.set_ylim(60, 170)
    ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
    ax.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20"])
    ax.set_xlabel("distance (km)")
    ax.set_ylabel("path loss (dB)")
    ax.set_title("900 MHz", fontsize=10)
    ax.grid(True, which="major", lw=0.5)
    ax.legend(loc="upper left", fontsize=8, frameon=True, framealpha=0.95, edgecolor="#CCCCCC")
    save(fig, "30", "fig-30-1-path-loss-models")


# ---------------------------------------------------------------------------
def _jakes(t, fd, n_paths, rng):
    """Sum-of-sinusoids Clarke/Jakes fading, unit mean power."""
    alpha = rng.uniform(0, 2 * np.pi, n_paths)
    phi = rng.uniform(0, 2 * np.pi, n_paths)
    h = np.exp(1j * (2 * np.pi * fd * np.outer(t, np.cos(alpha)) + phi)).sum(axis=1)
    return h / np.sqrt(n_paths)


def fig_30_2():
    """Rayleigh fading envelope, 120 km/h at 2 GHz (f_D = 222 Hz)."""
    v = 120 / 3.6
    fd = v * 2e9 / 3e8
    t = np.arange(0, 0.1, 1e-5)
    best = None
    for seed in range(200):
        rng = np.random.default_rng(seed)
        h = _jakes(t, fd, 64, rng)
        p = np.abs(h) ** 2
        p /= p.mean()
        pdb = 10 * np.log10(p)
        nfade = np.sum((pdb[1:] < -10) & (pdb[:-1] >= -10))
        if nfade == 16 and pdb.min() < -28 and pdb.min() > -40:
            best = pdb
            break
    pdb = best
    fig, ax = new_fig(6.4, 3.9)
    tm = t * 1e3
    ax.plot(tm, pdb, color=COLORS[0], lw=1.0)
    ax.fill_between(tm, pdb, -10, where=pdb < -10, interpolate=True, color=COLORS[1], alpha=0.35, lw=0)
    ax.axhline(0, color=INK, ls="--", lw=0.9)
    ax.axhline(-10, color=COLORS[1], ls="--", lw=0.9)
    ax.text(101, 0, "mean", ha="left", va="center", fontsize=8.5, clip_on=False)
    ax.text(101, -10, "fade\nthreshold", ha="left", va="center", fontsize=8.5, color=COLORS[1],
            clip_on=False)
    # coherence time bracket
    tc = 0.423 / fd * 1e3
    x0 = 30.0
    ax.annotate("", xy=(x0, 6.5), xytext=(x0 + tc, 6.5),
                arrowprops=dict(arrowstyle="|-|", color=INK, lw=0.9, mutation_scale=3))
    ax.text(x0 + tc + 1.0, 6.5, f"coherence time $T_c\\approx$ {tc:.1f} ms", va="center", fontsize=8.5)
    ax.text(1, -37.5, f"$f_D$ = {fd:.0f} Hz;  16 fades below −10 dB in 100 ms "
            "(level-crossing rate ≈ 160 /s)", fontsize=8.5, va="bottom")
    ax.set_xlim(0, 100)
    ax.set_ylim(-40, 10)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("received power re mean (dB)")
    top = ax.secondary_xaxis("top", functions=(lambda x: x * v / 1e3, lambda s: s * 1e3 / v))
    top.set_xlabel("distance travelled at 120 km/h (m)")
    top.set_xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    save(fig, "30", "fig-30-2-rayleigh-fading-envelope")


# ---------------------------------------------------------------------------
def _mrc(gb, L):
    mu = np.sqrt(gb / (1 + gb))
    return ((1 - mu) / 2) ** L * sum(comb(L - 1 + k, k) * ((1 + mu) / 2) ** k for k in range(L))


def fig_30_3():
    """BPSK BER in AWGN and in Rayleigh fading with L-branch MRC."""
    from scipy.optimize import brentq
    x = np.linspace(0, 40, 800)
    g = db2lin(x)
    fig, ax = new_fig(6.4, 4.0)
    curves = [("AWGN", lambda g: Q(np.sqrt(2 * g)), COLORS[7], "-"),
              ("Rayleigh, $L$ = 1 (1 decade per 10 dB)", lambda g: _mrc(g, 1), COLORS[1], "-"),
              ("MRC, $L$ = 2 (2 decades per 10 dB)", lambda g: _mrc(g, 2), COLORS[0], "-"),
              ("MRC, $L$ = 4", lambda g: _mrc(g, 4), COLORS[2], "-")]
    x3 = {}
    for name, f, c, ls in curves:
        ax.semilogy(x, f(g), color=c, ls=ls, label=name)
        with np.errstate(divide="ignore"):
            x3[name] = brentq(lambda d: np.log(f(db2lin(d))) - np.log(1e-3), 0, 45)
        ax.plot(x3[name], 1e-3, "o", color=c, ms=5, mec="white", mew=0.8, zorder=5)
    ax.axhline(1e-3, color=INK, ls="--", lw=0.8)
    names = [c[0] for c in curves]
    xa, x1, x2, x4 = (x3[n] for n in names)
    ax.text(xa + 0.3, 1.25e-3, f"{xa:.1f}", fontsize=8, color=INK)
    ax.text(x4 - 0.3, 1.25e-3, f"{x4:.1f}", fontsize=8, color=COLORS[2], ha="right")
    ax.text(x2 + 0.3, 1.25e-3, f"{x2:.1f}", fontsize=8, color=COLORS[0])
    ax.text(x1 + 0.3, 1.25e-3, f"{x1:.1f} dB", fontsize=8, color=COLORS[1])
    # diversity-gain and fading-penalty arrows, labelled to the right of the L = 1 point
    yb = 6e-5
    ax.annotate("", xy=(x2, yb), xytext=(x1, yb),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[0], lw=1.0, mutation_scale=9))
    ax.plot([x2, x2], [yb, 1e-3], color=COLORS[0], lw=0.6, ls=":")
    ax.text(x1 + 0.6, yb, f"{x1 - x2:.0f} dB diversity gain\n($L$ = 1 → 2)", ha="left", va="center",
            fontsize=8.5, color=COLORS[0])
    ya = 6e-6
    ax.annotate("", xy=(x1, ya), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.0, mutation_scale=9))
    ax.plot([xa, xa], [ya, 1e-3], color=COLORS[1], lw=0.6, ls=":")
    ax.plot([x1, x1], [ya, 1e-3], color=COLORS[1], lw=0.6, ls=":")
    ax.text(x1 + 0.6, ya, f"{x1 - xa:.0f} dB fading penalty\n(AWGN → Rayleigh)", ha="left", va="center",
            fontsize=8.5, color=COLORS[1])
    ax.set_xlim(0, 40)
    ax.set_ylim(1e-6, 0.5)
    ax.set_xlabel(r"mean $E_b/N_0$ per branch (dB)")
    ax.set_ylabel("bit error rate")
    ax.grid(True, which="major", lw=0.5)
    ax.legend(loc="upper right", fontsize=8.5)
    save(fig, "30", "fig-30-3-ber-fading-diversity")


# ---------------------------------------------------------------------------
def fig_30_4():
    """Hexagonal N = 7 reuse pattern (i = 2, j = 1)."""
    R = 1.0
    letters = "ABCDEFG"
    fig, ax = plt.subplots(figsize=(6.4, 4.95))
    ax.set_aspect("equal")
    ax.axis("off")
    W, H = 8.6, 5.6

    def centre(q, r):
        return R * np.sqrt(3) * (q + r / 2), R * 1.5 * r

    first_tier = []
    for q in range(-12, 13):
        for r in range(-4, 5):
            x, y = centre(q, r)
            if abs(x) > W - 0.87 or abs(y) > H - 1.0:      # keep only whole cells
                continue
            lab = (3 * q + r) % 7
            tier1 = (lab == 0) and abs(np.hypot(x, y) - np.sqrt(21)) < 1e-6
            if q == 0 and r == 0:
                fc, tc = COLORS[1], "white"
            elif tier1:
                fc, tc = "#F2B48A", INK
                first_tier.append((x, y))
            elif lab == 0:
                fc, tc = "#FBE3D2", INK
            else:
                fc, tc = "#F4F6F9", "#444444"
            ax.add_patch(RegularPolygon((x, y), 6, radius=R, orientation=0, fc=fc, ec="#8899AA", lw=0.8))
            ty = y + 0.38 if (q == 0 and r == 0) else y
            ax.text(x, ty, letters[lab], ha="center", va="center", fontsize=8.5, color=tc,
                    fontweight="bold" if lab == 0 else "normal")
    for (x, y) in first_tier:
        ax.plot([0, x], [0, y], color=INK, ls="--", lw=1.0)
    # label one D line (towards the co-channel cell at i = 2, j = 1)
    xt, yt = centre(2, 1)
    ang = np.arctan2(yt, xt)
    px, py = 0.0, 0.0
    ax.text(0.55 * xt + px, 0.55 * yt + py, "$D$ = 4.58 $R$", fontsize=9, rotation=np.degrees(ang),
            ha="center", va="center", fontweight="bold",
            bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.9))
    # cell radius on the centre hexagon (centre to a vertex)
    vx, vy = R * np.cos(np.radians(-30)), R * np.sin(np.radians(-30))
    ax.annotate("", xy=(vx, vy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.3, mutation_scale=8))
    ax.text(0.30, -0.55, "$R$", color="white", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.set_xlim(-W, W)
    ax.set_ylim(-H - 1.7, H)
    ax.text(0, -H - 0.95,
            r"$N = i^2+ij+j^2 = 7$ ($i$ = 2, $j$ = 1):   $D/R=\sqrt{3N}$ = 4.58,   "
            r"SIR $\approx (D/R)^4/6$ = 18.7 dB for $n$ = 4",
            ha="center", va="center", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", lw=0.8))
    save(fig, "30", "fig-30-4-hexagonal-reuse-n7")


# ---------------------------------------------------------------------------
def fig_30_5():
    """OFDM transmitter and receiver with cyclic prefix, plus CP timing inset."""
    fig = plt.figure(figsize=(6.8, 5.0))
    ax = fig.add_axes([0.0, 0.36, 1.0, 0.64])
    ax.set_xlim(0, 17.6)
    ax.set_ylim(0.6, 7.0)
    ax.set_aspect("equal")
    ax.axis("off")
    bw, bh, gap = 2.05, 1.25, 0.3
    x0 = 1.0
    fs_ = 7.6
    tx = ["channel\ncoding +\ninterleaving", "QAM\nmapping", "serial-to-\nparallel", "IFFT\n$N$ = 2048",
          "add CP\n144 samples", "parallel-\nto-serial", "DAC + RF up\n30.72 MS/s"]
    rx = ["RF down\n+ ADC", "remove\nCP", "serial-to-\nparallel", "FFT\n$N$ = 2048",
          "one-tap\nequalizer\n$Y_k/H_k$", "QAM\ndemapping", "deinterleave\n+ decode"]
    ytx, yrx = 5.0, 1.0
    xs = [x0 + k * (bw + gap) for k in range(7)]
    ax.text(0.05, 6.65, "Transmitter", fontsize=9.5, fontweight="bold", va="center")
    ax.text(0.05, 2.75, "Receiver", fontsize=9.5, fontweight="bold", va="center")
    arrow(ax, 0.15, ytx + bh / 2, x0, ytx + bh / 2)
    ax.text(0.55, ytx + bh / 2 + 0.1, "bits", ha="center", va="bottom", fontsize=8)
    for k, (x, t) in enumerate(zip(xs, tx)):
        fc = "#DCE9F5" if k in (3, 4) else "#EEF3F8"
        box(ax, x, ytx, bw, bh, t, fontsize=fs_, fc=fc)
        if k < 6:
            arrow(ax, x + bw, ytx + bh / 2, x + bw + gap, ytx + bh / 2)
    ax.text(xs[2] + bw / 2, ytx - 0.1, "2048 subcarriers,\n1200 used + pilots", ha="center", va="top",
            fontsize=7, color="#555555")
    xr = xs[::-1]
    for k, (x, t) in enumerate(zip(xr, rx)):
        fc = "#DCE9F5" if k in (1, 3) else "#EEF3F8"
        box(ax, x, yrx, bw, bh, t, fontsize=fs_, fc=fc)
        if k < 6:
            arrow(ax, x, yrx + bh / 2, x - gap, yrx + bh / 2)
    arrow(ax, xr[-1], yrx + bh / 2, 0.15, yrx + bh / 2)
    ax.text(0.55, yrx + bh / 2 + 0.1, "bits", ha="center", va="bottom", fontsize=8)
    ax.text(xr[4] + bw / 2, yrx + bh + 0.08, "pilot-based $H_k$ estimates", ha="center", va="bottom",
            fontsize=7, color="#555555")
    # channel block between the rows, under the last transmitter block
    xc = xs[-1] + bw / 2
    box(ax, xs[-1] - 0.5, 2.85, bw + 0.5, 1.4, "channel\nmultipath $h(\\tau)$\n+ noise", fontsize=fs_,
        fc="#FDF0E6")
    xc = xs[-1] + bw / 2 - 0.25 + 0.25
    arrow(ax, xc, ytx, xc, 4.25)
    arrow(ax, xc, 2.85, xc, yrx + bh)

    # ---- inset timing diagram
    ax2 = fig.add_axes([0.04, 0.02, 0.93, 0.36])
    Ts, Tcp, Tu, dly = 71.4, 4.7, 66.7, 3.0
    ax2.set_xlim(-17, 80)
    ax2.set_ylim(-0.5, 3.9)
    ax2.axis("off")
    ax2.text(-17, 3.65, "Cyclic prefix timing (LTE, normal CP)", fontsize=8.5, fontweight="bold", va="center")
    # direct path
    yA, yB, h = 1.75, 0.65, 0.8
    ax2.add_patch(Rectangle((-6, yA), 6, h, fc="#E6E6E6", ec="#999999", lw=0.8))
    ax2.add_patch(Rectangle((0, yA), Tcp, h, fc="#F2B48A", ec=INK, lw=0.9))
    ax2.add_patch(Rectangle((Tcp, yA), Tu, h, fc="#CFE2F3", ec=INK, lw=0.9))
    ax2.text(Tcp + Tu / 2, yA + h / 2, "useful part $T_u$ = 66.7 µs", ha="center", va="center", fontsize=7.6)
    ax2.text(Tcp / 2, yA + h / 2, "CP", ha="center", va="center", fontsize=7)
    ax2.text(-7, yA + h / 2, "direct path", ha="right", va="center", fontsize=7.6)
    # echo delayed by 3 us
    ax2.add_patch(Rectangle((-6, yB), 6 + dly, h, fc="#E6E6E6", ec="#999999", lw=0.8, hatch="////"))
    ax2.add_patch(Rectangle((dly, yB), Tcp, h, fc="#F9DCC8", ec=INK, lw=0.9, ls="--"))
    ax2.add_patch(Rectangle((dly + Tcp, yB), Tu, h, fc="#E5EFF8", ec=INK, lw=0.9, ls="--"))
    ax2.text(dly + Tcp + Tu / 2, yB + h / 2, "echo of the same symbol, delayed 3 µs", ha="center",
             va="center", fontsize=7.6)
    ax2.text(-7, yB + h / 2, "echo (+3 µs)", ha="right", va="center", fontsize=7.6)
    # symbol length and CP length
    ax2.annotate("", xy=(0, 2.85), xytext=(Ts, 2.85), arrowprops=dict(arrowstyle="<|-|>", lw=0.8, mutation_scale=7))
    ax2.text(Ts / 2, 2.9, "one OFDM symbol, 71.4 µs = CP 4.7 µs + 66.7 µs", ha="center", va="bottom", fontsize=7.6)
    # FFT window
    ax2.plot([Tcp, Tcp], [0.0, 2.6], color=COLORS[1], lw=1.0, ls=":")
    ax2.plot([Ts, Ts], [0.0, 2.6], color=COLORS[1], lw=1.0, ls=":")
    ax2.annotate("", xy=(Tcp, 0.2), xytext=(Ts, 0.2),
                 arrowprops=dict(arrowstyle="<|-|>", lw=0.8, color=COLORS[1], mutation_scale=7))
    ax2.text((Tcp + Ts) / 2, 0.15, "FFT window: only the current symbol from both paths", ha="center",
             va="top", fontsize=7.4, color=COLORS[1])
    ax2.annotate("previous symbol's echo\nends at 3 µs, inside the CP", xy=(1.5, yB + 0.1), xytext=(-16.5, -0.15),
                 fontsize=7, va="center", ha="left",
                 arrowprops=dict(arrowstyle="-|>", lw=0.7, color=INK, mutation_scale=7))
    save(fig, "30", "fig-30-5-ofdm-transceiver")


# ---------------------------------------------------------------------------
def fig_30_6():
    """Signal-level diagram of the 10 km, 5.8 GHz link budget."""
    stages = ["transmitter", "after Tx\ncable", "EIRP (after\nTx antenna)", "after free-\nspace loss",
              "after Rx\nantenna", "receiver\ninput"]
    fspl = 20 * np.log10(4 * np.pi * 10e3 * 5.8e9 / C0)
    steps = [-1.0, +28.0, -fspl, +28.0, -1.0]
    lv = [20.0]
    for s_ in steps:
        lv.append(lv[-1] + s_)
    noise = -174 + 10 * np.log10(20e6) + 5
    req = noise + 25
    fig, ax = new_fig(6.4, 4.3)
    hw = 0.28
    for k, y in enumerate(lv):
        ax.plot([k - hw, k + hw], [y, y], color=COLORS[0], lw=2.6, solid_capstyle="butt")
        if k < len(lv) - 1:
            ax.plot([k + hw, k + 1 - hw], [y, lv[k + 1]], color=COLORS[0], lw=1.0, ls="-")
    # level labels
    pos = {0: ("above", 0), 1: ("below", 0), 2: ("above", 0), 3: ("below", 0), 4: ("above", 0), 5: ("above", 0)}
    for k, y in enumerate(lv):
        where, _ = pos[k]
        ax.text(k, y + (3.5 if where == "above" else -3.5), f"{y:+.1f}".replace("-", "−"),
                ha="center", va="bottom" if where == "above" else "top", fontsize=8.5, color=COLORS[0])
    lbls = ["−1 dB", "+28 dBi", f"−{fspl:.1f} dB", "+28 dBi", "−1 dB"]
    for k, t in enumerate(lbls):
        xm = k + 0.5
        ym = (lv[k] + lv[k + 1]) / 2
        dy = {0: 5, 4: -6}.get(k, 0)
        dx, ha = (-0.07, "right") if k == 3 else (0.07, "left")
        ax.text(xm + dx, ym + dy, t, fontsize=8, color="#555555", ha=ha, va="center")
    ax.axhline(noise, color=INK, ls="--", lw=0.9)
    ax.text(-0.35, noise - 2.5, f"noise floor −{abs(noise):.1f} dBm (20 MHz, NF 5 dB)", fontsize=8.5, va="top")
    ax.axhline(req, color=COLORS[1], ls=":", lw=1.3)
    ax.text(-0.35, req + 2.5, f"required for 256-QAM:\n−{abs(req):.1f} dBm (noise + 25 dB)", fontsize=8.5,
            va="bottom", color=COLORS[1])
    xb = 5.38
    ax.annotate("", xy=(xb, req), xytext=(xb, lv[-1]),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.0, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.text(xb + 0.07, (req + lv[-1]) / 2, f"margin\n{lv[-1] - req:.1f} dB", fontsize=8.5, va="center",
            color=COLORS[1])
    xa = 5.95
    ax.annotate("", xy=(xa, noise), xytext=(xa, lv[-1]),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.0, mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.text(xa + 0.07, (noise + req) / 2 - 2, f"SNR\n{lv[-1] - noise:.1f} dB", fontsize=8.5, va="center")
    ax.plot([5 + hw, xa], [lv[-1], lv[-1]], color="#999999", lw=0.6, ls=":")
    ax.set_xticks(range(len(lv)))
    ax.set_xticklabels(stages, fontsize=8)
    ax.set_xlim(-0.45, 6.6)
    ax.set_ylim(-110, 60)
    ax.set_ylabel("signal level (dBm)")
    ax.set_title("10 km link at 5.8 GHz, 28 dBi dishes, 20 dBm transmitter", fontsize=10)
    ax.grid(True, axis="y", lw=0.5)
    save(fig, "30", "fig-30-6-link-budget-levels")


if __name__ == "__main__":
    fig_30_1()
    fig_30_2()
    fig_30_3()
    fig_30_4()
    fig_30_5()
    fig_30_6()
