# Contributing — Circuits, Signals and Communications

Corrections, clearer explanations, better figures and new worked examples are welcome. Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to contribute

- **Found an error?** Open an [Erratum](../../issues/new?template=erratum.yml) issue with the section number (e.g. §14.8), what the book says and what it should say, with a derivation or a numerical check.
- **A figure is wrong or unclear?** Open a [Figure](../../issues/new?template=figure.yml) issue, or fix `figures/scripts/chNN.py` and send a pull request.
- **Build, figure-script or MCP-server problem?** Open a [Tooling bug](../../issues/new?template=tooling-bug.yml).
- **Bigger change** (a new section, a rewrite, a new worked example)? Open a [Proposal](../../issues/new?template=proposal.yml) first so the scope can be agreed.

## Pull requests

1. One topic per pull request: a fix, a figure, a section.
2. Follow the house style below; every number you add must be checked (e.g. with Python).
3. Run the checks locally before pushing (CI runs the same ones):

```bash
npm ci
```

```bash
npm run check
```

```bash
python scripts/build-figures.py ch14
```

4. Changed a figure? Commit the script and the regenerated PNG together. Added a figure marker? Draw it, run `node scripts/insert-figures.mjs` and `npm run figures:plan`.
5. Leave `pdf/` alone; the PDF is rebuilt and attached to each release by the release workflow.

By contributing you agree that your contribution is licensed under the repository's [MIT License](LICENSE).

---

# House Style

The master outline is [`TOC.md`](TOC.md). It is fixed: 7 parts, 35 chapters. Do not skip, merge or rename listed topics; every bullet in the TOC must be covered by a section or subsection of its chapter.

## Files

- Each part is a folder `part-N-<slug>/`. Its `README.md` is the part opener; `NN-<slug>.md` (NN two digits, global chapter number) is a chapter. The exact file names are listed in the TOC.
- Markdown only. Math is GitHub-style LaTeX: `$...$` inline, `$$...$$` display (display math on its own lines). Never `\(...\)` or `\[...\]`.
- In tables, never put a raw `|` inside math; use `\lvert ... \rvert` or `\Vert`.
- Use `\mathrm{}` for units in math, e.g. `$R=4.7\ \mathrm{k\Omega}$`. Prefer plain text units outside math.
- Use $j=\sqrt{-1}$ (engineering convention). Phasors in bold or with a bar are both acceptable, but be consistent inside a chapter.
- **No exercises, problems, quizzes or answer sections.** Worked examples inside the text are welcome.

## Chapter layout

```
# Chapter N — Title

*Part X · Part title*

Opening paragraph that starts from an engineering problem (a tripped breaker, a ringing bus, an aliased measurement, a dropped call).

> **Question 1?**
> **Question 2?**

| Concept | Engineering destination |
|---|---|
| ... | ... |

**Roadmap.** Short arrow-chain through the sections (N.1 → N.2–N.3 → ...).

---

## N.1 Section title
...
---
## N.2 ...
...
## What remains open

| Open question | Where it is answered |
|---|---|

**Next:** one sentence pointing to the next chapter.
```

Use `### ` subsections freely inside sections. Separate `## ` sections with `---`.

## Voice and method

1. **Start from the engineering problem**, not a definition: a power-factor penalty on an industrial bill, an oscilloscope probe that rings, a cable that reflects a fast edge, an audio recording full of aliasing, a modem that falls back to a lower rate, a drone that oscillates when its gain is raised. Draw examples from across EEE (power, electronics, instrumentation, audio, biomedical signals, telecom, radar, control) and beyond where signals appear (mechanical vibration, seismic data).
2. **Model → analysis → consequence.** Every method is introduced as a model with stated assumptions, solved with the right mathematics, and taken to a measurable consequence on a real circuit, signal or link.
3. **Every concept gets an engineering destination.** The opening table maps concepts to where an engineer uses them.
4. **Status box after every important law, theorem or rule**, using exactly one of four labels:
   - **Fundamental** — follows from physical law (charge conservation → KCL, energy conservation → KVL in lumped circuits, Maxwell's equations → telegrapher's equations).
   - **Derived** — a mathematical consequence of more basic results (Thévenin from linearity, convolution from LTI, the sampling theorem, Shannon capacity from information theory).
   - **Approximate** — valid under stated simplifying assumptions (lumped elements, small-signal, narrowband, high-SNR, dominant-pole). State the assumptions and the domain.
   - **Empirical** — fitted to observation (Hata/COST-231 path loss, Ziegler–Nichols tuning rules, fibre attenuation curves, Carson's rule as a rule of thumb).

   Format:
   ```
   > **Status of the principle: Name**
   > *Derived.* One sentence on why and where it holds.
   ```
5. **Show why an approximation works, then where it fails.** The lumped model fails when wires are a sizable fraction of a wavelength; superposition fails for power; the sampling theorem fails for non-bandlimited signals. A failure is missing physics or a changed regime, never an arbitrary exception.
6. **Real numbers.** Give representative values (with units) in tables: resistor tolerances, capacitor ESR, mains voltages and frequencies, coaxial-cable impedances and losses, audio/telecom sample rates, ADC bit depths, modulation spectral efficiencies, fibre loss at 1310/1550 nm, path-loss exponents, noise figures. Values must be correct to typical handbook accuracy; say "typical" or give ranges where they vary. Recompute every worked example.
7. **Worked examples** as `**Worked example — title.**` paragraphs with full numbers.
8. **Respect the boundaries** (see the table at the end of `TOC.md`). The mathematics of transforms and probability lives in *The Mathematics Universe*: recap a result in a paragraph and use it, do not re-derive the whole theory. Field theory lives in *Engineering Physics*; transistor and op-amp circuits in *Electronics & Computing*; machines and power hardware in *Electrical Energy & Machines*. Add a short `> **Boundary.**` note where a chapter touches those.
9. Do not overclaim. State domains of validity.

## Figure markers

Planned figures are recorded in the chapter as an HTML comment on its own line, at the exact point the figure should appear (invisible in the PDF until the figure exists):

```
<!-- FIGURE 6.3 | figures/ch06/fig-6-3-rc-step-response.png | plot | Caption sentence. | Content: what is drawn, axes, data ranges, labels. -->
```

Fields: number, target path, kind (`plot`, `circuit`, `schematic`, `block-diagram`, `phasor`, `spectrum`, `pole-zero`, `bode`, `smith-chart`, `constellation`, `flowchart`, `table-graphic`), caption, and a brief content spec for whoever draws it. Captions and specs must not contain the `|` character.

Figures are drawn by `figures/scripts/chNN.py` (shared style in `figures/scripts/figstyle.py`; circuit drawings may use `schemdraw`) and saved to the marker's path. `node scripts/insert-figures.mjs` then places each drawn figure directly below its marker; the marker stays as the figure's specification:

```
<!-- FIGURE 6.3 | ... -->

![Figure 6.3 — Caption](../figures/ch06/fig-6-3-rc-step-response.png)

*Figure 6.3 — Caption.*
```

The full plan is collected in [`FIGURES.md`](FIGURES.md) (`node scripts/figure-plan.mjs`).
