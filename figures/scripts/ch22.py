"""Figures for Chapter 22 — Discrete Fourier Transform.

Run from the repository root:  python figures/scripts/ch22.py
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, schematic, save, COLORS, INK, GRID  # noqa: E402

CH = "22"
BLUE, RED, GREEN, PURPLE, ORANGE, SKY = COLORS[0], COLORS[1], COLORS[2], COLORS[3], COLORS[4], COLORS[5]


def _stem(ax, n, x, color=INK, ms=4.5, lw=1.1, bottom=0, zorder=3, label=None):
    ml, sl, bl = ax.stem(n, x, basefmt=" ", bottom=bottom, label=label)
    plt.setp(sl, color=color, lw=lw, zorder=zorder)
    plt.setp(ml, color=color, ms=ms, zorder=zorder + 1)
    return ml, sl


def fig_22_1():
    """DFT samples of the DTFT of a 16-sample cosine record."""
    N = 16
    n = np.arange(N)
    x = np.cos(2 * np.pi * 0.15 * n)
    nu = np.linspace(0, 1, 4001)
    Xd = np.abs(np.exp(-2j * np.pi * np.outer(nu, n)) @ x)
    Xk = np.abs(np.fft.fft(x))
    fig, ax = new_fig(6.4, 3.8)
    ax.plot(nu, Xd, color=BLUE, lw=1.5, label=r"DTFT $|X(e^{j\omega})|$ of the 16-sample record")
    _stem(ax, n / N, Xk, color=RED, ms=5, label=r"DFT $|X[k]|$ at $\omega/2\pi = k/16$")
    ax.axvline(0.5, color="0.5", ls=":", lw=1)
    ax.text(0.5, 9.3, "mirror symmetry about 0.5\n(real signal: $X[N-k]=X^*[k]$)", ha="center", va="bottom",
            fontsize=8.5, color="0.3", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.annotate("", xy=(4 / 16, -0.55), xytext=(3 / 16, -0.55),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=INK, mutation_scale=8))
    ax.text(3.5 / 16, -0.75, "1/N = 1/16", ha="center", va="top", fontsize=8.5)
    ax.text(0.15, 8.6, "0.15", ha="center", fontsize=8, color=BLUE)
    ax.text(0.85, 8.6, "0.85", ha="center", fontsize=8, color=BLUE)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.7, 11.5)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"normalised frequency $\omega/2\pi$ (cycles per sample)")
    ax.set_ylabel("magnitude")
    ax.set_xticks(np.arange(0, 1.01, 0.125))
    ax.legend(loc="center", fontsize=8, bbox_to_anchor=(0.5, 0.52), frameon=True, framealpha=0.95,
              edgecolor="none")
    save(fig, CH, "fig-22-1-dtft-dft-samples")


def fig_22_2():
    """Eight-point radix-2 DIT FFT flow graph."""
    fig, ax = schematic(6.8, 4.6, xlim=(-1.4, 14.2), ylim=(-0.9, 9.6))
    order = [0, 4, 2, 6, 1, 5, 3, 7]
    ys = [8.4 - 1.1 * i for i in range(8)]
    cols = [0.6, 3.3, 6.0, 8.7]
    node_kw = dict(color=INK, ms=4, zorder=5)
    for c in cols:
        for y in ys:
            ax.plot(c, y, "o", **node_kw)
    for i, y in enumerate(ys):
        ax.text(cols[0] - 0.2, y, f"$x[{order[i]}]$", ha="right", va="center", fontsize=9)
        ax.text(cols[3] + 0.2, y, f"$X[{i}]$", ha="left", va="center", fontsize=9)
    stage_tw = [lambda j: 0, lambda j: 2 * (j % 2), lambda j: j]
    spans = [1, 2, 4]
    for s, span in enumerate(spans):
        c0, c1 = cols[s], cols[s + 1]
        done = set()
        j_in_group = 0
        for top in range(8):
            if top in done:
                continue
            bot = top + span
            done.add(bot)
            k = top % span
            tw = (k * (8 // (2 * span)))
            yt, yb = ys[top], ys[bot]
            # straight paths
            ax.plot([c0, c1], [yt, yt], color=INK, lw=0.9)
            ax.plot([c0, c1], [yb, yb], color=INK, lw=0.9)
            # cross paths
            ax.plot([c0, c1], [yt, yb], color=INK, lw=0.9)
            ax.plot([c0, c1], [yb, yt], color=INK, lw=0.9)
            # twiddle on the lower input branch
            ax.text(c0 + 0.12, yb + 0.08, f"$W_8^{tw}$", ha="left", va="bottom", fontsize=7.5, color=BLUE)
            # -1 on the lower output branch
            ax.text(c1 - 0.15, yb + 0.08, "$-1$", ha="right", va="bottom", fontsize=7.5, color=RED)
        ax.text((c0 + c1) / 2, 9.15, f"Stage {s + 1}", ha="center", va="bottom", fontsize=9.5, weight="bold")
    ax.text(cols[0] - 0.9, 9.15, "bit-reversed\ninput", ha="center", va="bottom", fontsize=8, color="0.35")
    ax.text(cols[3] + 0.75, 9.15, "natural\norder", ha="center", va="bottom", fontsize=8, color="0.35")
    # inset butterfly
    bx0, bx1 = 10.9, 12.7
    by0, by1 = 7.9, 5.9
    ax.add_patch(Rectangle((10.2, 4.3), 3.95, 5.2, fill=False, ec="0.6", lw=0.8))
    ax.text(12.18, 9.2, "one butterfly", ha="center", va="center", fontsize=9, weight="bold")
    for y in (by0, by1):
        ax.plot(bx0, y, "o", **node_kw)
        ax.plot(bx1, y, "o", **node_kw)
        ax.plot([bx0, bx1], [y, y], color=INK, lw=1.0)
    ax.plot([bx0, bx1], [by0, by1], color=INK, lw=1.0)
    ax.plot([bx0, bx1], [by1, by0], color=INK, lw=1.0)
    ax.text(bx0 - 0.12, by0, "$a$", ha="right", va="center", fontsize=10)
    ax.text(bx0 - 0.12, by1, "$b$", ha="right", va="center", fontsize=10)
    ax.text(bx0 + 0.12, by1 - 0.1, "$W$", ha="left", va="top", fontsize=9, color=BLUE)
    ax.text(bx1 - 0.15, by1 - 0.1, "$-1$", ha="right", va="top", fontsize=9, color=RED)
    ax.text(bx1 + 0.15, by0, "$a+Wb$", ha="left", va="center", fontsize=9.5)
    ax.text(bx1 + 0.15, by1, "$a-Wb$", ha="left", va="center", fontsize=9.5)
    ax.text(12.18, 4.5, "1 complex multiply,\n2 outputs", ha="center", va="bottom", fontsize=8, color="0.35")
    ax.text(12.2, 2.4, r"$W_N^k=e^{-j2\pi k/N}$" + "\n\n3 stages × 4 butterflies\n= 12 multiplications\n(direct DFT: 64)",
            ha="center", va="center", fontsize=8.5)
    save(fig, CH, "fig-22-2-radix2-flowgraph")


def _db(v, floor=-300):
    return np.maximum(20 * np.log10(np.abs(v) + 1e-320), floor)


def fig_22_3():
    """Leakage for an on-bin and a half-bin tone, rectangular window."""
    fs, N = 25600.0, 4096
    n = np.arange(N)
    k = np.arange(150, 173)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.8), sharex=True)
    for ax, f0, title in ((a1, 1000.0, "1000 Hz tone: exactly on bin 160"),
                          (a2, 1003.125, "1003.125 Hz tone: bin 160.5, half-way between bins")):
        x = np.cos(2 * np.pi * f0 * n / fs)
        X = np.fft.fft(x)[k] / (N / 2)
        d = _db(X)
        floor = -80
        dd = np.maximum(d, floor)
        ml, sl = _stem(ax, k, dd, color=BLUE, ms=4.5, bottom=floor)
        if f0 == 1000.0:
            ax.text(171.5, -74, "all other bins below −300 dB (shown at the floor)", ha="right",
                    va="bottom", fontsize=8.5, color="0.3")
        else:
            kc = np.linspace(150, 172.5, 4000)
            off = kc - 160.5
            Wk = np.abs(np.sin(np.pi * off) / (N * np.sin(np.pi * off / N)))
            ax.plot(kc, 20 * np.log10(Wk + 1e-12), color="0.6", lw=0.9, zorder=1,
                    label="rectangular-window (Dirichlet) kernel")
            ax.axhline(-3.92, color=RED, ls=":", lw=0.9)
            ax.annotate("scalloping loss: −3.92 dB\nin bins 160 and 161", xy=(160, -3.92), xytext=(150.2, -6),
                        fontsize=8.5, color=RED, va="top", ha="left",
                        arrowprops=dict(arrowstyle="-|>", lw=0.8, color=RED, mutation_scale=8))
            ax.annotate("first side lobe −13.3 dB", xy=(161.93, -13.3), xytext=(163.3, -5.3), fontsize=8.5,
                        color="0.3", va="top",
                        arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
            v = d[k == 172][0]
            ax.annotate(f"{v:.1f} dB at 11.5 bins".replace("-", "−") + "\n(−33.4 dB at 15.5 bins)", xy=(172, v),
                        xytext=(168.3, -10.3), fontsize=8, ha="center", va="top",
                        arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
            ax.legend(loc="lower left", fontsize=8)
        ax.set_ylim(-80, 3)
        ax.set_ylabel("magnitude (dB re tone)")
        ax.set_title(title, loc="left", fontsize=10)
    a2.set_xlim(149.5, 172.5)
    a2.set_xticks(range(150, 173, 2))
    a2.set_xlabel(r"bin index $k$  ($f_s$ = 25.6 kHz, $N$ = 4096, $\Delta f$ = 6.25 Hz)")
    fig.tight_layout(h_pad=0.8)
    save(fig, CH, "fig-22-3-leakage-on-off-bin")


def fig_22_4():
    """Window shapes and their spectra."""
    N = 64
    wins = [("rectangular", np.ones(N), INK),
            ("Hann", signal.get_window("hann", N), BLUE),
            ("Hamming", signal.get_window("hamming", N), GREEN),
            ("Blackman–Harris (4-term)", signal.get_window("blackmanharris", N), PURPLE),
            ("flat-top (5-term)", signal.get_window("flattop", N), ORANGE)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.7), gridspec_kw=dict(width_ratios=[1, 1.35]))
    t = np.arange(N) / N
    M = 64
    for name, w, c in wins:
        a1.plot(t, w, color=c, lw=1.4, label=name)
        W = np.fft.fftshift(np.abs(np.fft.fft(w, N * M)))
        W /= W.max()
        b = (np.arange(N * M) - N * M // 2) / M
        sel = np.abs(b) <= 8.2
        a2.plot(b[sel], 20 * np.log10(W[sel] + 1e-12), color=c, lw=1.1)
    a1.axhline(0, color="0.5", lw=0.6)
    a1.set_xlim(0, 1)
    a1.set_ylim(-0.1, 1.1)
    a1.set_xlabel("$n/N$")
    a1.set_ylabel("amplitude")
    a1.legend(loc="upper center", fontsize=7, bbox_to_anchor=(0.5, -0.2), ncol=2, handlelength=1.4)
    a1.set_title("time", fontsize=10)
    for lvl, c, txt in ((-13.3, INK, "−13.3"), (-31.5, BLUE, "−31.5"), (-42.7, GREEN, "−42.7"),
                        (-92.0, PURPLE, "−92")):
        a2.axhline(lvl, color=c, ls=":", lw=0.8)
        a2.text(-7.85, lvl + 0.8, txt, ha="left", va="bottom", fontsize=7.5, color=c,
                bbox=dict(fc="white", ec="none", pad=0.6))
    a2.set_xlim(-8, 8)
    a2.set_ylim(-120, 2)
    a2.set_xticks(range(-8, 9, 2))
    a2.set_xlabel("bin offset")
    a2.set_ylabel("normalised magnitude (dB)")
    a2.set_title("spectrum (highest side lobes marked)", fontsize=10)
    fig.tight_layout(w_pad=1.2)
    save(fig, CH, "fig-22-4-window-shapes-spectra")


def fig_22_5():
    """Zero padding versus a longer record: two Doppler targets 20 Hz apart."""
    prf = 2000.0
    f1, f2 = 100.0, 120.0

    def spec(Nrec, Nfft):
        n = np.arange(Nrec)
        x = np.exp(2j * np.pi * f1 * n / prf) + np.exp(2j * np.pi * f2 * n / prf)
        w = signal.get_window("hann", Nrec)
        X = np.fft.fftshift(np.fft.fft(x * w, Nfft))
        f = (np.arange(Nfft) - Nfft // 2) * prf / Nfft
        return f, np.abs(X)

    f64, X64 = spec(64, 64)
    f512, X512 = spec(64, 512)
    f256, X256 = spec(256, 4096)
    ref = X512.max()
    fig, ax = new_fig(6.4, 3.9)
    ax.plot(f256, 20 * np.log10(X256 / X256.max() + 1e-12), ls="--", color=GREEN, lw=1.3,
            label="256-pulse record (128 ms), Hann: 7.8 Hz bins — two peaks")
    ax.plot(f512, 20 * np.log10(X512 / ref + 1e-12), color=BLUE, lw=1.2,
            label="64 pulses zero-padded to 512: 3.9 Hz spacing — one lobe")
    sel = (f64 >= -100) & (f64 <= 300)
    ml, sl = _stem(ax, f64[sel], 20 * np.log10(X64[sel] / ref + 1e-12), color=RED, ms=5, bottom=-40,
                   label="64-point DFT: 31.25 Hz bins")
    for fx in (f1, f2):
        ax.axvline(fx, color="0.6", lw=0.7, ls=":")
    ax.text(110, 1.2, "targets 100 and 120 Hz", ha="center", va="bottom", fontsize=8, color="0.3")
    ax.annotate("", xy=(31.25 * 6, -38.5), xytext=(31.25 * 5, -38.5),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.9, color=RED, mutation_scale=8))
    ax.text(215, -36.5, "1/T = 31.25 Hz\n(64 pulses, 32 ms)", ha="left", va="center", fontsize=8.5, color=RED)
    ax.set_xlim(-100, 300)
    ax.set_ylim(-40, 4)
    ax.set_xlabel("Doppler frequency (Hz)")
    ax.set_ylabel("magnitude (dB)")
    ax.legend(loc="upper center", fontsize=8, bbox_to_anchor=(0.5, -0.17), ncol=1)
    save(fig, CH, "fig-22-5-zero-padding")


def fig_22_6():
    """Single periodogram versus Welch estimate for a simulated 5-minute EEG record."""
    fs, N = 256.0, 76800
    rng = np.random.default_rng(22)
    f = np.fft.rfftfreq(N, 1 / fs)
    S = 10 ** 2.6 / (1 + f) ** 1.6 + 60 * np.exp(-(f - 10) ** 2 / (2 * 0.8 ** 2))   # uV^2/Hz, one-sided
    wn = rng.standard_normal(N)
    X = np.fft.rfft(wn) * np.sqrt(S * fs / 2)
    x = np.fft.irfft(X, N)
    fp, Pp = signal.periodogram(x, fs=fs, window="boxcar")
    fw, Pw = signal.welch(x, fs=fs, window="hann", nperseg=512, noverlap=256)
    K = (N - 512) // 256 + 1
    sd = np.sqrt((1 + 2 / 36) / K)
    fig, ax = new_fig(6.4, 3.9)
    sel = fp <= 40
    ax.plot(fp[sel], 10 * np.log10(Pp[sel]), color="0.72", lw=0.35,
            label="periodogram, full record (76 800 samples, 0.0033 Hz bins)")
    selw = fw <= 40
    ax.fill_between(fw[selw], 10 * np.log10(Pw[selw] * (1 - sd)), 10 * np.log10(Pw[selw] * (1 + sd)),
                    color=BLUE, alpha=0.3, lw=0, label=r"Welch $\pm1\sigma$ (+0.25/−0.27 dB)")
    ax.plot(fw[selw], 10 * np.log10(Pw[selw]), color=BLUE, lw=1.8,
            label=f"Welch: 512-sample Hann, 50 % overlap, K = {K}, 0.5 Hz bins")
    ax.plot(f[f <= 40], 10 * np.log10(S[f <= 40]), color=RED, lw=0.9, ls="--", label="true PSD of the model")
    ax.annotate("alpha peak (8–13 Hz)", xy=(10, 10 * np.log10(Pw[fw == 10][0])), xytext=(16, 24),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3", mutation_scale=8))
    ax.set_xlim(0, 40)
    ax.set_ylim(-10, 30)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel(r"PSD (dB re 1 µV$^2$/Hz)")
    ax.legend(loc="lower left", fontsize=7.3, frameon=True, framealpha=0.92, edgecolor="none")
    save(fig, CH, "fig-22-6-periodogram-vs-welch")


if __name__ == "__main__":
    fig_22_1()
    fig_22_2()
    fig_22_3()
    fig_22_4()
    fig_22_5()
    fig_22_6()
