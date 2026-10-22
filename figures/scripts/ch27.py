"""Figures for Chapter 27 — Digital Communication. Run from the repository root: python figures/scripts/ch27.py"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

from figstyle import new_fig, save, COLORS, INK

CH = "27"
RNG = np.random.default_rng(27)


def Q(x):
    return 0.5 * erfc(np.asarray(x) / np.sqrt(2))


# ----------------------------------------------------------------------------- Figure 27.1
def _mulaw(x, mu):
    if mu == 0:
        return x
    return np.sign(x) * np.log1p(mu * np.abs(x)) / np.log1p(mu)


def _mulaw_inv(y, mu):
    return np.sign(y) * np.expm1(np.abs(y) * np.log1p(mu)) / mu


def _sqnr_mulaw(level_db, n=8, mu=255):
    """Simulated SQNR of a sine through mu-law compressor, n-bit uniform midrise quantizer, expander."""
    ph = np.linspace(0, 2 * np.pi, 20000, endpoint=False) + 0.123
    out = []
    L = 2 ** n
    step = 2.0 / L
    for ldb in level_db:
        sp, npow = 0.0, 0.0
        for jit in np.linspace(-0.75, 0.75, 13):  # average over a small spread of levels
            a = 10 ** (min(ldb + jit, 0.0) / 20)
            x = a * np.sin(ph)
            y = _mulaw(x, mu)
            yq = np.clip((np.floor(y / step) + 0.5) * step, -1 + step / 2, 1 - step / 2)
            xq = _mulaw_inv(yq, mu)
            sp += np.mean(x ** 2)
            npow += np.mean((x - xq) ** 2)
        out.append(10 * np.log10(sp / npow))
    return np.array(out)


def fig_27_1():
    """mu-law compressor characteristic and SQNR versus input level."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.6), gridspec_kw=dict(width_ratios=[1, 1.35]))
    x = np.linspace(0, 1, 801)
    for mu, c in [(0, INK), (15, COLORS[0]), (255, COLORS[1])]:
        a1.plot(x, _mulaw(x, mu), color=c, label=f"$\\mu$ = {mu}")
    xs = np.linspace(0, 0.012, 10)
    a1.plot(xs, 46 * xs, ":", color=COLORS[1], lw=1.2)
    a1.annotate("slope at origin\n$\\mu/\\ln(1+\\mu)$ = 46\n($\\mu$ = 255)", xy=(0.011, 0.45), xytext=(0.3, 0.08),
                fontsize=8.5, arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8))
    a1.set_xlim(0, 1)
    a1.set_ylim(0, 1.02)
    a1.set_xlabel("input |x| (fraction of full scale)")
    a1.set_ylabel("compressed output y")
    a1.legend(loc="center right", fontsize=8.5)
    a1.set_title("(a) µ-law compressor", loc="left", fontsize=10)

    L = np.linspace(-60, 0, 121)
    a2.axvspan(-40, 0, color=COLORS[5], alpha=0.15, lw=0)
    a2.text(-20, 3, "speech dynamic range", ha="center", fontsize=8.5, color="#2B6C8F")
    a2.plot(L, 6.02 * 8 + 1.76 + L, color=COLORS[0], label="uniform 8-bit")
    a2.plot(L, 6.02 * 13 + 1.76 + L, color=COLORS[2], label="uniform 13-bit")
    a2.plot(L, _sqnr_mulaw(L), color=COLORS[1], label="µ-law 8-bit ($\\mu$ = 255)")
    a2.axhline(38, color=COLORS[1], lw=0.7, ls=":")
    a2.text(-59, 39.5, "≈ 38 dB", fontsize=8, color=COLORS[1])
    a2.annotate("49.9 dB", xy=(0, 49.9), xytext=(-12, 56), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.7))
    a2.annotate("80.0 dB", xy=(0, 80), xytext=(-14, 74), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.7))
    a2.set_xlim(-60, 0)
    a2.set_ylim(0, 85)
    a2.set_xlabel("sine input level re full scale (dB)")
    a2.set_ylabel("SQNR (dB)")
    a2.legend(loc="upper left", fontsize=8)
    a2.set_title("(b) SQNR versus input level", loc="left", fontsize=10)
    fig.tight_layout(w_pad=1.5)
    save(fig, CH, "fig-27-1-pcm-companding")


# ----------------------------------------------------------------------------- Figure 27.2
def _dm(x, delta):
    est = np.empty_like(x)
    bits = np.empty(len(x), int)
    e = 0.0
    for i, v in enumerate(x):
        b = 1 if v > e else 0
        e += delta if b else -delta
        bits[i] = b
        est[i] = e
    return est, bits


def fig_27_2():
    """Delta modulation of a 1 kHz, 1 V tone at fs = 64 kHz with Delta = 0.06 V and 0.1 V."""
    fs, fm, A = 64e3, 1e3, 1.0
    tc = np.linspace(0, 1.5e-3, 3001)
    n = np.arange(int(1.5e-3 * fs) + 1)
    tn = n / fs
    xs = A * np.sin(2 * np.pi * fm * tn)
    fig = plt.figure(figsize=(6.8, 5.2))
    gs = fig.add_gridspec(5, 1, height_ratios=[3, 0.45, 0.45, 3, 0.45], hspace=0.12)
    for k, (delta, tag) in enumerate([(0.06, "a"), (0.1, "b")]):
        ax = fig.add_subplot(gs[3 * k])
        axb = fig.add_subplot(gs[3 * k + 1], sharex=ax)
        est, bits = _dm(xs, delta)
        ax.plot(tc * 1e3, A * np.sin(2 * np.pi * fm * tc), color=INK, lw=1.4, label="input m(t)")
        ax.step(tn * 1e3, est, where="post", color=COLORS[0], lw=1.2, label="staircase $\\hat m(t)$")
        ax.set_ylim(-1.2, 1.2)
        ax.set_ylabel("volts (V)")
        ax.set_xlim(0, 1.5)
        ax.tick_params(labelbottom=False)
        ax.axhline(0, color=INK, lw=0.4)
        ok = delta * fs >= 2 * np.pi * fm * A
        ax.set_title(f"({tag})  Δ = {delta} V, $f_s$ = 64 kHz:  Δ$f_s$ = {delta*fs:.0f} V/s "
                     f"{'≥' if ok else '<'} $2\\pi f_m A$ = 6283 V/s", loc="left", fontsize=9.5)
        if not ok:
            ax.text(1.0, -0.62, "slope overload: Δ$f_s$ < 2π$f_m$A", fontsize=8.5, color=COLORS[1])
            ax.annotate("", xy=(0.13, 0.36), xytext=(1.0, -0.55),
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9))
            ax.annotate("", xy=(1.08, 0.2), xytext=(1.12, -0.42),
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9))
        else:
            ax.annotate("granular noise", xy=(0.27, 1.02), xytext=(0.42, 0.55), fontsize=8.5,
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9), color=COLORS[1])
            ax.annotate("", xy=(1.25, 1.02), xytext=(0.62, 0.62),
                        arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=0.9))
            ax.legend(loc="lower right", fontsize=8)
        # bit stream as tick row
        for tb, b in zip(tn, bits):
            axb.plot([tb * 1e3, tb * 1e3], [0, 1 if b else 0.35], color=COLORS[2] if b else "#999999", lw=1.0)
        axb.set_ylim(0, 1.05)
        axb.set_yticks([])
        axb.spines["left"].set_visible(False)
        axb.text(-0.01, 0.5, "bits", ha="right", va="center", fontsize=8, transform=axb.get_yaxis_transform())
        if k == 0:
            axb.tick_params(labelbottom=False)
        else:
            axb.set_xlabel("time (ms)   [bit stream: tall tick = 1, short tick = 0]")
    save(fig, CH, "fig-27-2-delta-modulation")


# ----------------------------------------------------------------------------- Figure 27.3
def fig_27_3():
    """Binary line codes for 1 0 1 1 0 0 0 0 1 0 and their PSDs."""
    bits = [1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    N = len(bits)
    os = 200
    t = np.arange(N * os) / os

    def nrz(levels):
        return np.repeat(levels, os).astype(float)

    uni = nrz(bits)
    pol = nrz([1 if b else -1 for b in bits])
    rz = np.zeros(N * os)
    for i, b in enumerate(bits):
        if b:
            rz[i * os:i * os + os // 2] = 1
    ami_l, last = [], -1
    for b in bits:
        if b:
            last = -last
            ami_l.append(last)
        else:
            ami_l.append(0)
    def rzp(levels):  # 50 % duty pulses, as used on E1/T1 bipolar lines
        w = np.zeros(N * os)
        for i, v in enumerate(levels):
            w[i * os:i * os + os // 2] = v
        return w

    ami = rzp(ami_l)
    man = np.zeros(N * os)
    for i, b in enumerate(bits):
        first, second = (-1, 1) if b else (1, -1)  # IEEE 802.3: 1 = low-to-high
        man[i * os:i * os + os // 2] = first
        man[i * os + os // 2:(i + 1) * os] = second
    # HDB3: run of 4 zeros (bits 5-8) after an odd count (3) of marks -> 000V, V same polarity as last mark
    hdb = [1, 0, -1, 1, 0, 0, 0, 1, -1, 0]
    hdb3 = rzp(hdb)

    fig = plt.figure(figsize=(6.8, 5.0))
    gs = fig.add_gridspec(6, 2, width_ratios=[1.45, 1], wspace=0.32, hspace=0.35)
    rows = [("unipolar NRZ", uni), ("polar NRZ", pol), ("unipolar RZ", rz),
            ("AMI", ami), ("Manchester", man), ("HDB3", hdb3)]
    for r, (name, w) in enumerate(rows):
        ax = fig.add_subplot(gs[r, 0])
        ax.plot(t, w, color=COLORS[0], lw=1.3, drawstyle="steps-post")
        ax.axhline(0, color="#AAAAAA", lw=0.5)
        for k in range(N + 1):
            ax.axvline(k, color="#DDDDDD", lw=0.5, zorder=0)
        ax.set_xlim(0, N)
        ax.set_ylim(-1.5, 1.5)
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(["−V", "0", "+V"], fontsize=7)
        ax.text(-0.25, 1.75, name, fontsize=8.5, ha="left", va="bottom", fontweight="bold")
        ax.tick_params(axis="x", labelsize=7.5)
        if r == 0:
            for k, b in enumerate(bits):
                ax.text(k + 0.5, 3.1, str(b), ha="center", fontsize=9, color=COLORS[1], fontweight="bold")
            ax.text(-0.1, 3.1, "data", ha="right", fontsize=8, color=COLORS[1])
        if name == "HDB3":
            ax.text(7.62, 0.45, "V", ha="left", fontsize=8.5, color=COLORS[1], fontweight="bold")
            ax.annotate("", xy=(4, 1.3), xytext=(8, 1.3),
                        arrowprops=dict(arrowstyle="<->", color=COLORS[1], lw=0.8, shrinkA=0, shrinkB=0))
            ax.text(6.0, 1.4, "000V substitution", ha="center", va="bottom", fontsize=7.5, color=COLORS[1])
        if r < 5:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel("time  t / $T_b$")

    ax = fig.add_subplot(gs[:, 1])
    f = np.linspace(1e-4, 2, 2001)
    sinc2 = np.sinc(f) ** 2
    ax.plot(f, sinc2, color=COLORS[0], label="polar NRZ")
    ax.plot(f, np.sinc(f / 2) ** 2 * np.sin(np.pi * f / 2) ** 2, color=COLORS[2], label="Manchester")
    ax.plot(f, 0.25 * np.sinc(f / 2) ** 2 * np.sin(np.pi * f) ** 2, color=COLORS[3], label="AMI (50 % pulses)")
    ax.plot(f, 0.25 * sinc2, "--", color=COLORS[1], label="unipolar NRZ")
    ax.annotate("", xy=(0.0, 1.08), xytext=(0.0, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2.0, shrinkA=0, shrinkB=0))
    ax.text(0.04, 1.11, "DC impulse (unipolar NRZ)", fontsize=8, color=COLORS[1], va="center")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.18)
    ax.set_xticks([0, 0.5, 1, 1.5, 2])
    ax.set_xlabel("normalised frequency  $fT_b$")
    ax.set_ylabel("PSD  $S(f)/(V^2T_b)$")
    ax.legend(loc="center left", bbox_to_anchor=(0.45, 0.68), fontsize=8)
    ax.set_title("power spectral densities", fontsize=9.5)
    save(fig, CH, "fig-27-3-line-codes")


# ----------------------------------------------------------------------------- Figure 27.4
def _rc_pulse(t, a):
    t = np.asarray(t, float)
    p = np.sinc(t)
    if a == 0:
        return p
    den = 1 - (2 * a * t) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        out = p * np.cos(np.pi * a * t) / den
    sing = np.isclose(den, 0)
    out[sing] = np.pi / 4 * np.sinc(1 / (2 * a))
    return out


def _rc_spec(f, a):
    f = np.abs(f)
    lo, hi = (1 - a) / 2, (1 + a) / 2
    P = np.where(f <= lo, 1.0, 0.0)
    if a > 0:
        mid = (f > lo) & (f <= hi)
        P = np.where(mid, 0.5 * (1 + np.cos(np.pi / a * (f - lo))), P)
    return P


def _rrc_taps(a, sps, span):
    t = np.arange(-span * sps, span * sps + 1) / sps
    h = np.zeros_like(t)
    for i, ti in enumerate(t):
        if np.isclose(ti, 0):
            h[i] = 1 - a + 4 * a / np.pi
        elif np.isclose(abs(ti), 1 / (4 * a)):
            h[i] = a / np.sqrt(2) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * a)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * a)))
        else:
            h[i] = (np.sin(np.pi * ti * (1 - a)) + 4 * a * ti * np.cos(np.pi * ti * (1 + a))) / (
                np.pi * ti * (1 - (4 * a * ti) ** 2))
    return h / np.sqrt(np.sum(h ** 2))


def fig_27_4():
    """Raised-cosine pulses and spectra, and eye diagrams without and with noise."""
    fig, axs = plt.subplots(2, 2, figsize=(6.8, 5.0))
    t = np.linspace(-4, 4, 1601)
    f = np.linspace(0, 1, 801)
    cols = [INK, COLORS[0], COLORS[1]]
    for a, c in zip([0, 0.35, 1.0], cols):
        axs[0, 0].plot(t, _rc_pulse(t, a), color=c, lw=1.4, label=f"α = {a}")
        axs[0, 1].plot(f, _rc_spec(f, a), color=c, lw=1.4, label=f"α = {a}")
    ax = axs[0, 0]
    ax.axhline(0, color="#AAAAAA", lw=0.5)
    ax.plot(np.arange(-4, 5)[np.arange(-4, 5) != 0], np.zeros(8), "o", ms=3.5, color=COLORS[2], zorder=5)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.3, 1.1)
    ax.set_xlabel("$t/T_s$")
    ax.set_ylabel("p(t)")
    ax.legend(fontsize=7.5, loc="upper right")
    ax.set_title("(a) pulses: zeros at nonzero integers", loc="left", fontsize=9)
    ax = axs[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.axvline(0.5, color="#AAAAAA", lw=0.6, ls=":")
    ax.text(0.51, 1.03, "$1/(2T_s)$", fontsize=8)
    ax.set_xlabel("$fT_s$")
    ax.set_ylabel("$P(f)/T_s$")
    ax.legend(fontsize=7.5, loc="lower left")
    ax.set_title("(b) spectra: flat to (1−α)/2, edge at (1+α)/2", loc="left", fontsize=9)

    # eye diagrams
    a, sps, span = 0.35, 32, 8
    h = _rrc_taps(a, sps, span)
    nb = 200
    data = RNG.choice([-1.0, 1.0], nb)
    up = np.zeros(nb * sps)
    up[::sps] = data
    tx = np.convolve(up, h)
    rx_clean = np.convolve(tx, h)
    delay = 2 * span * sps
    peak = np.max(np.convolve(h, h))
    rx_clean = rx_clean / peak
    ebn0 = 10 ** (10 / 10)
    sigma = np.sqrt(1 / (2 * ebn0))  # noise std at the matched-filter sample, signal = +-1
    w = RNG.standard_normal(len(tx))
    nrx = np.convolve(w, h)  # unit variance after unit-energy RRC
    rx_noisy = rx_clean + sigma * nrx[:len(rx_clean)]
    tt = np.arange(2 * sps + 1) / sps - 1.0  # -1 .. +1 Ts around the sampling instant
    for ax, rx, title in [(axs[1, 0], rx_clean, "(c) eye, α = 0.35, no noise"),
                          (axs[1, 1], rx_noisy, "(d) eye with noise, $E_b/N_0$ = 10 dB")]:
        for k in range(span + 2, nb - span - 2):
            c0 = delay + k * sps
            seg = rx[c0 - sps:c0 + sps + 1]
            ax.plot(tt, seg, color=COLORS[0], lw=0.5, alpha=0.35)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-2.0, 2.0)
        ax.set_xlabel("time re sampling instant ($T_s$)")
        ax.set_ylabel("matched-filter output")
        ax.set_title(title, loc="left", fontsize=9)
        ax.axvline(0, color=COLORS[1], lw=0.9, ls="--")
    ax = axs[1, 0]
    # eye opening at t = 0
    ax.annotate("", xy=(0.04, 1.0), xytext=(0.04, -1.0),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.9, mutation_scale=8, shrinkA=0, shrinkB=0))
    wb = dict(fc="white", ec="none", alpha=0.85, pad=1.0)
    ax.text(0.08, 0.45, "noise\nmargin", fontsize=7.5, bbox=wb)
    ax.annotate("", xy=(-0.42, 0), xytext=(0.42, 0),
                arrowprops=dict(arrowstyle="<|-|>", color=COLORS[2], lw=0.9, mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(-0.22, -0.3, "timing tolerance", fontsize=7.5, color=COLORS[2], ha="center", bbox=wb)
    ax.text(-0.03, -1.85, "optimum sampling instant", fontsize=7.5, color=COLORS[1], ha="right")
    ax = axs[1, 1]
    ax.axvline(0.3, color=COLORS[3], lw=1.2)
    ax.text(0.34, 1.85, "0.3 $T_s$ timing\noffset", fontsize=7.5, color=COLORS[3], va="top", bbox=wb)
    fig.tight_layout(h_pad=1.0, w_pad=1.0)
    save(fig, CH, "fig-27-4-raised-cosine-eye")


# ----------------------------------------------------------------------------- Figure 27.5
def fig_27_5():
    """Gray-coded BPSK, QPSK, 8-PSK and 16-QAM constellations (unit average energy)."""
    fig, axs = plt.subplots(2, 2, figsize=(6.4, 6.0))
    lim = 1.5

    def setup(ax, title):
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axhline(0, color="#BBBBBB", lw=0.5, zorder=0)
        ax.axvline(0, color="#BBBBBB", lw=0.5, zorder=0)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel("I", labelpad=1)
        ax.set_ylabel("Q", labelpad=1)
        ax.set_title(title, loc="left", fontsize=9.5)

    def cloud(ax, p):
        z = p + 0.1 * (RNG.standard_normal(200) + 1j * RNG.standard_normal(200))
        ax.scatter(z.real, z.imag, s=2, color=COLORS[5], alpha=0.6, zorder=2)

    def pts(ax, z, labels, fs=8, off=0.17, radial=False):
        ax.plot(z.real, z.imag, "o", color=COLORS[0], ms=5, zorder=4)
        for p, l in zip(z, labels):
            if radial:
                q = p * (1 + off / abs(p))
            else:
                q = p + 1j * off
            ax.text(q.real, q.imag, l, ha="center", va="center", fontsize=fs, zorder=5,
                    bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.4))

    def dmin(ax, p1, p2, text, toff):
        ax.annotate("", xy=(p2.real, p2.imag), xytext=(p1.real, p1.imag),
                    arrowprops=dict(arrowstyle="<|-|>", color=COLORS[1], lw=1.0, mutation_scale=8, shrinkA=3, shrinkB=3))
        m = (p1 + p2) / 2 + toff
        ax.text(m.real, m.imag, text, fontsize=8, color=COLORS[1], ha="center", va="center",
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6), zorder=6)

    bd = dict(color=INK, lw=0.8, ls="--")
    # BPSK
    ax = axs[0, 0]
    setup(ax, "(a) BPSK")
    z = np.array([1 + 0j, -1 + 0j])
    ax.axvline(0, **bd)
    cloud(ax, z[0])
    pts(ax, z, ["1", "0"], fs=9, off=0.38)
    dmin(ax, z[1], z[0], "$d_{min}$ = 2", -0.45j)
    # QPSK
    ax = axs[0, 1]
    setup(ax, "(b) QPSK (Gray)")
    s = 1 / np.sqrt(2)
    z = np.array([s + 1j * s, -s + 1j * s, -s - 1j * s, s - 1j * s])
    ax.axvline(0, **bd)
    ax.axhline(0, **bd)
    cloud(ax, z[0])
    pts(ax, z, ["00", "01", "11", "10"], off=0.36)
    dmin(ax, z[3], z[0], "$d_{min}$ = 1.414", -0.62)
    # 8-PSK
    ax = axs[1, 0]
    setup(ax, "(c) 8-PSK (Gray)")
    ang = np.arange(8) * np.pi / 4
    z = np.exp(1j * ang)
    gray = ["000", "001", "011", "010", "110", "111", "101", "100"]
    for k in range(8):
        b = np.pi / 8 + k * np.pi / 4
        ax.plot([0, 2 * np.cos(b)], [0, 2 * np.sin(b)], **bd)
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(th), np.sin(th), color="#CCCCCC", lw=0.6, zorder=0)
    cloud(ax, z[0])
    pts(ax, z, gray, fs=7.5, off=0.3, radial=True)
    dmin(ax, z[0], z[1], "$d_{min}$ = 0.765", 0.30 + 0.0j)
    # 16-QAM
    ax = axs[1, 1]
    setup(ax, "(d) 16-QAM (Gray)")
    lv = np.array([-3, -1, 1, 3]) / np.sqrt(10)
    g2 = ["00", "01", "11", "10"]
    z, lab = [], []
    for i, xi in enumerate(lv):
        for j, yj in enumerate(lv):
            z.append(xi + 1j * yj)
            lab.append(g2[i] + g2[j])
    z = np.array(z)
    for b in [-2 / np.sqrt(10), 0, 2 / np.sqrt(10)]:
        ax.axvline(b, **bd)
        ax.axhline(b, **bd)
    cloud(ax, lv[3] + 1j * lv[3])
    pts(ax, z, lab, fs=6.5, off=-0.15)
    dmin(ax, lv[2] + 1j * lv[0], lv[3] + 1j * lv[0], "", 0)
    ax.text((lv[2] + lv[3]) / 2, lv[0] - 0.42, "$d_{min}$ = 0.632", fontsize=8, color=COLORS[1], ha="center",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
    fig.tight_layout(h_pad=1.2, w_pad=1.0)
    save(fig, CH, "fig-27-5-constellations")


# ----------------------------------------------------------------------------- Figure 27.6
def fig_27_6():
    """BER versus Eb/N0 for binary and M-ary modulations, with the Shannon limit."""
    x = np.linspace(-2, 26, 2801)
    g = 10 ** (x / 10)

    def qam(M):
        k = np.log2(M)
        p = 2 * (1 - 1 / np.sqrt(M)) * Q(np.sqrt(3 * k * g / (M - 1)))
        return (1 - (1 - p) ** 2) / k

    curves = [
        ("BPSK / QPSK", Q(np.sqrt(2 * g)), INK, "-"),
        ("DPSK", 0.5 * np.exp(-g), COLORS[0], "--"),
        ("coherent FSK / OOK", Q(np.sqrt(g)), COLORS[2], "-"),
        ("noncoherent FSK", 0.5 * np.exp(-g / 2), COLORS[2], "--"),
        ("16-QAM", qam(16), COLORS[1], "-"),
        ("64-QAM", qam(64), COLORS[3], "-"),
        ("256-QAM", qam(256), COLORS[4], "-"),
    ]
    fig, ax = new_fig(6.6, 4.6)
    marks = []
    for name, y, c, ls in curves:
        ax.semilogy(x, y, color=c, ls=ls, lw=1.6, label=name)
        i = np.argmin(np.abs(np.log10(np.maximum(y, 1e-300)) + 6))
        marks.append((x[i], c))
    ax.axhline(1e-6, color="#777777", lw=0.8, ls="--")
    # staggered labels for the 1e-6 crossings
    yl = [3e-8, 1.2e-8, 3e-8, 1.2e-8, 3e-8, 3e-8, 3e-8]
    has = ["center", "center", "right", "center", "left", "center", "center"]
    wb = dict(fc="white", ec="none", alpha=0.85, pad=0.5)
    for (xc, c), yv, ha in zip(marks, yl, has):
        ax.plot([xc], [1e-6], "o", color=c, ms=4, zorder=5)
        ax.plot([xc, xc], [1e-6, yv * 1.6], color=c, lw=0.6)
        ax.text(xc, yv, f"{xc:.1f}", ha=ha, va="top", fontsize=7.5, color=c, bbox=wb, zorder=6)
    ax.axvline(-1.59, color=COLORS[1], lw=1.0, ls="--")
    ax.text(-1.35, 1e-4, "Shannon limit −1.6 dB", fontsize=8, color=COLORS[1], rotation=90, va="center")
    ax.text(25.8, 1.3e-6, "$10^{-6}$", fontsize=8, ha="right", va="bottom", color="#555555")
    ax.set_xlim(-2, 26)
    ax.set_ylim(1e-8 * 0.5, 0.5)
    ax.set_xlabel("$E_b/N_0$ (dB)")
    ax.set_ylabel("bit-error probability $P_b$")
    ax.grid(True, which="major", lw=0.5)
    ax.legend(loc="upper right", fontsize=8)
    save(fig, CH, "fig-27-6-ber-curves")


if __name__ == "__main__":
    fig_27_1()
    fig_27_2()
    fig_27_3()
    fig_27_4()
    fig_27_5()
    fig_27_6()
