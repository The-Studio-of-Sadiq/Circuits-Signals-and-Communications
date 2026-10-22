"""Figures for Chapter 18 — Frequency-Domain System Analysis.

Run from the repository root:  python figures/scripts/ch18.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy import signal

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import new_fig, save, COLORS, INK  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

CH = "18"


# ------------------------------------------------------------------ 18.1
def fig_18_1():
    t = np.linspace(0, 2e-3, 4001)
    f0 = 1e3
    sq = np.sign(np.sin(2 * np.pi * f0 * t))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1.25, 1]))
    a1.plot(t * 1e3, sq, color="0.55", lw=1.2, label="square wave ±1 V")
    for N, c, lw in [(1, COLORS[2], 1.2), (3, COLORS[0], 1.2), (15, COLORS[1], 1.3)]:
        k = np.arange(1, 2 * N, 2)
        s = (4 / np.pi) * np.sum(np.sin(2 * np.pi * np.outer(k, t) * f0) / k[:, None], axis=0)
        lab = f"{N} harmonic" + ("" if N == 1 else "s") + f" (to {k[-1]} kHz)"
        a1.plot(t * 1e3, s, color=c, lw=lw, label=lab)
        if N == 15:
            pk = s[: len(t) // 4].max()
    a1.annotate(f"Gibbs: peak {pk:.2f} V, overshoot ≈ {100 * (pk - 1) / 2:.0f} % of the 2 V jump",
                xy=(0.02, pk), xytext=(0.12, 1.42),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    a1.axhline(0, color=INK, lw=0.5)
    a1.set_xlim(0, 2)
    a1.set_ylim(-1.45, 2.4)
    a1.set_yticks([-1, -0.5, 0, 0.5, 1, 1.5])
    a1.set_xlabel("t (ms)")
    a1.set_ylabel("V")
    a1.set_title("Partial Fourier sums", fontsize=10)
    a1.legend(fontsize=7.2, loc="upper center", ncol=2, columnspacing=0.8, handlelength=1.4)

    k = np.array([1, 3, 5, 7, 9])
    Ain = 4 / (np.pi * k)
    Aout = Ain / np.sqrt(1 + k ** 2)
    w = 0.38
    a2.bar(k - w / 2, Ain, width=w * 0.95, color=COLORS[0], label="input")
    a2.bar(k + w / 2, Aout, width=w * 0.95, color=COLORS[1], label="after RC, $f_c$ = 1 kHz")
    for ki, ai, ao in zip(k, Ain, Aout):
        a2.text(ki - w / 2, ai + 0.02, f"{ai:.3f}", ha="center", va="bottom", fontsize=6.5,
                rotation=90)
        a2.text(ki + w / 2, ao + 0.02, f"{ao:.3f}", ha="center", va="bottom", fontsize=6.5,
                rotation=90, color=COLORS[1])
    a2.set_ylim(0, 1.6)
    a2.set_yticks(np.arange(0, 1.41, 0.2))
    a2.set_xticks(k)
    a2.set_xlabel("frequency (kHz)")
    a2.set_ylabel("amplitude (V)")
    a2.set_title("Line spectrum", fontsize=10)
    a2.legend(fontsize=7.5, loc="upper right")
    fig.tight_layout(w_pad=1.2)
    save(fig, CH, "fig-18-1-square-wave-series-rc")


# ------------------------------------------------------------------ 18.2
def fig_18_2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[0.8, 1.3]))
    t = np.linspace(-1.5, 1.5, 3001)
    a1.plot(t, (np.abs(t) <= 0.5).astype(float), color=COLORS[0], label="τ = 1 µs")
    a1.plot(t, (np.abs(t) <= 0.25).astype(float), "--", color=COLORS[1], label="τ = 0.5 µs")
    a1.set_xlim(-1.5, 1.5)
    a1.set_ylim(0, 1.35)
    a1.set_xlabel("t (µs)")
    a1.set_ylabel("x(t) (V)")
    a1.set_title("Pulses", fontsize=10)
    a1.legend(fontsize=8, loc="upper right")

    f = np.linspace(-4, 4, 8001)  # MHz
    ref = 1.0  # 1 us peak area (V us)
    floor = -45
    for tau, c, ls in [(1.0, COLORS[0], "-"), (0.5, COLORS[1], "--")]:
        X = tau * np.abs(np.sinc(f * tau)) / ref
        db = 20 * np.log10(np.maximum(X, 1e-6))
        a2.plot(f, np.maximum(db, floor), ls, color=c, lw=1.4)
    # 1/f sidelobe envelope of the 1 us pulse
    fe = np.linspace(0.6, 4, 200)
    env = 20 * np.log10(1 / (np.pi * fe * 1.0))
    a2.plot(fe, env, ":", color=INK, lw=1)
    a2.plot(-fe, env, ":", color=INK, lw=1)
    a2.text(3.95, -17.5, "1/f envelope", fontsize=7.5, ha="right")
    # main lobe shading (1 us)
    fm = np.linspace(-1, 1, 801)
    a2.fill_between(fm, floor, 20 * np.log10(np.maximum(np.abs(np.sinc(fm)), 1e-6)),
                    color=COLORS[0], alpha=0.15, lw=0)
    a2.text(0, -30, "main lobe:\n90 % of\nenergy", ha="center", fontsize=7.5, color=COLORS[0])
    # first sidelobe
    fs1 = 1.4303
    sl = 20 * np.log10(abs(np.sinc(fs1)))
    a2.plot([fs1], [sl], "o", ms=4, color=COLORS[0])
    a2.annotate(f"first sidelobe {sl:.1f} dB".replace("-", "−"), xy=(fs1, sl), xytext=(1.55, -4.5), fontsize=7.5,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    for fn, c in [(1, COLORS[0]), (2, COLORS[1])]:
        for sgn in (-1, 1):
            a2.axvline(sgn * fn, color=c, lw=0.6, ls=":")
        a2.text(-fn - 0.06 if fn == 1 else fn + 0.06, floor + 0.8, f"±{fn} MHz",
                ha="right" if fn == 1 else "left", va="bottom", fontsize=7.5, color=c,
                bbox=dict(fc="white", ec="none", pad=0.5))
    a2.set_xlim(-4, 4)
    a2.set_ylim(floor, 3)
    a2.set_xlabel("f (MHz)")
    a2.set_ylabel("|X(f)| (dB re 1 µs peak)")
    a2.set_title("Magnitude spectra (first nulls marked)", fontsize=10)
    fig.tight_layout(w_pad=1.0)
    save(fig, CH, "fig-18-2-rect-pulse-sinc")


# ------------------------------------------------------------------ 18.3
def fig_18_3():
    w0 = 2 * np.pi * 50
    Q = 10
    b = [1, 0, w0 ** 2]
    a = [1, w0 / Q, w0 ** 2]
    p = np.roots(a)
    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(3, 2, width_ratios=[0.9, 1.4], hspace=0.35, wspace=0.42)
    ax = fig.add_subplot(gs[:, 0])
    ax.axhline(0, color=INK, lw=0.6)
    ax.axvline(0, color=INK, lw=0.6)
    ax.plot([0, 0], [w0, -w0], "o", mfc="white", mec=COLORS[0], ms=8, mew=1.6, ls="none",
            label="zeros ±j314.2")
    ax.plot(p.real, p.imag, "x", color=COLORS[1], ms=9, mew=2, ls="none",
            label="poles −15.7 ± j313.8")
    wt = 2 * np.pi * 45
    ax.plot([0], [wt], "s", color=INK, ms=4)
    ax.text(3, wt - 18, r"$j2\pi\cdot45$", fontsize=8, va="top")
    for (x0, y0), c in [((0, w0), COLORS[0]), ((0, -w0), COLORS[0]),
                        ((p[0].real, p[0].imag), COLORS[1]), ((p[1].real, p[1].imag), COLORS[1])]:
        ax.annotate("", xy=(0, wt), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=0.9, mutation_scale=8,
                                    shrinkA=4, shrinkB=2, alpha=0.8))
    ax.set_xlim(-60, 10)
    ax.set_ylim(-400, 400)
    ax.set_xlabel("σ (s⁻¹)")
    ax.set_ylabel("jω (rad/s)")
    ax.set_title("s-plane", fontsize=10)
    ax.legend(fontsize=7, loc="lower left", bbox_to_anchor=(0.0, 0.0), handletextpad=0.3)
    ax.grid(True, lw=0.4)

    f = np.linspace(10, 100, 40001)
    _, H = signal.freqs(b, a, worN=2 * np.pi * f)
    mag = 20 * np.log10(np.maximum(np.abs(H), 1e-5))
    ph = np.degrees(np.angle(H))
    # group delay of the pole pair (the on-axis zeros add only a jump at 50 Hz)
    ws = 2 * np.pi * f
    phu = np.unwrap(np.angle(H))
    gd = -np.gradient(phu, ws)
    gd[np.abs(f - 50) < 0.05] = np.nan

    a1 = fig.add_subplot(gs[0, 1])
    a1.plot(f, mag, color=COLORS[0])
    for fx in (47.56, 52.56):
        a1.axvline(fx, color="0.5", ls=":", lw=0.8)
    a1.axhline(-3, color="0.5", ls=":", lw=0.8)
    a1.text(46.8, -36, "47.56", ha="right", fontsize=7.5)
    a1.text(53.3, -36, "52.56 Hz", ha="left", fontsize=7.5)
    a1.text(98, -6, "−3 dB", ha="right", va="top", fontsize=7.5, color="0.4")
    a1.set_ylim(-40, 1)
    a1.set_ylabel("|H| (dB)")
    a2 = fig.add_subplot(gs[1, 1], sharex=a1)
    a2.plot(f[f < 50], ph[f < 50], color=COLORS[2])
    a2.plot(f[f > 50], ph[f > 50], color=COLORS[2])
    a2.plot([50, 50], [-90, 90], ":", color=COLORS[2], lw=1)
    a2.set_ylim(-95, 95)
    a2.set_yticks([-90, -45, 0, 45, 90])
    a2.set_ylabel("∠H (deg)")
    a3 = fig.add_subplot(gs[2, 1], sharex=a1)
    a3.plot(f, gd * 1e3, color=COLORS[1])
    for fx, ty in ((40, 12), (45, 30), (47, 48)):
        v = np.interp(fx, f, np.nan_to_num(gd)) * 1e3
        a3.plot(fx, v, "o", ms=4, color=INK)
        a3.annotate(f"{v:.1f} ms @ {fx} Hz" if v < 10 else f"{v:.0f} ms @ {fx} Hz",
                    xy=(fx, v), xytext=(36, ty), ha="right", va="center", fontsize=7.5,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color="0.4"))
    a3.set_ylim(0, 75)
    a3.set_ylabel(r"$\tau_g$ (ms)")
    a3.set_xlabel("f (Hz)")
    a3.text(54, 58, f"peak ≈ 1/σ = {np.nanmax(gd) * 1e3:.0f} ms at 50 Hz\n"
            "(on-axis zeros add only the\nphase jump at exactly 50 Hz)", fontsize=7, ha="left",
            va="center")
    a3.set_xlim(10, 100)
    for axx in (a1, a2):
        plt.setp(axx.get_xticklabels(), visible=False)
    for axx in (a1, a2, a3):
        axx.grid(True, lw=0.4)
        axx.tick_params(labelsize=8)
    ax.tick_params(labelsize=8)
    save(fig, CH, "fig-18-3-notch-pole-zero-response")


# ------------------------------------------------------------------ 18.4
def fig_18_4():
    f = np.logspace(2, np.log10(20e3), 2000)
    fc = 1e3
    fig, ax = new_fig(6.4, 3.9)
    # template: forbidden regions shaded
    ax.fill_between([100, 1e3], -3, -60, color="0.88", lw=0)
    ax.fill_between([2e3, 20e3], -20, 5, color="0.88", lw=0)
    ax.plot([100, 1e3, 1e3], [-3, -3, -60], color="0.45", lw=1)
    ax.plot([2e3, 2e3, 20e3], [5, -20, -20], color="0.45", lw=1)
    for n, c in [(2, COLORS[0]), (4, COLORS[1])]:
        mag = -10 * np.log10(1 + (f / fc) ** (2 * n))
        ax.plot(f, mag, color=c, label=f"Butterworth n = {n}")
        asym = -20 * n * np.log10(f / fc)
        ax.plot(f[f > fc], asym[f > fc], ":", color=c, lw=1)
        v = -10 * np.log10(1 + 2 ** (2 * n))
        ax.plot(2e3, v, "o", color=c, ms=5, zorder=5)
        ax.text(2.15e3, v + 0.6, f"{v:.1f} dB".replace("-", "−"), fontsize=8, color=c, va="bottom")
    ax.text(3.3e3, -47, "−40 dB/dec", fontsize=8, color=COLORS[0], rotation=-27)
    ax.text(2.4e3, -57, "−80 dB/dec", fontsize=8, color=COLORS[1], rotation=-48)
    ax.text(300, 1.5, "passband", ha="center", fontsize=9)
    ax.text(1.42e3, 1.5, "transition\nband", ha="center", fontsize=8.5, va="bottom")
    ax.text(6.5e3, 1.5, "stopband", ha="center", fontsize=9)
    ax.text(300, -8, "max loss 3 dB", ha="center", fontsize=8, color="0.35")
    ax.text(6.5e3, -16.5, "min attenuation 20 dB", ha="center", fontsize=8, color="0.35")
    ax.set_xscale("log")
    ax.set_xlim(100, 20e3)
    ax.set_ylim(-60, 5)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|H| (dB)")
    ax.grid(True, which="both", lw=0.4)
    ax.legend(fontsize=8.5, loc="lower left")
    save(fig, CH, "fig-18-4-filter-specs-butterworth")


# ------------------------------------------------------------------ 18.5
def fig_18_5():
    wc = 2 * np.pi * 1e3
    b, a = [wc ** 2], [1, np.sqrt(2) * wc, wc ** 2]
    f = np.logspace(1, np.log10(5e3), 3000)
    w = 2 * np.pi * f
    _, H = signal.freqs(b, a, worN=w)
    gd = -np.gradient(np.unwrap(np.angle(H)), w)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6))
    a1.semilogx(f, gd * 1e6, color=COLORS[0])
    ipk = np.argmax(gd)
    a1.plot(f[ipk], gd[ipk] * 1e6, "o", ms=4, color=COLORS[1])
    a1.text(f[ipk], gd[ipk] * 1e6 + 12, f"peak {gd[ipk] * 1e6:.0f} µs at {f[ipk]:.0f} Hz",
            fontsize=7.5, ha="center", va="bottom", color=COLORS[1])
    for fx, ha, dx in ((500, "right", 0.88), (1000, "left", 1.12), (2000, "left", 1.12)):
        v = np.interp(fx, f, gd) * 1e6
        a1.plot(fx, v, "o", ms=4, color=INK)
        a1.text(fx * dx, v, f"{v:.0f} µs @ {fx:g} Hz", fontsize=7.5, va="center", ha=ha)
    a1.text(12, 225 + 4, "225 µs (= √2/ω$_c$)", fontsize=7.5, va="bottom")
    a1.set_xlim(10, 5e3)
    a1.set_ylim(0, 320)
    a1.set_xlabel("frequency (Hz)")
    a1.set_ylabel(r"group delay $\tau_g$ (µs)")
    a1.set_title("2nd-order Butterworth, $f_c$ = 1 kHz", fontsize=9.5)
    a1.grid(True, which="both", lw=0.4)

    # time responses to a 0.5 ms pulse
    fsamp = 1e6
    Ttot = 0.2  # long record so circular effects vanish
    N = int(Ttot * fsamp)
    t = np.arange(N) / fsamp
    x = ((t >= 0.5e-3) & (t < 1.0e-3)).astype(float)
    _, yb, _ = signal.lsim((b, a), x, t)
    F = np.fft.rfftfreq(N, 1 / fsamp)
    Hmag = 1 / np.sqrt(1 + (F / 1e3) ** 4)
    yfir = np.fft.irfft(np.fft.rfft(x) * Hmag * np.exp(-1j * 2 * np.pi * F * 0.5e-3), n=N)
    sel = t <= 3e-3
    a2.plot(t[sel] * 1e3, x[sel], "--", color="0.45", lw=1.2, label="input pulse")
    a2.plot(t[sel] * 1e3, yb[sel], color=COLORS[0], label="Butterworth")
    a2.plot(t[sel] * 1e3, yfir[sel], ":", color=COLORS[1], lw=1.8,
            label="linear-phase, same |H|,\ndelay 0.5 ms")
    os_ = -yb.min() * 100
    a2.annotate(f"undershoot ≈ {os_:.1f} %\n(asymmetric tail)", xy=(t[np.argmin(yb)] * 1e3, yb.min()),
                xytext=(1.95, 0.35), fontsize=7.5, color=COLORS[0],
                arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=0.7))
    a2.axhline(0, color=INK, lw=0.5)
    a2.set_xlim(0, 3)
    a2.set_ylim(-0.15, 1.3)
    a2.set_xlabel("t (ms)")
    a2.set_ylabel("amplitude")
    a2.set_title("Response to a 0.5 ms pulse", fontsize=9.5)
    a2.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.04, 1.04))
    fig.tight_layout(w_pad=1.2)
    save(fig, CH, "fig-18-5-butterworth-group-delay")
    return os_


# ------------------------------------------------------------------ 18.6
def fig_18_6():
    T, B = 10e-6, 10e6
    k = B / T
    fig, axs = plt.subplots(3, 1, figsize=(6.6, 5.4), gridspec_kw=dict(height_ratios=[1, 1, 1.2]))
    # (top) real part, displayed with a 1 -> 2 MHz sweep for visibility
    t = np.linspace(0, 12e-6, 12001)
    on = (t <= T)
    f_lo, Bv = 1e6, 1e6
    xv = np.where(on, np.cos(2 * np.pi * (f_lo * t + 0.5 * Bv / T * t ** 2)), 0)
    axs[0].plot(t * 1e6, xv, color=COLORS[0], lw=0.8)
    axs[0].set_xlim(0, 12)
    axs[0].set_ylim(-1.3, 1.6)
    axs[0].set_yticks([-1, 0, 1])
    axs[0].set_ylabel("Re{x(t)}")
    axs[0].set_xlabel("t (µs)", labelpad=1)
    axs[0].text(11.9, 1.55, "chirp, T = 10 µs (sweep drawn as 1→2 MHz for visibility)",
                ha="right", va="top", fontsize=8)
    # (middle) instantaneous frequency
    tt = np.linspace(0, T, 10)
    axs[1].plot(tt * 1e6, (-B / 2 + k * tt) / 1e6, color=COLORS[1], lw=2)
    axs[1].axhline(0, color=INK, lw=0.5)
    axs[1].set_xlim(0, 12)
    axs[1].set_ylim(-6.5, 6.5)
    axs[1].set_yticks([-5, 0, 5])
    axs[1].set_ylabel("f$_i$ (MHz)")
    axs[1].set_xlabel("t (µs)", labelpad=1)
    axs[1].text(0.3, 4.5, "B = 10 MHz swept linearly in T = 10 µs", fontsize=8, va="center")
    axs[1].grid(True, lw=0.4)
    # (bottom) matched-filter output
    fs = 400e6
    n = np.arange(int(T * fs))
    tc = n / fs - T / 2
    x = np.exp(1j * np.pi * k * tc ** 2)
    r = np.correlate(x, x, mode="full")
    lag = (np.arange(len(r)) - (len(x) - 1)) / fs
    rdb = 20 * np.log10(np.maximum(np.abs(r) / np.abs(r).max(), 1e-6))
    sel = np.abs(lag) <= 1e-6
    axs[2].plot(lag[sel] * 1e6, rdb[sel], color=COLORS[2], lw=1.3)
    # -4 dB width
    above = lag[(rdb > -4) & (np.abs(lag) < 0.2e-6)]
    w4 = above.max() - above.min()
    axs[2].annotate("", xy=(above.min() * 1e6, -4), xytext=(above.max() * 1e6, -4),
                    arrowprops=dict(arrowstyle="<|-|>", lw=0.8, mutation_scale=6, color=INK))
    axs[2].text(0.09, -4.3, f"{w4 * 1e6:.2f} µs at −4 dB", fontsize=8, ha="left", va="center")
    # first sidelobe level
    pk_idx = signal.find_peaks(rdb[sel])[0]
    lv = np.sort(rdb[sel][pk_idx])[::-1]
    sl = lv[1] if len(lv) > 1 else np.nan
    axs[2].axhline(sl, color="0.5", ls=":", lw=0.8)
    axs[2].text(-0.98, sl + 0.8, f"first sidelobes {sl:.1f} dB".replace("-", "−"), fontsize=8, va="bottom")
    axs[2].text(0.98, 1, "TB = 100\ncompression gain 20 dB", ha="right", va="top", fontsize=8.5,
                bbox=dict(fc="white", ec="0.7", lw=0.6, boxstyle="round,pad=0.3"))
    axs[2].set_xlim(-1, 1)
    axs[2].set_ylim(-45, 3)
    axs[2].set_xlabel("delay from peak (µs)")
    axs[2].set_ylabel("matched-filter\noutput (dB)")
    for ax in axs:
        ax.tick_params(labelsize=8)
    fig.tight_layout(h_pad=0.6)
    save(fig, CH, "fig-18-6-chirp-pulse-compression")
    return w4, sl


if __name__ == "__main__":
    fig_18_1()
    fig_18_2()
    fig_18_3()
    fig_18_4()
    print("18.5 overshoot %:", fig_18_5())
    print("18.6 -4 dB width, sidelobe:", fig_18_6())
