"""Figures for Chapter 29 — Random Signals and Communication Noise.

Run from the repository root:  python figures/scripts/ch29.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from scipy.special import erfc

from figstyle import new_fig, save, box, arrow, COLORS, INK


def Q(x):
    return 0.5 * erfc(np.asarray(x) / np.sqrt(2))


def db2lin(x):
    return 10 ** (np.asarray(x) / 10)


# ---------------------------------------------------------------------------
def fig_29_1():
    """Bandpass Gaussian noise, its envelope, and their amplitude distributions."""
    rng = np.random.default_rng(29)
    fs = 50e3                       # sample rate (Hz), > 2 x 10.5 kHz
    n = 2 ** 22                     # 84 s of noise, so the histograms use nearly independent samples
    f0, bw = 10e3, 1e3
    # complex baseband noise, ideal low-pass |f| < bw/2, then n = Re{z e^{j w0 t}}
    z = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    Z = np.fft.fft(z)
    f = np.fft.fftfreq(n, 1 / fs)
    Z[np.abs(f) > bw / 2] = 0
    z = np.fft.ifft(Z)
    z /= np.sqrt(np.mean(np.abs(z) ** 2) / 2)          # var(nI) = var(nQ) = 1
    t = np.arange(n) / fs
    x = np.real(z * np.exp(2j * np.pi * f0 * t))       # sigma = 1 V
    r = np.abs(z)                                      # Rayleigh envelope

    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], hspace=0.45, wspace=0.28)
    ax = fig.add_subplot(gs[0, :])
    fs_plot = 400e3                 # re-synthesise a 2 ms excerpt on a fine grid for display
    k0 = int(0.1 * fs)
    zz = np.fft.fft(z[k0:k0 + 512])
    zi = np.fft.ifft(np.concatenate([zz[:256], np.zeros(512 * 7, complex), zz[256:]])) * 8
    ti = k0 / fs + np.arange(512 * 8) / fs_plot
    xi = np.real(zi * np.exp(2j * np.pi * f0 * ti))
    seg = slice(int(4e-3 * fs_plot), int(6e-3 * fs_plot))   # middle of the block, away from edges
    tm = (ti[seg] - ti[seg][0]) * 1e3
    ax.plot(tm, xi[seg], color=COLORS[0], lw=0.9, label=r"noise $n(t)$")
    ax.plot(tm, np.abs(zi[seg]), color=COLORS[1], lw=1.6, label=r"envelope $r(t)$")
    ax.plot(tm, -np.abs(zi[seg]), color=COLORS[1], lw=1.0, ls="--")
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_xlim(0, 2)
    ax.set_ylim(-4, 4)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("voltage (V)")
    ax.set_title(r"Bandpass noise: $f_c$ = 10 kHz, $B$ = 1 kHz, $\sigma$ = 1 V", fontsize=10)
    ax.legend(loc="upper right", ncol=2, fontsize=8.5)

    N = 100_000
    step = n // N                   # 0.8 ms spacing, about one correlation time
    xs_, rs_ = x[::step][:N], r[::step][:N]
    ax2 = fig.add_subplot(gs[1, 0])
    u = np.linspace(-4, 4, 400)
    ax2.hist(xs_, bins=80, range=(-4, 4), density=True, color=COLORS[0], alpha=0.35,
             label="histogram")
    ax2.plot(u, np.exp(-u ** 2 / 2) / np.sqrt(2 * np.pi), color=COLORS[0],
             label=r"Gaussian, $\sigma$ = 1")
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(0, 0.5)
    ax2.set_xlabel(r"noise sample $n$ (V)")
    ax2.set_ylabel("probability density (1/V)")
    ax2.legend(loc="upper left", fontsize=8)

    ax3 = fig.add_subplot(gs[1, 1])
    v = np.linspace(0, 5, 400)
    ax3.hist(rs_, bins=80, range=(0, 5), density=True, color=COLORS[1], alpha=0.35,
             label="histogram")
    ax3.plot(v, v * np.exp(-v ** 2 / 2), color=COLORS[1], label=r"Rayleigh, $\sigma$ = 1")
    a6 = np.sqrt(2 * np.log(1e6))
    ax3.axvline(a6, color=INK, ls=":", lw=1.2)
    ax3.set_xlim(0, 5.6)
    ax3.set_ylim(0, 0.75)
    ax3.annotate(r"$P(r>5.26\sigma)=10^{-6}$", xy=(a6, 0.30), xytext=(2.3, 0.36),
                 fontsize=8.5, va="center",
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8))
    ax3.set_xlabel(r"envelope $r$ (V)")
    ax3.set_ylabel("probability density (1/V)")
    ax3.legend(loc="upper right", fontsize=8)
    save(fig, "29", "fig-29-1-gaussian-noise-and-envelope")


# ---------------------------------------------------------------------------
def fig_29_2():
    """Equivalent noise bandwidth of a first-order RC low-pass filter."""
    fc = 10.0
    BN = np.pi / 2 * fc
    f = np.linspace(0, 60, 1200)
    g = 1 / (1 + (f / fc) ** 2)
    fig, ax = new_fig(6.4, 3.8)
    ax.add_patch(Rectangle((0, 0), BN, 1, fc=COLORS[5], alpha=0.18, ec="none"))
    ax.add_patch(Rectangle((0, 0), BN, 1, fc="none", ec=COLORS[0], ls="--", lw=1.4))
    ax.fill_between(f, g, color=COLORS[1], alpha=0.12)
    ax.plot(f, g, color=COLORS[1], label=r"$|H(f)|^2=1/[1+(f/f_c)^2]$")
    ax.plot([], [], color=COLORS[0], ls="--", label=r"rectangle of width $B_N$, same area")
    ax.plot([fc, fc], [0, 0.5], color=INK, ls=":", lw=1.2)
    ax.plot([0, fc], [0.5, 0.5], color=INK, ls=":", lw=1.0)
    ax.plot(fc, 0.5, "o", color=INK, ms=4)
    ax.text(fc + 0.6, 0.53, r"$-3$ dB point" "\n" r"$f_c$ = 10 kHz", fontsize=9, va="bottom")
    ax.annotate(r"$B_N=(\pi/2)f_c$ = 15.7 kHz", xy=(BN, 0.9), xytext=(22, 0.9),
                fontsize=9.5, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=9))
    ax.text(5.0, 0.22, "equal\nareas", ha="center", fontsize=9.5)
    ax.text(32, 0.12, "skirt beyond $B_N$\nbalances the corner\ncut off inside it",
            fontsize=8.5, ha="center", color=COLORS[1])
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("frequency (kHz)")
    ax.set_ylabel(r"power gain $|H(f)|^2$")
    ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.0, 1.02))
    tbl = ("Butterworth  $B_N/f_c$\n"
           "order 1     1.571\n"
           "order 2     1.111\n"
           "order 3     1.047\n"
           "order 4     1.026")
    ax.text(46, 0.38, tbl, fontsize=8.5, family="DejaVu Sans Mono", va="center", ha="center",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", lw=0.8))
    save(fig, "29", "fig-29-2-noise-bandwidth")


# ---------------------------------------------------------------------------
def _amp(ax, cx, cy, text, w=1.6, h=1.2, fc="#EEF3F8"):
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(Polygon([[x, y], [x, y + h], [x + w, cy]], closed=True, fc=fc, ec=INK, lw=1.0))
    ax.text(x + w * 0.36, cy, text, ha="center", va="center", fontsize=9)
    return x, x + w


def _mixer(ax, cx, cy, rad=0.5):
    ax.add_patch(Circle((cx, cy), rad, fc="#FDF0E6", ec=INK, lw=1.0))
    d = rad * 0.7
    ax.plot([cx - d, cx + d], [cy - d, cy + d], color=INK, lw=1.0)
    ax.plot([cx - d, cx + d], [cy + d, cy - d], color=INK, lw=1.0)
    arrow(ax, cx, cy + rad + 0.6, cx, cy + rad)
    ax.text(cx + 0.15, cy + rad + 0.45, "LO", ha="left", va="center", fontsize=8.5)
    return cx - rad, cx + rad


def _antenna(ax, x, y):
    ax.plot([x, x], [y, y + 0.9], color=INK, lw=1.2)
    ax.plot([x - 0.3, x, x + 0.3, x - 0.3], [y + 1.3, y + 0.9, y + 1.3, y + 1.3], color=INK, lw=1.2)


def fig_29_3():
    """Friis noise budget of a three-stage receiver, and the mixer-first alternative."""
    F = {"LNA": 10 ** 0.1, "MIX": 10 ** 0.8, "IF": 10 ** 0.4}
    G = {"LNA": 10 ** 1.5, "MIX": 10 ** -0.7, "IF": 10 ** 3.0}
    names = {"LNA": "LNA", "MIX": "mixer", "IF": "IF amplifier"}
    pars = {"LNA": "NF 1.0 dB\nG 15 dB", "MIX": "NF 8 dB\nG −7 dB", "IF": "NF 4 dB\nG 30 dB"}

    def cascade(order):
        contrib, cum, gtot, tot = [], [], 1.0, 0.0
        for k, s in enumerate(order):
            c = F[s] if k == 0 else (F[s] - 1) / gtot
            contrib.append(c)
            tot += c
            cum.append(10 * np.log10(tot))
            gtot *= G[s]
        return contrib, cum, tot

    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.set_xlim(0, 17)
    ax.set_ylim(0.0, 11.2)
    ax.set_aspect("equal")
    ax.axis("off")
    cols = [4.0, 6.6, 9.2]
    xtot = 15.4
    grey = "#555555"

    def chain(cy, order):
        _antenna(ax, 2.5, cy)
        xprev = 2.5
        for cx, s in zip(cols, order):
            if s == "MIX":
                x0, x1 = _mixer(ax, cx, cy)
            else:
                x0, x1 = _amp(ax, cx, cy, "LNA" if s == "LNA" else "IF")
            arrow(ax, xprev, cy, x0, cy)
            ax.text(cx, cy - 0.75, names[s], ha="center", va="top", fontsize=8.5)
            xprev = x1
        arrow(ax, xprev, cy, 11.0, cy)
        box(ax, 11.0, cy - 0.5, 2.5, 1.0, "demodulator", fontsize=8.5)

    # --- receiver as built
    cy = 8.4
    ax.text(0.1, 10.6, "Receiver as built: LNA first", fontsize=9.5, fontweight="bold", va="center")
    chain(cy, ["LNA", "MIX", "IF"])
    contrib, cum, tot = cascade(["LNA", "MIX", "IF"])
    rows = [(6.55, "stage"), (5.45, "term in $F$"), (4.75, "NF so far")]
    for y, lab in rows:
        ax.text(0.1, y, lab, fontsize=8.5, color=grey, va="center")
    for cx, s, c, cm in zip(cols, ["LNA", "MIX", "IF"], contrib, cum):
        ax.text(cx, 6.55, pars[s], ha="center", va="center", fontsize=8, linespacing=1.1)
        ax.text(cx, 5.45, f"{c:.3f}", ha="center", va="center", fontsize=9, color=COLORS[0])
        ax.text(cx, 4.75, f"{cm:.2f} dB", ha="center", va="center", fontsize=9, color=COLORS[1],
                fontweight="bold")
    ax.text(xtot, 5.45, f"F = {tot:.3f}", ha="center", va="center", fontsize=9, color=COLORS[0])
    ax.text(xtot, 4.75, f"NF = {10*np.log10(tot):.2f} dB", ha="center", va="center", fontsize=9,
            color=COLORS[1], fontweight="bold")
    ax.text(16.9, 10.6,
            r"Sensitivity (B = 200 kHz, SNR$_{\min}$ = 10 dB):" "\n"
            "$-174+53.0+2.2+10=-108.8$ dBm",
            ha="right", va="center", fontsize=8, linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.35", fc="#FFF8E6", ec="#C9A227", lw=0.8))
    ax.plot([0.1, 16.9], [4.15, 4.15], color="#BBBBBB", lw=0.8)

    # --- comparison: mixer first
    cy2 = 2.0
    ax.text(0.1, 3.6, "Comparison: mixer first", fontsize=9.5, fontweight="bold", va="center")
    chain(cy2, ["MIX", "LNA", "IF"])
    contrib2, cum2, tot2 = cascade(["MIX", "LNA", "IF"])
    ax.text(0.1, 0.45, "term in $F$", fontsize=8.5, color=grey, va="center")
    for cx, c in zip(cols, contrib2):
        ax.text(cx, 0.45, f"{c:.3f}", ha="center", va="center", fontsize=9, color=COLORS[0])
    ax.text(xtot, 0.45, f"NF = {10*np.log10(tot2):.2f} dB", ha="center", va="center", fontsize=9,
            color=COLORS[1], fontweight="bold")
    ax.text(xtot, 2.0, f"F = {tot2:.2f}\n{10*np.log10(tot2/tot):.1f} dB worse\nwith the same parts",
            ha="center", va="center", fontsize=8, color=COLORS[1])
    save(fig, "29", "fig-29-3-receiver-cascade")

# ---------------------------------------------------------------------------
def fig_29_4():
    """Threshold detection in Gaussian noise and the ROC."""
    from scipy.stats import norm
    d = np.sqrt(db2lin(13))
    gam = norm.isf(1e-6)
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.32))
    y = np.linspace(-4, 9, 1000)
    p0 = norm.pdf(y)
    p1 = norm.pdf(y - d)
    ax.plot(y, p0, color=COLORS[0], label=r"$f(y\,|\,H_0)$")
    ax.plot(y, p1, color=COLORS[1], label=r"$f(y\,|\,H_1)$")
    m = y >= gam
    ax.fill_between(y[m], p1[m], color=COLORS[1], alpha=0.25)
    ax.fill_between(y[m], p0[m], color=COLORS[0], alpha=0.9)
    ax.axvline(gam, color=INK, ls="--", lw=1.1)
    ax.text(gam + 0.12, 0.49, "threshold\n" r"$\gamma$ = 4.75", fontsize=8.5, va="top")
    ax.text(-0.9, 0.34, r"$H_0$", ha="right", color=COLORS[0], fontsize=10)
    ax.text(5.6, 0.355, r"$H_1$, $d$ = 4.47", ha="left", va="center", color=COLORS[1], fontsize=9)
    ax.annotate(r"$P_D$ = 0.39", xy=(5.4, 0.13), xytext=(6.5, 0.24), fontsize=9, color=COLORS[1],
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9, mutation_scale=9))
    ax.text(-3.8, 0.49, r"$P_{FA}=10^{-6}$: blue tail beyond" "\n" r"$\gamma$ (too thin to see)",
            fontsize=8, color=COLORS[0], va="top")
    ax.set_xlim(-4, 9)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel("normalized matched-filter output $y$")
    ax.set_ylabel("probability density")
    ax.set_title(r"$2E/N_0$ = 13 dB", fontsize=10)

    pfa = np.logspace(-8, 0, 400)
    for snr, c in [(10, COLORS[2]), (13, COLORS[1]), (15, COLORS[3])]:
        dd = np.sqrt(db2lin(snr))
        ax2.semilogx(pfa, Q(norm.isf(pfa) - dd), color=c, label=f"{snr} dB")
    pts = [(1e-6, 0.39, COLORS[1]), (1e-3, 0.92, COLORS[1]), (1e-6, 0.81, COLORS[3])]
    for x_, y_, c in pts:
        ax2.plot(x_, y_, "o", color=c, ms=5, mec="white", mew=0.8, zorder=5)
    ax2.annotate("(10$^{-6}$, 0.39)", xy=(1e-6, 0.39), xytext=(2e-8, 0.48), fontsize=8,
                 arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax2.annotate("(10$^{-3}$, 0.92)", xy=(1e-3, 0.92), xytext=(1.5e-6, 1.0), fontsize=8,
                 arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax2.annotate("(10$^{-6}$, 0.81)", xy=(1e-6, 0.81), xytext=(1.2e-8, 0.86), fontsize=8,
                 arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
    ax2.set_xlim(1e-8, 1)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel(r"false-alarm probability $P_{FA}$")
    ax2.set_ylabel(r"detection probability $P_D$")
    ax2.legend(title=r"$2E/N_0$", loc="lower right", fontsize=8.5, title_fontsize=8.5)
    ax2.set_title("ROC", fontsize=10)
    ax2.grid(True, which="major", lw=0.5)
    save(fig, "29", "fig-29-4-detection-threshold-roc")


# ---------------------------------------------------------------------------
def fig_29_5():
    """BER versus Eb/N0 for common modulations in AWGN."""
    from scipy.optimize import brentq
    x = np.linspace(0, 24, 600)
    g = db2lin(x)
    curves = [
        ("BPSK / QPSK", lambda g: Q(np.sqrt(2 * g)), "-", COLORS[0]),
        ("DPSK", lambda g: 0.5 * np.exp(-g), "--", COLORS[0]),
        ("coherent BFSK", lambda g: Q(np.sqrt(g)), "-", COLORS[2]),
        ("noncoherent BFSK", lambda g: 0.5 * np.exp(-g / 2), "--", COLORS[2]),
        ("16-QAM", lambda g: 0.75 * Q(np.sqrt(0.8 * g)), "-", COLORS[1]),
        ("64-QAM", lambda g: 7 / 12 * Q(np.sqrt(2 / 7 * g)), "-", COLORS[3]),
        ("256-QAM", lambda g: 15 / 32 * Q(np.sqrt(8 / 85 * g)), "-", COLORS[4]),
    ]
    fig, ax = new_fig(6.4, 4.2)
    for name, f, ls, c in curves:
        with np.errstate(divide="ignore"):
            x5 = brentq(lambda d: np.log(f(db2lin(d))) - np.log(1e-5), 0, 30)
        ax.semilogy(x, f(g), ls=ls, color=c, label=f"{name}  ({x5:.1f} dB)")
        ax.plot(x5, 1e-5, "o", color=c, ms=5, mec="white", mew=0.8, zorder=5)
    ax.axhline(1e-5, color=INK, ls="--", lw=0.9)
    ax.text(21.9, 1.3e-5, r"BER = $10^{-5}$", ha="right", va="bottom", fontsize=8.5)
    ax.set_xlim(0, 24)
    ax.set_ylim(1e-7, 0.5)
    ax.set_xlabel(r"$E_b/N_0$ (dB)")
    ax.set_ylabel("bit error rate")
    ax.grid(True, which="major", lw=0.5)
    ax.legend(loc="lower left", fontsize=7.5, handlelength=1.6, borderaxespad=0.3, labelspacing=0.3,
              frameon=True, framealpha=0.95, edgecolor="#CCCCCC")
    save(fig, "29", "fig-29-5-ber-curves")


if __name__ == "__main__":
    fig_29_1()
    fig_29_2()
    fig_29_3()
    fig_29_4()
    fig_29_5()
