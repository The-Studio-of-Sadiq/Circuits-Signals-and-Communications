# Changelog

All notable changes to *Circuits, Signals and Communications*. Dates are ISO 8601. Versions follow the tags in this repository; each release attaches the compiled PDF.

## [1.0.0] — 2026-10-22

First complete edition.

### Added
- **Part I — Circuit Fundamentals** (Chapters 1–5): electrical quantities and circuit models, circuit laws, nodal and mesh analysis, network theorems, capacitors and inductors.
- **Part II — Transient and AC Analysis** (6–10): first- and second-order circuits, sinusoidal steady state, AC power, three-phase circuits.
- **Part III — Advanced Network Theory** (11–14): Laplace-domain analysis, two-port networks, network frequency response, transmission lines.
- **Part IV — Signals and Systems** (15–20): signal and system fundamentals, LTI systems, frequency-domain analysis, sampling and reconstruction, discrete-time systems.
- **Part V — Digital Signal Processing** (21–24): DSP fundamentals, the DFT and FFT, digital filters, advanced signal processing.
- **Part VI — Communication Theory** (25–32): communication-system fundamentals, analog and digital communication, information theory and coding, noise, wireless, optical, RF and microwave.
- **Part VII — Control-System Fundamentals** (33–35): dynamic-system modelling, feedback and stability, control design.
- Seven part openers, one per part folder.
- 201 figures, each drawn by a reproducible script in `figures/scripts/chNN.py` from the chapter's own numbers; figure plan in `FIGURES.md`.
- `pdf/Circuits-Signals-and-Communications.pdf`: 780 pages with clickable contents, PDF bookmarks and KaTeX math, built by `scripts/build-pdf.mjs`.
- MCP server (`mcp/server.mjs`) to list, read, search and typeset the book and fetch its figures.
- Book checks (`scripts/check-book.mjs`), CI and release workflows, issue and pull-request templates, community files, citation file, social preview image and wiki.

### Fixed (before release, from figure-agent cross-checks)
- §18.9: second-order Butterworth group-delay peak is 272 µs at 644 Hz, not 265 µs; a short pulse undershoots rather than overshoots.
- §21.2: Gaussian-signal SQNR at 16 bits now includes overload noise (52 dB at C = 4; optimum near C = 6, 85.5 dB).
- §31: ten 80 km spans are about 800 km, not 900 km; §29 noise-figure cascade and GPS SNR explanation; Chapter 1 burden-voltage example made consistent (12 mA, about 22 mV); assorted rounding slips in Chapters 7, 11, 17, 19, 26, 27 and 33.
