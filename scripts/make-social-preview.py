"""Render the GitHub social preview (1280x640) to docs/social-preview.png.

    python scripts/make-social-preview.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "social-preview.png"

BG = "#0b2230"
INK = "#f2f5f9"
MUTED = "#9fb8c8"
ACCENT = ["#56B4E9", "#E69F00", "#009E73", "#CC79A7", "#F0E442"]

plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "cm"})
fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor=BG)

# Upper right: series-RLC step responses for three damping ratios (Chapter 7).
ax = fig.add_axes([0.62, 0.55, 0.35, 0.36], facecolor=BG)
t = np.linspace(0, 12, 800)
for zeta, c in zip((0.1, 0.3, 0.7), ACCENT):
    wd = np.sqrt(1 - zeta**2)
    y = 1 - np.exp(-zeta * t) * (np.cos(wd * t) + zeta / wd * np.sin(wd * t))
    ax.plot(t, y, color=c, lw=2.4)
    k = y.argmax()
    ax.text(t[k] + 0.35, y[k] + 0.09, rf"$\zeta={zeta}$", color=c, fontsize=15, va="bottom")
ax.axhline(1, color=MUTED, lw=0.8, ls="--", alpha=0.6)
ax.set_xlim(0, 14.5)
ax.set_ylim(-0.05, 1.85)
ax.axis("off")

# Lower right: noisy 16-QAM constellation (Chapter 27).
ax2 = fig.add_axes([0.66, 0.08, 0.27, 0.42], facecolor=BG)
rng = np.random.default_rng(7)
levels = np.array([-3, -1, 1, 3])
for i, I in enumerate(levels):
    for j, Q in enumerate(levels):
        n = rng.normal(scale=0.22, size=(60, 2))
        ax2.scatter(I + n[:, 0], Q + n[:, 1], s=5, color=ACCENT[(i + j) % 4], alpha=0.45, lw=0)
        ax2.scatter([I], [Q], s=26, color=INK, lw=0)
for v in (-2, 0, 2):
    ax2.axhline(v, color=MUTED, lw=0.6, ls=":", alpha=0.7)
    ax2.axvline(v, color=MUTED, lw=0.6, ls=":", alpha=0.7)
ax2.set_xlim(-4.3, 4.3)
ax2.set_ylim(-4.3, 4.3)
ax2.set_aspect("equal")
ax2.axis("off")

# Left panel: title block.
fig.text(0.06, 0.83, "BOOK 3  ·  EEE CORE", color=ACCENT[0], fontsize=20, weight="bold")
fig.text(0.06, 0.63, "Circuits, Signals\nand Communications", color=INK, fontsize=38, weight="bold",
         va="center", linespacing=1.12)
fig.text(0.06, 0.45, "Networks, transients and AC, transmission lines,\nsignals and systems, DSP, "
         "communication theory\nand introductory control.",
         color=MUTED, fontsize=16, style="italic", va="top", linespacing=1.35)
fig.text(0.06, 0.24, r"$v_C(t)=1-e^{-\zeta\omega_0 t}\left[\cos\omega_d t+\frac{\zeta}{\sqrt{1-\zeta^2}}\sin\omega_d t\right]$",
         color=INK, fontsize=17)
fig.text(0.06, 0.14, "7 parts · 35 chapters · 201 figures · 780-page PDF · MCP server", color=INK, fontsize=14)
fig.text(0.06, 0.07, "github.com/The-Studio-of-Sadiq/Circuits-Signals-and-Communications", color=MUTED, fontsize=12)

OUT.parent.mkdir(exist_ok=True)
fig.savefig(OUT, facecolor=BG)
print(f"wrote {OUT.relative_to(ROOT)}")
